import pandas as pd

class IncomeCalculator:
    def __init__(self, annual_income, personal_allowance = 12570, bonus=0,
                 pension_percentage=0, plan_type="Plan 1", is_scottish=False, is_married=False, is_blind=False):
        self.annual_income = annual_income
        self.bonus = bonus
        self.personal_allowance = personal_allowance
        self.pension_percentage = pension_percentage
        self.plan_type = plan_type
        self.is_scottish = is_scottish
        self.is_married = is_married
        self.is_blind = is_blind

    def calculate_uk_tax(self, income):
        """
        Take a £ value and calculate the tax on it, with logging for each band.
        """
        tax_bands = [
            (0, 12570, 0.0),         # No tax band
            (12571, 50270, 0.20),    # 20% tax band
            (50271, 125140, 0.40),   # 40% tax band
            (125141, None, 0.45)     # 45% tax band
        ]
        
        tax = 0
        taxable_income = income

        for lower, upper, rate in tax_bands:
            if taxable_income > lower:
                if upper is None:
                    taxed_amount = taxable_income - lower
                else:
                    taxed_amount = min(taxable_income, upper) - lower
                tax_from_band = taxed_amount * rate
                tax += tax_from_band
                print(f"Tax from {lower} to {upper if upper is not None else 'infinity'} at {rate*100}%: £{tax_from_band:.2f}")
                if taxable_income <= upper or upper is None:
                    break

        print(f"Total Tax: £{tax:.2f}")
        return tax


    def calculate_national_insurance(self):
        weekly_income = self.annual_income / 52.0

        ni_code_a_bands = [
            (0, 242, 0.0),
            (242, 967, 0.1),
            (967, float('inf'), 0.02)
        ]

        total_ni_contributions = 0

        for start, end, rate in ni_code_a_bands:
            if weekly_income > end:
                total_ni_contributions += (end - start + 1) * rate  # Calculate contributions for the band
            elif start <= weekly_income <= end:
                total_ni_contributions += (weekly_income - start + 1) * rate  # Calculate contributions for the band
                break  # Stop processing further bands

        return total_ni_contributions * 52  # Multiply by the number of weeks in a year

    def calculate_student_loan_deductions(self):
        if self.plan_type == "Plan 1":
            threshold = 22015
            rate = 0.09
        elif self.plan_type == "Plan 2":
            threshold = 27295
            rate = 0.09
        elif self.plan_type == "Plan 4":
            threshold = 27660
            rate = 0.09
        else:
            # Assuming Postgraduate Loan plan
            threshold = 21000
            rate = 0.06

        # Calculate student loan deductions
        if self.annual_income <= threshold:
            return 0
        else:
            return (self.annual_income - threshold) * rate

    def calculate_pension_contributions(self):
        return self.annual_income * (self.pension_percentage / 100)

    def calculate_total_deductions(self, is_married=False, is_blind=False):
        # Calculate pension contributions
        pension_contributions = self.calculate_pension_contributions()

        # Adjusted annual income after deducting pension contributions
        adjusted_annual_income = self.annual_income - pension_contributions

        # Apply Blindness Allowance and Married Rebate (if applicable)
        blindness_allowance = 2870 if self.is_blind else 0
        married_rebate = min(1037.50, max(0, 1037.50 - (adjusted_annual_income - 100000) / 2)) if self.is_married else 0
        
        # Adjusted net income for personal allowance reduction and additional allowances
        adjusted_net_income = adjusted_annual_income - married_rebate - blindness_allowance

        # Calculate income tax based on the adjusted net income
        income_tax = self.calculate_uk_tax(income = adjusted_net_income)

        # Calculate national insurance
        ni_contributions = self.calculate_national_insurance()

        # Calculate student loan deductions
        student_loan_deductions = self.calculate_student_loan_deductions()

        # Calculate total deductions including income tax, national insurance, student loan, and pension contributions
        total_deductions = income_tax + ni_contributions + student_loan_deductions + pension_contributions

        return total_deductions, income_tax, ni_contributions, student_loan_deductions, pension_contributions

    def calculate_net_income(self):
        # Calculate total deductions
        total_deductions, income_tax, ni_contributions, student_loan_deductions, pension_contributions = self.calculate_total_deductions()

        # Calculate net income after deductions
        net_income = self.annual_income - total_deductions

        return net_income

# to do - handle bonus month

annual_income = 73548

bonus = 0
pension_percentage = 5  # Adjust as needed

# Assuming Plan 1 for student loan, adjust plan_type as needed
calculator = IncomeCalculator(annual_income, bonus, pension_percentage=5, plan_type="Plan 1",
                              is_scottish=False, is_blind=False, is_married=False)

total_deductions, tax, ni, student_loan_deductions, pension_contributions = calculator.calculate_total_deductions()

net_income = calculator.calculate_net_income()

# Create a DataFrame for the table
data = {
    'Gross Income': [],
    'Pension Contributions': [],
    'Income Tax': [],
    'NI Contributions': [],
    'Student Loan': [],
    'Net Income': [],
}

data['Gross Income'].append(annual_income)
data['Pension Contributions'].append(pension_contributions)
data['Income Tax'].append(tax)
data['NI Contributions'].append(ni)
data['Student Loan'].append(student_loan_deductions)
data['Net Income'].append(net_income)


# Create the DataFrame
df = pd.DataFrame(data).T
df.columns = ['Annual']
df['Monthly'] = df['Annual'] / 12

# Print the table
print(df)
