from collections import defaultdict


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

    return transactions
