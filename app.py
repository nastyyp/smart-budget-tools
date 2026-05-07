import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Smart Budget",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Custom style
# -----------------------------
st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at 20% 20%, rgba(124, 58, 237, 0.18), transparent 22%),
            radial-gradient(circle at 85% 80%, rgba(99, 102, 241, 0.14), transparent 25%),
            linear-gradient(135deg, #050816 0%, #0b1020 55%, #10172b 100%);
        color: white;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1020 0%, #111827 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.10);
    }

    .login-wrapper {
        max-width: 520px;
        margin: 50px auto 0 auto;
        padding: 34px 30px;
        border-radius: 24px;
        background: rgba(15, 23, 42, 0.82);
        border: 1px solid rgba(168, 85, 247, 0.18);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
    }

    .avatar-circle {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        margin: 0 auto 18px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, rgba(124,58,237,0.55), rgba(59,130,246,0.35));
        border: 1px solid rgba(255,255,255,0.08);
        font-size: 48px;
    }

    .login-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        color: #ffffff;
    }

    .login-subtitle {
        text-align: center;
        font-size: 1rem;
        color: #cbd5e1;
        margin-bottom: 1.4rem;
    }

    .page-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 0.25rem;
    }

    .page-subtitle {
        color: #cbd5e1;
        font-size: 0.98rem;
        margin-bottom: 1rem;
    }

    .soft-card {
        background: rgba(15, 23, 42, 0.82);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.18);
    }

    .metric-card {
        background: linear-gradient(180deg, rgba(20, 28, 48, 0.95), rgba(12, 18, 35, 0.95));
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 18px;
        padding: 16px 18px;
        min-height: 112px;
    }

    .metric-label {
        font-size: 0.88rem;
        color: #94a3b8;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: white;
        margin-bottom: 8px;
    }

    .metric-change {
        font-size: 0.84rem;
        color: #22c55e;
    }

    .section-title {
        color: white;
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.9rem;
        margin-top: 0.2rem;
    }

    .mini-item {
        background: rgba(30, 41, 59, 0.55);
        border: 1px solid rgba(148, 163, 184, 0.10);
        border-radius: 14px;
        padding: 12px 14px;
        margin-bottom: 10px;
    }

    .mini-item-title {
        color: white;
        font-weight: 600;
        font-size: 0.95rem;
    }

    .mini-item-sub {
        color: #94a3b8;
        font-size: 0.82rem;
        margin-top: 2px;
    }

    .mini-item-amount-pos {
        color: #22c55e;
        font-weight: 700;
        font-size: 0.92rem;
    }

    .mini-item-amount-neg {
        color: #f87171;
        font-weight: 700;
        font-size: 0.92rem;
    }

    div[data-testid="metric-container"] {
        background: rgba(15, 23, 42, 0.82);
        border: 1px solid rgba(148, 163, 184, 0.12);
        border-radius: 16px;
        padding: 10px 14px;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: linear-gradient(90deg, #7c3aed, #8b5cf6);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.55rem 1rem;
    }

    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background: linear-gradient(90deg, #8b5cf6, #9333ea);
        color: white;
    }

    .stTextInput > div > div > input,
    .stNumberInput input,
    .stDateInput input {
        background-color: rgba(255,255,255,0.06) !important;
        color: white !important;
        border-radius: 12px !important;
    }

    .stSelectbox > div > div,
    .stDateInput > div > div {
        border-radius: 12px !important;
    }

    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
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
        self.savings_entries = []
        self.savings_boxes = []

    def add_income(self, amount, note="", entry_date=None):
        if amount > 0:
            self.incomes.append({
                "Type": "Income",
                "Amount": amount,
                "Note": note,
                "Date": str(entry_date if entry_date else date.today())
            })

    def add_expense(self, amount, note="", entry_date=None):
        if amount > 0:
            self.expenses.append({
                "Type": "Expense",
                "Amount": amount,
                "Note": note,
                "Date": str(entry_date if entry_date else date.today())
            })

    def add_savings_entry(self, amount, note="", entry_date=None):
        if amount > 0:
            self.savings_entries.append({
                "Type": "Savings",
                "Amount": amount,
                "Note": note,
                "Date": str(entry_date if entry_date else date.today())
            })

    def total_income(self):
        return sum(item["Amount"] for item in self.incomes)

    def total_expenses(self):
        return sum(item["Amount"] for item in self.expenses)

    def total_savings(self):
        return sum(item["Amount"] for item in self.savings_entries)

    def balance(self):
        return self.total_income() - self.total_expenses()

    def savings_rate(self):
        if self.total_income() == 0:
            return 0.0
        return (self.total_savings() / self.total_income()) * 100

    def income_df(self):
        if not self.incomes:
            return pd.DataFrame(columns=["Type", "Amount", "Note", "Date"])
        return pd.DataFrame(self.incomes)

    def expense_df(self):
        if not self.expenses:
            return pd.DataFrame(columns=["Type", "Amount", "Note", "Date"])
        return pd.DataFrame(self.expenses)

    def savings_df(self):
        if not self.savings_entries:
            return pd.DataFrame(columns=["Type", "Amount", "Note", "Date"])
        return pd.DataFrame(self.savings_entries)

    def recent_activity(self):
        all_items = self.incomes + self.expenses + self.savings_entries
        if not all_items:
            return []
        def parse_dt(item):
            return pd.to_datetime(item["Date"])
        return sorted(all_items, key=parse_dt, reverse=True)[:5]

    def total_boxes_amount(self):
        total = 0.0
        for box in self.savings_boxes:
            total += sum(entry["Amount"] for entry in box["Entries"])
        return total

# -----------------------------
# Helpers
# -----------------------------
def metric_card(label, value, hint="", hint_color="#22c55e"):
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-change" style="color:{hint_color};">{hint}</div>
    </div>
    """

def filter_by_month(items, selected_date):
    result = []
    for item in items:
        d = pd.to_datetime(item["Date"])
        if d.month == selected_date.month and d.year == selected_date.year:
            result.append(item)
    return result

def income_expense_chart(monthly_income, monthly_expenses):
    fig, ax = plt.subplots(figsize=(6, 3.6))
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")

    labels = ["Income", "Expenses"]
    values = [monthly_income, monthly_expenses]
    colors = ["#22c55e", "#ef4444"]

    bars = ax.bar(labels, values, color=colors, width=0.55)

    ax.set_title("Spending Overview", color="white", fontsize=14, pad=12)
    ax.tick_params(colors="#cbd5e1")
    ax.set_ylabel("€", color="#cbd5e1")
    ax.grid(axis="y", alpha=0.16, color="#94a3b8")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#475569")
    ax.spines["bottom"].set_color("#475569")

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width()/2,
            value,
            f"€{value:,.0f}",
            ha="center",
            va="bottom",
            color="white",
            fontsize=10
        )

    st.pyplot(fig)
    plt.close(fig)

def comparison_chart(user):
    labels = ["Income", "Expenses", "Savings"]
    values = [user.total_income(), user.total_expenses(), user.total_savings()]
    colors = ["#22c55e", "#ef4444", "#8b5cf6"]

    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")

    bars = ax.bar(labels, values, color=colors, width=0.55)
    ax.set_title("Financial Comparison", color="white", fontsize=14, pad=12)
    ax.tick_params(colors="#cbd5e1")
    ax.set_ylabel("€", color="#cbd5e1")
    ax.grid(axis="y", alpha=0.16, color="#94a3b8")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#475569")
    ax.spines["bottom"].set_color("#475569")

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width()/2,
            value,
            f"€{value:,.0f}",
            ha="center",
            va="bottom",
            color="white",
            fontsize=10
        )

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

if "savings_box_count" not in st.session_state:
    st.session_state.savings_box_count = 3

# -----------------------------
# Login page
# -----------------------------
if not st.session_state.logged_in:
    left, center, right = st.columns([1.2, 2, 1.2])

    with center:
        st.markdown("<div class='login-wrapper'>", unsafe_allow_html=True)
        st.markdown("<div class='avatar-circle'>👤</div>", unsafe_allow_html=True)
        st.markdown("<div class='login-title'>Smart Budget</div>", unsafe_allow_html=True)
        st.markdown("<div class='login-subtitle'>Track. Save. Achieve.</div>", unsafe_allow_html=True)

        with st.form("login_form"):
            name = st.text_input("Your name", placeholder="Enter your name")
            login_button = st.form_submit_button("Continue", use_container_width=True)

            if login_button:
                if name.strip():
                    st.session_state.user = User(name.strip())
                    st.session_state.logged_in = True
                    st.session_state.page = "Dashboard"
                    st.rerun()
                else:
                    st.error("Please enter your name.")

        st.caption("Your data stays private.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# -----------------------------
# Main app
# -----------------------------
user = st.session_state.user

with st.sidebar:
    st.markdown("## 💜 Smart Budget")
    st.write(f"Welcome, **{user.name}** ✨")

    selected_page = st.radio(
        "Menu",
        ["Dashboard", "Income", "Expense", "Savings", "Summary"],
        index=["Dashboard", "Income", "Expense", "Savings", "Summary"].index(st.session_state.page)
    )
    st.session_state.page = selected_page

    st.divider()
    st.metric("Income", f"€{user.total_income():,.2f}")
    st.metric("Expenses", f"€{user.total_expenses():,.2f}")
    st.metric("Balance", f"€{user.balance():,.2f}")

    st.divider()
    if st.button("Log out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "Dashboard"
        st.rerun()

# -----------------------------
# Dashboard
# -----------------------------
if st.session_state.page == "Dashboard":
    head_left, head_right = st.columns([5, 1.35])

    with head_left:
        st.markdown("<div class='page-title'>Dashboard</div>", unsafe_allow_html=True)
        st.markdown("<div class='page-subtitle'>Here’s your financial overview.</div>", unsafe_allow_html=True)

    with head_right:
        selected_date = st.date_input("Month", value=date.today(), key="dashboard_month")

    monthly_incomes = filter_by_month(user.incomes, selected_date)
    monthly_expenses = filter_by_month(user.expenses, selected_date)

    monthly_income = sum(item["Amount"] for item in monthly_incomes)
    monthly_expenses_total = sum(item["Amount"] for item in monthly_expenses)
    monthly_balance = monthly_income - monthly_expenses_total

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card("Total Income", f"€{monthly_income:,.2f}", "This month", "#22c55e"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("Total Expenses", f"€{monthly_expenses_total:,.2f}", "This month", "#f87171"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("Saved", f"€{user.total_savings():,.2f}", "Current", "#a78bfa"), unsafe_allow_html=True)
    with c4:
        color = "#22c55e" if monthly_balance >= 0 else "#f87171"
        st.markdown(metric_card("Balance", f"€{monthly_balance:,.2f}", "Current", color), unsafe_allow_html=True)

    st.write("")

    left_col, right_col = st.columns([1.45, 1])

    with left_col:
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Spending Overview</div>", unsafe_allow_html=True)
        income_expense_chart(monthly_income, monthly_expenses_total)
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Recent Activity</div>", unsafe_allow_html=True)

        recent = user.recent_activity()
        if recent:
            for item in recent:
                if item["Type"] == "Income":
                    amount_class = "mini-item-amount-pos"
                    sign = "+"
                elif item["Type"] == "Expense":
                    amount_class = "mini-item-amount-neg"
                    sign = "-"
                else:
                    amount_class = "mini-item-amount-pos"
                    sign = "+"

                st.markdown(f"""
                    <div class="mini-item">
                        <div class="mini-item-title">{item["Note"] if item["Note"] else item["Type"]}</div>
                        <div class="mini-item-sub">{item["Date"]} • {item["Type"]}</div>
                        <div class="{amount_class}" style="margin-top:6px;">{sign}€{item["Amount"]:,.2f}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No activity yet.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Quick Actions</div>", unsafe_allow_html=True)

        q1, q2 = st.columns(2)
        with q1:
            if st.button("Add Income", use_container_width=True, key="quick_income"):
                st.session_state.page = "Income"
                st.rerun()
        with q2:
            if st.button("Add Expense", use_container_width=True, key="quick_expense"):
                st.session_state.page = "Expense"
                st.rerun()

        q3, q4 = st.columns(2)
        with q3:
            if st.button("Go to Savings", use_container_width=True, key="quick_savings"):
                st.session_state.page = "Savings"
                st.rerun()
        with q4:
            if st.button("Open Summary", use_container_width=True, key="quick_summary"):
                st.session_state.page = "Summary"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Income
# -----------------------------
elif st.session_state.page == "Income":
    st.markdown("<div class='page-title'>Income</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Add and manage your income.</div>", unsafe_allow_html=True)

    st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
    with st.form("income_form"):
        c1, c2 = st.columns(2)

        with c1:
            income_amount = st.number_input("Income amount (€)", min_value=0.0, step=1.0, format="%.2f")
            income_date = st.date_input("Income date", value=date.today(), key="income_date")

        with c2:
            income_note = st.text_input("Note", placeholder="e.g. Scholarship")

        save_income = st.form_submit_button("Save Income", use_container_width=True)

        if save_income:
            if income_amount > 0:
                user.add_income(income_amount, income_note, income_date)
                st.success(f"Income of €{income_amount:.2f} added.")
                st.rerun()
            else:
                st.error("Please enter an amount greater than 0.")
    st.markdown("</div>", unsafe_allow_html=True)

    income_df = user.income_df()
    if not income_df.empty:
        st.write("")
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Income History</div>", unsafe_allow_html=True)

        display_df = income_df.copy()
        display_df["Amount"] = display_df["Amount"].apply(lambda x: f"€{x:,.2f}")
        st.dataframe(display_df[::-1].reset_index(drop=True), use_container_width=True, hide_index=True)

        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Expense
# -----------------------------
elif st.session_state.page == "Expense":
    st.markdown("<div class='page-title'>Expense</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Add and manage your expenses.</div>", unsafe_allow_html=True)

    st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
    with st.form("expense_form"):
        c1, c2 = st.columns(2)

        with c1:
            expense_amount = st.number_input("Expense amount (€)", min_value=0.0, step=1.0, format="%.2f")
            expense_date = st.date_input("Expense date", value=date.today(), key="expense_date")

        with c2:
            expense_note = st.text_input("Note", placeholder="e.g. Groceries")

        save_expense = st.form_submit_button("Save Expense", use_container_width=True)

        if save_expense:
            if expense_amount > 0:
                user.add_expense(expense_amount, expense_note, expense_date)
                st.success(f"Expense of €{expense_amount:.2f} added.")
                st.rerun()
            else:
                st.error("Please enter an amount greater than 0.")
    st.markdown("</div>", unsafe_allow_html=True)

    expense_df = user.expense_df()
    if not expense_df.empty:
        st.write("")
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Expense History</div>", unsafe_allow_html=True)

        display_df = expense_df.copy()
        display_df["Amount"] = display_df["Amount"].apply(lambda x: f"€{x:,.2f}")
        st.dataframe(display_df[::-1].reset_index(drop=True), use_container_width=True, hide_index=True)

        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Savings
# -----------------------------
elif st.session_state.page == "Savings":
    st.markdown("<div class='page-title'>Savings</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Add money to savings and track each box separately.</div>", unsafe_allow_html=True)

    top_left, top_right = st.columns([1.1, 1])

    with top_left:
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Add Savings Entry</div>", unsafe_allow_html=True)

        with st.form("main_savings_form"):
            savings_amount = st.number_input(
                "How much do you want to add to savings? (€)",
                min_value=0.0,
                step=1.0,
                format="%.2f"
            )
            savings_date = st.date_input("Savings date", value=date.today(), key="savings_date")
            savings_note = st.text_input("Note", placeholder="e.g. Monthly savings")

            save_savings = st.form_submit_button("Add Savings", use_container_width=True)

            if save_savings:
                if savings_amount > 0:
                    user.add_savings_entry(savings_amount, savings_note, savings_date)
                    st.success(f"Savings entry of €{savings_amount:.2f} added.")
                    st.rerun()
                else:
                    st.error("Please enter an amount greater than 0.")

        st.markdown("</div>", unsafe_allow_html=True)

    with top_right:
        st.markdown(metric_card("Saved Money", f"€{user.total_savings():,.2f}", "Total saved", "#a78bfa"), unsafe_allow_html=True)
        st.write("")
        st.markdown(metric_card("Savings Rate", f"{user.savings_rate():.1f}%", "Of total income", "#22c55e"), unsafe_allow_html=True)
        st.write("")
        st.markdown(metric_card("Boxes Total", f"€{user.total_boxes_amount():,.2f}", "Inside boxes", "#60a5fa"), unsafe_allow_html=True)

    st.write("")

    st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Savings Boxes Setup</div>", unsafe_allow_html=True)

    box_count = st.number_input(
        "How many savings boxes do you want?",
        min_value=1,
        max_value=12,
        value=st.session_state.savings_box_count,
        step=1
    )
    st.session_state.savings_box_count = box_count

    with st.form("boxes_setup_form"):
        new_boxes = []

        for i in range(box_count):
            st.write(f"### Box {i+1}")
            c1, c2 = st.columns(2)

            default_name = user.savings_boxes[i]["Name"] if i < len(user.savings_boxes) else f"Box {i+1}"
            default_purpose = user.savings_boxes[i]["Purpose"] if i < len(user.savings_boxes) else ""

            with c1:
                box_name = st.text_input(
                    f"Box name {i+1}",
                    value=default_name,
                    key=f"setup_box_name_{i}"
                )

            with c2:
                box_purpose = st.text_input(
                    f"Purpose {i+1}",
                    value=default_purpose,
                    placeholder="e.g. Travel, Emergency, Laptop",
                    key=f"setup_box_purpose_{i}"
                )

            old_entries = []
            if i < len(user.savings_boxes):
                old_entries = user.savings_boxes[i]["Entries"]

            new_boxes.append({
                "Name": box_name,
                "Purpose": box_purpose,
                "Entries": old_entries
            })

        save_boxes = st.form_submit_button("Save Boxes Setup", use_container_width=True)

        if save_boxes:
            user.savings_boxes = new_boxes
            st.success("Savings boxes setup updated.")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    if user.savings_boxes:
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Add Money to a Box</div>", unsafe_allow_html=True)

        with st.form("box_entry_form"):
            box_names = [box["Name"] for box in user.savings_boxes]

            c1, c2, c3 = st.columns(3)
            with c1:
                selected_box = st.selectbox("Choose box", box_names)
            with c2:
                box_add_amount = st.number_input(
                    "How much do you add? (€)",
                    min_value=0.0,
                    step=1.0,
                    format="%.2f",
                    key="box_add_amount"
                )
            with c3:
                box_add_date = st.date_input("Entry date", value=date.today(), key="box_add_date")

            box_add_note = st.text_input("Note", placeholder="e.g. Added part of scholarship", key="box_add_note")

            save_box_entry = st.form_submit_button("Add to Box", use_container_width=True)

            if save_box_entry:
                if box_add_amount > 0:
                    for box in user.savings_boxes:
                        if box["Name"] == selected_box:
                            box["Entries"].append({
                                "Amount": box_add_amount,
                                "Date": str(box_add_date),
                                "Note": box_add_note
                            })
                            break
                    st.success(f"€{box_add_amount:.2f} added to {selected_box}.")
                    st.rerun()
                else:
                    st.error("Please enter an amount greater than 0.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")

    lower_left, lower_right = st.columns([1.2, 1])

    with lower_left:
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Savings History</div>", unsafe_allow_html=True)

        savings_df = user.savings_df()
        if not savings_df.empty:
            display_df = savings_df.copy()
            display_df["Amount"] = display_df["Amount"].apply(lambda x: f"€{x:,.2f}")
            st.dataframe(display_df[::-1].reset_index(drop=True), use_container_width=True, hide_index=True)
        else:
            st.info("No savings entries yet.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.write("")

        if user.savings_boxes:
            st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
            st.markdown("<div class='section-title'>Boxes Table</div>", unsafe_allow_html=True)

            table_rows = []
            for box in user.savings_boxes:
                total_box = sum(entry["Amount"] for entry in box["Entries"])
                last_added = box["Entries"][-1]["Amount"] if box["Entries"] else 0.0

                table_rows.append({
                    "Name": box["Name"],
                    "Purpose": box["Purpose"],
                    "Last Added (€)": f"€{last_added:,.2f}",
                    "Total in Box (€)": f"€{total_box:,.2f}"
                })

            boxes_df = pd.DataFrame(table_rows)
            st.dataframe(boxes_df, use_container_width=True, hide_index=True)

            st.markdown("</div>", unsafe_allow_html=True)

    with lower_right:
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Box Summary</div>", unsafe_allow_html=True)

        allocated = user.total_boxes_amount()
        remaining = user.total_savings() - allocated

        if remaining > 0:
            st.info(f"You still have **€{remaining:,.2f}** not assigned to any box.")
        elif remaining < 0:
            st.error(f"You assigned **€{abs(remaining):,.2f}** more than your total savings.")
        else:
            st.success("All your savings are assigned to boxes.")

        if user.savings_boxes:
            for box in user.savings_boxes:
                total_box = sum(entry["Amount"] for entry in box["Entries"])
                last_added = box["Entries"][-1]["Amount"] if box["Entries"] else 0.0

                st.markdown(f"""
                <div class="mini-item">
                    <div class="mini-item-title">{box["Name"]}</div>
                    <div class="mini-item-sub">{box["Purpose"] if box["Purpose"] else "No purpose added"}</div>
                    <div class="mini-item-sub" style="margin-top:6px;">Last added: €{last_added:,.2f}</div>
                    <div class="mini-item-amount-pos" style="margin-top:6px;">Total: €{total_box:,.2f}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No savings boxes yet.")

        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Summary
# -----------------------------
elif st.session_state.page == "Summary":
    st.markdown("<div class='page-title'>Summary</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>General conclusion of your financial situation.</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(metric_card("Income", f"€{user.total_income():,.2f}", "Total", "#22c55e"), unsafe_allow_html=True)
    with c2:
        st.markdown(metric_card("Expenses", f"€{user.total_expenses():,.2f}", "Total", "#f87171"), unsafe_allow_html=True)
    with c3:
        st.markdown(metric_card("Savings", f"€{user.total_savings():,.2f}", "Current", "#a78bfa"), unsafe_allow_html=True)
    with c4:
        color = "#22c55e" if user.balance() >= 0 else "#f87171"
        st.markdown(metric_card("Balance", f"€{user.balance():,.2f}", "Current", color), unsafe_allow_html=True)

    st.write("")
    left_sum, right_sum = st.columns([1.2, 1])

    with left_sum:
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>Financial Comparison</div>", unsafe_allow_html=True)
        comparison_chart(user)
        st.markdown("</div>", unsafe_allow_html=True)

    with right_sum:
        st.markdown("<div class='soft-card'>", unsafe_allow_html=True)
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

            if user.total_savings() > 0:
                st.info(f"You have saved €{user.total_savings():,.2f}.")
            else:
                st.warning("You have not entered savings yet.")

        st.markdown("</div>", unsafe_allow_html=True)
