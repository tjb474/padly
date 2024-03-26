import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from finance_manager import FinanceManager
from util import *

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Assuming FinanceManager initialization doesn't require parameters,
# or you have predefined parameters to pass.
finance_manager = FinanceManager(config_path="config/config.json",
                                 db_uri="mongodb://localhost:27017/",
                                 db_name="finance_app_db")

@app.route('/add_stream', methods=['POST'])
def add_stream():
    data = request.json
    logging.info(f'Received request to add stream: {data}')
    user_id = data.get('user_id')
    stream_type = data.get('stream_type')

    # Common fields for both income and expense streams
    common_fields = {
        'start_date_str': format_date(data.get('start_date_str'), default=None),
        'end_date_str': format_date(data.get('end_date_str'), default=None),
    }

    try:
        if stream_type == 'income':
            kwargs = {
                **common_fields,
                'annual_income': to_int(data.get('annual_income')),
                'personal_allowance': to_int(data.get('personal_allowance'), 12570),
                'bonus': to_int(data.get('bonus')),
                'pension_percentage': to_int(data.get('pension_percentage')),
                'plan_type': data.get('plan_type', 'Plan 1'),
                'is_scottish': data.get('is_scottish', False),
                'is_married': data.get('is_married', False),
                'is_blind': data.get('is_blind', False),
            }
        elif stream_type == 'expense':
            kwargs = {
                **common_fields,
                'principal': to_int(data.get('principal')),
                'annual_interest_rate': to_float(data.get('annual_interest_rate')),
                'years': to_int(data.get('years')),
            }
        else:
            return jsonify({"error": "Invalid stream type provided."}), 400

        stream_id = finance_manager.add_stream(user_id=user_id, stream_type=stream_type, **kwargs)
        logging.info(f'Stream added successfully: {stream_id}')
        return jsonify({"stream_id": str(stream_id)}), 201

    except Exception as e:
        logging.error(f'Error adding stream: {str(e)}')
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)  # Consider removing debug=True in production
