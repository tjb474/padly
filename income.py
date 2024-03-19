import pandas as pd
import json

class IncomeCalculator:
<<<<<<< HEAD
    def __init__(self, config, annual_income, personal_allowance = 12570, bonus=0,
=======
    def __init__(self, config_path, annual_income, start_date_str, end_date_str, personal_allowance = 12570, bonus=0,
>>>>>>> 6d06040... Add FinanceManager class to handle income/expsense streams
                 pension_percentage=0, plan_type="Plan 1", is_scottish=False, is_married=False, is_blind=False):
        self.config = config
        self.annual_income = annual_income
        self.bonus = bonus
        self.personal_allowance = personal_allowance
        self.pension_percentage = pension_percentage
        self.plan_type = plan_type
        self.is_scottish = is_scottish
        self.is_married = is_married
        self.is_blind = is_blind
        self.start_date_str = start_date_str
        self.end_date_str = end_date_str

    def calculate_uk_tax(self, income):
        """
        Take a £ value and calculate the tax on it, with logging for each band.
        """
        tax_bands = self.config['uk_tax_bands']
        tax = 0
        taxable_income = income

        for band in tax_bands:
            lower = band['lower']
            upper = band['upper']
            rate = band['rate']

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
        # Retrieve student loan plans from the configuration
        student_loan_plans = self.config.get('student_loan_plans', {})
        plan_details = student_loan_plans.get(self.plan_type, None)

        if plan_details is None:
            # Handle the case where the plan_type is not found in the configuration
            print(f"Plan type {self.plan_type} not found in configuration.")
            return 0

        threshold = plan_details['threshold']
        rate = plan_details['rate']

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

    def generate_monthly_data(self):
        start_date = datetime.strptime(self.start_date_str, "%d-%m-%Y")
        end_date = datetime.strptime(self.end_date_str, "%d-%m-%Y")

        columns = ['Date', 'Gross Income', 'Pension Contributions', 'Income Tax', 'NI Contributions', 'Student Loan', 'Net Income']
        data = []

        current_date = start_date
        while current_date <= end_date:
            # Reuse self attributes for the calculation
            total_deductions, tax, ni, student_loan_deductions, pension_contributions = self.calculate_total_deductions()
            net_income = self.calculate_net_income()

            formatted_date = current_date.strftime("%d-%m-%Y")
            monthly_data = [formatted_date, self.annual_income / 12, pension_contributions / 12, tax / 12, ni / 12, student_loan_deductions / 12, net_income / 12]
            data.append(monthly_data)

            current_date += relativedelta(months=+1)

        df = pd.DataFrame(data, columns=columns)
        return df

# # to do - handle bonus month

# config_path = 'config/config.json'
# annual_income = 73548
# bonus = 0
# pension_percentage = 5  # Adjust as needed

# calculator = IncomeCalculator(config_path=config_path, annual_income=annual_income, bonus=bonus, pension_percentage=pension_percentage, plan_type="Plan 1",
#                               is_scottish=False, is_blind=False, is_married=False)

# start_date = "01-03-2024"
# end_date = "01-03-2025"

# monthly_income_df = calculator.generate_monthly_data(start_date, end_date)
# print(monthly_income_df)
