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
    return "Welcome to the SuperKart Supermarkets Sales Revenue Prediction API"

# Define an endpoint for single property prediction (POST request)
@sales_revenue_predictor_api.post('/v1/predict')
def predict_sales_revenue():
    """
    This function handles POST requests to the '/v1/predict' endpoint.
    It expects a JSON payload containing product sales details and returns
    the predicted sales revenue as a JSON response.
    """
    # Get the JSON data from the request body
    data = request.get_json()

    # Extract relevant features from the JSON data
    sample = {
        'Product_Weight': data['Product_Weight'],
        'Product_Sugar_Content': data['Product_Sugar_Content'],
        'Product_Allocated_Area': data['Product_Allocated_Area'],
        'Product_MRP': data['Product_MRP'],
        'Store_Size': data['Store_Size'],
        'Store_Location_City_Type': data['Store_Location_City_Type'],
        'Store_Type': data['Store_Type'],
        'Product_Id_char': data['Product_Id_char'],
        'Store_Age_Years': data['Store_Age_Years'],
        'Product_Type_Category': data['Product_Type_Category']
    }

    # Convert the extracted data into a Pandas DataFrame
    input_data = pd.DataFrame([sample])

    # Make prediction 
    predicted_sales_revenue = model.predict(input_data)[0]

    # Return the actual sales
    return jsonify({'Sales': predicted_sales_revenue})

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
    output_dict = {str(i): round(pred, 2) for i, pred in enumerate(predicted_sales_revenues)}
    
    # Return the predictions dictionary as a JSON response
    return jsonify(output_dict)

# Run the Flask application in debug mode if this script is executed directly
if __name__ == '__main__':
    sales_revenue_predictor_api.run(debug=True)
