
const API_URL = "http://127.0.0.1:8001";

// Retrieve expenses from FastAPI
async function getExpenses() {
    try {
        const response = await fetch(`${API_URL}/expenses`);

        if (!response.ok) {
            throw new Error("Unable to fetch expenses");
        }

        const expenses = await response.json();

        displayExpenses(expenses);

    } catch (error) {
        console.error(error);
        alert("Could not connect to backend");
    }
}

// Display expenses
function displayExpenses(expenses) {
    const expenseList = document.getElementById("expenseList");

    expenseList.innerHTML = "";

    let total = 0;

    expenses.forEach(expense => {
        total += Number(expense.amount ?? 0);

        const row = document.createElement("tr");

        const date = document.createElement("td");
        date.textContent = expense.date;

        const category = document.createElement("td");
        category.textContent = expense.category;

        const description = document.createElement("td");
        description.textContent = expense.description;

        const amount = document.createElement("td");
        amount.textContent = `₹${expense.amount}`;

        const action = document.createElement("td");
        const deleteButton = document.createElement("button");

        deleteButton.textContent = "Delete";
        deleteButton.addEventListener("click", () => {
            deleteExpense(expense.id);
        });

        action.appendChild(deleteButton);

        row.append(date, category, description, amount, action);
        expenseList.appendChild(row);
    });

    document.getElementById("total").textContent =
        `₹${total.toFixed(2)}`;

    document.getElementById("count").textContent =
        expenses.length;
}

// Add new expense
document.getElementById("expenseForm")
    .addEventListener("submit", async function(event)) {

    event.preventDefault();

    const expense = {
        date: document.getElementById("date").value,
        category: document.getElementById("category").value,
        description: document.getElementById("description").value,
        amount: Number(document.getElementById("amount").value)
    };

  
 
    const response = await fetch(
        "http://127.0.0.1:8001/expenses",
        {
            method: "POST",
                headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(expense)
        }
    )};

// Delete expense
async function deleteExpense(id) {
    if (!confirm("Are you sure you want to delete this expense?")) {
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/expenses/${id}`,
            { method: "DELETE" }
        );

        if (!response.ok) {
            throw new Error("Delete failed");
        }

        getExpenses();

    } catch (error) {
        console.error(error);
        alert("Could not delete expense");
    }
}

// Load expenses when page opens
getExpenses();
