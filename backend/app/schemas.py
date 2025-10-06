from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    pin: str = Field(..., min_length=4, max_length=6)


class LoginResponse(BaseModel):
    token: str
    user_id: int
    name: str


class BalanceResponse(BaseModel):
    balance: float


class TransactionRequest(BaseModel):
    amount: float = Field(..., gt=0)


class TransactionResponse(BaseModel):
    new_balance: float


class DailyLimitResponse(BaseModel):
    daily_limit: float
    withdrawn_today: float
    remaining_today: float

