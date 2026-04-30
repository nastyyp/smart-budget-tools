import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date


# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Budget",
    page_icon="💶",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Constants ─────────────────────────────────────────────────────────────────
INCOME_CATEGORIES = [
    "Salary / Part-time",
    "Scholarship",
    "Family Support",
    "Freelance",
    "Gift",
    "Other"
]

EXPENSE_CATEGORIES = [
    "Rent",
    "Food & Groceries",
    "Transport",
    "Books & Supplies",
    "Entertainment",
    "Health",
    "Clothing",
    "Subscriptions",
    "Other"
]

SAVINGS_COLORS = [
    "#4CAF50", "#2196F3", "#9C27B0", "#FF9800", "#E91E63",
    "#00BCD4", "#8BC34A", "#FFC107", "#795548", "#607D8B"
]


# ── Data model ────────────────────────────────────────────────────────────────
class User:
    def __init__(self, name):
        self.name = name
        self.transactions = []
        self.saved_amount = 0.0
        self.savings_boxes = []

    def add_income(self, amount, category, note="", tx_date=None):
        if amount > 0:
            self.transactions.append({
                "type": "Income",
                "amount": amount,
                "category": category,
                "note": note,
                "date": str(tx_date if tx_date else date.today())
            })

    def add_expense(self, amount, category, note="", tx_date=None):
        if amount > 0:
            self.transactions.append({
                "type": "Expense",
                "amount": amount,
                "category": category,
                "note": note,
                "date": str(tx_date if tx_date else date.today())
            })

    def total_income(self):
        return sum(t["amount"] for t in self.transactions if t["type"] == "Income")

    def total_expenses(self):
        return sum(t["amount"] for t in self.transactions if t["type"] == "Expense")

    def balance(self):
        return self.total_income() - self.total_expenses()

    def savings_rate(self):
        if self.total_income() == 0:
            return 0.0
        return (self.balance() / self.total_income()) * 100

    def transactions_df(self):
        if not self.transactions:
            return pd.DataFrame(columns=["date", "type", "category", "amount", "note"])
        return pd.DataFrame(self.transactions)

    def set_savings_plan(self, saved_amount, boxes):
        self.saved_amount = saved_amount
        self.savings_boxes = boxes

    def savings_df(self):
        if not self.savings_boxes:
            return pd.DataFrame(columns=["Box", "Percent", "Amount (€)"])

        rows = []
        for box in self.savings_boxes:
            amount = self.saved_amount * box["percent"] / 100
            rows.append({
                "Box": box["name"],
                "Percent": box["percent"],
                "Amount (€)": round(amount, 2)
            })
        return pd.DataFrame(rows)


# ── Session state ─────────────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None

if "savings_box_count" not in st.session_state:
    st.session_state.savings_box_count = 3


# ── Helpers ───────────────────────────────────────────────────────────────────
def show_profile_page():
    st.title("💶 Student Budget")
    st.subheader("Simple budgeting for students")
    st.write("Track your income, manage expenses, and plan your savings.")

    col1, col2, col3 = st.columns(3)
    col1.info("📊 Budget dashboard")
    col2.success("➕ Add income and expenses")
    col3.warning("💰 Separate savings planner")

    st.write("")
    st.write("### Create your profile")

    with st.form("create_profile_form"):
        name = st.text_input("Enter your name")
        submitted = st.form_submit_button("Create Profile", use_container_width=True)

        if submitted:
            if name.strip():
                st.session_state.user = User(name.strip())
                st.success(f"Profile created for {name.strip()}!")
                st.rerun()
            else:
                st.error("Please enter your name.")


def draw_pie_chart(labels, values, title):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.pie(
        values,
        labels=labels,
        autopct="%1.0f%%",
        startangle=90,
        colors=SAVINGS_COLORS[:len(values)]
    )
    ax.set_title(title)
    st.pyplot(fig)
    plt.close(fig)


def draw_balance_chart(df):
    df = df.copy()
    df["signed_amount"] = df.apply(
        lambda row: row["amount"] if row["type"] == "Income" else -row["amount"],
        axis=1
    )
    df["cumulative_balance"] = df["signed_amount"].cumsum()

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(df.index, df["cumulative_balance"], marker="o")
    ax.axhline(0, linestyle="--")
    ax.set_title("Balance Over Time")
    ax.set_ylabel("€")
    ax.set_xlabel("Transaction Number")
    st.pyplot(fig)
    plt.close(fig)


# ── Main app ──────────────────────────────────────────────────────────────────
if st.session_state.user is None:
    show_profile_page()
    st.stop()

user = st.session_state.user

# Sidebar
with st.sidebar:
    st.title("Navigation")
    st.write(f"### 👋 Hello, {user.name}")

    page = st.radio(
        "Go to",
        ["Dashboard", "Add Income", "Add Expense", "History", "Savings"],
        index=0
    )

    st.divider()
    st.write("### Quick Summary")
    st.metric("Income", f"€{user.total_income():,.2f}")
    st.metric("Expenses", f"€{user.total_expenses():,.2f}")
    st.metric("Balance", f"€{user.balance():,.2f}")

    st.divider()
    if st.button("Switch User", use_container_width=True):
        st.session_state.user = None
        st.rerun()


# ── Dashboard ─────────────────────────────────────────────────────────────────
if page == "Dashboard":
    st.title("📊 Dashboard")
    st.caption("Overview of your current budget")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Income", f"€{user.total_income():,.2f}")
    col2.metric("Total Expenses", f"€{user.total_expenses():,.2f}")
    col3.metric("Balance", f"€{user.balance():,.2f}")
    col4.metric("Savings Rate", f"{user.savings_rate():.1f}%")

    df = user.transactions_df()

    if df.empty:
        st.info("No transactions yet. Add income or expenses to see analytics.")
    else:
        left, right = st.columns(2)

        with left:
            st.write("### Income by category")
            income_df = df[df["type"] == "Income"]
            if not income_df.empty:
                income_grouped = income_df.groupby("category")["amount"].sum()
                draw_pie_chart(
                    income_grouped.index.tolist(),
                    income_grouped.values.tolist(),
                    "Income Breakdown"
                )
            else:
                st.info("No income data yet.")

        with right:
            st.write("### Expenses by category")
            expense_df = df[df["type"] == "Expense"]
            if not expense_df.empty:
                expense_grouped = expense_df.groupby("category")["amount"].sum()
                draw_pie_chart(
                    expense_grouped.index.tolist(),
                    expense_grouped.values.tolist(),
                    "Expense Breakdown"
                )
            else:
                st.info("No expense data yet.")

        st.write("### Balance trend")
        df_sorted = df.sort_values("date").reset_index(drop=True)
        draw_balance_chart(df_sorted)

        st.write("### Recent transactions")
        display_df = df_sorted[["date", "type", "category", "amount", "note"]].copy()
        display_df["amount"] = display_df["amount"].apply(lambda x: f"€{x:,.2f}")
        display_df.columns = ["Date", "Type", "Category", "Amount", "Note"]
        st.dataframe(display_df[::-1].head(5), use_container_width=True, hide_index=True)


# ── Add Income ────────────────────────────────────────────────────────────────
elif page == "Add Income":
    st.title("➕ Add Income")
    st.caption("Record a new income transaction")

    with st.form("income_form"):
        col1, col2 = st.columns(2)

        with col1:
            amount = st.number_input("Amount (€)", min_value=0.0, step=1.0, format="%.2f")
            category = st.selectbox("Category", INCOME_CATEGORIES)

        with col2:
            tx_date = st.date_input("Date", value=date.today())
            note = st.text_input("Note (optional)", placeholder="e.g. Part-time salary")

        submitted = st.form_submit_button("Save Income", use_container_width=True)

        if submitted:
            if amount > 0:
                user.add_income(amount, category, note, tx_date)
                st.success(f"Income of €{amount:.2f} added.")
                st.rerun()
            else:
                st.error("Please enter an amount greater than 0.")


# ── Add Expense ───────────────────────────────────────────────────────────────
elif page == "Add Expense":
    st.title("➖ Add Expense")
    st.caption("Record a new expense transaction")

    with st.form("expense_form"):
        col1, col2 = st.columns(2)

        with col1:
            amount = st.number_input("Amount (€)", min_value=0.0, step=1.0, format="%.2f")
            category = st.selectbox("Category", EXPENSE_CATEGORIES)

        with col2:
            tx_date = st.date_input("Date", value=date.today())
            note = st.text_input("Note (optional)", placeholder="e.g. Grocery shopping")

        submitted = st.form_submit_button("Save Expense", use_container_width=True)

        if submitted:
            if amount > 0:
                user.add_expense(amount, category, note, tx_date)
                st.success(f"Expense of €{amount:.2f} added.")
                st.rerun()
            else:
                st.error("Please enter an amount greater than 0.")


# ── History ───────────────────────────────────────────────────────────────────
elif page == "History":
    st.title("📋 Transaction History")
    st.caption("View and export all transactions")

    df = user.transactions_df()

    if df.empty:
        st.info("No transactions yet.")
    else:
        filter_type = st.selectbox("Filter", ["All", "Income", "Expense"])

        if filter_type == "Income":
            filtered_df = df[df["type"] == "Income"]
        elif filter_type == "Expense":
            filtered_df = df[df["type"] == "Expense"]
        else:
            filtered_df = df

        display_df = filtered_df[["date", "type", "category", "amount", "note"]].copy()
        display_df["amount"] = display_df["amount"].apply(lambda x: f"€{x:,.2f}")
        display_df.columns = ["Date", "Type", "Category", "Amount", "Note"]

        st.dataframe(display_df[::-1].reset_index(drop=True), use_container_width=True, hide_index=True)

        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            csv,
            file_name="budget_export.csv",
            mime="text/csv"
        )


# ── Savings ───────────────────────────────────────────────────────────────────
elif page == "Savings":
    st.title("💰 Savings Planner")
    st.caption("This section is separate from your main budget.")

    st.info("Here you manually enter how much money you have saved, then divide it into your own savings boxes.")

    col1, col2 = st.columns(2)

    with col1:
        saved_amount = st.number_input(
            "How much have you saved? (€)",
            min_value=0.0,
            step=1.0,
            value=float(user.saved_amount),
            format="%.2f"
        )

    with col2:
        box_count = st.number_input(
            "How many savings boxes do you want?",
            min_value=1,
            max_value=10,
            value=int(st.session_state.savings_box_count),
            step=1
        )
        st.session_state.savings_box_count = box_count

    st.write("### Configure your savings boxes")

    boxes = []
    total_percent = 0.0

    with st.form("savings_form"):
        for i in range(box_count):
            st.write(f"#### Box {i+1}")
            c1, c2 = st.columns(2)

            with c1:
                box_name = st.text_input(
                    f"Box name {i+1}",
                    value=user.savings_boxes[i]["name"] if i < len(user.savings_boxes) else f"Box {i+1}",
                    key=f"box_name_{i}"
                )

            with c2:
                box_percent = st.number_input(
                    f"Percent (%) {i+1}",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(user.savings_boxes[i]["percent"]) if i < len(user.savings_boxes) else 0.0,
                    step=1.0,
                    key=f"box_percent_{i}"
                )

            boxes.append({"name": box_name, "percent": box_percent})
            total_percent += box_percent

        submitted = st.form_submit_button("Save Savings Plan", use_container_width=True)

        if submitted:
            user.set_savings_plan(saved_amount, boxes)
            st.success("Savings plan updated.")
            st.rerun()

    st.write("### Current summary")
    st.metric("Saved Amount", f"€{saved_amount:,.2f}")
    st.metric("Total Box Percentage", f"{total_percent:.1f}%")

    if total_percent == 100:
        st.success("Your savings boxes add up to 100%.")
    elif total_percent < 100:
        st.warning(f"Your total is {total_percent:.1f}%. Add more to reach 100%.")
    else:
        st.error(f"Your total is {total_percent:.1f}%. Please reduce it to 100%.")

    savings_df = pd.DataFrame([
        {
            "Box": box["name"],
            "Percent": box["percent"],
            "Amount (€)": round(saved_amount * box["percent"] / 100, 2)
        }
        for box in boxes
    ])

    st.write("### Savings allocation table")
    st.dataframe(savings_df, use_container_width=True, hide_index=True)

    valid_df = savings_df[savings_df["Percent"] > 0]

    if not valid_df.empty:
        st.write("### Savings allocation chart")
        draw_pie_chart(
            valid_df["Box"].tolist(),
            valid_df["Amount (€)"].tolist(),
            "Savings Allocation"
        )
