FROM python:3.9-slim

WORKDIR /app

# Install Flask
RUN pip install flask

# Create logs directory
RUN mkdir -p /app/logs

# Copy application
COPY app.py .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "app.py"]
