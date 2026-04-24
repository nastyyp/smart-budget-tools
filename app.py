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

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f8fbff 0%, #eef6ff 100%);
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 18px;
        color: #475569;
        margin-top: 0;
        margin-bottom: 25px;
    }

    .card {
        background: white;
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.07);
        border: 1px solid #e2e8f0;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 10px;
    }

    .small-note {
        color: #64748b;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None

st.markdown('<p class="main-title">Smart Student Budgeting Tool</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Track your income, expenses, and savings with a simple dashboard.</p>', unsafe_allow_html=True)

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

    with st.sidebar:
        st.markdown(f"## 👋 Hello, {user.name}")
        st.write("Welcome to your finance dashboard.")
        st.divider()

        st.markdown("### Quick Stats")
        st.write(f"**Income:** €{user.total_income():.2f}")
        st.write(f"**Expenses:** €{user.total_expenses():.2f}")
        st.write(f"**Balance:** €{user.balance():.2f}")

        st.divider()

        if st.button("Reset Profile", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    st.markdown(f"## Welcome back, {user.name}!")

    # Dashboard first
    tab1, tab2, tab3 = st.tabs(["Dashboard", "Add Income", "Add Expense"])

    with tab1:
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Income", f"€{user.total_income():.2f}")
        col2.metric("Total Expenses", f"€{user.total_expenses():.2f}")
        col3.metric("Balance", f"€{user.balance():.2f}")
        col4.metric("Savings Rate", f"{user.savings_rate():.1f}%")

        st.divider()

        left, right = st.columns([2, 1])

        with left:
            st.markdown("### Financial Overview")

            if user.history:
                running_balance = []
                current = 0
                for item in user.history:
                    if item["Type"] == "Income":
                        current += item["Amount"]
                    else:
                        current -= item["Amount"]
                    running_balance.append(current)

                line_df = pd.DataFrame({
                    "Step": list(range(1, len(running_balance) + 1)),
                    "Balance (€)": running_balance
                }).set_index("Step")

                st.line_chart(line_df)

                compare_df = pd.DataFrame({
                    "Type": ["Income", "Expenses"],
                    "Amount": [user.total_income(), user.total_expenses()]
                }).set_index("Type")

                st.bar_chart(compare_df)

            else:
                st.info("No data yet. Add some income or expenses first.")

        with right:
            st.markdown("### Expense vs Income Analytics")

            if user.total_income() > 0 or user.total_expenses() > 0:
                pie_df = pd.DataFrame({
                    "Category": ["Income", "Expenses"],
                    "Amount": [user.total_income(), user.total_expenses()]
                })

                st.pyplot(
                    pie_df.set_index("Category").plot.pie(
                        y="Amount",
                        autopct="%1.1f%%",
                        figsize=(4, 4),
                        legend=False
                    ).figure
                )
            else:
                st.info("Pie chart will appear after adding data.")

            st.markdown("### Savings Progress")
            progress = max(0.0, min(user.savings_rate() / 100, 1.0))
            st.progress(progress)
            st.write(f"Current savings progress: **{user.savings_rate():.1f}%**")

        st.divider()

        colA, colB = st.columns(2)

        with colA:
            st.markdown("### Recent Activity")
            if user.history:
                history_df = pd.DataFrame(user.history[::-1])
                history_df["Amount"] = history_df["Amount"].apply(lambda x: f"€{x:.2f}")
                st.dataframe(history_df, use_container_width=True, hide_index=True)
            else:
                st.write("No activity yet.")

        with colB:
            st.markdown("### Quick Insights")

            if user.total_income() == 0 and user.total_expenses() == 0:
                st.info("Start by adding income and expenses.")
            else:
                if user.balance() > 0:
                    st.success("Great job! Your balance is positive.")
                elif user.balance() < 0:
                    st.error("Your expenses are higher than your income.")
                else:
                    st.warning("Your balance is exactly zero.")

                st.write(f"- Number of income records: **{len(user.incomes)}**")
                st.write(f"- Number of expense records: **{len(user.expenses)}**")
                st.write(f"- Current balance: **€{user.balance():.2f}**")

    with tab2:
        st.markdown("### Add Income")
        st.write("Enter a new income amount below")

        income = st.number_input(
            "Income amount (€)",
            min_value=0.0,
            step=1.0,
            key="income_input"
        )

        if st.button("Add Income", use_container_width=True):
            if income > 0:
                user.add_income(income)
                st.success(f"Income of €{income:.2f} added.")
                st.rerun()
            else:
                st.error("Enter an amount greater than 0.")

    with tab3:
        st.markdown("### Add Expense")
        st.write("Enter a new expense amount below.")

        expense = st.number_input(
            "Expense amount (€)",
            min_value=0.0,
            step=1.0,
            key="expense_input"
        )

        if st.button("Add Expense", use_container_width=True):
            if expense > 0:
                user.add_expense(expense)
                st.success(f"Expense of €{expense:.2f} added.")
                st.rerun()
            else:
                st.error("Enter an amount greater than 0.")
