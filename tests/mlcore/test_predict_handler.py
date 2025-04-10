import io
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image
from pytest import approx

from mlcore.grpc_core.protos.predict import predict_pb2
from mlcore.grpc_core.servers.handlers.predict import PredictHandler

TEST_IMAGE_DATA = b"fake_data"
TEST_PLANT_TYPE = predict_pb2.PLANT_TOMATO

@pytest.fixture
def mock_image():
    img = Image.new("RGB", (100, 100), color="red")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="JPEG")
    return img_byte_arr.getvalue()

def test_bytes_to_image(mock_image):
    image = PredictHandler.bytes_to_image(mock_image)

    assert isinstance(image, Image.Image)
    assert image.size == (100, 100)

@patch("os.path.abspath")
def test_get_model_path(mock_abspath):
    mock_abspath.return_value = "/fake/path"
    path = PredictHandler.get_model_path(TEST_PLANT_TYPE)

    assert "tomato_cls_model.pt" in path

@patch("ultralytics.YOLO")
def test_run_model_success(mock_yolo):
    mock_model = MagicMock()
    mock_model.names = {0: "healthy", 1: "disease"}
    mock_result = MagicMock()
    mock_result.probs.data = [0.8, 0.2]
    mock_model.predict.return_value = [mock_result]
    mock_yolo.return_value = mock_model

    results = PredictHandler.run_model(mock_model, MagicMock())

    assert len(results) == 2
    assert results[0]["class_name"] == "healthy"

def test_convert_to_class_probabilities():
    test_data = [
        {"class_name": "healthy", "probability": 0.9},
        {"class_name": "disease", "probability": 0.1},
    ]

    result = PredictHandler.convert_to_class_probabilities(test_data)

    assert len(result.results) == 2
    assert result.results[0].class_name == "healthy"

@patch("mlcore.grpc_core.servers.handlers.predict.PredictHandler.get_model_path")
@patch("ultralytics.YOLO")
def test_full_flow(mock_get_model, mock_yolo, mock_image):
    mock_get_model.return_value = "test.pt"

    mock_model = MagicMock()
    mock_model.names = {0: "healthy"}
    mock_get_model.return_value = mock_model

    mock_result = MagicMock()
    mock_result.probs.data = [0.9]
    mock_model.predict.return_value = [mock_result]

    mock_yolo.return_value = mock_model

    image = PredictHandler.bytes_to_image(mock_image)
    results = PredictHandler.run_model(mock_model, image)
    pb_result = PredictHandler.convert_to_class_probabilities(results)

    assert len(pb_result.results) == 1
    assert pb_result.results[0].probability == approx(0.9, abs=1e-6)
