# Use a minimal Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Required for Cloud Run to detect your service
EXPOSE 8080

# Launch app on the expected port
CMD ["python", "app.py"]
