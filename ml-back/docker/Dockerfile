# Pull base image
FROM python:3.12

# Set work directory
WORKDIR /app

# Copy project
COPY docker/requirements.txt /app/requirements.txt
COPY predict/predict_server.py /app/predict_server.py
COPY predict/proto /app/proto
COPY predict/models /app/models

# Install dependencies
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6  -

CMD ["python", "predict_server.py"]
