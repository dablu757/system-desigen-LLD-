'''
Liskov Substitution Principle states that child classes must be usable 
in place of parent classes without breaking client code.

'''

from abc import ABC, abstractmethod
class NonWithdrawableAccount(ABC):
    """
    Base abstraction: every account can deposit
    """

    def __init__(self, balance: float = 0.0):
        self.balance = balance

    @abstractmethod
    def deposit(self, amount: float) -> None:
        pass

class WithdrawableAccount(NonWithdrawableAccount):
    """
    Only accounts that support withdrawal inherit this
    """

    @abstractmethod
    def withdraw(self, amount: float) -> None:
        pass



class FixedDepositAccount(NonWithdrawableAccount):
    def deposit(self, amount: float) -> None:
        self.balance += amount
        print(f"Fixed Deposit: Deposited ₹{amount}")


class SavingsAccount(WithdrawableAccount):
    def deposit(self, amount: float) -> None:
        self.balance += amount
        print(f"Savings Account: Deposited ₹{amount}")

    def withdraw(self, amount: float) -> None:
        if amount > self.balance:
            raise ValueError("Insufficient balance")
        self.balance -= amount
        print(f"Savings Account: Withdrawn ₹{amount}")


class CurrentAccount(WithdrawableAccount):
    def deposit(self, amount: float) -> None:
        self.balance += amount
        print(f"Current Account: Deposited ₹{amount}")

    def withdraw(self, amount: float) -> None:
        self.balance -= amount  # overdraft allowed
        print(f"Current Account: Withdrawn ₹{amount}")


class Client:
    def __init__(self):
        self.non_withdrawable_accounts: list[NonWithdrawableAccount] = []
        self.withdrawable_accounts: list[WithdrawableAccount] = []

    def add_non_withdrawable(self, account: NonWithdrawableAccount):
        self.non_withdrawable_accounts.append(account)

    def add_withdrawable(self, account: WithdrawableAccount):
        self.withdrawable_accounts.append(account)

    def process_accounts(self):
        print("\n--- Depositing to all accounts ---")
        for acc in self.non_withdrawable_accounts:
            acc.deposit(1000)

        print("\n--- Depositing & withdrawing from withdrawable accounts ---")
        for acc in self.withdrawable_accounts:
            acc.deposit(1000)
            acc.withdraw(500)



if __name__ == "__main__":
    client = Client()

    fd = FixedDepositAccount(5000)
    savings = SavingsAccount(2000)
    current = CurrentAccount(1000)

    client.add_non_withdrawable(fd)
    client.add_withdrawable(savings)
    client.add_withdrawable(current)

    client.process_accounts()




