import logging
from flask import Flask, request, jsonify
from finance_manager import FinanceManager

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Assuming FinanceManager initialization doesn't require parameters,
# or you have predefined parameters to pass.
finance_manager = FinanceManager(db_uri="mongodb://localhost:27017/", db_name="finance_app_db")

@app.route('/add_stream', methods=['POST'])
def add_stream():
    data = request.json
    logging.info(f'Received request to add stream: {data}')
    user_id = data.get('user_id')
    stream_type = data.get('stream_type')

    # Convert start_date_str and end_date_str from "yyyy-mm-dd" to "dd-mm-yyyy"
    if 'start_date_str' in data:
        start_date = datetime.strptime(data['start_date_str'], "%Y-%m-%d").strftime("%d-%m-%Y")
        kwargs['start_date_str'] = start_date
    if 'end_date_str' in data:
        end_date = datetime.strptime(data['end_date_str'], "%Y-%m-%d").strftime("%d-%m-%Y")
        kwargs['end_date_str'] = end_date

    if stream_type == 'income':
        kwargs = {
            'config_path': data.get('config_path'),  # Ensure this path is accessible by your Flask app
            'annual_income': data.get('annual_income'),
            'start_date_str': data.get('start_date_str'),
            'end_date_str': data.get('end_date_str'),
            'personal_allowance': data.get('personal_allowance', 12570),  # Default to 12570 if not provided
            'bonus': data.get('bonus', 0),  # Default to 0 if not provided
            'pension_percentage': data.get('pension_percentage', 0),  # Default to 0 if not provided
            'plan_type': data.get('plan_type', 'Plan 1'),  # Default to 'Plan 1' if not provided
            'is_scottish': data.get('is_scottish', False),  # Default to False if not provided
            'is_married': data.get('is_married', False),  # Default to False if not provided
            'is_blind': data.get('is_blind', False),  # Default to False if not provided
        }
    elif stream_type == 'expense':
        # Initialize with your default values or ensure they're provided in the request
        kwargs = {
            'principal': data.get('principal'),
            'annual_interest_rate': data.get('annual_interest_rate'),
            'years': data.get('years'),
            'start_date_str': data.get('start_date_str'),
        }
    else:
        return jsonify({"error": "Invalid stream type provided."}), 400

    try:
        # Attempt to add the stream and return the ID
        stream_id = finance_manager.add_stream(user_id=user_id, stream_type=stream_type, **kwargs)
        logging.info(f'Stream added successfully: {stream_id}')
        return jsonify({"stream_id": str(stream_id)}), 201
    except Exception as e:
        logging.error(f'Error adding stream: {str(e)}')
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)  # Consider removing debug=True in production
