import streamlit as st
import pandas as pd

class User:
    def __init__(self, name):
        self.name = name
        self.incomes = []
        self.expenses = []
        self.history = []

    def add_income(self, amount):
        if amount > 0:
            self.incomes.append(amount)
            self.history.append({"Type": "Income", "Amount": amount})

    def add_expense(self, amount):
        if amount > 0:
            self.expenses.append(amount)
            self.history.append({"Type": "Expense", "Amount": amount})

    def total_income(self):
        return sum(self.incomes)

    def total_expenses(self):
        return sum(self.expenses)

    def balance(self):
        return self.total_income() - self.total_expenses()

    def savings_rate(self):
        if self.total_income() == 0:
            return 0
        return (self.balance() / self.total_income()) * 100


st.set_page_config(
    page_title="Smart Student Budgeting Tool",
    page_icon="💶",
    layout="wide"
)

# ---------- Simple styling ----------
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .title-style {
        font-size: 40px;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0;
    }
    .subtitle-style {
        font-size: 18px;
        color: #64748b;
        margin-top: 0;
        margin-bottom: 20px;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.06);
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Session state ----------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------- Header ----------
st.markdown('<p class="title-style">Smart Student Budgeting Tool</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-style">Track your income, expenses, and savings in a simple way.</p>', unsafe_allow_html=True)

# ---------- Create profile ----------
if st.session_state.user is None:
    st.markdown("### Create a User Profile")
    name = st.text_input("Enter your name")

    if st.button("Create Profile", use_container_width=True):
        if name.strip():
            st.session_state.user = User(name)
            st.success(f"Profile created for {name}!")
            st.rerun()
        else:
            st.error("Please enter a name.")

else:
    user = st.session_state.user

    # Sidebar
    with st.sidebar:
        st.markdown(f"## 👋 Hello, {user.name}")
        st.write("Welcome to your budgeting dashboard.")
        st.divider()

        if st.button("Reset Profile", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    # Top welcome
    st.markdown(f"## Welcome back, {user.name}!")

    # ---------- Input area ----------
    tab1, tab2, tab3 = st.tabs(["Add Income", "Add Expense", "Dashboard"])

    with tab1:
        st.markdown("### Add Income")
        income = st.number_input("Enter income amount (€)", min_value=0.0, step=1.0, key="income")
        if st.button("Add Income", use_container_width=True):
            if income > 0:
                user.add_income(income)
                st.success(f"Income of €{income:.2f} added.")
                st.rerun()
            else:
                st.error("Enter an amount greater than 0.")

    with tab2:
        st.markdown("### Add Expense")
        expense = st.number_input("Enter expense amount (€)", min_value=0.0, step=1.0, key="expense")
        if st.button("Add Expense", use_container_width=True):
            if expense > 0:
                user.add_expense(expense)
                st.success(f"Expense of €{expense:.2f} added.")
                st.rerun()
            else:
                st.error("Enter an amount greater than 0.")

    with tab3:
        # ---------- Metrics ----------
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Income", f"€{user.total_income():.2f}")
        col2.metric("Total Expenses", f"€{user.total_expenses():.2f}")
        col3.metric("Balance", f"€{user.balance():.2f}")
        col4.metric("Savings Rate", f"{user.savings_rate():.1f}%")

        st.divider()

        # ---------- Analytics ----------
        left, right = st.columns([2, 1])

        with left:
            st.markdown("### Financial Overview")

            if user.history:
                df = pd.DataFrame(user.history)

                # Running balance chart
                running_balance = []
                current = 0
                for item in user.history:
                    if item["Type"] == "Income":
                        current += item["Amount"]
                    else:
                        current -= item["Amount"]
                    running_balance.append(current)

                chart_df = pd.DataFrame({
                    "Step": list(range(1, len(running_balance) + 1)),
                    "Balance (€)": running_balance
                }).set_index("Step")

                st.line_chart(chart_df)

                # Income vs Expense chart
                compare_df = pd.DataFrame({
                    "Category": ["Income", "Expenses"],
                    "Amount": [user.total_income(), user.total_expenses()]
                }).set_index("Category")

                st.bar_chart(compare_df)

            else:
                st.info("No financial data yet. Add some income or expenses first.")

        with right:
            st.markdown("### Savings Progress")

            if user.total_income() > 0:
                progress = max(0, min(user.savings_rate() / 100, 1.0))
                st.progress(progress)
                st.write(f"Current savings progress: **{user.savings_rate():.1f}%**")
            else:
                st.progress(0)
                st.write("Current savings progress: **0.0%**")

            st.markdown("### Status")

            if user.balance() > 0:
                st.success("Good job! Your balance is positive.")
            elif user.balance() < 0:
                st.error("Warning: Your expenses are higher than your income.")
            else:
                st.warning("Your balance is currently zero.")

        st.divider()

        # ---------- Recent activity ----------
        st.markdown("### Recent Activity")

        if user.history:
            history_df = pd.DataFrame(user.history[::-1])  # newest first
            history_df["Amount"] = history_df["Amount"].apply(lambda x: f"€{x:.2f}")
            st.dataframe(history_df, use_container_width=True, hide_index=True)
        else:
            st.write("No activity yet.")

        # ---------- Small analytics text ----------
        st.divider()
        st.markdown("### Quick Insights")

        if user.total_income() == 0 and user.total_expenses() == 0:
            st.info("Start by adding income and expenses to see insights.")
        else:
            if user.total_income() > user.total_expenses():
                st.success("Your income is currently higher than your expenses.")
            elif user.total_income() < user.total_expenses():
                st.error("Your expenses are currently higher than your income.")
            else:
                st.warning("Your income and expenses are equal.")

            st.write(f"- You have added **{len(user.incomes)}** income records.")
            st.write(f"- You have added **{len(user.expenses)}** expense records.")
            st.write(f"- Your current balance is **€{user.balance():.2f}**.")
