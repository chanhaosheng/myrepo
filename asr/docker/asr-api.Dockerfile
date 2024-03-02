FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/asr_api.py .
COPY src/transcribe.py .

EXPOSE 8001

# Set environment variable to ensure Python logs are sent straight to terminal without being first buffered
ENV PYTHONUNBUFFERED True
ENV FLASK_APP=asr_api.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=8001"]