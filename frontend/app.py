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
Product_Sugar_Content = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar", "reg"])
Product_Allocated_Area = st.number_input("Product Allocated Area", min_value=0.0, value=0.027)
Product_MRP = st.number_input("Product MRP", min_value=0.0, value=117.08)
Store_Size = st.selectbox("Store Size", ["Medium", "High", "Small"])
Store_Location_City_Type = st.selectbox("Store Location City Type", ["Tier 2", "Tier 1", "Tier 3"])
Store_Type = st.selectbox("Store Type", ["Supermarket Type2", "Departmental Store", "Supermarket Type1", "Food Mart"])
Product_Id_char = st.selectbox("Product Id character", ["FD", "NC", "DR"])
Store_Age_Years = st.number_input("Store Age in Years", min_value=0, value=16)
Product_Type_Category = st.selectbox("Product Type Category", ["Non Perishables", "Perishables"])

# Create payload
input_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category
}

# Make prediction when the "Predict" button is clicked
if st.button("Predict", type="primary"):
    response = requests.post(
        f"{BACKEND_URL}/v1/predict", json=input_data
    )  # Send data to Flask API
    if response.status_code == 200:
        prediction = response.json()["Sales"]
        st.success(f"Predicted Product Store Sales Total: {prediction:.2f}")
    else:
        st.error("Unable to connect to the prediction API.")

# Section for batch prediction
st.subheader("Batch Prediction")

# Allow users to upload a CSV file for batch prediction
uploaded_file = st.file_uploader(
    "Upload CSV file for batch prediction", type=["csv"]
)

# Make batch prediction when the "Predict Batch" button is clicked
if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        # Reset file buffer pointer before sending
        uploaded_file.seek(0)
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
        response = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files)

        if response.status_code == 200:
            predictions = response.json()
            st.success("Batch predictions completed!")
            try:
                if isinstance(predictions, list):
                    df = pd.DataFrame(predictions)
                elif isinstance(predictions, dict):
                    # Check if all values are scalars
                    if all(not isinstance(v, (list, dict)) for v in predictions.values()):
                        df = pd.DataFrame([predictions])
                    else:
                        df = pd.DataFrame(predictions)
                else:
                    df = pd.DataFrame({"Result": [predictions]})
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"Unable to display results as a table: {e}")
                st.json(predictions)

            #st.write(predictions)
        else:
            st.error("Unable to connect to the prediction API.")
