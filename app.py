from flask import Flask, request, render_template
from income import IncomeCalculator
import pandas as pd
# Make sure to include the IncomeCalculator class definition here as well

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # Extract the form data
    annual_income = int(request.form.get('annual_income', 0))
    bonus = int(request.form.get('bonus', 0))
    pension_percentage = int(request.form.get('pension_percentage', 0))
    plan_type = request.form.get('plan_type', 'Plan 1')
    
    # Instantiate the IncomeCalculator
    calculator = IncomeCalculator(
        annual_income=annual_income,
        bonus=bonus,
        pension_percentage=pension_percentage,
        plan_type=plan_type
    )

    # Use the calculator to get deductions and net income
    total_deductions, tax, ni, student_loan_deductions, pension_contributions = calculator.calculate_total_deductions()
    net_income = calculator.calculate_net_income()

    # Prepare the DataFrame
    data = {
        'Description': ['Gross Income', 'Pension Contributions', 'Income Tax', 'NI Contributions', 'Student Loan', 'Net Income'],
        'Annual': [annual_income, pension_contributions, tax, ni, student_loan_deductions, net_income]
    }
    df = pd.DataFrame(data)
    df['Monthly'] = df['Annual'] / 12

    # Convert DataFrame to HTML
    table_html = df.to_html(index=False)

    # Render a template to display the result, pass the DataFrame HTML to the template
    return render_template('result.html', table_html=table_html)

if __name__ == '__main__':
    app.run(debug=True)
