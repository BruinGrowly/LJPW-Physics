import numpy as np
import matplotlib.pyplot as plt

def simulate_autopoietic_loan():
    """
    Simulates the 'Autopoietic Loan' structure where a borrower acts as a Sink,
    investing a 'Retention Premium' (1/n) alongside debt repayment to achieve
    a Crossover Point where Investment Income > Loan Cost.
    """
    print("--- LJPW Autopoietic Loan Simulation ---")
    
    # --- Parameters ---
    loan_amount = 500000.0       # $500k Mortgage
    loan_rate_annual = 0.06      # 6.0% Interest Rate
    loan_term_years = 30
    
    # The Power Algorithm: Retention (1/n)
    # The borrower pays an extra % 'premium' that goes into the Sink
    retention_premium_percent = 0.10  # 10% of monthly payment goes to Sink
    sink_yield_annual = 0.07          # 7.0% Return on Sink (Asset Portfolio)
    
    # --- Setup ---
    months = loan_term_years * 12
    monthly_rate_loan = loan_rate_annual / 12
    monthly_rate_sink = sink_yield_annual / 12
    
    # Standard Mortgage Calculation (Entropic Baseline)
    standard_monthly_payment = (loan_amount * monthly_rate_loan) / (1 - (1 + monthly_rate_loan)**(-months))
    print(f"Standard Monthly Payment: ${standard_monthly_payment:.2f}")
    
    # Autopoietic Payment Structure
    # Total Payment = Standard Payment * (1 + Retention Premium)
    retention_amount = standard_monthly_payment * retention_premium_percent
    total_monthly_outflow = standard_monthly_payment + retention_amount
    print(f"Autopoietic Monthly Outflow: ${total_monthly_outflow:.2f} (Includes ${retention_amount:.2f} retention)")
    
    # --- Simulation Loop ---
    balance = loan_amount
    sink_value = 0.0
    
    history_balance = []
    history_sink = []
    history_net_worth = []
    
    crossover_month = None
    freedom_month = None # When Sink Value > Loan Balance
    
    for m in range(1, months + 1):
        # 1. Loan Dynamics (Amortization)
        interest_cost = balance * monthly_rate_loan
        principal_pay = standard_monthly_payment - interest_cost
        balance -= principal_pay
        if balance < 0: balance = 0
        
        # 2. Sink Dynamics (Power Algorithm: Compounding)
        # Sink grows by yield + new retention injection
        investment_income = sink_value * monthly_rate_sink
        sink_value += investment_income + retention_amount
        
        # 3. Check Milestones
        # Crossover: When Investment Income > Interest Cost (The Entropic Leak is plugged)
        if crossover_month is None and investment_income > interest_cost:
            crossover_month = m
            
        # Freedom Point: When Sink Value > Remaining Debt (Net Worth positive)
        if freedom_month is None and sink_value > balance:
            freedom_month = m
            
        history_balance.append(balance)
        history_sink.append(sink_value)
        history_net_worth.append(sink_value - balance)
    
    # --- Results ---
    print("\n--- Results ---")
    print(f"Loan Term: {loan_term_years} Years")
    print(f"Final Sink Value: ${sink_value:,.2f}")
    
    if crossover_month:
        print(f"Crossover Point (Yield > Interest): Month {crossover_month} (Year {crossover_month/12:.1f})")
    else:
        print("Crossover not reached.")
        
    if freedom_month:
        print(f"Financial Freedom Point (Sink > Debt): Month {freedom_month} (Year {freedom_month/12:.1f})")
        print(f"  -> At this point, the customer effectively has 0 net debt.")
    else:
        print("Freedom point not reached.")
        
    # --- Plotting ---
    years = np.array(range(months)) / 12
    
    plt.figure(figsize=(10, 6))
    plt.plot(years, history_balance, label='Loan Balance (Liability)', color='red', linestyle='--')
    plt.plot(years, history_sink, label='Sink Value (Asset)', color='green', linewidth=2)
    plt.axhline(y=0, color='black', linewidth=0.5)
    
    if freedom_month:
        plt.axvline(x=freedom_month/12, color='blue', linestyle=':', label='Freedom Point')
        plt.scatter([freedom_month/12], [history_sink[freedom_month-1]], color='blue')
        plt.text(freedom_month/12, history_sink[freedom_month-1] + 20000, '  Net Positive', color='blue')

    plt.title('The Autopoietic Loan: Power Algorithm Simulation')
    plt.xlabel('Years')
    plt.ylabel('Value ($)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.savefig('autopoietic_loan_chart.png')
    print("\nChart saved as 'autopoietic_loan_chart.png'")

if __name__ == "__main__":
    simulate_autopoietic_loan()
