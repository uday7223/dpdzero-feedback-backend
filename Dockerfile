# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY ./app ./app
COPY requirements.txt .


# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY .env .env  

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Start the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
