from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore
import uvicorn

# Инициализация Firebase
cred = credentials.Certificate("splitpaysplitergroup-firebase-adminsdk-fp08h-3551a8a3cb.json")
firebase_admin.initialize_app(cred)

# Инициализация Firestore
db = firestore.client()

app = FastAPI()

class Debt(BaseModel):
    debtor: str
    creditor: str
    amount: float

@app.post("/optimize_debts/")
async def optimize_debts(debts: list[Debt]):
    # Словарь для хранения чистых балансов
    net_balances = {}

    # Расчет чистых балансов
    for debt in debts:
        net_balances[debt.debtor] = net_balances.get(debt.debtor, 0) - debt.amount
        net_balances[debt.creditor] = net_balances.get(debt.creditor, 0) + debt.amount

    # Разделение на должников и кредиторов
    debtors = [(person, -balance) for person, balance in net_balances.items() if balance < 0]
    creditors = [(person, balance) for person, balance in net_balances.items() if balance > 0]

    transactions = []
    i, j = 0, 0

    # Оптимизация долгов
    while i < len(debtors) and j < len(creditors):
        debtor, debt_amount = debtors[i]
        creditor, credit_amount = creditors[j]
        transaction_amount = min(debt_amount, credit_amount)

        transactions.append((debtor, creditor, transaction_amount))

        # Обновление оставшихся долгов
        debtors[i] = (debtor, debt_amount - transaction_amount)
        creditors[j] = (creditor, credit_amount - transaction_amount)

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    # Отправка транзакций в Firestore
    for debtor, creditor, amount in transactions:
        transaction_data = {
            'debtor_id': debtor,
            'creditor_id': creditor,
            'amount': amount
        }
        try:
            db.collection('transactions').add(transaction_data)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при добавлении транзакции в Firestore: {str(e)}")

    return {"optimized_transactions": transactions}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
