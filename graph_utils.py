import firebase_admin
from firebase_admin import credentials, firestore
from collections import defaultdict

# Инициализация Firebase
cred = credentials.Certificate("splitpaysplitergroup-firebase-adminsdk-fp08h-3551a8a3cb.json")
firebase_admin.initialize_app(cred)

# Инициализация Firestore
db = firestore.client()

def optimize_and_send_to_firebase(debts):
    # Словарь для хранения чистых балансов
    net_balances = defaultdict(int)
    
    # Расчет чистых балансов
    for debtor, creditor, amount in debts:
        net_balances[debtor] -= amount
        net_balances[creditor] += amount

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
            print(f"Транзакция добавлена: {debtor} должен {creditor} сумму {amount}.")
        except Exception as e:
            print(f"Ошибка при добавлении транзакции в Firestore: {str(e)}")

    return transactions

# Пример использования функции
debts = [
    ('user1', 'user2', 100),
    ('user2', 'user3', 50),
    ('user1', 'user3', 150),
]

optimized_transactions = optimize_and_send_to_firebase(debts)
print("Оптимизированные транзакции:", optimized_transactions)
