from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class MortgageCalculator:
    def __init__(self, principal, annual_interest_rate, years, start_date):
        self.principal = principal
        self.annual_interest_rate = annual_interest_rate
        self.years = years
        self.start_date = datetime.strptime(start_date, "%d-%m-%Y")
        self.monthly_interest_rate = annual_interest_rate / 12 / 100
        self.total_payments = years * 12

    def calculate_monthly_payment(self):
        p = self.principal
        r = self.monthly_interest_rate
        n = self.total_payments
        monthly_payment = p * (r * (1 + r) ** n) / ((1 + r) ** n - 1)
        return monthly_payment

    def generate_amortization_schedule(self):
        monthly_payment = self.calculate_monthly_payment()
        amortization_schedule = []
        
        remaining_balance = self.principal
        current_date = self.start_date
        
        for month in range(1, self.total_payments + 1):
            interest_payment = remaining_balance * self.monthly_interest_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            
            amortization_schedule.append({
                "Date": current_date.strftime("%d-%m-%Y"),
                "Interest Paid": interest_payment,
                "Principal Paid": principal_payment,
                "Remaining Balance": remaining_balance if remaining_balance > 0 else 0
            })
            
            current_date += relativedelta(months=+1)
        
        return pd.DataFrame(amortization_schedule)

    def plot_amortization_schedule(self):
        schedule = self.generate_amortization_schedule()
        
        plt.figure(figsize=(14, 7))
        ax1 = plt.gca()  # Get current Axes instance on the current figure
        
        # Convert data to numpy arrays before plotting
        payments = np.arange(1, len(schedule) + 1)
        remaining_balance = np.array(schedule['Remaining Balance'])
        interest_paid = np.array(schedule['Interest Paid'])
        principal_paid = np.array(schedule['Principal Paid'])
        
        # Plot Remaining Balance on the left y-axis
        ax1.plot(payments, remaining_balance, 'r-', label='Remaining Balance')
        ax1.set_xlabel('Payment Number')
        ax1.set_ylabel('Remaining Balance (£)', color='r')
        
        # Create a twin Axes sharing the xaxis for Interest and Principal Paid
        ax2 = ax1.twinx()
        # Plot Interest Paid and Principal Paid on the right y-axis
        ax2.plot(payments, interest_paid, 'b-', label='Interest Paid')
        ax2.plot(payments, principal_paid, 'g-', label='Principal Paid')
        ax2.set_ylabel('Amount (£)', color='b')
        
        plt.title('Amortization Schedule Over Time')
        # Add legends
        ax1.legend(loc='upper left')
        ax2.legend(loc='upper right')
        
        plt.grid(True)
        plt.tight_layout()
        plt.show()

# Example usage
calculator = MortgageCalculator(principal=500000, annual_interest_rate=5, years=30, start_date="01-03-2024")
amortization_schedule = calculator.generate_amortization_schedule()
calculator.plot_amortization_schedule()

print(amortization_schedule.head(10))
