FROM python:3.11-slim

WORKDIR /app

COPY inventory.py .

# Force Python output to display immediately in terminal without buffering
ENV PYTHONUNBUFFERED=1

CMD ["python", "inventory.py"]
