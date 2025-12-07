from risk_toolkit.credit_risk import (
    portfolio_expected_loss,
    simulate_credit_losses,
    credit_var_es,
)

def main():
    exposures = {
        "Bond_A": 1_000_000,
        "Bond_B": 750_000,
        "Bond_C": 500_000,
    }

    ratings = {
        "Bond_A": "BBB",
        "Bond_B": "BB",
        "Bond_C": "B",
    }

    el = portfolio_expected_loss(exposures, ratings)
    print(f"Portfolio expected credit loss (1Y): {el:,.2f}")

    losses = simulate_credit_losses(exposures, ratings, n_sims=50_000)
    var95, es95 = credit_var_es(losses, alpha=0.95)
    print(f"Credit loss 95% VaR: {var95:,.2f}")
    print(f"Credit loss 95% ES : {es95:,.2f}")

if __name__ == "__main__":
    main()
