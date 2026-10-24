import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Set the title of the Streamlit app
st.title("SuperKart Supermarket Sales Revenue Prediction")

# Section for online prediction
st.subheader("Online Prediction")

# Collect user input for product sales features
Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.65)
Product_Sugar_Content = st.selectbox('Product Sugar Content', ['Low Sugar', 'Regular', 'No Sugar', 'reg'])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, value=0.07)
Product_Type = st.selectbox('Product Type', ['Frozen Foods', 'Dairy', 'Canned', 'Baking Goods', 'Health and Hygiene', 'Snack Foods', 'Meat', 'Household', 'Hard Drinks', 'Fruits and Vegetables', 'Breads', 'Soft Drinks', 'Breakfast', 'Others', 'Starchy Foods', 'Seafood'])
Product_MRP = st.number_input("Review Score Rating", min_value=0.0, value=147.03)
Store_Id = st.selectbox('Store Id', ['OUT004', 'OUT003', 'OUT001', 'OUT002'])
Store_Size = st.selectbox('Store Size', ['Medium', 'High', 'Small'])
Store_Location_City_Type = st.selectbox('Store Location City Type', ['Tier 2', 'Tier 1', 'Tier 3'])
Store_Type = st.selectbox('Store Type', ['Supermarket Type2', 'Departmental Store', 'Supermarket Type1', 'Food Mart'])
Store_Establishment_Year = st.number_input("Review Score Rating", min_value=0, max_value=2026, step=1, value=2002)

# Convert user input into a DataFrame
input_data = pd.DataFrame([{
    'Product_Sugar_Content': Product_Sugar_Content,
    'Product_Type': Product_Type,
    'Store_Id': Store_Id,
    'Store_Size': Store_Size,
    'Store_Location_City_Type': Store_Location_City_Type,
    'Store_Type': Store_Type,
    'Product_Weight': Product_Weight,
    'Product_Allocated_Area': Product_Allocated_Area,
    'Product_MRP': Product_MRP,
    'Store_Establishment_Year': Store_Establishment_Year
}])

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=input_data.to_dict(orient='records')[0])  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()['Predicted revenue (in dollars)']
        st.success(f"Predicted Sales Revenue (in dollars): {prediction}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader("Upload CSV file for batch prediction", type=["csv"])

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file})  # Send file to Flask API
        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            st.write(predictions)  # Display the predictions
        else:
            st.error("Unable to connect to the prediction API.")
