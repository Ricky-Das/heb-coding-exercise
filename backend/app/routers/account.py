from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app.models import User, Transaction
from app.schemas import (
    BalanceResponse,
    TransactionRequest,
    TransactionResponse,
    DailyLimitResponse
)
from app.auth import get_current_user

router = APIRouter(prefix="/account", tags=["Account Operations"])


@router.get("/balance", response_model=BalanceResponse)
def get_balance(current_user: User = Depends(get_current_user)):
    """Get current account balance"""
    return BalanceResponse(balance=current_user.account.balance)


@router.post("/withdraw", response_model=TransactionResponse)
def withdraw(
    request: TransactionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Withdraw cash from account"""
    account = current_user.account
    
    if account.balance < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    # Reset daily withdrawal if new day
    today = date.today()
    if account.last_withdrawal_date != today:
        account.withdrawn_today = 0.0
        account.last_withdrawal_date = today
    
    # Check daily withdrawal limit
    if account.withdrawn_today + request.amount > account.daily_withdrawal_limit:
        remaining = account.daily_withdrawal_limit - account.withdrawn_today
        raise HTTPException(
            status_code=400,
            detail=f"Daily withdrawal limit exceeded. Remaining: ${remaining:.2f}"
        )
    
    # Process withdrawal
    account.balance -= request.amount
    account.withdrawn_today += request.amount
    
    db.add(Transaction(account_id=account.id, type="withdrawal", amount=request.amount))
    db.commit()
    
    return TransactionResponse(new_balance=account.balance)


@router.post("/deposit", response_model=TransactionResponse)
def deposit(
    request: TransactionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Deposit cash to account"""
    account = current_user.account
    account.balance += request.amount
    
    db.add(Transaction(account_id=account.id, type="deposit", amount=request.amount))
    db.commit()
    
    return TransactionResponse(new_balance=account.balance)


@router.get("/daily-limit", response_model=DailyLimitResponse)
def get_daily_limit(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get daily withdrawal limit information"""
    account = current_user.account
    
    # Reset daily withdrawal if new day
    today = date.today()
    if account.last_withdrawal_date != today:
        account.withdrawn_today = 0.0
        account.last_withdrawal_date = today
        db.commit()
    
    return DailyLimitResponse(
        daily_limit=account.daily_withdrawal_limit,
        withdrawn_today=account.withdrawn_today,
        remaining_today=account.daily_withdrawal_limit - account.withdrawn_today
    )
