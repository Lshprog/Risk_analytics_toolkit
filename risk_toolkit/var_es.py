import numpy as np
import pandas as pd
from typing import Tuple

def historical_var_es(
    returns: pd.Series,
    alpha: float = 0.95
) -> Tuple[float, float]:
    """
    Historical VaR and ES for a 1-day horizon.
    VaR_alpha: quantile of loss distribution
    ES_alpha: average loss beyond VaR
    returns: daily returns (positive/negative)
    """
    # Convert returns to losses
    losses = -returns.dropna()
    var = np.quantile(losses, alpha)
    es = losses[losses >= var].mean()
    return var, es


def parametric_var_es(
    returns: pd.Series,
    alpha: float = 0.95
) -> Tuple[float, float]:
    """
    Parametric (variance-covariance) VaR and ES assuming normality.
    """
    mu = returns.mean()
    sigma = returns.std(ddof=1)

    # One-day loss distribution ~ N(-mu, sigma)
    from scipy.stats import norm

    z = norm.ppf(alpha)
    var = -(mu - z * sigma)  # VaR as positive loss

    # ES for normal dist: ES = σ * φ(z) / (1-α) - μ
    phi = norm.pdf(z)
    es = (sigma * phi / (1 - alpha)) - mu

    return var, es


def monte_carlo_var_es(
    returns: pd.Series,
    alpha: float = 0.95,
    n_sims: int = 100_000
) -> Tuple[float, float]:
    """
    Monte Carlo VaR/ES assuming normal returns.
    """
    mu = returns.mean()
    sigma = returns.std(ddof=1)

    sims = np.random.normal(mu, sigma, size=n_sims)
    losses = -sims
    var = np.quantile(losses, alpha)
    es = losses[losses >= var].mean()
    return var, es
