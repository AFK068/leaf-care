# Pull base image
FROM python:3.12

# Set work directory
WORKDIR /app

# Copy requirements
COPY ./requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6  -

# Copy code
COPY . .

# CMD
CMD ["python3", "main.py"]
