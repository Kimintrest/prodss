from collections import defaultdict
import firebase_admin
from firebase_admin import credentials, firestore

# Инициализация Firebase
cred = credentials.Certificate("splitpaysplitergroup-firebase-adminsdk-fp08h-3551a8a3cb.json")
firebase_admin.initialize_app(cred)

# Инициализация Firestore
db = firestore.client()

def optimize(debts):
    # Словарь для учета чистых балансов
    net_balances = defaultdict(int)

    for debtor, creditor, amount in debts:
        net_balances[debtor] -= amount
        net_balances[creditor] += amount

    # Создание списков должников и кредиторов
    debtors = [(person, -balance) for person, balance in net_balances.items() if balance < 0]
    creditors = [(person, balance) for person, balance in net_balances.items() if balance > 0]

    # Сортировка должников по задолженности (по возрастанию)
    debtors.sort(key=lambda x: x[1])  # Сортируем по второму элементу (сумме долга)

    # Сортировка кредиторов по кредиту (по убыванию)
    creditors.sort(key=lambda x: x[1], reverse=True)  # Сортируем по второму элементу (сумме кредита)

    transactions = []
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor, debt_amount = debtors[i]
        creditor, credit_amount = creditors[j]
        transaction_amount = min(debt_amount, credit_amount)

        transactions.append((debtor, creditor, transaction_amount))

        debtors[i] = (debtor, debt_amount - transaction_amount)
        creditors[j] = (creditor, credit_amount - transaction_amount)

        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1

    # Отправка транзакций в Firestore
    save_transactions_to_firebase(transactions)
    
    return transactions

def save_transactions_to_firebase(transactions):
    try:
        for debtor, creditor, amount in transactions:
            transaction_data = {
                "debtor": debtor,
                "creditor": creditor,
                "amount": amount
            }
            db.collection('transactions').add(transaction_data)
        print("Transactions saved to Firebase successfully.")
    except Exception as e:
        print(f"Error saving transactions to Firebase: {e}")

# Пример использования функции optimize
debts = [
    ("Alice", "Bob", 50),
    ("Bob", "Charlie", 30),
    ("Charlie", "Alice", 20),
]

optimized_transactions = optimize(debts)
print("Optimized Transactions:", optimized_transactions)
