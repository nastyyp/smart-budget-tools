import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Budget",
    page_icon="💶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Data model ───────────────────────────────────────────────────────────────
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
        if not self.incomes:
            return pd.DataFrame(columns=["Amount", "Note", "Date"])
        return pd.DataFrame(self.incomes)

    def expense_df(self):
        if not self.expenses:
            return pd.DataFrame(columns=["Amount", "Note", "Date"])
        return pd.DataFrame(self.expenses)


# ── Session state ────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "open_dashboard" not in st.session_state:
    st.session_state.open_dashboard = False


# ── Login page ───────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    left, center, right = st.columns([1, 2, 1])

    with center:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("💶 Smart Budget")
        st.subheader("Login")
        st.write("Enter your name to continue.")

        with st.form("login_form"):
            name = st.text_input("Your name")
            login_button = st.form_submit_button("Login", use_container_width=True)

            if login_button:
                if name.strip():
                    st.session_state.user = User(name.strip())
                    st.session_state.logged_in = True
                    st.session_state.page = "Home"
                    st.rerun()
                else:
                    st.error("Please enter your name.")

    st.stop()


# ── Main app ─────────────────────────────────────────────────────────────────
user = st.session_state.user

with st.sidebar:
    st.title("Smart Budget")
    st.write(f"### Hi, {user.name} 👋")

    selected_page = st.radio(
        "Navigation",
        ["Home", "Income", "Expense", "Savings", "Summary"],
        index=["Home", "Income", "Expense", "Savings", "Summary"].index(st.session_state.page)
    )
    st.session_state.page = selected_page

    st.divider()
    st.metric("Income", f"€{user.total_income():,.2f}")
    st.metric("Expenses", f"€{user.total_expenses():,.2f}")
    st.metric("Balance", f"€{user.balance():,.2f}")

    st.divider()
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "Home"
        st.session_state.open_dashboard = False
        st.rerun()


# ── Home page ────────────────────────────────────────────────────────────────
if st.session_state.page == "Home":
    st.title("🏠 Home Page")
    st.write("Welcome to your budget app.")

    top1, top2, top3, top4 = st.columns(4)
    top1.metric("Total Income", f"€{user.total_income():,.2f}")
    top2.metric("Total Expenses", f"€{user.total_expenses():,.2f}")
    top3.metric("Saved Money", f"€{user.saved_amount:,.2f}")
    top4.metric("Balance", f"€{user.balance():,.2f}")

    st.write("")

    btn_left, btn_center, btn_right = st.columns([1, 2, 1])
    with btn_center:
        if st.button("Open Dashboard", use_container_width=True):
            st.session_state.open_dashboard = True

    if st.session_state.open_dashboard:
        st.write("## Dashboard")

        cards1, cards2, cards3, cards4 = st.columns(4)
        cards1.metric("Income", f"€{user.total_income():,.2f}")
        cards2.metric("Expenses", f"€{user.total_expenses():,.2f}")
        cards3.metric("Saved", f"€{user.saved_amount:,.2f}")
        cards4.metric("Balance", f"€{user.balance():,.2f}")

        st.write("")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.write("### Income vs Expenses")
            values = [user.total_income(), user.total_expenses()]
            labels = ["Income", "Expenses"]

            fig, ax = plt.subplots(figsize=(5, 4))
            ax.bar(labels, values)
            ax.set_ylabel("€")
            ax.set_title("Income vs Expenses")
            st.pyplot(fig)
            plt.close(fig)

        with chart_col2:
            st.write("### Expense Overview")
            if user.total_expenses() > 0:
                fig, ax = plt.subplots(figsize=(5, 4))
                ax.pie(
                    [user.total_expenses(), max(user.total_income() - user.total_expenses(), 0)],
                    labels=["Expenses", "Remaining"],
                    autopct="%1.0f%%",
                    startangle=90
                )
                ax.set_title("Expense Breakdown")
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.info("No expenses yet.")

        st.write("")
        st.write("### Quick Info")

        q1, q2 = st.columns(2)
        with q1:
            st.info(f"Income records: {len(user.incomes)}")
            st.info(f"Expense records: {len(user.expenses)}")
        with q2:
            if user.balance() > 0:
                st.success("Your balance is positive.")
            elif user.balance() < 0:
                st.error("Your expenses are higher than your income.")
            else:
                st.warning("Your balance is zero.")

            if user.saved_amount > 0:
                st.success(f"You saved €{user.saved_amount:,.2f}.")
            else:
                st.info("No savings added yet.")


# ── Income page ──────────────────────────────────────────────────────────────
elif st.session_state.page == "Income":
    st.title("➕ Income")
    st.write("Add your income here.")

    with st.form("income_form"):
        c1, c2 = st.columns(2)

        with c1:
            income_amount = st.number_input(
                "Income amount (€)",
                min_value=0.0,
                step=1.0,
                format="%.2f"
            )
            income_date = st.date_input("Income date", value=date.today())

        with c2:
            income_note = st.text_input("Note", placeholder="e.g. Salary or scholarship")

        save_income = st.form_submit_button("Save Income", use_container_width=True)

        if save_income:
            if income_amount > 0:
                user.add_income(income_amount, income_note, income_date)
                st.success(f"Income of €{income_amount:.2f} added.")
                st.rerun()
            else:
                st.error("Please enter an amount greater than 0.")

    income_df = user.income_df()
    if not income_df.empty:
        st.write("### Income History")
        display_df = income_df.copy()
        display_df["Amount"] = display_df["Amount"].apply(lambda x: f"€{x:,.2f}")
        st.dataframe(
            display_df[::-1].reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )


# ── Expense page ─────────────────────────────────────────────────────────────
elif st.session_state.page == "Expense":
    st.title("➖ Expense")
    st.write("Add your expenses here.")

    with st.form("expense_form"):
        c1, c2 = st.columns(2)

        with c1:
            expense_amount = st.number_input(
                "Expense amount (€)",
                min_value=0.0,
                step=1.0,
                format="%.2f"
            )
            expense_date = st.date_input("Expense date", value=date.today())

        with c2:
            expense_note = st.text_input("Note", placeholder="e.g. Food or transport")

        save_expense = st.form_submit_button("Save Expense", use_container_width=True)

        if save_expense:
            if expense_amount > 0:
                user.add_expense(expense_amount, expense_note, expense_date)
                st.success(f"Expense of €{expense_amount:.2f} added.")
                st.rerun()
            else:
                st.error("Please enter an amount greater than 0.")

    expense_df = user.expense_df()
    if not expense_df.empty:
        st.write("### Expense History")
        display_df = expense_df.copy()
        display_df["Amount"] = display_df["Amount"].apply(lambda x: f"€{x:,.2f}")
        st.dataframe(
            display_df[::-1].reset_index(drop=True),
            use_container_width=True,
            hide_index=True
        )


# ── Savings page ─────────────────────────────────────────────────────────────
elif st.session_state.page == "Savings":
    st.title("💰 Savings")
    st.write("This section is separate from income and expenses.")

    with st.form("savings_form"):
        saved_amount = st.number_input(
            "How much money have you saved? (€)",
            min_value=0.0,
            value=float(user.saved_amount),
            step=1.0,
            format="%.2f"
        )

        save_savings = st.form_submit_button("Save Savings", use_container_width=True)

        if save_savings:
            user.set_saved_amount(saved_amount)
            st.success(f"Saved amount updated to €{saved_amount:.2f}.")
            st.rerun()

    s1, s2 = st.columns(2)
    s1.metric("Saved Money", f"€{user.saved_amount:,.2f}")
    s2.metric("Savings Rate", f"{user.savings_rate():.1f}%")

    if user.saved_amount > 0 or user.total_income() > 0:
        other_money = max(user.total_income() - user.saved_amount, 0)

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(
            [user.saved_amount, other_money],
            labels=["Saved", "Other Money"],
            autopct="%1.0f%%",
            startangle=90
        )
        ax.set_title("Savings Overview")
        st.pyplot(fig)
        plt.close(fig)


# ── Summary page ─────────────────────────────────────────────────────────────
elif st.session_state.page == "Summary":
    st.title("📌 Summary")
    st.write("Your current financial conclusion.")

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
            st.success("You are managing your budget well because your balance is positive.")
        elif user.balance() < 0:
            st.error("Your expenses are higher than your income.")
        else:
            st.warning("Your balance is zero.")

        if user.saved_amount > 0:
            st.info(f"You have saved €{user.saved_amount:,.2f}.")
        else:
            st.warning("You have not entered savings yet.")

    st.write("### Financial Comparison")
    labels = ["Income", "Expenses", "Savings"]
    values = [user.total_income(), user.total_expenses(), user.saved_amount]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(labels, values)
    ax.set_ylabel("€")
    ax.set_title("Income vs Expenses vs Savings")
    st.pyplot(fig)
    plt.close(fig)
