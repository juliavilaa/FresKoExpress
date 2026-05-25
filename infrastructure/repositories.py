from typing import List
from domain.models import Batch

class IInventoryRepository:
    """Repository Interface (Dictated by the architecture)"""
    def save(self, batch: Batch):
        pass
        
    def find_all(self) -> List[Batch]:
        pass

class MemoryInventoryRepository(IInventoryRepository):
    """In-memory implementation for the MVP (Our temporary DB)"""
    def __init__(self):
        # This list is our database for today
        self._db: List[Batch] = [] 

    def save(self, batch: Batch):
        self._db.append(batch)
        print(f"[DB LOG] Batch of {batch.product.name} saved in memory.")

    def find_all(self) -> List[Batch]:
        return self._db