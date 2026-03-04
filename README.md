# Quantum Portfolio Analytics Engine 📊

A personal portfolio analytics tool built with Streamlit that helps you analyze Indian (and US) stocks with institutional-grade metrics — without needing a Bloomberg terminal.

---

## What it does

You type in a few stock tickers, hit analyze, and it gives you:

- **Key metrics** — Annual return, volatility, beta, and Sharpe ratio for each stock
- **Efficient Frontier** — Runs 10,000 Monte Carlo simulations to find the mathematically optimal way to combine your stocks (Max Sharpe & Min Volatility portfolios)
- **Correlation Heatmap** — Shows how your stocks move relative to each other, so you can spot diversification gaps
- **Cumulative Returns Chart** — Compares all your stocks vs Nifty 50 over time

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/quantum-portfolio-engine.git
cd quantum-portfolio-engine
```

**2. Install dependencies**
```bash
pip install streamlit yfinance pandas numpy plotly scipy
```

**3. Run the app**
```bash
streamlit run quantum_portfolio.py
```

That's it. Opens in your browser at `localhost:8501`.

---

## How to use it

**For Indian stocks (NSE)** — add `.NS` after the ticker:
```
RELIANCE.NS, TCS.NS, HDFCBANK.NS, INFY.NS, ICICIBANK.NS
```

**For US stocks** — just use the ticker directly:
```
AAPL, MSFT, GOOGL, NVDA
```

You can mix both in the same search.

---

## Settings (inside the code)

| Setting | Default | What it does |
|---|---|---|
| `risk_free_rate` | 0.07 | 7% — based on Indian govt bond rate |
| `start_date` | 2020-01-01 | 5 year lookback window |
| `market_index` | ^NSEI | Nifty 50 as benchmark |
| `N_SIMULATIONS` | 10,000 | Monte Carlo simulation count |

---

## Tech Stack

- **Streamlit** — App framework
- **yFinance** — Stock data from Yahoo Finance
- **Plotly** — Interactive charts
- **SciPy** — Portfolio optimization
- **Pandas / NumPy** — Data crunching

---

## Known Limitations

- Data comes from Yahoo Finance — occasionally some tickers have gaps (shows NaN)
- If a stock was listed after your start date, it may show incomplete data
- For best results use `.NS` tickers (NSE) over `.BO` (BSE) — cleaner data

---

## Project Structure

```
quantum-portfolio-engine/
│
├── quantum_portfolio.py    # Main app
└── README.md
```

---

Built by **DGen Analytics** — because good portfolio tools shouldn't cost $2,000/month.
