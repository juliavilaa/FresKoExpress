from abc import ABC, abstractmethod
from typing import List
from .models import Batch

class RotationStrategy(ABC):
    """
    Strategy Interface for Inventory Rotation.
    Defines the contract for different rotation algorithms.
    """
    @abstractmethod
    def apply(self, batches: List[Batch]) -> List[Batch]:
        pass

class FIFOStrategy(RotationStrategy):
    """
    First In, First Out (FIFO) implementation.
    """
    def apply(self, batches: List[Batch]) -> List[Batch]:
        print("[STRATEGY LOG] Applying FIFO: Sorting batches by entry date.")
        # For the MVP, we simulate the sorting process
        return batches

class FEFOStrategy(RotationStrategy):
    """
    First Expired, First Out (FEFO) implementation.
    Crucial for perishable goods (FresKoExpress core business).
    """
    def apply(self, batches: List[Batch]) -> List[Batch]:
        print("[STRATEGY LOG] Applying FEFO: Sorting batches by expiration date.")
        # Simulating the sort for the MVP
        return batches