# Pull base image
FROM python:3.12

# Set work directory
WORKDIR /app/bot

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY ./requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy code
COPY . .

# CMD
CMD ["python3", "main.py"]
