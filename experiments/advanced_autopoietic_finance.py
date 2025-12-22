import numpy as np
import matplotlib.pyplot as plt

class AutopoieticProduct:
    def __init__(self, name, loan_amount, base_rate, term_years, retention_premium, sink_allocation_strategy='balanced'):
        self.name = name
        self.initial_loan = loan_amount
        self.base_rate = base_rate
        self.term_months = term_years * 12
        self.retention_premium = retention_premium # Monthly $ amount
        self.strategy = sink_allocation_strategy
        
    def get_market_return(self):
        """
        Simulates monthly market return based on strategy volatility.
        Justice Dimension: Truth/Risk.
        """
        if self.strategy == 'conservative':
            # Mean 4% annual, 3% volatility
            mu = 0.04 / 12
            sigma = 0.03 / np.sqrt(12)
        elif self.strategy == 'aggressive':
            # Mean 9% annual, 18% volatility
            mu = 0.09 / 12
            sigma = 0.18 / np.sqrt(12)
        else: # Balanced
            # Mean 7% annual, 10% volatility
            mu = 0.07 / 12
            sigma = 0.10 / np.sqrt(12)
            
        return np.random.normal(mu, sigma)

    def calculate_dynamic_rate(self, current_balance, current_sink):
        """
        Wisdom Dimension: Dynamic Pricing.
        As the Sink (Collateral) grows, the Net Risk drops.
        The bank rewards this by lowering the rate.
        Formula: Rate = Base - (Collateral_Ratio * Discount_Factor)
        """
        if current_balance <= 0: return 0.0
        
        collateral_ratio = current_sink / current_balance
        # Max discount capped at 1.5% reduction
        discount = min(0.015, collateral_ratio * 0.02) 
        
        effective_rate = max(0.03, self.base_rate - discount) # Floor at 3%
        return effective_rate

    def run_monte_carlo(self, simulations=100):
        print(f"Running {simulations} simulations for {self.name}...")
        
        results_final_net_worth = []
        freedom_months = []
        
        # Calculate standard payment (fixed) for baseline
        r_monthly = self.base_rate / 12
        standard_payment = (self.initial_loan * r_monthly) / (1 - (1 + r_monthly)**(-self.term_months))
        
        all_sink_trajectories = []
        all_loan_trajectories = []
        
        for sim in range(simulations):
            balance = self.initial_loan
            sink = 0.0
            
            sim_sink_history = []
            sim_loan_history = []
            freedom_hit = False
            
            for m in range(self.term_months):
                # 1. Wisdom: Adjust Rate based on Real-time Collateral
                current_annual_rate = self.calculate_dynamic_rate(balance, sink)
                monthly_interest = balance * (current_annual_rate / 12)
                
                # 2. Loan Payment
                principal_pay = standard_payment - monthly_interest
                balance -= principal_pay
                if balance < 0: balance = 0
                
                # 3. Justice: Market Volatility
                market_return = self.get_market_return()
                sink_growth = sink * market_return
                sink += sink_growth + self.retention_premium
                
                sim_sink_history.append(sink)
                sim_loan_history.append(balance)
                
                # Check Freedom Point
                if not freedom_hit and sink > balance:
                    freedom_months.append(m)
                    freedom_hit = True
            
            results_final_net_worth.append(sink - balance)
            all_sink_trajectories.append(sim_sink_history)
            all_loan_trajectories.append(sim_loan_history)

        return {
            'net_worth': results_final_net_worth,
            'freedom_months': freedom_months,
            'sinks': np.array(all_sink_trajectories),
            'loans': np.array(all_loan_trajectories)
        }

def visualize_monte_carlo(results, title):
    sinks = results['sinks']
    loans = results['loans']
    months = sinks.shape[1]
    years = np.arange(months) / 12
    
    plt.figure(figsize=(12, 7))
    
    # Plot the Cone of Possibility for Sinks (5th to 95th percentile)
    sink_p05 = np.percentile(sinks, 5, axis=0)
    sink_p50 = np.percentile(sinks, 50, axis=0)
    sink_p95 = np.percentile(sinks, 95, axis=0)
    
    plt.fill_between(years, sink_p05, sink_p95, color='green', alpha=0.2, label='Sink Volatility (90% Conf.)')
    plt.plot(years, sink_p50, color='green', linewidth=2, label='Median Sink Performance')
    
    # Plot Median Loan Payoff
    loan_median = np.median(loans, axis=0)
    plt.plot(years, loan_median, color='red', linestyle='--', label='Loan Balance (Dynamic Rate)')
    
    plt.title(f'Monte Carlo Analysis: {title} (Dynamic Rate + Volatility)')
    plt.xlabel('Years')
    plt.ylabel('Value ($)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    filename = f"advanced_simulation_{title.replace(' ', '_').lower()}.png"
    plt.savefig(filename)
    print(f"Chart saved as {filename}")

if __name__ == "__main__":
    # Scenario 1: The Mortgage "Freedom" Product
    # $500k Loan, 6% Base Rate, $300/mo Retention
    mortgage_sim = AutopoieticProduct("Autopoietic Mortgage", 500000, 0.06, 30, 300, 'balanced')
    results = mortgage_sim.run_monte_carlo(200)
    
    # Analysis
    success_rate = len(results['freedom_months']) / 200 * 100
    median_nw = np.median(results['net_worth'])
    
    print("\n--- Advanced Simulation Results (Mortgage) ---")
    print(f"Success Rate (Sink > Debt before term end): {success_rate:.1f}%")
    print(f"Median Final Net Worth: ${median_nw:,.2f}")
    if results['freedom_months']:
        avg_freedom_year = np.mean(results['freedom_months']) / 12
        print(f"Average Freedom Year: {avg_freedom_year:.1f}")
        
    visualize_monte_carlo(results, "Autopoietic Mortgage")
