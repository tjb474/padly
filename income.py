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

    def calculate_income_tax(self):
        # Apply Scottish tax rates if the user is in Scotland
        if self.is_scottish:
            return self.calculate_scottish_tax()
        else:
            return self.calculate_uk_tax()

    def calculate_uk_tax(self):
        taxable_income = max(0, self.annual_income - self.personal_allowance)

        # UK tax bands and rates
        uk_tax_bands = [
            (0, 37700, 0.20),
            (37701, 125140, 0.40),
            (125141, float('inf'), 0.45)
        ]

        total_tax = 0

        for start, end, rate in uk_tax_bands:
            if taxable_income > end:
                tax_at_band = (end - start + 1) * rate  # Calculate tax for the entire band
                total_tax += tax_at_band
            elif start <= taxable_income <= end:
                tax_at_band = (taxable_income - start + 1) * rate  # Calculate tax within the band
                total_tax += tax_at_band
                break  # Break since we've covered the entire taxable income

        return total_tax

    def calculate_scottish_tax(self, taxable_income):
        # Scottish tax bands and rates
        scottish_tax_bands = [
            (0, 2162, 0.19),
            (2163, 13118, 0.20),
            (13119, 31092, 0.21),
            (31093, 125140, 0.42),
            (125141, float('inf'), 0.47)
        ]

        return self.calculate_tax(taxable_income, scottish_tax_bands)

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

        # Calculate income tax
        income_tax = self.calculate_income_tax()

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

# Example usage:
annual_income = 52000
# annual_income = 73548
# annual_income = 72500

bonus = 0
pension_percentage = 5  # Adjust as needed

# Assuming Plan 1 for student loan, adjust plan_type as needed
calculator = IncomeCalculator(annual_income, bonus, pension_percentage=5, plan_type="Plan 1",
                              is_scottish=False, is_blind=False, is_married=False)

tax = calculator.calculate_uk_tax()
print(f"Tax: £{tax:.2f}")

total_deductions, tax, ni, student_loan_deductions, pension_contributions = calculator.calculate_total_deductions()

# ni = calculator.calculate_national_insurance()
# student_loan_deductions = calculator.calculate_student_loan_deductions()
# pension_contributions = calculator.calculate_total_deductions()
net_income = calculator.calculate_net_income()


# Print the results
# print(f"--------")
# print(f"Pension %: {pension_percentage:.2f}")
# print(f"UK Income Tax: £{tax:.2f}")
# print(f"National Insurance Code A: £{ni:.2f}")
# print(f"Student Loan Deductions: £{calculator.calculate_student_loan_deductions():.2f}")
# print(f"Pension Contributions: £{pension_contributions:.2f}")
# print(f"Total Deductions (UK): £{total_deductions:.2f}")
# print(f"Net Income (UK): £{net_income:.2f}")
# print(f"Net Monthly Income (UK): £{net_income / 12:.2f}")


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
