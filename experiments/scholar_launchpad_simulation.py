import numpy as np
import matplotlib.pyplot as plt

def simulate_scholar_launchpad():
    """
    Simulates the 'Scholar's Launchpad' Autopoietic Loan.
    - Loan is a drawdown facility (School fees paid annually).
    - Parents pay monthly installments to service debt + build Sink.
    - Goal: Debt is cleared by Year 12, and Child receives the Sink.
    """
    print("--- LJPW 'Scholar's Launchpad' Simulation ---")
    
    # --- Parameters ---
    years = 12
    initial_annual_fee = 15000.0   # Year 1 School Fees
    fee_inflation = 0.05           # 5% annual increase in fees
    
    loan_interest_rate = 0.08      # 8.0% Interest
    sink_yield_rate = 0.07         # 7.0% Investment Return
    
    # The Parents' Commitment
    # They pay a fixed monthly amount that covers the growing loan + the sink
    # We estimate a "levelized" payment needed to clear the debt, then add the premium
    base_monthly_payment = 1800.0  # Service debt + principal
    retention_premium = 250.0      # The "Gift" contribution (1/n)
    
    total_monthly_outflow = base_monthly_payment + retention_premium
    print(f"Monthly Payment: ${total_monthly_outflow:.2f} (Debt: ${base_monthly_payment}, Sink: ${retention_premium})")
    
    # --- Setup ---
    months = years * 12
    monthly_loan_rate = loan_interest_rate / 12
    monthly_sink_rate = sink_yield_rate / 12
    
    loan_balance = 0.0
    sink_value = 0.0
    total_fees_paid = 0.0
    
    history_loan = []
    history_sink = []
    history_fees = [] # Cumulative fees paid by bank
    
    # --- Simulation Loop ---
    for m in range(1, months + 1):
        year_current = (m - 1) // 12 + 1
        
        # 1. Annual Fee Drawdown (Start of each year - Month 1, 13, 25...)
        if (m - 1) % 12 == 0:
            current_fee = initial_annual_fee * ((1 + fee_inflation) ** (year_current - 1))
            loan_balance += current_fee
            total_fees_paid += current_fee
            # print(f"Year {year_current} Start: Paid School Fee ${current_fee:,.2f}")
            
        # 2. Loan Dynamics
        interest_charge = loan_balance * monthly_loan_rate
        # Principal pay is the remainder of the base payment
        principal_pay = base_monthly_payment - interest_charge
        
        # If loan is fully paid, redirect base payment to Sink? 
        # For this sim, we'll stop charging interest but keep logic simple.
        loan_balance -= principal_pay
        if loan_balance < 0: 
            # If debt is cleared early, the extra goes to Sink! (Autopoietic Bonus)
            sink_value += abs(loan_balance)
            loan_balance = 0
            
        # 3. Sink Dynamics (Power Algorithm)
        investment_income = sink_value * monthly_sink_rate
        sink_value += investment_income + retention_premium
        
        history_loan.append(loan_balance)
        history_sink.append(sink_value)
        history_fees.append(total_fees_paid)

    # --- Results ---
    print("\n--- Graduation Day (End of Year 12) ---")
    print(f"Total School Fees Paid: ${total_fees_paid:,.2f}")
    print(f"Remaining Debt: ${loan_balance:,.2f}")
    print(f"Student's Launchpad Fund (Sink): ${sink_value:,.2f}")
    
    net_position = sink_value - loan_balance
    print(f"Net Family Asset: ${net_position:,.2f}")
    
    # --- Plotting ---
    time_axis = np.array(range(months)) / 12
    
    plt.figure(figsize=(10, 6))
    plt.plot(time_axis, history_fees, label='Cumulative Fees Paid (Value Received)', color='gray', linestyle=':', alpha=0.6)
    plt.plot(time_axis, history_loan, label='Loan Balance', color='red')
    plt.plot(time_axis, history_sink, label='Student Launchpad Fund', color='green', linewidth=2)
    
    plt.title("The 'Scholar's Launchpad': Autopoietic Education Finance")
    plt.xlabel('Years (Grade 1-12)')
    plt.ylabel('Value ($)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Annotate the final result
    plt.scatter([12], [sink_value], color='green', zorder=5)
    plt.text(12.2, sink_value, f'${sink_value/1000:.1f}k Gift', color='green', fontweight='bold')
    
    plt.savefig('scholar_launchpad_chart.png')
    print("\nChart saved as 'scholar_launchpad_chart.png'")

if __name__ == "__main__":
    simulate_scholar_launchpad()
