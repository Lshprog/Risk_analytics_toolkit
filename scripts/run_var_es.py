from risk_toolkit.data_loader import load_or_download_prices
from risk_toolkit.returns import compute_log_returns, compute_portfolio_returns
from risk_toolkit.var_es import historical_var_es, parametric_var_es, monte_carlo_var_es

def main():
    tickers = ["SPY", "LQD", "IEF"]
    weights = {"SPY": 0.5, "LQD": 0.3, "IEF": 0.2}

    prices = load_or_download_prices(tickers, start="2018-01-01")
    rets = compute_log_returns(prices)
    port_rets = compute_portfolio_returns(rets, weights)

    h_var, h_es = historical_var_es(port_rets, alpha=0.95)
    p_var, p_es = parametric_var_es(port_rets, alpha=0.95)
    m_var, m_es = monte_carlo_var_es(port_rets, alpha=0.95)

    print("Portfolio 1-day 95% VaR / ES:")
    print(f"Historical   VaR={h_var:.4%}, ES={h_es:.4%}")
    print(f"Parametric   VaR={p_var:.4%}, ES={p_es:.4%}")
    print(f"Monte Carlo  VaR={m_var:.4%}, ES={m_es:.4%}")

if __name__ == "__main__":
    main()
