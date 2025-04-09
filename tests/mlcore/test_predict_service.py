from unittest.mock import MagicMock, patch

import grpc
import numpy as np
import pytest
from PIL import Image
from pytest import approx

from mlcore.grpc_core.protos.predict import predict_pb2
from mlcore.grpc_core.servers.handlers.predict import PredictHandler
from mlcore.grpc_core.servers.services.predict import PredictService


@pytest.fixture
def predict_service():
    return PredictService()

@pytest.fixture
def valid_request():
    return predict_pb2.PredictorRequest(
        plant=predict_pb2.PLANT_TOMATO,
        image_data=[b"fake_1", b"fake_2"],
    )

@pytest.fixture
def mock_image():
    return Image.fromarray(np.zeros((256, 256, 3), dtype=np.uint8))

def test_predict_success(predict_service, valid_request, mock_image):
    with patch.object(PredictHandler, "get_or_create_model") as mock_get_model, \
         patch.object(PredictHandler, "bytes_to_image") as mock_bytes_to_image, \
         patch.object(PredictHandler, "run_model") as mock_run_model, \
         patch.object(PredictHandler, "convert_to_class_probabilities") as mock_convert:

        mock_model = MagicMock()

        mock_get_model.return_value = mock_model
        mock_bytes_to_image.return_value = mock_image
        mock_run_model.return_value = "mock_result"
        mock_convert.return_value = predict_pb2.ImageResults(
            results=[
                predict_pb2.ClassProbability(class_name="healthy", probability=0.9),
                predict_pb2.ClassProbability(class_name="diseased", probability=0.1),
            ],
        )

        context = MagicMock()
        response = predict_service.Predict(valid_request, context)

        assert len(response.result) == 2
        assert response.result[0].results[0].class_name == "healthy"
        assert response.result[0].results[0].probability == approx(0.9, abs=1e-6)

        context.set_code.assert_not_called()
        context.set_details.assert_not_called()

def test_predict_invalid_plant_type(predict_service):
    invalid_request = predict_pb2.PredictorRequest(
        plant=predict_pb2.PLANT_TOMATO,
        image_data=[b"fake_image_data"],
    )

    with patch.object(PredictHandler, "get_or_create_model") as mock_get_model:
        mock_get_model.side_effect = ValueError("Unsupported plant type")

        context = MagicMock()
        response = predict_service.Predict(invalid_request, context)

        assert len(response.result) == 0

        context.set_code.assert_called_once_with(grpc.StatusCode.INVALID_ARGUMENT)
        context.set_details.assert_called_once_with(
            "Invalid plant type: Unsupported plant type",
        )

def test_predict_image_processing_error(predict_service, valid_request):
    with patch.object(PredictHandler, "get_or_create_model") as mock_get_model, \
         patch.object(PredictHandler, "bytes_to_image") as mock_bytes_to_image:

        mock_get_model.return_value = MagicMock()
        mock_bytes_to_image.side_effect = Exception("Image processing failed")

        context = MagicMock()
        response = predict_service.Predict(valid_request, context)

        assert len(response.result) == 0

        context.set_code.assert_called_once_with(grpc.StatusCode.INTERNAL)
        context.set_details.assert_called_once_with(
            "Error processing image: Image processing failed",
        )

def test_predict_model_run_error(predict_service, valid_request, mock_image):
    with patch.object(PredictHandler, "get_or_create_model") as mock_get_model, \
         patch.object(PredictHandler, "bytes_to_image") as mock_bytes_to_image, \
         patch.object(PredictHandler, "run_model") as mock_run_model:

        mock_get_model.return_value = MagicMock()
        mock_bytes_to_image.return_value = mock_image
        mock_run_model.side_effect = Exception("Model run failed")

        context = MagicMock()
        response = predict_service.Predict(valid_request, context)

        assert len(response.result) == 0

        context.set_code.assert_called_once_with(grpc.StatusCode.INTERNAL)
        context.set_details.assert_called_once_with(
            "Error processing image: Model run failed",
        )

def test_predict_empty_image_data(predict_service):
    empty_request = predict_pb2.PredictorRequest(
        plant=predict_pb2.PLANT_TOMATO,
        image_data=[],
    )

    context = MagicMock()
    response = predict_service.Predict(empty_request, context)

    assert len(response.result) == 0

    context.set_code.assert_not_called()
    context.set_details.assert_not_called()

def test_predict_partial_success(predict_service, valid_request, mock_image):
    with patch.object(PredictHandler, "get_or_create_model") as mock_get_model, \
         patch.object(PredictHandler, "bytes_to_image") as mock_bytes_to_image, \
         patch.object(PredictHandler, "run_model") as mock_run_model, \
         patch.object(PredictHandler, "convert_to_class_probabilities") as mock_convert:

        mock_model = MagicMock()
        mock_get_model.return_value = mock_model

        mock_bytes_to_image.side_effect = [
            mock_image,
            Exception("Image processing failed"),
        ]

        mock_run_model.return_value = "mock_result"
        mock_convert.return_value = predict_pb2.ImageResults(
            results=[
                predict_pb2.ClassProbability(class_name="healthy", probability=0.9),
            ],
        )

        context = MagicMock()
        response = predict_service.Predict(valid_request, context)

        assert len(response.result) == 0

        context.set_code.assert_called_once_with(grpc.StatusCode.INTERNAL)
        context.set_details.assert_called_once_with(
            "Error processing image: Image processing failed",
        )
