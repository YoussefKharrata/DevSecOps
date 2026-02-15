FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first
COPY app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire app folder into container
COPY app/ .

EXPOSE 5000

CMD ["python", "app.py"]
