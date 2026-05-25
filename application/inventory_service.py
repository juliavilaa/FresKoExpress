from domain.strategies import RotationStrategy
from infrastructure.repositories import IInventoryRepository
from domain.models import Batch

class InventoryService:
    """
    Application Service that orchestrates domain logic and infrastructure.
    """
    def __init__(self, repository: IInventoryRepository, strategy: RotationStrategy):
        # Dependency Injection (DI) allows us to change the DB or Strategy easily
        self.repository = repository
        self.strategy = strategy

    def add_batch(self, batch: Batch):
        """Registers a new product batch into the inventory"""
        print(f"[SERVICE LOG] Registering new batch of {batch.product.name}...")
        self.repository.save(batch)

    def get_available_stock(self) -> list:
        """Retrieves stock and applies the defined rotation strategy (FIFO/FEFO)"""
        print("[SERVICE LOG] Fetching stock from database...")
        all_batches = self.repository.find_all()
        
        print("[SERVICE LOG] Applying business rules...")
        return self.strategy.apply(all_batches)