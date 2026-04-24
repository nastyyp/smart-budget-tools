import streamlit as st

class User:
    def __init__(self, name):
        self.name = name
        self.incomes = []
        self.expenses = []

    def add_income(self, amount):
        if amount > 0:
            self.incomes.append(amount)

    def add_expense(self, amount):
        if amount > 0:
            self.expenses.append(amount)

    def total_income(self):
        return sum(self.incomes)

    def total_expenses(self):
        return sum(self.expenses)

    def balance(self):
        return self.total_income() - self.total_expenses()


st.set_page_config(page_title="Smart Budgeting Tool", page_icon="💰", layout="centered")

st.title("Smart Student Budgeting Tool")

if "user" not in st.session_state:
    st.session_state.user = None

# Create profile
if st.session_state.user is None:
    st.subheader("Create a User Profile")
    name = st.text_input("Enter your name")

    if st.button("Create Profile"):
        if name.strip():
            st.session_state.user = User(name)
            st.success(f"Profile created for {name}!")
        else:
            st.error("Please enter a name.")

else:
    user = st.session_state.user
    st.subheader(f"Welcome, {user.name}")

    tab1, tab2, tab3 = st.tabs(["Add Income", "Add Expense", "Summary"])

    with tab1:
        income = st.number_input("Enter income amount", min_value=0.0, step=1.0, key="income")
        if st.button("Add Income"):
            if income > 0:
                user.add_income(income)
                st.success(f"Income of ${income:.2f} added.")
            else:
                st.error("Enter an amount greater than 0.")

    with tab2:
        expense = st.number_input("Enter expense amount", min_value=0.0, step=1.0, key="expense")
        if st.button("Add Expense"):
            if expense > 0:
                user.add_expense(expense)
                st.success(f"Expense of ${expense:.2f} added.")
            else:
                st.error("Enter an amount greater than 0.")

    with tab3:
        st.write(f"**Name:** {user.name}")
        st.write(f"**Total Income:** ${user.total_income():.2f}")
        st.write(f"**Total Expenses:** ${user.total_expenses():.2f}")
        st.write(f"**Balance:** ${user.balance():.2f}")