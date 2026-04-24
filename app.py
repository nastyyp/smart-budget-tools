import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from datetime import datetime

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Budget",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    color: #e8e8f0;
}
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04);
    border-right: 1px solid rgba(255,255,255,0.08);
}
.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 20px 24px;
}
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.5rem 1.5rem;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 25px rgba(99,102,241,0.4);
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #a5b4fc;
    border-bottom: 2px solid #6366f1;
}
h1, h2, h3 { font-family: 'Space Mono', monospace; color: #e8e8f0; }
hr { border-color: rgba(255,255,255,0.08); }
</style>
""", unsafe_allow_html=True)

# ── Matplotlib dark theme ─────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#1a1a2e",
    "axes.facecolor":    "#1a1a2e",
    "axes.edgecolor":    "#333355",
    "axes.labelcolor":   "#e8e8f0",
    "xtick.color":       "#a0a0c0",
    "ytick.color":       "#a0a0c0",
    "text.color":        "#e8e8f0",
    "grid.color":        "#2a2a4a",
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
    "font.family":       "sans-serif",
    "font.size":         11,
})

INCOME_COLORS  = ["#6366f1","#818cf8","#a5b4fc","#c7d2fe","#e0e7ff"]
EXPENSE_COLORS = ["#f87171","#fb923c","#fbbf24","#34d399","#22d3ee",
                  "#818cf8","#e879f9","#94a3b8","#f472b6"]

CATEGORIES_INCOME  = ["Salary / Part-time","Scholarship","Family Support","Freelance","Other"]
CATEGORIES_EXPENSE = ["Rent","Food & Groceries","Transport","Books & Supplies",
                      "Entertainment","Health","Clothing","Subscriptions","Other"]

# ── Data model ────────────────────────────────────────────────────────────────
class User:
    def __init__(self, name):
        self.name = name
        self.transactions = []

    def add_income(self, amount, category, note=""):
        if amount > 0:
            self.transactions.append({
                "type": "income", "amount": amount,
                "category": category, "note": note,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })

    def add_expense(self, amount, category, note=""):
        if amount > 0:
            self.transactions.append({
                "type": "expense", "amount": amount,
                "category": category, "note": note,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })

    def total_income(self):
        return sum(t["amount"] for t in self.transactions if t["type"] == "income")

    def total_expenses(self):
        return sum(t["amount"] for t in self.transactions if t["type"] == "expense")

    def balance(self):
        return self.total_income() - self.total_expenses()

    def df(self):
        return pd.DataFrame(self.transactions) if self.transactions else pd.DataFrame()


# ── Session state ─────────────────────────────────────────────────────────────
if "user" not in st.session_state:
    st.session_state.user = None

# ── Onboarding ────────────────────────────────────────────────────────────────
if st.session_state.user is None:
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.title("💶 Student Budget")
        st.markdown("Track your money with style.")
        st.markdown("---")
        name = st.text_input("What's your name?", placeholder="e.g. Alex")
        if st.button("Get Started →", use_container_width=True):
            if name.strip():
                st.session_state.user = User(name.strip())
                st.rerun()
            else:
                st.error("Please enter your name.")
    st.stop()

user = st.session_state.user

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 👋 {user.name}")
    st.markdown("---")
    bal = user.balance()
    bal_color = "#4ade80" if bal >= 0 else "#f87171"
    st.markdown(f"""
    <div class='metric-card' style='text-align:center;margin-bottom:12px'>
        <div style='font-size:12px;opacity:.6;letter-spacing:1px;text-transform:uppercase'>Balance</div>
        <div style='color:{bal_color};font-size:2rem;font-family:Space Mono,monospace;font-weight:700'>
            €{bal:,.2f}
        </div>
    </div>
    <div style='display:flex;gap:10px'>
        <div class='metric-card' style='flex:1;text-align:center'>
            <div style='font-size:11px;opacity:.55;text-transform:uppercase'>Income</div>
            <div style='color:#4ade80;font-size:1.1rem;font-weight:700'>€{user.total_income():,.2f}</div>
        </div>
        <div class='metric-card' style='flex:1;text-align:center'>
            <div style='font-size:11px;opacity:.55;text-transform:uppercase'>Spent</div>
            <div style='color:#f87171;font-size:1.1rem;font-weight:700'>€{user.total_expenses():,.2f}</div>
        </div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🚪 Switch user", use_container_width=True):
        st.session_state.user = None
        st.rerun()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_dash, tab_in, tab_ex, tab_hist = st.tabs(["📊 Dashboard", "➕ Add Income", "➖ Add Expense", "📋 History"])

# ── DASHBOARD ─────────────────────────────────────────────────────────────────
with tab_dash:
    df = user.df()

    if df.empty:
        st.info("No transactions yet — add some income or expenses to see your dashboard.")
    else:
        inc_df = df[df["type"] == "income"]
        exp_df = df[df["type"] == "expense"]
        savings_rate = (user.balance() / user.total_income() * 100) if user.total_income() else 0.0

        # KPI cards
        k1, k2, k3, k4 = st.columns(4)
        for col, label, value, color in [
            (k1, "Total Income",   f"€{user.total_income():,.2f}",  "#4ade80"),
            (k2, "Total Expenses", f"€{user.total_expenses():,.2f}","#f87171"),
            (k3, "Net Balance",    f"€{user.balance():,.2f}",       "#4ade80" if bal >= 0 else "#f87171"),
            (k4, "Savings Rate",   f"{savings_rate:.1f}%",          "#818cf8"),
        ]:
            col.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:11px;opacity:.55;text-transform:uppercase;letter-spacing:.8px'>{label}</div>
                <div style='color:{color};font-size:1.5rem;font-family:Space Mono,monospace;font-weight:700;margin-top:4px'>
                    {value}
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Pie charts row
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### Income breakdown")
            if not inc_df.empty:
                grp = inc_df.groupby("category")["amount"].sum()
                fig, ax = plt.subplots(figsize=(5, 4))
                wedges, texts, autotexts = ax.pie(
                    grp.values, labels=grp.index,
                    colors=INCOME_COLORS[:len(grp)],
                    autopct="%1.0f%%", startangle=90,
                    wedgeprops=dict(width=0.55, edgecolor="#0f0f1a", linewidth=2),
                    pctdistance=0.75,
                )
                for t in autotexts:
                    t.set_color("#0f0f1a"); t.set_fontsize(9); t.set_fontweight("bold")
                for t in texts:
                    t.set_color("#e8e8f0"); t.set_fontsize(9)
                ax.text(0, 0, f"€{user.total_income():,.0f}", ha="center", va="center",
                        fontsize=13, color="#4ade80", fontweight="bold")
                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.caption("No income recorded yet.")

        with c2:
            st.markdown("#### Expense breakdown")
            if not exp_df.empty:
                grp = exp_df.groupby("category")["amount"].sum()
                fig, ax = plt.subplots(figsize=(5, 4))
                wedges, texts, autotexts = ax.pie(
                    grp.values, labels=grp.index,
                    colors=EXPENSE_COLORS[:len(grp)],
                    autopct="%1.0f%%", startangle=90,
                    wedgeprops=dict(width=0.55, edgecolor="#0f0f1a", linewidth=2),
                    pctdistance=0.75,
                )
                for t in autotexts:
                    t.set_color("#0f0f1a"); t.set_fontsize(9); t.set_fontweight("bold")
                for t in texts:
                    t.set_color("#e8e8f0"); t.set_fontsize(9)
                ax.text(0, 0, f"€{user.total_expenses():,.0f}", ha="center", va="center",
                        fontsize=13, color="#f87171", fontweight="bold")
                fig.tight_layout()
                st.pyplot(fig)
                plt.close(fig)
            else:
                st.caption("No expenses recorded yet.")

        # Cumulative balance line chart
        st.markdown("#### Balance over time")
        df_sorted = df.sort_values("date").copy()
        df_sorted["signed"] = df_sorted.apply(
            lambda r: r["amount"] if r["type"] == "income" else -r["amount"], axis=1
        )
        df_sorted["cumulative"] = df_sorted["signed"].cumsum()

        fig, ax = plt.subplots(figsize=(10, 3))
        x = range(len(df_sorted))
        y = df_sorted["cumulative"].values
        ax.plot(x, y, color="#6366f1", linewidth=2.5, zorder=3)
        ax.fill_between(x, y, 0, color="#6366f1", alpha=0.15)
        ax.scatter(x, y, color="#a5b4fc", s=50, zorder=4, edgecolors="#0f0f1a", linewidths=1.5)
        ax.axhline(0, color=(1, 1, 1, 0.2), linestyle="--", linewidth=1)
        ax.set_xticks(list(x))
        ax.set_xticklabels(df_sorted["date"].str[:10].tolist(), rotation=30, ha="right", fontsize=8)
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"€{v:,.0f}"))
        ax.grid(axis="y")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        # Grouped bar chart
        if not inc_df.empty and not exp_df.empty:
            st.markdown("#### Income vs Expenses by category")
            inc_grp = inc_df.groupby("category")["amount"].sum().rename("Income")
            exp_grp = exp_df.groupby("category")["amount"].sum().rename("Expenses")
            merged  = pd.concat([inc_grp, exp_grp], axis=1).fillna(0)

            fig, ax = plt.subplots(figsize=(10, 3.5))
            n = len(merged)
            x = range(n)
            w = 0.35
            ax.bar([i - w/2 for i in x], merged["Income"],   width=w, color="#4ade80",
                   label="Income",   edgecolor="#0f0f1a", linewidth=0.8)
            ax.bar([i + w/2 for i in x], merged["Expenses"], width=w, color="#f87171",
                   label="Expenses", edgecolor="#0f0f1a", linewidth=0.8)
            ax.set_xticks(list(x))
            ax.set_xticklabels(merged.index, rotation=25, ha="right", fontsize=9)
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"€{v:,.0f}"))
            ax.legend(facecolor="#1a1a2e", edgecolor="#333355", labelcolor="#e8e8f0")
            ax.grid(axis="y")
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)

# ── ADD INCOME ────────────────────────────────────────────────────────────────
with tab_in:
    st.markdown("### Add Income")
    col1, col2 = st.columns(2)
    with col1:
        inc_amount = st.number_input("Amount (€)", min_value=0.0, step=1.0, format="%.2f", key="inc_amt")
        inc_cat    = st.selectbox("Category", CATEGORIES_INCOME, key="inc_cat")
    with col2:
        inc_note = st.text_input("Note (optional)", placeholder="e.g. January salary", key="inc_note")
    if st.button("Add Income ➕", use_container_width=True):
        if inc_amount > 0:
            user.add_income(inc_amount, inc_cat, inc_note)
            st.success(f"✅ Income of **€{inc_amount:.2f}** ({inc_cat}) added.")
            st.rerun()
        else:
            st.error("Enter an amount greater than €0.")

# ── ADD EXPENSE ───────────────────────────────────────────────────────────────
with tab_ex:
    st.markdown("### Add Expense")
    col1, col2 = st.columns(2)
    with col1:
        exp_amount = st.number_input("Amount (€)", min_value=0.0, step=1.0, format="%.2f", key="exp_amt")
        exp_cat    = st.selectbox("Category", CATEGORIES_EXPENSE, key="exp_cat")
    with col2:
        exp_note = st.text_input("Note (optional)", placeholder="e.g. Monthly rent", key="exp_note")
    if st.button("Add Expense ➖", use_container_width=True):
        if exp_amount > 0:
            user.add_expense(exp_amount, exp_cat, exp_note)
            st.success(f"✅ Expense of **€{exp_amount:.2f}** ({exp_cat}) added.")
            st.rerun()
        else:
            st.error("Enter an amount greater than €0.")

# ── HISTORY ───────────────────────────────────────────────────────────────────
with tab_hist:
    st.markdown("### Transaction History")
    df = user.df()
    if df.empty:
        st.info("No transactions yet.")
    else:
        filter_type = st.radio("Show", ["All", "Income only", "Expenses only"], horizontal=True)
        filtered = df if filter_type == "All" else \
                   df[df["type"] == ("income" if filter_type == "Income only" else "expense")]

        display = filtered[["date","type","category","amount","note"]].copy()
        display["amount"] = display["amount"].apply(lambda x: f"€{x:,.2f}")
        display["type"]   = display["type"].str.capitalize()
        display.columns   = ["Date","Type","Category","Amount","Note"]
        st.dataframe(display[::-1].reset_index(drop=True), use_container_width=True, hide_index=True)

        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "budget_export.csv", "text/csv")
