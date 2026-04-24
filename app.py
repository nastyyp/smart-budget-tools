import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Budget",
    page_icon="💶",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    color: #e8e8f0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.04);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Metric cards */
.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 20px 24px;
    backdrop-filter: blur(10px);
}

/* Positive balance */
.balance-positive { color: #4ade80; }
.balance-negative { color: #f87171; }

/* Inputs */
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] select {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #e8e8f0 !important;
    border-radius: 10px !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 10px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 600;
    padding: 0.5rem 1.5rem;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 25px rgba(99,102,241,0.4);
}

/* Tabs */
[data-testid="stTabs"] [role="tab"] {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    color: rgba(232,232,240,0.6);
    border-radius: 8px 8px 0 0;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    color: #a5b4fc;
    border-bottom: 2px solid #6366f1;
}

/* Headings */
h1, h2, h3 { font-family: 'Space Mono', monospace; color: #e8e8f0; }

/* Divider */
hr { border-color: rgba(255,255,255,0.08); }

/* Success / error */
[data-testid="stAlert"] { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


# ── Data model ────────────────────────────────────────────────────────────────
CATEGORIES_INCOME  = ["Salary / Part-time", "Scholarship", "Family Support", "Freelance", "Other"]
CATEGORIES_EXPENSE = ["Rent", "Food & Groceries", "Transport", "Books & Supplies",
                      "Entertainment", "Health", "Clothing", "Subscriptions", "Other"]

class User:
    def __init__(self, name: str):
        self.name = name
        self.transactions: list[dict] = []   # {type, amount, category, note, date}

    def add_income(self, amount: float, category: str, note: str = ""):
        if amount > 0:
            self.transactions.append({
                "type": "income", "amount": amount,
                "category": category, "note": note,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })

    def add_expense(self, amount: float, category: str, note: str = ""):
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


# ── Helper: plotly theme ──────────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#e8e8f0"),
    margin=dict(t=30, b=20, l=10, r=10),
)

INCOME_COLORS  = ["#6366f1","#818cf8","#a5b4fc","#c7d2fe","#e0e7ff"]
EXPENSE_COLORS = ["#f87171","#fb923c","#fbbf24","#34d399","#22d3ee",
                  "#818cf8","#e879f9","#94a3b8","#f472b6"]


# ── Onboarding ────────────────────────────────────────────────────────────────
if st.session_state.user is None:
    col_l, col_c, col_r = st.columns([1, 2, 1])
    with col_c:
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


# ── Main app ──────────────────────────────────────────────────────────────────
user: User = st.session_state.user

# Sidebar
with st.sidebar:
    st.markdown(f"### 👋 {user.name}")
    st.markdown("---")
    bal = user.balance()
    color_cls = "balance-positive" if bal >= 0 else "balance-negative"
    st.markdown(f"""
    <div class='metric-card' style='text-align:center;margin-bottom:12px'>
        <div style='font-size:12px;opacity:.6;letter-spacing:1px;text-transform:uppercase'>Balance</div>
        <div class='{color_cls}' style='font-size:2rem;font-family:Space Mono,monospace;font-weight:700'>
            €{bal:,.2f}
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='display:flex;gap:10px'>
        <div class='metric-card' style='flex:1;text-align:center'>
            <div style='font-size:11px;opacity:.55;text-transform:uppercase;letter-spacing:.8px'>Income</div>
            <div style='color:#4ade80;font-size:1.1rem;font-weight:700'>€{user.total_income():,.2f}</div>
        </div>
        <div class='metric-card' style='flex:1;text-align:center'>
            <div style='font-size:11px;opacity:.55;text-transform:uppercase;letter-spacing:.8px'>Spent</div>
            <div style='color:#f87171;font-size:1.1rem;font-weight:700'>€{user.total_expenses():,.2f}</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🚪 Switch user", use_container_width=True):
        st.session_state.user = None
        st.rerun()

# Page tabs
tab_dash, tab_in, tab_ex, tab_hist = st.tabs(["📊 Dashboard", "➕ Add Income", "➖ Add Expense", "📋 History"])


# ── DASHBOARD ─────────────────────────────────────────────────────────────────
with tab_dash:
    df = user.df()

    if df.empty:
        st.info("No transactions yet — add some income or expenses to see your dashboard.")
    else:
        inc_df = df[df["type"] == "income"]
        exp_df = df[df["type"] == "expense"]

        # ── Row 1: KPI cards ──
        k1, k2, k3, k4 = st.columns(4)
        savings_rate = (user.balance() / user.total_income() * 100) if user.total_income() else 0

        for col, label, value, color in [
            (k1, "Total Income",    f"€{user.total_income():,.2f}",   "#4ade80"),
            (k2, "Total Expenses",  f"€{user.total_expenses():,.2f}", "#f87171"),
            (k3, "Net Balance",     f"€{user.balance():,.2f}",        "#4ade80" if user.balance() >= 0 else "#f87171"),
            (k4, "Savings Rate",    f"{savings_rate:.1f}%",           "#818cf8"),
        ]:
            col.markdown(f"""
            <div class='metric-card'>
                <div style='font-size:11px;opacity:.55;text-transform:uppercase;letter-spacing:.8px'>{label}</div>
                <div style='color:{color};font-size:1.6rem;font-family:Space Mono,monospace;font-weight:700;margin-top:4px'>
                    {value}
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Row 2: Pie charts ──
        c_left, c_right = st.columns(2)

        with c_left:
            st.markdown("#### Income breakdown")
            if not inc_df.empty:
                grp = inc_df.groupby("category")["amount"].sum().reset_index()
                fig = go.Figure(go.Pie(
                    labels=grp["category"], values=grp["amount"],
                    hole=0.55,
                    marker=dict(colors=INCOME_COLORS, line=dict(color="#0f0f1a", width=2)),
                    textfont=dict(size=12, color="#e8e8f0"),
                    hovertemplate="<b>%{label}</b><br>€%{value:,.2f}<extra></extra>",
                ))
                fig.add_annotation(text=f"€{user.total_income():,.0f}",
                                   x=0.5, y=0.5, font=dict(size=18, color="#4ade80", family="Space Mono"),
                                   showarrow=False)
                fig.update_layout(**PLOTLY_LAYOUT, showlegend=True,
                                  legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.caption("No income recorded yet.")

        with c_right:
            st.markdown("#### Expense breakdown")
            if not exp_df.empty:
                grp = exp_df.groupby("category")["amount"].sum().reset_index()
                fig = go.Figure(go.Pie(
                    labels=grp["category"], values=grp["amount"],
                    hole=0.55,
                    marker=dict(colors=EXPENSE_COLORS, line=dict(color="#0f0f1a", width=2)),
                    textfont=dict(size=12, color="#e8e8f0"),
                    hovertemplate="<b>%{label}</b><br>€%{value:,.2f}<extra></extra>",
                ))
                fig.add_annotation(text=f"€{user.total_expenses():,.0f}",
                                   x=0.5, y=0.5, font=dict(size=18, color="#f87171", family="Space Mono"),
                                   showarrow=False)
                fig.update_layout(**PLOTLY_LAYOUT, showlegend=True,
                                  legend=dict(orientation="h", y=-0.15, x=0.5, xanchor="center"))
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.caption("No expenses recorded yet.")

        # ── Row 3: Cumulative balance line chart ──
        st.markdown("#### Balance over time")
        df_sorted = df.sort_values("date").copy()
        df_sorted["signed"] = df_sorted.apply(
            lambda r: r["amount"] if r["type"] == "income" else -r["amount"], axis=1
        )
        df_sorted["cumulative"] = df_sorted["signed"].cumsum()
        df_sorted["label"] = df_sorted["date"].str[:10]

        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=df_sorted["label"], y=df_sorted["cumulative"],
            mode="lines+markers",
            line=dict(color="#6366f1", width=3),
            marker=dict(size=7, color="#a5b4fc", line=dict(color="#0f0f1a", width=2)),
            fill="tozeroy",
            fillcolor="rgba(99,102,241,0.12)",
            hovertemplate="€%{y:,.2f}<extra></extra>",
        ))
        fig_line.add_hline(y=0, line_dash="dot", line_color="rgba(255,255,255,0.2)")
        fig_line.update_layout(
            **PLOTLY_LAYOUT,
            xaxis=dict(showgrid=False, tickfont=dict(size=11)),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)",
                       tickprefix="€", tickfont=dict(size=11)),
            height=280,
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # ── Row 4: Grouped bar by category ──
        if not inc_df.empty and not exp_df.empty:
            st.markdown("#### Income vs Expenses by category")
            inc_grp = inc_df.groupby("category")["amount"].sum().reset_index().rename(columns={"amount": "Income"})
            exp_grp = exp_df.groupby("category")["amount"].sum().reset_index().rename(columns={"amount": "Expenses"})
            merged = pd.merge(inc_grp, exp_grp, on="category", how="outer").fillna(0)

            fig_bar = go.Figure()
            fig_bar.add_trace(go.Bar(name="Income",   x=merged["category"], y=merged["Income"],
                                     marker_color="#4ade80", marker_line_width=0))
            fig_bar.add_trace(go.Bar(name="Expenses", x=merged["category"], y=merged["Expenses"],
                                     marker_color="#f87171", marker_line_width=0))
            fig_bar.update_layout(
                **PLOTLY_LAYOUT, barmode="group", bargap=0.25, bargroupgap=0.08,
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.06)", tickprefix="€"),
                legend=dict(orientation="h", y=1.08, x=1, xanchor="right"),
                height=300,
            )
            st.plotly_chart(fig_bar, use_container_width=True)


# ── ADD INCOME ────────────────────────────────────────────────────────────────
with tab_in:
    st.markdown("### Add Income")
    col1, col2 = st.columns([1, 1])
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
    col1, col2 = st.columns([1, 1])
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
        display.columns   = ["Date", "Type", "Category", "Amount", "Note"]

        st.dataframe(display[::-1].reset_index(drop=True),
                     use_container_width=True, hide_index=True)

        # Download button
        csv = filtered.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download CSV", csv, "budget_export.csv", "text/csv")
