import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Smart Budget",
    page_icon="💶",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #050816 0%, #0b1020 55%, #111827 100%);
    }

    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
        text-align: center;
        margin-bottom: 0.3rem;
    }

    .sub-text {
        color: #cbd5e1;
        font-size: 1rem;
        text-align: center;
        margin-bottom: 1.2rem;
    }

    .login-box {
        background: rgba(17, 24, 39, 0.88);
        border: 1px solid rgba(148, 163, 184, 0.18);
        padding: 28px;
        border-radius: 20px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    }

    .profile-circle {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        background: linear-gradient(135deg, #334155, #64748b);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 60px;
        margin: 0 auto 20px auto;
        color: white;
    }

    .section-title {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
    }

    [data-testid="stSidebar"] {
        background: rgba(9, 14, 30, 0.96);
        border-right: 1px solid rgba(148, 163, 184, 0.15);
    }

    div[data-testid="metric-container"] {
        background: rgba(17, 24, 39, 0.88);
        border: 1px solid rgba(148, 163, 184, 0.18);
        padding: 14px 16px;
        border-radius: 16px;
    }

    label, .stRadio label, .stSelectbox label, .stDateInput label {
        color: #e2e8f0 !important;
    }
</style>
""", unsafe_allow_html=True)

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
        if not self.incomes:
            return pd.DataFrame(columns=["Amount", "Note", "Date"])
        return pd.DataFrame(self.incomes)

    def expense_df(self):
        if not self.expenses:
            return pd.DataFrame(columns=["Amount", "Note", "Date"])
        return pd.DataFrame(self.expenses)


# -----------------------------
# Helpers
# -----------------------------
def filter_by_month(items, selected_date):
    result = []
    for item in items:
        d = pd.to_datetime(item["Date"])
        if d.month == selected_date.month and d.year == selected_date.year:
            result.append(item)
    return result


def dark_bar_chart(labels, values, title):
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")

    bars = ax.bar(labels, values, color=["#22c55e", "#ef4444"])
    ax.set_title(title, color="white", fontsize=14, pad=12)
    ax.set_ylabel("€", color="#cbd5e1")
    ax.tick_params(colors="#cbd5e1")
    ax.spines["bottom"].set_color("#475569")
    ax.spines["left"].set_color("#475569")
    ax.spines["top"].set_color("#111827")
    ax.spines["right"].set_color("#111827")
    ax.grid(axis="y", alpha=0.2, color="#94a3b8")

    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"€{height:,.0f}",
            ha="center",
            va="bottom",
            color="white",
            fontsize=10
        )

    st.pyplot(fig)
    plt.close(fig)


def dark_pie_chart(values, labels, title):
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")

    colors = ["#8b5cf6", "#334155"]
    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct="%1.0f%%",
        startangle=90,
        colors=colors,
        wedgeprops=dict(edgecolor="#111827", linewidth=2)
    )

    for t in texts:
        t.set_color("white")
    for t in autotexts:
        t.set_color("white")
        t.set_fontweight("bold")

    ax.set_title(title, color="white", fontsize=14, pad=12)
    st.pyplot(fig)
    plt.close(fig)


# -----------------------------
# Session state
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# -----------------------------
# Login page
# -----------------------------
if not st.session_state.logged_in:
    left, center, right = st.columns([1.2, 2, 1.2])

    with center:
        st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<div class='profile-circle'>👤</div>", unsafe_allow_html=True)
        st.markdown("<div class='main-title'>Smart Budget</div>", unsafe_allow_html=True)

        with st.form("login_form"):
            name = st.text_input("Log in or Sign in")
            login_button = st.form_submit_button("Log in", use_container_width=True)

            if login_button:
                if name.strip():
                    st.session_state.user = User(name.strip())
                    st.session_state.logged_in = True
                    st.session_state.page = "Dashboard"
                    st.rerun()
                else:
                    st.error("Please enter your name.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# -----------------------------
# Main app
# -----------------------------
user = st.session_state.user

with st.sidebar:
    st.title("Smart Budget")
    st.write(f"Hi, {user.name} 👋")

    selected_page = st.radio(
        "Navigation",
        ["Dashboard", "Income", "Expense", "Savings", "Summary"],
        index=["Dashboard", "Income", "Expense", "Savings", "Summary"].index(st.session_state.page)
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
        st.session_state.page = "Dashboard"
        st.rerun()

# -----------------------------
# Dashboard
# -----------------------------
if st.session_state.page == "Dashboard":
    top_left, top_right = st.columns([5, 1.4])

    with top_left:
        st.markdown("<div class='main-title' style='text-align:left;'>📊 Dashboard</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-text' style='text-align:left;'>Main information about your budget.</div>", unsafe_allow_html=True)

    with top_right:
        selected_date = st.date_input(
            "Month",
            value=date.today(),
            key="dashboard_month"
        )

    monthly_incomes = filter_by_month(user.incomes, selected_date)
    monthly_expenses = filter_by_month(user.expenses, selected_date)

    monthly_income = sum(item["Amount"] for item in monthly_incomes)
    monthly_expenses_total = sum(item["Amount"] for item in monthly_expenses)
    monthly_balance = monthly_income - monthly_expenses_total

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Income", f"€{monthly_income:,.2f}")
    c2.metric("Total Expenses", f"€{monthly_expenses_total:,.2f}")
    c3.metric("Saved Money", f"€{user.saved_amount:,.2f}")
    c4.metric("Balance", f"€{monthly_balance:,.2f}")

    st.write("")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("<div class='section-title'>Income vs Expenses</div>", unsafe_allow_html=True)
        dark_bar_chart(
            ["Income", "Expenses"],
            [monthly_income, monthly_expenses_total],
            "Income vs Expenses"
        )

    with chart_col2:
        st.markdown("<div class='section-title'>Savings Overview</div>", unsafe_allow_html=True)
        if user.saved_amount > 0 or monthly_income > 0:
            other_money = max(monthly_income - user.saved_amount, 0)
            dark_pie_chart(
                [user.saved_amount, other_money],
                ["Saved", "Other Money"],
                "Savings Distribution"
            )
        else:
            st.info("No savings or income data yet.")

    st.write("")

    info1, info2 = st.columns(2)

    with info1:
        st.markdown("<div class='section-title'>Quick Info</div>", unsafe_allow_html=True)
        st.info(f"Income records this month: {len(monthly_incomes)}")
        st.info(f"Expense records this month: {len(monthly_expenses)}")

        monthly_savings_rate = 0
        if monthly_income > 0:
            monthly_savings_rate = (user.saved_amount / monthly_income) * 100

        st.info(f"Savings rate: {monthly_savings_rate:.1f}%")

    with info2:
        st.markdown("<div class='section-title'>Status</div>", unsafe_allow_html=True)
        if monthly_balance > 0:
            st.success("Your balance is positive this month.")
        elif monthly_balance < 0:
            st.error("Your expenses are higher than your income this month.")
        else:
            st.warning("Your balance is zero this month.")

        if user.saved_amount > 0:
            st.success(f"You saved €{user.saved_amount:,.2f}.")
        else:
            st.info("No savings added yet.")

# -----------------------------
# Income
# -----------------------------
elif st.session_state.page == "Income":
    st.markdown("<div class='main-title' style='text-align:left;'>➕ Income</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text' style='text-align:left;'>Add your income here.</div>", unsafe_allow_html=True)

    with st.form("income_form"):
        c1, c2 = st.columns(2)

        with c1:
            income_amount = st.number_input("Income amount (€)", min_value=0.0, step=1.0, format="%.2f")
            income_date = st.date_input("Income date", value=date.today(), key="income_date")

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
        st.markdown("<div class='section-title'>Income History</div>", unsafe_allow_html=True)
        display_df = income_df.copy()
        display_df["Amount"] = display_df["Amount"].apply(lambda x: f"€{x:,.2f}")
        st.dataframe(display_df[::-1].reset_index(drop=True), use_container_width=True, hide_index=True)

# -----------------------------
# Expense
# -----------------------------
elif st.session_state.page == "Expense":
    st.markdown("<div class='main-title' style='text-align:left;'>➖ Expense</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text' style='text-align:left;'>Add your expenses here.</div>", unsafe_allow_html=True)

    with st.form("expense_form"):
        c1, c2 = st.columns(2)

        with c1:
            expense_amount = st.number_input("Expense amount (€)", min_value=0.0, step=1.0, format="%.2f")
            expense_date = st.date_input("Expense date", value=date.today(), key="expense_date")

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
        st.markdown("<div class='section-title'>Expense History</div>", unsafe_allow_html=True)
        display_df = expense_df.copy()
        display_df["Amount"] = display_df["Amount"].apply(lambda x: f"€{x:,.2f}")
        st.dataframe(display_df[::-1].reset_index(drop=True), use_container_width=True, hide_index=True)

# -----------------------------
# Savings
# -----------------------------
elif st.session_state.page == "Savings":
    st.markdown("<div class='main-title' style='text-align:left;'>💰 Savings</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text' style='text-align:left;'>This section is separate from income and expenses.</div>", unsafe_allow_html=True)

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
        dark_pie_chart(
            [user.saved_amount, other_money],
            ["Saved", "Other Money"],
            "Savings Overview"
        )

# -----------------------------
# Summary
# -----------------------------
elif st.session_state.page == "Summary":
    st.markdown("<div class='main-title' style='text-align:left;'>📌 Summary</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-text' style='text-align:left;'>Your current financial conclusion.</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Income", f"€{user.total_income():,.2f}")
    c2.metric("Expenses", f"€{user.total_expenses():,.2f}")
    c3.metric("Savings", f"€{user.saved_amount:,.2f}")
    c4.metric("Balance", f"€{user.balance():,.2f}")

    st.markdown("<div class='section-title'>Conclusion</div>", unsafe_allow_html=True)

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

    st.markdown("<div class='section-title'>Financial Comparison</div>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")
    labels = ["Income", "Expenses", "Savings"]
    values = [user.total_income(), user.total_expenses(), user.saved_amount]
    ax.bar(labels, values, color=["#22c55e", "#ef4444", "#8b5cf6"])
    ax.set_ylabel("€", color="#cbd5e1")
    ax.set_title("Income vs Expenses vs Savings", color="white", pad=12)
    ax.tick_params(colors="#cbd5e1")
    ax.grid(axis="y", alpha=0.2, color="#94a3b8")
    st.pyplot(fig)
    plt.close(fig)
