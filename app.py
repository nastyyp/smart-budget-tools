import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit,
    QVBoxLayout, QHBoxLayout, QFrame, QGridLayout, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class User:
    def __init__(self, name):
        self.name = name
        self.incomes = []
        self.expenses = []
        self.history = []

    def add_income(self, amount):
        if amount > 0:
            self.incomes.append(amount)
            self.history.append(("Income", amount))

    def add_expense(self, amount):
        if amount > 0:
            self.expenses.append(amount)
            self.history.append(("Expense", amount))

    def total_income(self):
        return sum(self.incomes)

    def total_expenses(self):
        return sum(self.expenses)

    def balance(self):
        return self.total_income() - self.total_expenses()


class Card(QFrame):
    def __init__(self, title, value, color):
        super().__init__()
        self.setObjectName("card")
        layout = QVBoxLayout()

        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Arial", 10))
        self.title_label.setStyleSheet("color: #444;")

        self.value_label = QLabel(value)
        self.value_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.value_label.setStyleSheet(f"color: {color};")

        layout.addWidget(self.title_label)
        layout.addWidget(self.value_label)
        self.setLayout(layout)


class BudgetApp(QWidget):
    def __init__(self):
        super().__init__()
        self.user = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Smart Student Budgeting Tool")
        self.resize(1000, 700)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)

        # Header
        title = QLabel("Smart Student Budgeting Tool")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("color: black;")

        subtitle = QLabel("Simple desktop budgeting app in Python")
        subtitle.setStyleSheet("color: #555; font-size: 14px;")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # Profile section
        profile_frame = QFrame()
        profile_frame.setObjectName("section")
        profile_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your name")

        self.create_profile_btn = QPushButton("Create Profile")
        self.create_profile_btn.clicked.connect(self.create_profile)

        self.profile_label = QLabel("No profile created yet")
        self.profile_label.setStyleSheet("font-weight: bold; color: #333;")

        profile_layout.addWidget(QLabel("Profile:"))
        profile_layout.addWidget(self.name_input)
        profile_layout.addWidget(self.create_profile_btn)
        profile_layout.addWidget(self.profile_label)

        profile_frame.setLayout(profile_layout)
        main_layout.addWidget(profile_frame)

        # Summary cards
        cards_layout = QGridLayout()

        self.income_card = Card("Total Income", "€0.00", "#16a34a")
        self.expense_card = Card("Total Expenses", "€0.00", "#dc2626")
        self.balance_card = Card("Balance", "€0.00", "#2563eb")

        cards_layout.addWidget(self.income_card, 0, 0)
        cards_layout.addWidget(self.expense_card, 0, 1)
        cards_layout.addWidget(self.balance_card, 0, 2)

        main_layout.addLayout(cards_layout)

        # Input section
        actions_frame = QFrame()
        actions_frame.setObjectName("section")
        actions_layout = QGridLayout()

        self.income_input = QLineEdit()
        self.income_input.setPlaceholderText("Enter income amount (€)")

        self.expense_input = QLineEdit()
        self.expense_input.setPlaceholderText("Enter expense amount (€)")

        self.add_income_btn = QPushButton("Add Income")
        self.add_expense_btn = QPushButton("Add Expense")

        self.add_income_btn.clicked.connect(self.add_income)
        self.add_expense_btn.clicked.connect(self.add_expense)

        actions_layout.addWidget(QLabel("Income:"), 0, 0)
        actions_layout.addWidget(self.income_input, 0, 1)
        actions_layout.addWidget(self.add_income_btn, 0, 2)

        actions_layout.addWidget(QLabel("Expense:"), 1, 0)
        actions_layout.addWidget(self.expense_input, 1, 1)
        actions_layout.addWidget(self.add_expense_btn, 1, 2)

        actions_frame.setLayout(actions_layout)
        main_layout.addWidget(actions_frame)

        # History table
        history_title = QLabel("Recent Activity")
        history_title.setFont(QFont("Arial", 14, QFont.Bold))
        history_title.setStyleSheet("color: black;")
        main_layout.addWidget(history_title)

        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Type", "Amount"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        main_layout.addWidget(self.table)

        self.setLayout(main_layout)
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
                font-family: Arial;
                color: black;
            }

            QFrame#section {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 14px;
                padding: 10px;
            }

            QFrame#card {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 16px;
                padding: 12px;
            }

            QLineEdit {
                background-color: white;
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                padding: 8px;
                color: black;
            }

            QPushButton {
                border: none;
                border-radius: 10px;
                padding: 10px 14px;
                font-weight: bold;
                color: white;
            }

            QPushButton:hover {
                opacity: 0.9;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                gridline-color: #e5e7eb;
                color: black;
            }

            QHeaderView::section {
                background-color: #eaf2ff;
                color: black;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

        self.create_profile_btn.setStyleSheet("""
            QPushButton {
                background-color: #7c3aed;
                color: white;
                border-radius: 10px;
                padding: 10px 14px;
                font-weight: bold;
            }
        """)

        self.add_income_btn.setStyleSheet("""
            QPushButton {
                background-color: #16a34a;
                color: white;
                border-radius: 10px;
                padding: 10px 14px;
                font-weight: bold;
            }
        """)

        self.add_expense_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc2626;
                color: white;
                border-radius: 10px;
                padding: 10px 14px;
                font-weight: bold;
            }
        """)

    def create_profile(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Please enter your name.")
            return

        self.user = User(name)
        self.profile_label.setText(f"Logged in as: {name}")
        QMessageBox.information(self, "Success", f"Profile created for {name}.")

    def add_income(self):
        if not self.user:
            QMessageBox.warning(self, "Error", "Create a profile first.")
            return

        try:
            amount = float(self.income_input.text())
            if amount <= 0:
                raise ValueError
            self.user.add_income(amount)
            self.income_input.clear()
            self.update_ui()
        except ValueError:
            QMessageBox.warning(self, "Error", "Enter a valid income amount.")

    def add_expense(self):
        if not self.user:
            QMessageBox.warning(self, "Error", "Create a profile first.")
            return

        try:
            amount = float(self.expense_input.text())
            if amount <= 0:
                raise ValueError
            self.user.add_expense(amount)
            self.expense_input.clear()
            self.update_ui()
        except ValueError:
            QMessageBox.warning(self, "Error", "Enter a valid expense amount.")

    def update_ui(self):
        self.income_card.value_label.setText(f"€{self.user.total_income():.2f}")
        self.expense_card.value_label.setText(f"€{self.user.total_expenses():.2f}")
        self.balance_card.value_label.setText(f"€{self.user.balance():.2f}")

        self.table.setRowCount(len(self.user.history))
        for row, (entry_type, amount) in enumerate(reversed(self.user.history)):
            self.table.setItem(row, 0, QTableWidgetItem(entry_type))
            self.table.setItem(row, 1, QTableWidgetItem(f"€{amount:.2f}"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BudgetApp()
    window.show()
    sys.exit(app.exec_())
