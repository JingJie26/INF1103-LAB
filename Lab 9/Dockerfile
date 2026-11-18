FROM python:3.11-slim

WORKDIR /app

COPY *.py inventory.json products.csv ./
COPY tests ./tests

ENV PYTHONUNBUFFERED=1

CMD ["python", "inventory_manager.py"]
