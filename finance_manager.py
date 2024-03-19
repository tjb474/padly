import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from income import IncomeCalculator
from mortgage import MortgageCalculator

class FinanceManager:
    def __init__(self):
        # Streams will be stored as a dictionary with unique IDs as keysfinancew
        self.streams = {}
        self.next_id = 1  # Incremental ID to keep track of the next stream ID

    def add_stream(self, stream_type, config_path, **kwargs):
        """
        Add a new income or expense stream.

        :param stream_type: A string indicating the type of stream ('income' or 'expense').
        :param config: Configuration data required for the stream calculator.
        :param kwargs: Additional arguments required for the specific calculator.
        :return: The ID of the newly added stream.
        """
        if stream_type == 'income':
            calculator = IncomeCalculator(config_path=config_path, **kwargs)
        elif stream_type == 'expense':
            calculator = MortgageCalculator(**kwargs)
        else:
            raise ValueError("Invalid stream type. Please choose 'income' or 'expense'.")

        data = calculator.generate_monthly_data()

        # Add the calculator and data stream to the streams dictionary
        stream_id = self.next_id
        self.streams[stream_id] = {'calculator': calculator, 'data': data}
        self.next_id += 1

        return stream_id

    def remove_stream(self, stream_id):
        """
        Remove an existing stream by its ID.

        :param stream_id: The ID of the stream to remove.
        """
        if stream_id in self.streams:
            del self.streams[stream_id]
        else:
            raise ValueError("Stream ID not found.")

    def generate_monthly_statement(self, start_date_str, end_date_str):
        """
        Generate a monthly statement of all income and expense streams.

        :param start_date_str: The start date of the statement period.
        :param end_date_str: The end date of the statement period.
        :return: A DataFrame containing the monthly statement.
        """
        combined_data_frames = [stream_info['data'] for stream_info in self.streams.values()]

        if combined_data_frames:
            # placeholder for joining the streams together
            return combined_df
        else:
            # Return an empty DataFrame or handle the case where there are no streams
            return pd.DataFrame()


finance_manager = FinanceManager()

# Example configuration and details for adding an income stream
config_path = 'config/config.json'
annual_income = 73548
bonus = 0
pension_percentage = 5

# Add an income stream
stream_id = finance_manager.add_stream(
    stream_type='income',
    config_path=config_path,
    annual_income=annual_income,
    bonus=bonus,
    pension_percentage=pension_percentage,
    plan_type="Plan 1",
    is_scottish=False,
    is_blind=False,
    is_married=False,
    start_date_str="01-03-2024",
    end_date_str="01-03-2025"
)


# Example details for adding a mortgage (expense) stream
principal = 300000  # $300,000 mortgage
interest_rate = 3  # 3% annual interest
years = 30  # 30-year mortgage

# Add a mortgage (expense) stream
mortgage_stream_id = finance_manager.add_stream(
    stream_type='expense',
    config_path=config_path,
    principal=principal,
    annual_interest_rate=interest_rate,
    years=years,
    start_date_str="01-03-2024"
)

print(f"Income stream added with ID: {stream_id}")

print(finance_manager.streams)
