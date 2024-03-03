FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY elastic-backend/src/cv-index.py .

CMD ["python", "./cv-index.py"]