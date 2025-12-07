import numpy as np
import pandas as pd
from typing import Dict

def compute_log_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Compute daily log returns from price data.
    r_t = ln(P_t / P_{t-1})
    """
    return np.log(prices / prices.shift(1)).dropna()

def compute_portfolio_returns(
    returns: pd.DataFrame,
    weights: Dict[str, float]
) -> pd.Series:
    """
    Compute portfolio returns from asset returns and weights.
    weights: dict like {"SPY": 0.5, "LQD": 0.3, "IEF": 0.2}
    """
    w = pd.Series(weights)
    w = w / w.sum()
    returns = returns[w.index]  # align columns
    port_ret = returns.dot(w)
    port_ret.name = "portfolio"
    return port_ret
