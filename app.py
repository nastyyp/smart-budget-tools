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

# Force light look as much as possible with pure Streamlit elements
st.title("Smart Student Budgeting Tool")
st.caption("Track your income, expenses, and savings in euros.")

if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- LOGIN / PROFILE PAGE ----------------
if st.session_state.user is None:
    st.subheader("Create Your Profile")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.info("👋 Welcome to your budgeting app")
        st.success("✅ Track income")
        st.warning("💸 Manage expenses")
        st.info("📊 View analytics")
        st.success("🎯 Improve savings")

    with col2:
        st.write("### Let's get started")
        name = st.text_input("Enter your name")

        favorite_color = st.selectbox(
            "Choose your dashboard mood",
            ["Blue", "Green", "Purple", "Orange"]
        )

        if st.button("Create Profile", use_container_width=True):
            if name.strip():
                st.session_state.user = User(name)
                st.session_state.color = favorite_color
                st.success(f"Profile created for {name}!")
                st.rerun()
            else:
                st.error("Please enter a name.")

    st.divider()

    a, b, c, d = st.columns(4)
    a.metric("Easy Setup", "1 min")
    b.metric("Currency", "Euro €")
    c.metric("Charts", "Included")
    d.metric("Mode", "Student Friendly")

# ---------------- MAIN APP ----------------
else:
    user = st.session_state.user
    color = st.session_state.get("color", "Blue")

    # Sidebar
    with st.sidebar:
        st.write(f"## Hello, {user.name} 👋")
        st.write("### Profile")
        st.write(f"**Theme mood:** {color}")
        st.write(f"**Income:** €{user.total_income():.2f}")
        st.write(f"**Expenses:** €{user.total_expenses():.2f}")
        st.write(f"**Balance:** €{user.balance():.2f}")

        st.divider()

        if st.button("Reset Profile", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    st.subheader(f"Welcome back, {user.name}")

    tab1, tab2, tab3 = st.tabs(["Dashboard", "Add Income", "Add Expense"])

    # ---------------- DASHBOARD ----------------
    with tab1:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Income", f"€{user.total_income():.2f}")
        c2.metric("Total Expenses", f"€{user.total_expenses():.2f}")
        c3.metric("Balance", f"€{user.balance():.2f}")
        c4.metric("Savings Rate", f"{user.savings_rate():.1f}%")

        st.divider()

        left, right = st.columns([2, 1])

        with left:
            st.write("### Financial Overview")

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
                st.info("No data yet. Add income or expenses first.")

        with right:
            st.write("### Income vs Expenses")

            if user.total_income() > 0 or user.total_expenses() > 0:
                pie_values = [user.total_income(), user.total_expenses()]
                pie_labels = ["Income", "Expenses"]

                fig, ax = plt.subplots()
                ax.pie(
                    pie_values,
                    labels=pie_labels,
                    autopct="%1.1f%%",
                    startangle=90
                )
                ax.axis("equal")
                st.pyplot(fig)
            else:
                st.info("Pie chart will appear after adding data.")

            st.write("### Savings Progress")
            progress = max(0.0, min(user.savings_rate() / 100, 1.0))
            st.progress(progress)
            st.write(f"Current savings progress: **{user.savings_rate():.1f}%**")

        st.divider()

        p1, p2 = st.columns(2)

        with p1:
            st.write("### Recent Activity")
            if user.history:
                history_df = pd.DataFrame(user.history[::-1])
                history_df["Amount"] = history_df["Amount"].apply(lambda x: f"€{x:.2f}")
                st.dataframe(history_df, use_container_width=True, hide_index=True)
            else:
                st.write("No activity yet.")

        with p2:
            st.write("### Quick Insights")

            if user.total_income() == 0 and user.total_expenses() == 0:
                st.info("Start by adding income and expenses.")
            else:
                if user.balance() > 0:
                    st.success("Great job! Your balance is positive.")
                elif user.balance() < 0:
                    st.error("Your expenses are higher than your income.")
                else:
                    st.warning("Your balance is zero.")

                st.write(f"- Income records: **{len(user.incomes)}**")
                st.write(f"- Expense records: **{len(user.expenses)}**")
                st.write(f"- Current balance: **€{user.balance():.2f}**")

    # ---------------- ADD INCOME ----------------
    with tab2:
        st.write("### Add Income")
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

    # ---------------- ADD EXPENSE ----------------
    with tab3:
        st.write("### Add Expense")
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
