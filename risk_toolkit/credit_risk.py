import numpy as np
import pandas as pd
from typing import Dict, List

# Example 1-year PD table by rating (toy numbers, not exact)
PD_TABLE = {
    "AAA": 0.0005,
    "AA":  0.001,
    "A":   0.002,
    "BBB": 0.01,
    "BB":  0.03,
    "B":   0.06,
    "CCC": 0.15,
}

DEFAULT_LGD = 0.60  # 60% loss given default


def expected_loss(exposure: float, pd: float, lgd: float = DEFAULT_LGD) -> float:
    """
    EL = PD * LGD * Exposure
    """
    return exposure * pd * lgd


def portfolio_expected_loss(
    exposures: Dict[str, float],
    ratings: Dict[str, str],
    lgd: float = DEFAULT_LGD
) -> float:
    """
    exposures: {"Bond1": 1_000_000, "Bond2": 500_000, ...}
    ratings:   {"Bond1": "BBB",     "Bond2": "BB",     ...}
    """
    total_el = 0.0
    for name, exp in exposures.items():
        rating = ratings[name]
        pd = PD_TABLE[rating]
        total_el += expected_loss(exp, pd, lgd)
    return total_el


def simulate_credit_losses(
    exposures: Dict[str, float],
    ratings: Dict[str, str],
    lgd: float = DEFAULT_LGD,
    n_sims: int = 100_000,
) -> pd.Series:
    """
    Monte Carlo simulation of portfolio credit losses over 1 year.
    Each bond defaults with probability PD independently.
    """
    bond_names = list(exposures.keys())
    pds = np.array([PD_TABLE[ratings[b]] for b in bond_names])
    exps = np.array([exposures[b] for b in bond_names])

    losses = []
    for _ in range(n_sims):
        # Bernoulli default indicators
        defaults = np.random.binomial(1, pds)
        loss = np.sum(defaults * exps * lgd)
        losses.append(loss)

    return pd.Series(losses, name="credit_loss")


def credit_var_es(
    losses: pd.Series,
    alpha: float = 0.95
):
    """
    VaR/ES on simulated credit-loss distribution.
    """
    var = np.quantile(losses, alpha)
    es = losses[losses >= var].mean()
    return var, es
