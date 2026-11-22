from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from database import (
    get_expenses,
    add_expense,
    get_total_spending,
    update_expense,
    delete_expense,
)

app = FastAPI(title="Expense Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExpenseCreate(BaseModel):
    date: str
    category: str
    description: str
    amount: float = Field(gt=0)

    
@app.get("/")
def home():
    return {"message": "Welcome to Expense Tracker API"}


@app.get("/expenses")
def view_expenses():
    return get_expenses()


@app.get("/total-spending")
def total_spending():
    return {"total": get_total_spending()}


@app.post("/add-expense", status_code=201)
def create_expense(expense: ExpenseCreate):
    expense_id = add_expense(
        expense.date,
        expense.category,
        expense.description,
        expense.amount,
    )
    return {
        "message": "Expense added successfully",
        "expense_id": expense_id,
    }


@app.put("/expenses/{expense_id}")
def update_expense_api(expense_id: int, expense: ExpenseCreate):
    updated = update_expense(
        expense_id,
        expense.date,
        expense.category,
        expense.description,
        expense.amount,
    )
    if updated == 0:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {
        "message": "Expense updated successfully",
        "expense_id": expense_id,
    }


@app.delete("/expenses/{expense_id}")
def remove_expense(expense_id: int):
    deleted = delete_expense(expense_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="Expense not found")

    return {
        "message": "Expense deleted successfully",
        "expense_id": expense_id,
    }
