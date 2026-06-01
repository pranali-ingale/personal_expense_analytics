# ============================================================
#   Personal Expense Analytics — src/analysis.py
#   Author  : Pranali jayprakash ingale
#   Purpose : Generate dataset + run full analysis + save charts
# ============================================================

import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from datetime import datetime, timedelta

# ── Paths ────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH   = os.path.join(BASE_DIR, "data",    "expenses.csv")
CHARTS_DIR  = os.path.join(BASE_DIR, "outputs", "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

# ── Seaborn theme ─────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "figure.dpi": 130,
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
})

# ─────────────────────────────────────────────────────────────
#  STEP 1 – Generate realistic sample dataset
# ─────────────────────────────────────────────────────────────

def generate_dataset(n: int = 1000, seed: int = 42) -> pd.DataFrame:
    """
    Create a synthetic expense dataset for one calendar year.
    Returns a DataFrame and saves it to data/expenses.csv.
    """
    random.seed(seed)
    np.random.seed(seed)

    categories = {
        "Food & Dining":      (150,  80),
        "Transportation":     (80,   40),
        "Shopping":           (200, 120),
        "Entertainment":      (100,  60),
        "Healthcare":         (120,  90),
        "Education":          (300, 150),
        "Utilities":          (60,   20),
        "Rent":               (8000, 500),   # monthly, handled separately
        "Personal Care":      (50,   25),
        "Savings & Investment":(500, 200),
    }

    payment_methods = ["Cash", "Credit Card", "Debit Card", "UPI", "Net Banking"]

    start_date = datetime(2024, 1, 1)
    end_date   = datetime(2024, 12, 31)
    date_range = (end_date - start_date).days

    records = []
    expense_id = 1

    # ── Monthly income (salary) ──
    monthly_income = 45000

    for month in range(1, 13):
        # Rent – one record per month
        rent_date = datetime(2024, month, 1)
        records.append({
            "ExpenseID"      : expense_id,
            "Date"           : rent_date.strftime("%Y-%m-%d"),
            "Category"       : "Rent",
            "Description"    : "Monthly Rent",
            "Amount"         : round(np.random.normal(8000, 200), 2),
            "PaymentMethod"  : "Net Banking",
            "MonthlyIncome"  : monthly_income,
        })
        expense_id += 1

    # ── Random daily expenses ──
    remaining = n - 12       # 12 records already used for rent
    for _ in range(remaining):
        cat = random.choice([c for c in categories if c != "Rent"])
        mean, std = categories[cat]
        amount = round(abs(np.random.normal(mean * 0.15, std * 0.10)) + 10, 2)

        rand_days = random.randint(0, date_range)
        exp_date  = start_date + timedelta(days=rand_days)

        records.append({
            "ExpenseID"      : expense_id,
            "Date"           : exp_date.strftime("%Y-%m-%d"),
            "Category"       : cat,
            "Description"    : f"{cat} expense",
            "Amount"         : amount,
            "PaymentMethod"  : random.choice(payment_methods),
            "MonthlyIncome"  : monthly_income,
        })
        expense_id += 1

    df = pd.DataFrame(records)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    df.to_csv(DATA_PATH, index=False)
    print(f"[✓] Dataset saved → {DATA_PATH}  ({len(df)} records)")
    return df


# ─────────────────────────────────────────────────────────────
#  STEP 2 – Data Cleaning
# ─────────────────────────────────────────────────────────────

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning: types, nulls, duplicates, derived columns."""
    print("\n── Data Cleaning ──")
    print(f"  Shape before : {df.shape}")

    df["Date"]   = pd.to_datetime(df["Date"])
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # Drop rows where Amount is null or zero
    before = len(df)
    df = df.dropna(subset=["Amount", "Category"])
    df = df[df["Amount"] > 0]
    df = df.drop_duplicates(subset=["ExpenseID"])
    print(f"  Rows dropped : {before - len(df)}")

    # Derived columns
    df["Month"]     = df["Date"].dt.month
    df["MonthName"] = df["Date"].dt.strftime("%b")
    df["Year"]      = df["Date"].dt.year
    df["DayOfWeek"] = df["Date"].dt.day_name()
    df["Week"]      = df["Date"].dt.isocalendar().week.astype(int)

    # Savings = income − total monthly spend (approximated per row)
    monthly_spend = df.groupby("Month")["Amount"].sum().rename("MonthlySpend")
    df = df.merge(monthly_spend.reset_index(), on="Month", how="left")
    df["MonthlySavings"] = df["MonthlyIncome"] - df["MonthlySpend"]

    print(f"  Shape after  : {df.shape}")
    print(f"  Null values  :\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    return df


# ─────────────────────────────────────────────────────────────
#  STEP 3 – EDA helpers
# ─────────────────────────────────────────────────────────────

def basic_stats(df: pd.DataFrame):
    print("\n── Basic Statistics ──")
    print(df[["Amount", "MonthlyIncome", "MonthlySavings"]].describe().round(2))

    total_spent   = df["Amount"].sum()
    avg_monthly   = df.groupby("Month")["Amount"].sum().mean()
    max_cat       = df.groupby("Category")["Amount"].sum().idxmax()

    print(f"\n  Total spent (2024)   : ₹{total_spent:,.2f}")
    print(f"  Avg monthly spend    : ₹{avg_monthly:,.2f}")
    print(f"  Highest-spend cat    : {max_cat}")
    return total_spent, avg_monthly, max_cat


# ─────────────────────────────────────────────────────────────
#  STEP 4 – Charts
# ─────────────────────────────────────────────────────────────

def _save(fig, name: str):
    path = os.path.join(CHARTS_DIR, name)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    print(f"  [✓] {name}")


# Chart 1 – Monthly Spending Trend (line chart)
def chart_monthly_trend(df: pd.DataFrame):
    monthly = (df.groupby(["Month", "MonthName"])["Amount"]
                 .sum()
                 .reset_index()
                 .sort_values("Month"))

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(monthly["MonthName"], monthly["Amount"],
            marker="o", linewidth=2.5, color="#2196F3", markersize=8)
    ax.fill_between(range(len(monthly)), monthly["Amount"],
                    alpha=0.12, color="#2196F3")
    ax.set_xticklabels(monthly["MonthName"])
    ax.set_title("Monthly Spending Trend (2024)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Spent (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    ax.grid(axis="y", linestyle="--", alpha=0.6)

    for i, row in monthly.iterrows():
        ax.annotate(f"₹{row['Amount']:,.0f}",
                    xy=(i - monthly.index[0], row["Amount"]),
                    xytext=(0, 10), textcoords="offset points",
                    ha="center", fontsize=8, color="#333")
    fig.tight_layout()
    _save(fig, "01_monthly_trend.png")


# Chart 2 – Category-wise Total Spending (horizontal bar)
def chart_category_bar(df: pd.DataFrame):
    cat_spend = (df.groupby("Category")["Amount"]
                   .sum()
                   .sort_values(ascending=True))

    colors = sns.color_palette("Blues_d", len(cat_spend))
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(cat_spend.index, cat_spend.values, color=colors, edgecolor="white")
    ax.bar_label(bars, fmt="₹%.0f", padding=5, fontsize=9)
    ax.set_title("Category-wise Total Spending")
    ax.set_xlabel("Total Amount (₹)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    fig.tight_layout()
    _save(fig, "02_category_bar.png")


# Chart 3 – Spending Distribution Pie Chart
def chart_category_pie(df: pd.DataFrame):
    cat_spend = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    top5   = cat_spend.head(5)
    others = cat_spend.iloc[5:].sum()
    labels = list(top5.index) + ["Others"]
    sizes  = list(top5.values) + [others]

    fig, ax = plt.subplots(figsize=(9, 9))
    wedge_props = {"edgecolor": "white", "linewidth": 2}
    ax.pie(sizes, labels=labels, autopct="%1.1f%%",
           startangle=140, wedgeprops=wedge_props,
           colors=sns.color_palette("pastel", len(labels)))
    ax.set_title("Expense Distribution by Category (Top 5 + Others)")
    fig.tight_layout()
    _save(fig, "03_category_pie.png")


# Chart 4 – Monthly Savings vs Spending (grouped bar)
def chart_savings_vs_spending(df: pd.DataFrame):
    monthly = (df.groupby(["Month", "MonthName"])
                 .agg(Spending=("Amount", "sum"),
                      Income=("MonthlyIncome", "first"))
                 .reset_index()
                 .sort_values("Month"))
    monthly["Savings"] = monthly["Income"] - monthly["Spending"]

    x      = np.arange(len(monthly))
    width  = 0.35
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x - width/2, monthly["Spending"], width,
           label="Spending", color="#EF5350", alpha=0.85)
    ax.bar(x + width/2, monthly["Savings"],  width,
           label="Savings",  color="#66BB6A", alpha=0.85)

    ax.set_xticks(x)
    ax.set_xticklabels(monthly["MonthName"])
    ax.set_title("Monthly Income vs Spending vs Savings")
    ax.set_ylabel("Amount (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    ax.legend()
    ax.axhline(monthly["Income"].iloc[0], linestyle="--",
               color="steelblue", linewidth=1.5, label="Income")
    ax.legend()
    fig.tight_layout()
    _save(fig, "04_savings_vs_spending.png")


# Chart 5 – Payment Method Distribution (donut chart)
def chart_payment_method(df: pd.DataFrame):
    pm = df.groupby("PaymentMethod")["Amount"].sum().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(8, 8))
    wedge_props = {"edgecolor": "white", "linewidth": 2.5, "width": 0.5}
    ax.pie(pm.values, labels=pm.index, autopct="%1.1f%%",
           startangle=90, wedgeprops=wedge_props,
           colors=sns.color_palette("Set2", len(pm)))
    ax.set_title("Spending by Payment Method")
    fig.tight_layout()
    _save(fig, "05_payment_method_donut.png")


# Chart 6 – Weekly Spending Heatmap (day-of-week vs week-of-year)
def chart_heatmap(df: pd.DataFrame):
    dow_order = ["Monday", "Tuesday", "Wednesday",
                 "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = (df.groupby(["DayOfWeek", "Week"])["Amount"]
               .sum()
               .unstack(fill_value=0))
    pivot = pivot.reindex(dow_order)

    fig, ax = plt.subplots(figsize=(18, 5))
    sns.heatmap(pivot, ax=ax, cmap="YlOrRd", linewidths=0.3,
                linecolor="white", cbar_kws={"label": "₹ Spent"})
    ax.set_title("Weekly Spending Heatmap (Day-of-Week × Week Number)")
    ax.set_xlabel("Week of Year")
    ax.set_ylabel("Day of Week")
    fig.tight_layout()
    _save(fig, "06_weekly_heatmap.png")


# Chart 7 – Top 5 Categories Monthly Stacked Bar
def chart_stacked_monthly(df: pd.DataFrame):
    top5_cats = (df.groupby("Category")["Amount"]
                   .sum()
                   .nlargest(5)
                   .index.tolist())
    sub = df[df["Category"].isin(top5_cats)]
    pivot = (sub.groupby(["Month", "Category"])["Amount"]
                .sum()
                .unstack(fill_value=0))
    pivot.index = [datetime(2024, m, 1).strftime("%b") for m in pivot.index]

    fig, ax = plt.subplots(figsize=(12, 6))
    pivot.plot(kind="bar", stacked=True, ax=ax,
               colormap="tab10", edgecolor="white", linewidth=0.5)
    ax.set_title("Top 5 Categories — Monthly Stacked Spending")
    ax.set_xlabel("Month")
    ax.set_ylabel("Amount (₹)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"₹{x:,.0f}"))
    ax.legend(loc="upper right", fontsize=9)
    plt.xticks(rotation=45)
    fig.tight_layout()
    _save(fig, "07_top5_stacked_bar.png")


# ─────────────────────────────────────────────────────────────
#  STEP 5 – Insights Summary
# ─────────────────────────────────────────────────────────────

def print_insights(df: pd.DataFrame):
    print("\n" + "="*55)
    print("       KEY INSIGHTS — Personal Expense Analytics")
    print("="*55)

    total_spent  = df["Amount"].sum()
    total_income = df["MonthlyIncome"].iloc[0] * 12
    total_saved  = total_income - total_spent
    savings_pct  = (total_saved / total_income) * 100

    monthly_spend = df.groupby(["Month","MonthName"])["Amount"].sum().reset_index()
    max_month = monthly_spend.loc[monthly_spend["Amount"].idxmax()]
    min_month = monthly_spend.loc[monthly_spend["Amount"].idxmin()]

    cat_spend = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)
    top_cat   = cat_spend.index[0]

    print(f"\n  💰 Total Income (2024)   : ₹{total_income:>12,.2f}")
    print(f"  💸 Total Spent  (2024)   : ₹{total_spent:>12,.2f}")
    print(f"  🏦 Total Saved  (2024)   : ₹{total_saved:>12,.2f}  ({savings_pct:.1f}%)")
    print(f"\n  📈 Highest-spend month   : {max_month['MonthName']}  (₹{max_month['Amount']:,.2f})")
    print(f"  📉 Lowest-spend month    : {min_month['MonthName']}  (₹{min_month['Amount']:,.2f})")
    print(f"\n  🏆 Top expense category  : {top_cat}  (₹{cat_spend[top_cat]:,.2f})")
    print("\n  📋 Category-wise Totals:")
    for cat, amt in cat_spend.items():
        pct = (amt / total_spent) * 100
        bar = "█" * int(pct / 2)
        print(f"     {cat:<25} ₹{amt:>9,.2f}  {pct:5.1f}%  {bar}")

    print("\n  ✅ Recommendations:")
    if savings_pct < 20:
        print("     ⚠ Savings rate below 20% — try to cut discretionary spending.")
    else:
        print("     ✔ Great savings rate! Aim to invest surplus in SIPs / FDs.")
    print(f"     • Reduce '{top_cat}' expenses to improve overall savings.")
    print("     • Use UPI / Debit Card to track spending more easily.")
    print("="*55)


# ─────────────────────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────────────────────

def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Personal Expense Analytics — 2024      ║")
    print("╚══════════════════════════════════════════╝\n")

    # 1. Generate data
    df_raw = generate_dataset(n=1000)

    # 2. Clean
    df = clean_data(df_raw)

    # 3. Stats
    basic_stats(df)

    # 4. Charts
    print("\n── Generating Charts ──")
    chart_monthly_trend(df)
    chart_category_bar(df)
    chart_category_pie(df)
    chart_savings_vs_spending(df)
    chart_payment_method(df)
    chart_heatmap(df)
    chart_stacked_monthly(df)

    # 5. Insights
    print_insights(df)

    print(f"\n[✓] All charts saved to → {CHARTS_DIR}")
    print("[✓] Analysis complete!\n")


if __name__ == "__main__":
    main()
