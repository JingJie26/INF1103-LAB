FROM python:3.11-slim

WORKDIR /app

COPY product.py inventory.py physical_product.py digital_product.py can_be_shipped.py inventory_manager.py inventory.json ./

ENV PYTHONUNBUFFERED=1

CMD ["python", "inventory_manager.py"]