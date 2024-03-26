import json
from bson import ObjectId
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import pandas as pd
# from dotenv import load_dotenv
import os
from income import IncomeCalculator
from mortgage import MortgageCalculator

class FinanceManager:
    def __init__(self, config_path=None, db_uri=None, db_name=None):
        self.config_path = config_path
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.streams_collection = self.db.streams  # Use a 'streams' collection

    def add_stream(self, user_id, stream_type, **kwargs):
        """
        Add a new income or expense stream to MongoDB.

        :param user_id: ID of the user adding the stream.
        :param stream_type: Type of the stream ('income' or 'expense').
        :param kwargs: Additional arguments for the specific calculator.
        :return: The ID of the newly added stream in MongoDB.
        """
        try:
            if stream_type == 'income':
                calculator = IncomeCalculator(config_path=self.config_path, **kwargs)
            elif stream_type == 'expense':
                calculator = MortgageCalculator(**kwargs)
            else:
                raise ValueError("Invalid stream type. Please choose 'income' or 'expense'.")

            # Assuming generate_monthly_data() produces a DataFrame
            df = calculator.generate_monthly_data()
            # Convert DataFrame to JSON string
            data_json = df.to_json(orient='records', date_format='iso')
            
            stream_document = {
                'user_id': user_id,
                'stream_type': stream_type,
                'data': data_json,  # Store the DataFrame as a JSON string
                'kwargs': kwargs  # Store the original parameters for potential future recalculations
            }
            result = self.streams_collection.insert_one(stream_document)
            return result.inserted_id
        except PyMongoError as e:
            print(f"An error occurred: {e}")
            return None

    def remove_stream(self, stream_id):
        """
        Remove an existing stream by its MongoDB ID.

        :param stream_id: The MongoDB ID of the stream to remove.
        """
        try:
            result = self.streams_collection.delete_one({'_id': ObjectId(stream_id)})
            if result.deleted_count == 0:
                raise ValueError("Stream ID not found.")
        except Exception as e:
            print(f"An error occurred while trying to remove the stream: {e}")

    def get_streams_by_user(self, user_id):
        """
        Retrieve all streams associated with a specific user_id and convert them to DataFrames.

        :param user_id: The ID of the user whose streams to retrieve.
        :return: A list of Pandas DataFrames associated with the user_id.
        """
        try:
            streams = self.streams_collection.find({'user_id': user_id})
            dataframes = []

            for stream in streams:
                # Deserialize the JSON string in 'data' back to a DataFrame
                df = pd.read_json(stream['data'], orient='records')
                # Optionally, you can add metadata from the stream document to the DataFrame
                # For example, adding a column for stream_type or including it in some other way
                df['stream_type'] = stream['stream_type']  # Adding stream type as an example
                dataframes.append(df)

            return dataframes
        except PyMongoError as e:
            print(f"An error occurred while retrieving streams: {e}")
            return []

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


# example usage

# load_dotenv()  # Load environment variables from .env file

# db_uri = os.getenv("MONGO_DB_URI")
# db_name = os.getenv("DB_NAME")



# Example configuration and details for adding an income stream
# config_path = 'config/config.json'
# annual_income = 73548
# bonus = 0
# pension_percentage = 5

# # Add an income stream
# stream_id = finance_manager.add_stream(
#     user_id="tom",
#     stream_type='income',
#     config_path=config_path,
#     annual_income=annual_income,
#     bonus=bonus,
#     pension_percentage=pension_percentage,
#     plan_type="Plan 1",
#     is_scottish=False,
#     is_blind=False,
#     is_married=False,
#     start_date_str="01-03-2024",
#     end_date_str="01-03-2025"
# )


# Example details for adding a mortgage (expense) stream
# principal = 300000  # $300,000 mortgage
# interest_rate = 3  # 3% annual interest
# years = 30  # 30-year mortgage

# Add a mortgage (expense) stream
# mortgage_stream_id = finance_manager.add_stream(
#     user_id="tom",
#     stream_type='expense',
#     config_path=config_path,
#     principal=principal,
#     annual_interest_rate=interest_rate,
#     years=years,
#     start_date_str="01-03-2024"
# )

# print(f"Income stream added with ID: {stream_id}")


# example of getting a user's streams
# finance_manager = FinanceManager(config_path="config/config.json",
#                                  db_uri="mongodb://localhost:27017/",
#                                  db_name="finance_app_db")

# user_id = "tom"  # Example user_id
# user_streams = finance_manager.get_streams_by_user(user_id)

# print(f"Streams for user {user_id}:")
# for stream in user_streams:
#     print(stream)
