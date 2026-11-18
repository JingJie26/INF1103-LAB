FROM python:3.11-slim

WORKDIR /app

COPY product.py supplier.py inventory.py order.py order_line.py physical_product.py digital_product.py can_be_shipped.py inventory_manager.py inventory.json test_lab8.py ./

ENV PYTHONUNBUFFERED=1

CMD ["python", "inventory_manager.py"]
