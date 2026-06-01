# Personal Expense Analytics
 
## Project Overview

**Personal Expense Analytics** is a complete end-to-end data analytics project that simulates, cleans, analyzes, and visualizes one year of personal expense data for a salaried individual in India. The project covers the entire data analytics workflow — from raw data generation and cleaning to insight extraction and professional chart creation.

---
*Intern Name:* Pranali Ingale  
*Intern ID:* CITS2281
*Domain:* Data Analytics  
*Organization:* CODTECH IT Solutions

## Objectives

- Generate a realistic expense dataset with 1,000+ records across 10 categories
- Perform thorough data cleaning and preprocessing
- Conduct exploratory data analysis (EDA)
- Identify monthly spending patterns and trends
- Analyze category-wise spending distribution
- Perform savings analysis and calculate savings rate
- Create 7 professional data visualizations
- Derive actionable insights and financial recommendations

---

## Tools & Libraries Used

| Tool / Library | Version | Purpose |
|---|---|---|
| Python | 3.10+ | Core programming language |
| Pandas | 2.1.4 | Data manipulation & analysis |
| NumPy | 1.26.4 | Numerical computations |
| Matplotlib | 3.8.2 | Chart creation |
| Seaborn | 0.13.2 | Statistical visualizations |
| Jupyter Notebook | 7.0.6 | Interactive analysis environment |

---

## Project Structure

```
personal_expense_analytics/
│
├── data/
│   └── expenses.csv             ← Auto-generated dataset (1000 records)
│
├── notebooks/
│   └── expense_analysis.ipynb   ← Full interactive analysis notebook
│
├── src/
│   └── analysis.py              ← Standalone Python script (run this!)
│
├── outputs/
│   └── charts/
│       ├── 01_monthly_trend.png
│       ├── 02_category_bar.png
│       ├── 03_category_pie.png
│       ├── 04_savings_vs_spending.png
│       ├── 05_payment_method_donut.png
│       ├── 06_weekly_heatmap.png
│       └── 07_top5_stacked_bar.png
│
├── README.md                    ← You are here
└── requirements.txt             ← Python dependencies
```

---

## Dataset Description

The dataset (`expenses.csv`) is synthetically generated and contains **1,000 records** spanning **January–December 2024**.

| Column | Type | Description |
|---|---|---|
| `ExpenseID` | Integer | Unique transaction ID |
| `Date` | Date | Transaction date (YYYY-MM-DD) |
| `Category` | String | Expense category |
| `Description` | String | Short description of expense |
| `Amount` | Float | Expense amount in Indian Rupees (₹) |
| `PaymentMethod` | String | Mode of payment used |
| `MonthlyIncome` | Integer | Fixed monthly salary (₹45,000) |

### Categories Covered
- 🏠 Rent
- 🍕 Food & Dining
- 🚌 Transportation
- 🛍️ Shopping
- 🎬 Entertainment
- 🏥 Healthcare
- 📚 Education
- 💡 Utilities
- 💆 Personal Care
- 📈 Savings & Investment

---

## Analysis Performed

| # | Analysis Type | Description |
|---|---|---|
| 1 | Data Cleaning | Null handling, type conversion, duplicate removal, derived columns |
| 2 | Descriptive Stats | Mean, median, std, min/max for all numeric columns |
| 3 | Monthly Trend | Total spending per month with line chart + annotations |
| 4 | Category Analysis | Category-wise totals, averages, and transaction counts |
| 5 | Savings Analysis | Monthly savings = Income − Spending; annual savings rate |
| 6 | Payment Method | Distribution of UPI/Cash/Card/etc. usage by spend value |
| 7 | Heatmap Analysis | Day-of-week × week-of-year spending intensity |
| 8 | Top 5 Stacked | Monthly breakdown by top 5 categories |

---

## Charts Generated

| Chart | File | Description |
|---|---|---|
| Monthly Spending Trend | `01_monthly_trend.png` | Line chart showing spend per month |
| Category Bar Chart | `02_category_bar.png` | Horizontal bar — total by category |
| Category Pie Chart | `03_category_pie.png` | Pie chart — top 5 + others |
| Savings vs Spending | `04_savings_vs_spending.png` | Grouped bar — savings vs spend |
| Payment Method Donut | `05_payment_method_donut.png` | Donut chart by payment method |
| Weekly Heatmap | `06_weekly_heatmap.png` | Day × week spending heatmap |
| Stacked Monthly Bar | `07_top5_stacked_bar.png` | Top 5 categories month-wise stack |

---

## Screenshots

> *After running the project, charts will appear in `outputs/charts/`. Add screenshots here for GitHub.*

| Chart | Preview |
|---|---|
| Monthly Trend | `outputs/charts/01_monthly_trend.png` |
| Category Bar | `outputs/charts/02_category_bar.png` |
| Pie Chart | `outputs/charts/03_category_pie.png` |
| Savings Analysis | `outputs/charts/04_savings_vs_spending.png` |
| Payment Method | `outputs/charts/05_payment_method_donut.png` |
| Heatmap | `outputs/charts/06_weekly_heatmap.png` |
| Stacked Bar | `outputs/charts/07_top5_stacked_bar.png` |

---

## Key Insights

1. **Rent is the single largest expense** (~40–45% of monthly income), which is typical for urban salaried employees.
2. **Shopping and Education** are the next highest discretionary categories — key areas to optimize.
3. **Spending peaks in certain months** (festive season, academic term starts) due to seasonal patterns.
4. **Weekend days show higher spending** than weekdays across most categories (visible in heatmap).
5. **UPI and Credit Card** are the dominant payment methods, reflecting the shift to digital payments in India.
6. **Savings rate fluctuates month-to-month** — automating savings on payday can help maintain consistency.
7. **Following the 50/30/20 rule** (Needs/Wants/Savings) would significantly improve financial health.

---

## How to Run the Project

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)
- VS Code (recommended) or any Python IDE

### Step 1 — Clone / Download the Project
```bash
git clone https://github.com/yourusername/personal-expense-analytics.git
cd personal_expense_analytics
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3A — Run as Python Script (Recommended for VS Code)
```bash
python src/analysis.py
```
This will:
- Generate `data/expenses.csv`
- Print statistics and insights to the terminal
- Save all 7 charts to `outputs/charts/`

### Step 3B — Run as Jupyter Notebook
```bash
jupyter notebook notebooks/expense_analysis.ipynb
```
Then click **"Run All Cells"** (Kernel → Restart & Run All).

---

## GitHub Upload Checklist

- [x] `README.md` with full documentation
- [x] `requirements.txt` with pinned versions
- [x] `src/analysis.py` — clean, commented Python script
- [x] `notebooks/expense_analysis.ipynb` — interactive notebook
- [x] `data/expenses.csv` — generated dataset
- [x] `outputs/charts/` — 7 professional charts
- [ ] Add `.gitignore` for `__pycache__/`, `.ipynb_checkpoints/`

---

## Author

Pranali ingale
B.Tech CSE (AI/ML) — 2nd Year 

---

*© 2024 | Built for educational and internship purposes*