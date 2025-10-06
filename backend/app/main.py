from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db, SessionLocal
from app.models import User, Account
from app.routers import auth, account

app = FastAPI(
    title="ATM API",
    description="Simple ATM REST API for customer authentication and account operations",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(account.router)


@app.on_event("startup")
def startup_event():
    """Initialize database and seed with test data"""
    init_db()
    
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            for name, pin, balance in [
                ("John Doe", "1234", 5000.0),
                ("Jane Smith", "5678", 10000.0),
                ("Bob Johnson", "9999", 2500.0),
            ]:
                user = User(name=name, pin=pin)
                db.add(user)
                db.flush()
                db.add(Account(user_id=user.id, balance=balance, daily_withdrawal_limit=1000.0))
            
            db.commit()
            print("✅ Database seeded with test PINs: 1234, 5678, 9999")
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "ATM API", "docs": "/docs"}

