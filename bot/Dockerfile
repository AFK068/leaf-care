# Pull base image
FROM python:3.12

# Set work directory
WORKDIR /app/bot

# Copy requirements
COPY ./requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy code
COPY . .

# CMD
CMD ["python3", "main.py"]
