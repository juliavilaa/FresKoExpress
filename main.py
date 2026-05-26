from fastapi import FastAPI
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from domain.models import Product, Batch
from domain.strategies import FEFOStrategy
from infrastructure.repositories import MemoryInventoryRepository
from infrastructure.event_bus import EventBus
from application.inventory_service import InventoryService

# 1. Initialize Infrastructure (The "Backend" of our Backend)
repository = MemoryInventoryRepository()
event_bus = EventBus()

# 2. Initialize Domain Strategies (The Business Rules - Pattern Strategy)
rotation_strategy = FEFOStrategy()

# 3. Initialize Application Service (The Orchestrator)
# Dependency Injection is applied here
inventory_service = InventoryService(repository, rotation_strategy)

# 4. Initialize FastAPI (The Microservice API Gateway)
app = FastAPI(title="FresKoExpress - Inventory Microservice", version="1.0 MVP")


# --- AUTH SERVICE SIMULATION ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Simulates the Auth Service generating a JWT token"""
    # Hardcoded validation for MVP
    if form_data.username == "admin" and form_data.password == "1234":
        return {"access_token": "fresko-super-secure-token-999", "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

# --- API Endpoints (The URLs we will test) ---

@app.get("/")
def read_root():
    return {"message": "Inventory Microservice is running!"}

@app.post("/api/inventory/batches")
def create_batch(product_name: str, category: str, quantity: int, days_to_expire: int, token: str = Depends(oauth2_scheme)):
    """Endpoint to add a new batch of a product"""
    
    # 1. Create domain objects
    product = Product(name=product_name, category=category)
    expiration = datetime.now() + timedelta(days=days_to_expire)
    new_batch = Batch(product=product, quantity=quantity, expiration_date=expiration)
    
    # 2. Use the application service
    inventory_service.add_batch(new_batch)
    
    # 3. Trigger Observer Pattern
    event_bus.publish("BatchCreated", {"product": product.name, "qty": quantity})
    
    return {"status": "success", "batch_id": new_batch.id}

@app.get("/api/inventory/stock")
def get_stock():
    """Endpoint to retrieve available stock applying FEFO strategy"""
    
    # Call the service which automatically applies the Strategy Pattern
    stock = inventory_service.get_available_stock()
    
    # Formatting the response for the frontend/client
    return [
        {
            "batch_id": b.id,
            "product": b.product.name,
            "quantity": b.quantity,
            "expires_in_days": (b.expiration_date - datetime.now()).days
        } for b in stock
    ]

# --- SIMULATED NOTIFICATION SERVICE (Listening to EventBus) ---
notification_history = []

def notification_listener(event_name: str, payload: dict):
    """Acts as the Notification Service subscribing to the EventBus"""
    time_now = datetime.now().strftime("%H:%M:%S")
    notification_history.insert(0, {"time": time_now, "event": event_name, "details": payload})

# Subscribe the listener to the bus
event_bus.subscribe(notification_listener)

@app.get("/api/notifications")
def get_notifications():
    """Endpoint to fetch live system events"""
    return notification_history[:5] # Return only the latest 5 events