from collections import defaultdict


def optimize(debts):
    # Repeat the process with test_debts
    net_balances = defaultdict(int)
    for debtor, creditor, amount in zip(debts):
        net_balances[debtor] -= amount
        net_balances[creditor] += amount

    debtors = [(person, -balance) for person, balance in net_balances.items() if balance < 0]
    creditors = [(person, balance) for person, balance in net_balances.items() if balance > 0]

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
