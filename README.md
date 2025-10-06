# ATM System

ATM (Automated Teller Machine) application built with React frontend and Python FastAPI backend.

## Features

### Part I - User Interface

- Customer authentication with PIN
- Display current account balance
- Simulate cash withdrawal
- Simulate deposits
- Display daily withdrawal limit

### Part II - REST API

- HTTP REST API with FastAPI
- OpenAPI/Swagger specification (auto-generated)
- SQLite persistent data store
- Clean, simple implementation following best practices

## Tech Stack

**Frontend:**

- React 18
- Vite
- Axios
- Modern CSS with gradient styling

**Backend:**

- Python 3.9+
- FastAPI
- SQLAlchemy ORM
- SQLite database
- Pydantic for data validation

## Quick Start

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

**API Documentation:** Visit `http://localhost:8000/docs` for interactive Swagger UI

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The application will be available at `http://localhost:5173`

## Test Accounts

The database is automatically seeded with test accounts:

| PIN  | Name        | Initial Balance |
| ---- | ----------- | --------------- |
| 1234 | John Doe    | $5,000.00       |
| 5678 | Jane Smith  | $10,000.00      |
| 9999 | Bob Johnson | $2,500.00       |

**Daily Withdrawal Limit:** $1,000.00 per account

## API Endpoints

### Authentication

- `POST /auth/login` - Authenticate with PIN

### Account Operations

- `GET /account/balance` - Get current balance
- `POST /account/withdraw` - Withdraw cash
- `POST /account/deposit` - Deposit cash
- `GET /account/daily-limit` - Get daily withdrawal limit info

Full API documentation available at `/docs` when running the backend.

### Database Schema

- **Users:** Store customer information and PINs
- **Accounts:** Track balance and withdrawal limits
- **Transactions:** Log all deposits and withdrawals
