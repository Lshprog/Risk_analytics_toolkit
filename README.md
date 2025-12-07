# Risk Analytics Toolkit

This project is a lightweight Python toolkit for **market risk** and **credit risk** analysis using real ETF data.  
It is designed as a compact, internship-level project that demonstrates core risk-modelling concepts and clean analytical code.

---

## Overview

The toolkit implements:

- **Market Risk**
  - Daily log return computation for multiple ETFs
  - Portfolio construction from asset-level returns and weights
  - 1-day 95% **Value-at-Risk (VaR)** and **Expected Shortfall (ES)** using:
    - Historical simulation
    - Parametric (variance–covariance) method
    - Monte Carlo simulation
  - Visualization of the portfolio loss distribution with VaR/ES markers

- **Credit Risk**
  - A small hypothetical bond portfolio with notional exposures and credit ratings
  - Rating-based **Probability of Default (PD)** assignment
  - Fixed **Loss Given Default (LGD)** and **Expected Loss (EL)** calculation
  - Monte Carlo simulation of default events to generate a credit-loss distribution
  - Computation of **credit VaR** and **credit ES**

Overall, the project ties together data ingestion, portfolio construction, risk metric computation, and distribution-based visualization in a way that mirrors basic workflows in market and credit risk teams.

---

## Project Structure

```text
risk-toolkit/
│
├─ risk_toolkit/
│  ├─ __init__.py
│  ├─ data_loader.py        # Downloads ETF prices (SPY, LQD, IEF) via yfinance
│  ├─ returns.py            # Computes log returns and portfolio returns
│  ├─ var_es.py             # Historical, parametric, and Monte Carlo VaR/ES
│  └─ credit_risk.py        # PD/LGD/EL and credit-loss simulation
│
├─ notebooks/
│  └─ 02_var_es_credit_risk_demo.ipynb   # Main demonstration notebook
│
├─ scripts/
│  ├─ run_var_es.py         # CLI script to compute market VaR/ES
│  └─ run_credit_sim.py     # CLI script to simulate credit losses
│
├─ data/                    # Cached ETF price data (auto-generated)
├─ requirements.txt
└─ README.md
