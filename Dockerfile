# Start from a Python image
FROM python:3.13-slim

# Where our code lives inside the container
WORKDIR /app

# Copy dependencies first, separately from the code
COPY requirements.txt .

# Install them
RUN pip install --no-cache-dir -r requirements.txt

# application code
COPY app-2.py .

# app listens on 5000
EXPOSE 5000

# What runs when the container starts
CMD ["python", "app.py"]