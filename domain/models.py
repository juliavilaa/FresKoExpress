import uuid
from datetime import datetime

class Product:
    def __init__(self, name: str, category: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.category = category

class Batch:
    def __init__(self, product: Product, quantity: int, expiration_date: datetime):
        self.id = str(uuid.uuid4())
        self.product = product
        self.quantity = quantity
        self.expiration_date = expiration_date

    def is_expired(self) -> bool:
        """Returns True if the current date is past the expiration date"""
        return datetime.now() > self.expiration_date