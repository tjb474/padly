from flask import Flask, request, jsonify
from income import IncomeCalculator
import json

app = Flask(__name__)

@app.route('/calculate', methods=['POST'])
def calculate_income():
    # Load configuration data
    config_path = 'config/config.json'
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)

    # Extract data from request
    data = request.get_json()
    annual_income = data['annualIncome']
    bonus = data['bonus']
    pension_percentage = data['pensionPercentage']
    plan_type = data['planType']

    # Create an instance of IncomeCalculator with the provided data
    calculator = IncomeCalculator(config=config, annual_income=annual_income, bonus=bonus, 
                                  pension_percentage=pension_percentage, plan_type=plan_type,
                                  is_scottish=False, is_blind=False, is_married=False)
    
    # Perform calculations
    total_deductions, tax, ni, student_loan_deductions, pension_contributions = calculator.calculate_total_deductions()
    net_income = calculator.calculate_net_income()

    # Prepare the response
    response_data = {
        'Gross Income': annual_income,
        'Pension Contributions': pension_contributions,
        'Income Tax': tax,
        'NI Contributions': ni,
        'Student Loan': student_loan_deductions,
        'Net Income': net_income,
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)