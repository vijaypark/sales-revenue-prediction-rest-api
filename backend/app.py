# Import necessary libraries
import numpy as np
import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize the Flask application
sales_revenue_predictor_api = Flask("Product Sales Revenue Predictor")

# Load the trained machine learning model
model = joblib.load("sales_revenue_prediction_model_v1_0.joblib")

# Define a route for the home page (GET request)
@sales_revenue_predictor_api.get('/')
def home():
    """
    This function handles GET requests to the root URL ('/') of the API.
    It returns a simple welcome message.
    """
    return "Welcome to the SuperKart Supermarkets Sales Revenue Prediction API!"

# Define an endpoint for single property prediction (POST request)
@sales_revenue_predictor_api.post('/v1/predict')
def predict_sales_revenue():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing product sales details and returns
    the predicted sales revenue as a JSON response.
    """
    # Get the JSON data from the request body
    property_data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': property_data['Product_Weight'],
        'Product_Allocated_Area': property_data['Product_Allocated_Area'],
        'Product_MRP': property_data['Product_MRP'],
        'Store_Establishment_Year': property_data['Store_Establishment_Year'],
        'Product_Sugar_Content': property_data['Product_Sugar_Content'],
        'Product_Type': property_data['Product_Type'],
        'Store_Id': property_data['Store_Id'],
        'Store_Size': property_data['Store_Size'],
        'Store_Location_City_Type': property_data['Store_Location_City_Type'],
        'Store_Type': property_data['Store_Type']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction (get log_price)
    predicted_sales_revenue = model.predict(input_data)[0]

    # Return the actual price
    return jsonify({'Predicted revenue (in dollars)': predicted_sales_revenue})

# Define an endpoint for batch prediction (POST request)
@sales_revenue_predictor_api.post('/v1/predictbatch')
def predict_sales_revenue_batch():
    """
    This function handles POST requests to the '/v1/predictbatch' endpoint.
    It expects a CSV file containing product sales details for multiple product sales
    and returns the predicted sales revenue as a dictionary in the JSON response.
    """
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the CSV file into a Pandas DataFrame
    input_data = pd.read_csv(file)

    # Make predictions for all properties in the DataFrame (get log_prices)
    predicted_sales_revenues = model.predict(input_data).tolist()

    # Create a dictionary of predictions with product IDs as keys
    product_ids = input_data['id'].tolist()  # Assuming 'id' is the property ID column
    output_dict = dict(zip(product_ids, predicted_sales_revenues))  # Use actual sales

    # Return the predictions dictionary as a JSON response
    return output_dict

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    sales_revenue_predictor_api.run(debug=True)