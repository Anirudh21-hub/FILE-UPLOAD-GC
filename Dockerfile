# Base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app code
COPY . .

# Expose port
EXPOSE 8080

# Run Flask app
CMD ["python", "app.py"]

