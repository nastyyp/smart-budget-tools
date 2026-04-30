import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(
    page_title="Student Budget",
    page_icon="💶",
    layout="wide"
)

# -----------------------------
# Data model
# -----------------------------
class User:
    def __init__(self, name):
        self.name = name
        self.incomes = []
        self.expenses = []
        self.saved_amount = 0.0

    def add_income(self, amount, note="", entry_date=None):
        if amount > 0:
            self.incomes.append({
                "Amount": amount,
                "Note": note,
                "Date": str(entry_date if entry_date else date.today())
            })

    def add_expense(self, amount, note="", entry_date=None):
        if amount > 0:
            self.expenses.append({
                "Amount": amount,
                "Note": note,
                "Date": str(entry_date if entry_date else date.today())
            })

    def total_income(self):
        return sum(item["Amount"] for item in self.incomes)

    def total_expenses(self):
        return sum(item["Amount"] for item in self.expenses)

    def balance(self):
        return self.total_income() - self.total_expenses()

    def set_saved_amount(self, amount):
        if amount >= 0:
            self.saved_amount = amount

    def savings_rate(self):
        if self.total_income() == 0:
            return 0.0
        return (self.saved_amount / self.total_income()) * 100

    def income_df(self):
        return pd.DataFrame(self.incomes) if self.incomes else pd.DataFrame(columns=["Amount", "Note", "Date"])

    def expense_df(self):
        return pd.DataFrame(self.expenses) if self.expenses else pd.DataFrame(columns=["Amount", "Note", "Date"])


# -----------------------------
# Session state
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None


# -----------------------------
# Login page
# -----------------------------
if not st.session_state.logged_in:
    st.title("💶 Student Budget App")
    st.subheader("Login")
    st.write("Enter your name to start using the app.")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form"):
            name = st.text_input("Your name")
            login_btn = st.form_submit_button("Login", use_container_width=True)

            if login_btn:
                if name.strip():
                    st.session_state.user = User(name.strip())
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Please enter your name.")

    st.stop()


# -----------------------------
# Main app
# -----------------------------
user = st.session_state.user

with st.sidebar:
    st.title("Menu")
    page = st.radio(
        "Go to",
        ["Home", "Income", "Expense", "Savings", "Summary"],
        index=0
    )

    st.divider()
    st.write(f"### 👋 {user.name}")

    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()


# -----------------------------
# Home page
# -----------------------------
if page == "Home":
    st.title("🏠 Home Page")
    st.write("Main information about your budget.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Income", f"€{user.total_income():,.2f}")
    c2.metric("Total Expenses", f"€{user.total_expenses():,.2f}")
    c3.metric("Saved Money", f"€{user.saved_amount:,.2f}")
    c4.metric("Balance", f"€{user.balance():,.2f}")

    st.write("")
    a1, a2 = st.columns(2)

    with a1:
        st.write("### Quick Info")
        st.info(f"Income records: {len(user.incomes)}")
        st.warning(f"Expense records: {len(user.expenses)}")
        st.success(f"Savings rate: {user.savings_rate():.1f}%")

    with a2:
        st.write("### Status")
        if user.balance() > 0:
            st.success("Your balance is positive.")
        elif user.balance() < 0:
            st.error("Your expenses are higher than your available money.")
        else:
            st.warning("Your balance is zero.")

        if user.saved_amount > 0:
            st.info(f"You have saved €{user.saved_amount:,.2f}.")
        else:
            st.info("You have not added savings yet.")


# -----------------------------
# Income page
# -----------------------------
elif page == "Income":
    st.title("➕ Income")
    st.write("Add your income here.")

    with st.form("income_form"):
        col1, col2 = st.columns(2)

        with col1:
            income_amount = st.number_input("Income amount (€)", min_value=0.0, step=1.0, format="%.2f")
            income_date = st.date_input("Income date", value=date.today())

        with col2:
            income_note = st.text_input("Note", placeholder="e.g. Salary, scholarship")

        save_income = st.form_submit_button("Save Income", use_container_width=True)

        if save_income:
            if income_amount > 0:
                user.add_income(income_amount, income_note, income_date)
                st.success(f"Income of €{income_amount:.2f} added.")
                st.rerun()
            else:
                st.error("Please enter an amount greater than 0.")

    df_income = user.income_df()
    if not df_income.empty:
        st.write("### Income History")
        df_income_display = df_income.copy()
        df_income_display["Amount"] = df_income_display["Amount"].apply(lambda x: f"€{x:,.2f}")
        st.dataframe(df_income_display[::-1].reset_index(drop=True), use_container_width=True, hide_index=True)


# -----------------------------
# Expense page
# -----------------------------
elif page == "Expense":
    st.title("➖ Expense")
    st.write("Add your expenses here.")

    with st.form("expense_form"):
        col1, col2 = st.columns(2)

        with col1:
            expense_amount = st.number_input("Expense amount (€)", min_value=0.0, step=1.0, format="%.2f")
            expense_date = st.date_input("Expense date", value=date.today())

        with col2:
            expense_note = st.text_input("Note", placeholder="e.g. Food, transport")

        save_expense = st.form_submit_button("Save Expense", use_container_width=True)

        if save_expense:
            if expense_amount > 0:
                user.add_expense(expense_amount, expense_note, expense_date)
                st.success(f"Expense of €{expense_amount:.2f} added.")
                st.rerun()
            else:
                st.error("Please enter an amount greater than 0.")

    df_expense = user.expense_df()
    if not df_expense.empty:
        st.write("### Expense History")
        df_expense_display = df_expense.copy()
        df_expense_display["Amount"] = df_expense_display["Amount"].apply(lambda x: f"€{x:,.2f}")
        st.dataframe(df_expense_display[::-1].reset_index(drop=True), use_container_width=True, hide_index=True)


# -----------------------------
# Savings page
# -----------------------------
elif page == "Savings":
    st.title("💰 Savings")
    st.write("This section is separate from income and expenses.")

    with st.form("savings_form"):
        saved_amount = st.number_input(
            "How much money have you saved? (€)",
            min_value=0.0,
            step=1.0,
            value=float(user.saved_amount),
            format="%.2f"
        )

        save_savings = st.form_submit_button("Save Savings", use_container_width=True)

        if save_savings:
            user.set_saved_amount(saved_amount)
            st.success(f"Saved amount updated to €{saved_amount:.2f}.")
            st.rerun()

    st.write("### Savings Overview")
    col1, col2 = st.columns(2)
    col1.metric("Saved Money", f"€{user.saved_amount:,.2f}")
    col2.metric("Savings Rate", f"{user.savings_rate():.1f}%")

    if user.total_income() > 0 or user.saved_amount > 0:
        chart_labels = ["Saved Money", "Remaining / Other Money"]
        other_amount = max(user.total_income() - user.saved_amount, 0)
        chart_values = [user.saved_amount, other_amount]

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(chart_values, labels=chart_labels, autopct="%1.0f%%", startangle=90)
        ax.set_title("Savings Distribution")
        st.pyplot(fig)
        plt.close(fig)


# -----------------------------
# Summary page
# -----------------------------
elif page == "Summary":
    st.title("📌 Summary")
    st.write("General conclusion of your current financial situation.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Income", f"€{user.total_income():,.2f}")
    c2.metric("Expenses", f"€{user.total_expenses():,.2f}")
    c3.metric("Savings", f"€{user.saved_amount:,.2f}")
    c4.metric("Balance", f"€{user.balance():,.2f}")

    st.write("### Conclusion")

    if user.total_income() == 0 and user.total_expenses() == 0:
        st.info("You have not added any financial data yet.")
    else:
        if user.balance() > 0:
            st.success("You are currently managing your budget well because your balance is positive.")
        elif user.balance() < 0:
            st.error("Your expenses are too high compared to your income.")
        else:
            st.warning("Your balance is zero, so you should track future spending carefully.")

        if user.saved_amount > 0:
            st.info(f"You have already saved €{user.saved_amount:,.2f}.")
        else:
            st.warning("You have not entered any savings yet.")

    st.write("### Financial Comparison")

    labels = ["Income", "Expenses", "Savings"]
    values = [user.total_income(), user.total_expenses(), user.saved_amount]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(labels, values)
    ax.set_ylabel("€")
    ax.set_title("Income vs Expenses vs Savings")
    st.pyplot(fig)
    plt.close(fig)
