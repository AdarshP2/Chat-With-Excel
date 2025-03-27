#ai_forecasting.py

import pandas as pd
import numpy as np
from pmdarima import auto_arima
import streamlit as st

def mean_absolute_percentage_error(y_true, y_pred):
    """Calculate Mean Absolute Percentage Error (MAPE)"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def generate_ai_forecast():
    """Generates AI-based forecast using AutoARIMA and returns the forecasted DataFrame in transposed format."""
    
    # Load the dataset
    data_path = "data\\Data_clean (1).xlsx"
    data_all = pd.read_excel(data_path)

    # ✅ Ensure 'Date' is in datetime format
    data_all['Date'] = pd.to_datetime(data_all['Date'], errors='coerce')

    # ✅ Filter data to include only actual values from 2025 to 2028
    actual_data = data_all[(data_all['Date'].dt.year >= 2025) & (data_all['Date'].dt.year <= 2028)].copy()
    
    # ✅ Set Month-Year Format
    actual_data['Month_Year'] = actual_data['Date'].dt.strftime('%b-%Y')

    # Forecasting Columns
    forecast_cols = [
        "Water", "Electricity and power", "Chemicals", "Third Party Services",
        "Technical Advisory", "Depreciation", "Supplies", "Insurance premium",
        "Rental expenses", "Preventive and Corrective Maintenance", "Tax, Permits and Licenses",
        "IT and Innovation", "Fuel (Gasoline/Diesel)", "Transporation Costs",
        "Office Supplies and Materials", "Professional Fees", "EHS", "Third Party Services.1",
        "Depreciation.1", "Amortization Expense", "Rental expenses.1",
        "Preventive and Corrective Maintenance.1", "Tax, Permits and Licenses.1",
        "Transporation Costs.1", "Office Supplies", "Professional Fees.1",
        "IT and Innovation.1", "Safety", "Insurance premium.1", "Community Relation",
        "Miscellaneous Expenses"
    ]

    constant_cols = ["Salary", "Training"]
    
    # ✅ Generate forecast for 2029
    future_dates = pd.date_range(start='2029-01-01', periods=12, freq='MS')
    
    # Initialize Forecast DataFrame
    forecast_rows = []
    last_row = actual_data.iloc[-1].copy()  # Get last actual data for reference

    mape_results = {}  # Dictionary to store MAPE values

    for col in forecast_cols:
        ts_series = actual_data[col].values
        model = auto_arima(ts_series, seasonal=True, m=12, error_action='ignore', suppress_warnings=True)
        col_forecasts = model.predict(n_periods=12)

        if 'forecast_df' not in locals():
            forecast_df = pd.DataFrame({'Date': future_dates})
            forecast_df['Month_Year'] = forecast_df['Date'].dt.strftime('%b-%Y')

        forecast_df[col] = col_forecasts

        # ✅ Compute MAPE for the column
        historical_values = ts_series[-12:]  # Last 12 months of actual values
        if len(historical_values) == 12:  # Ensure we have enough data
            mape_results[col] = mean_absolute_percentage_error(historical_values, col_forecasts)

    # Keep constant columns the same as last actual value
    for col in constant_cols:
        forecast_df[col] = last_row[col]

    # ✅ Combine actual data (2025-2028) with forecasted data (2029)
    combined_df = pd.concat([actual_data, forecast_df], ignore_index=True)

    # Compute Derived Columns
    combined_df['Var Costs'] = combined_df["Electricity and power"] + combined_df["Chemicals"]

    # Direct Costs Calculation
    combined_df['Direct Costs'] = (
        combined_df['Salary'] + combined_df['Training'] +
        combined_df["Third Party Services"] + combined_df["Technical Advisory"] +
        combined_df["Depreciation"] + combined_df["Supplies"] +
        combined_df["Insurance premium"] + combined_df["Rental expenses"] +
        combined_df["Preventive and Corrective Maintenance"] +
        combined_df["Tax, Permits and Licenses"] + combined_df["IT and Innovation"] +
        combined_df["Fuel (Gasoline/Diesel)"] + combined_df["Transporation Costs"] +
        combined_df["Office Supplies and Materials"] + combined_df["Professional Fees"] +
        combined_df["EHS"]
    )

    combined_df['Cost of Services'] = combined_df['Var Costs'] + combined_df['Direct Costs']
    combined_df['GROSS PROFIT'] = combined_df["Water"] - combined_df['Cost of Services']
    combined_df['GP Margin'] = combined_df['GROSS PROFIT'] / combined_df["Water"]
    combined_df['GENERAL AND ADMINISTRATIVE EXPENSES'] = (
        combined_df["Third Party Services.1"] + combined_df["Depreciation.1"] +
        combined_df["Amortization Expense"] + combined_df["Rental expenses.1"] +
        combined_df["Preventive and Corrective Maintenance.1"] +
        combined_df["Tax, Permits and Licenses.1"] + combined_df["Transporation Costs.1"] +
        combined_df["Office Supplies"] + combined_df["Professional Fees.1"] +
        combined_df["IT and Innovation.1"] + combined_df["Safety"] +
        combined_df["Insurance premium.1"] + combined_df["Community Relation"] +
        combined_df["Miscellaneous Expenses"]
    )
    
    combined_df['NET INCOME'] = combined_df['GROSS PROFIT'] - combined_df['GENERAL AND ADMINISTRATIVE EXPENSES']
    combined_df['NIAT Margin'] = combined_df['NET INCOME'] / combined_df["Water"]
    combined_df['MLD Serviced'] = combined_df["Water"]

    # ✅ Transform data to match the format in the "Upload & Forecast" page
    return transform_to_forecast_layout(combined_df), mape_results

def transform_to_forecast_layout(df):
    """
    Transforms AI forecasted data to match the layout of the Forecasted Data table:
    - Categories as rows
    - Dates as column headers (Month-Year format)
    """

    # ✅ Ensure Date column is formatted correctly
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

    # ✅ Drop the "Month_Year" column before transposing to prevent duplication
    df.drop(columns=["Month_Year"], inplace=True, errors="ignore")

    # ✅ Set "Date" as index and remove before transposing
    df.set_index("Date", inplace=True)

    # ✅ Transpose the data so that categories become rows & months become columns
    df_transposed = df.transpose().reset_index()

    # ✅ Remove the index name
    df_transposed.columns.name = None  

    # ✅ Convert date columns to formatted Month-Year
    df_transposed.columns = [col.strftime('%b-%Y') if isinstance(col, pd.Timestamp) else col for col in df_transposed.columns]

    return df_transposed