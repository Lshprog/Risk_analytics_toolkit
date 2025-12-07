# risk_toolkit/data_loader.py

from typing import List, Optional

import pandas as pd
import yfinance as yf


def download_prices(
    tickers: List[str],
    start: str = "2015-01-01",
    end: Optional[str] = None,
) -> pd.DataFrame:
    """
    Download daily price data for a list of tickers from Yahoo Finance
    and return a DataFrame of adjusted (or close) prices.

    Tries to be robust to different yfinance output formats.
    """
    data = yf.download(
        tickers,
        start=start,
        end=end,
        progress=False,
    )

    if data.empty:
        raise ValueError("No data downloaded. Check tickers and date range.")

    # yfinance can return:
    # - MultiIndex columns: (field, ticker) like ('Adj Close', 'SPY')
    # - or single-level columns with fields (Open, High, Low, Close, Adj Close, Volume)
    # - or directly per-ticker columns
    if isinstance(data.columns, pd.MultiIndex):
        # First level usually: 'Adj Close', 'Close', etc.
        lvl0 = list(data.columns.levels[0])
        if "Adj Close" in lvl0:
            field = "Adj Close"
        elif "Close" in lvl0:
            field = "Close"
        else:
            # Fall back to the first available field
            field = lvl0[0]

        prices = data[field]
    else:
        cols = list(data.columns)
        if "Adj Close" in cols:
            prices = data["Adj Close"]
        elif "Close" in cols:
            prices = data["Close"]
        else:
            # Assume it's already prices by ticker
            prices = data

    # Ensure DataFrame even for one ticker
    if isinstance(prices, pd.Series):
        prices = prices.to_frame()

    # Keep only the requested tickers and drop all-NaN rows
    prices = prices[[t for t in tickers if t in prices.columns]]
    return prices.dropna(how="all")


def load_or_download_prices(
    tickers: List[str],
    cache_path: str = "../data/prices_raw.csv",
    start: str = "2015-01-01",
    end: Optional[str] = None,
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    Load prices from CSV if available and valid, otherwise download and cache.
    """
    try:
        if use_cache:
            df = pd.read_csv(cache_path, index_col=0, parse_dates=True)
            # Make sure it contains all tickers
            missing = [t for t in tickers if t not in df.columns]
            if missing:
                raise ValueError(f"Missing tickers in cached file: {missing}")
            return df
    except Exception:
        # Fall back to fresh download
        pass

    df = download_prices(tickers, start=start, end=end)
    df.to_csv(cache_path)
    return df
