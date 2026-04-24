import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
        background: #ffffff;
        color: #111111;
    }

    html, body, [class*="css"] {
        color: #111111;
    }

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #111111;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 18px;
        color: #333333;
        margin-top: 0;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #111111;
        margin-bottom: 10px;
    }

    .login-box {
        background: linear-gradient(135deg, #e0f2fe 0%, #ede9fe 50%, #fce7f3 100%);
        padding: 35px;
        border-radius: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
        margin-top: 20px;
        margin-bottom: 20px;
    }

    .login-title {
        font-size: 34px;
        font-weight: 800;
        color: #111111;
        margin-bottom: 10px;
    }

    .login-subtitle {
        font-size: 17px;
        color: #222222;
        margin-bottom: 18px;
    }

    .info-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.05);
    }

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 16px;
        border-radius: 18px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #444444 !important;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #111111 !important;
    }

    .small-note {
        color: #444444;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    left, right = st.columns([1.1, 0.9])

    with left:
        st.markdown("""
        <div class="login-box">
            <div class="login-title">Smart Student Budgeting Tool</div>
            <div class="login-subtitle">
                Start managing your money in a simple and colorful way.
                Track your income, expenses, and savings with a clean dashboard.
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Create your profile")
        name = st.text_input("Enter your name")

        if st.button("Create Profile", use_container_width=True):
            if name.strip():
                st.session_state.user = User(name)
                st.success(f"Profile created for {name}!")
                st.rerun()
            else:
                st.error("Please enter a name.")

    with right:
        st.markdown("### What you can do")
        st.markdown("""
        <div class="info-card">
            <p style="font-size:18px; font-weight:700; color:#111111;">✨ Features</p>
            <p style="color:#111111;">• Add income in euros</p>
            <p style="color:#111111;">• Add expenses in euros</p>
            <p style="color:#111111;">• See your balance instantly</p>
            <p style="color:#111111;">• View charts and analytics</p>
            <p style="color:#111111;">• Track your savings progress</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.markdown("""
        <div class="info-card">
            <p style="font-size:18px; font-weight:700; color:#111111;">📊 Quick idea</p>
            <p style="color:#111111;">
                After creating your profile, the app opens on the dashboard first.
                Then you can add income and expenses and see the analytics update.
            </p>
        </div>
        """, unsafe_allow_html=True)

else:
    user = st.session_state.user

    st.markdown('<p class="main-title">Smart Student Budgeting Tool</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Track your income, expenses, and savings with a simple dashboard.</p>', unsafe_allow_html=True)

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

                fig, ax = plt.subplots(figsize=(4, 4))
                colors = ["#60a5fa", "#f472b6"]
                ax.pie(
                    pie_df["Amount"],
                    labels=pie_df["Category"],
                    autopct="%1.1f%%",
                    startangle=90,
                    colors=colors,
                    textprops={"color": "black", "fontsize": 10}
                )
                ax.axis("equal")
                fig.patch.set_facecolor("white")
                st.pyplot(fig)
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
        st.write("Enter a new income amount below.")

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
