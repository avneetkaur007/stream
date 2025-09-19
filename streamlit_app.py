# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score, classification_report

st.set_page_config(page_title="Smart Grid Predictive Maintenance", layout="wide")

st.title("⚡ Smart Grid Predictive Maintenance using AI")

# --- Upload Data ---
st.sidebar.header("smart")
uploaded_file = st.sidebar.file_uploader("smart", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel("smart.xlsx", engine="openpyxl")
    st.write("### Preview of Dataset", df.head())

    # Preprocessing
    X = df.drop(["Timestamp", "Transformer_ID", "Failure_Risk (0-1)"], axis=1)
    y = df["Failure_Risk (0-1)"]

    # Tabs for Regression & Classification
    tab1, tab2 = st.tabs(["📈 Regression Model", "🔍 Classification Model"])

    # ---------------- Regression ----------------
    with tab1:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        regressor = RandomForestRegressor(n_estimators=100, random_state=42)
        regressor.fit(X_train, y_train)
        y_pred = regressor.predict(X_test)

        st.subheader("Model Performance")
        st.write(f"**R² Score:** {r2_score(y_test, y_pred):.2f}")
        st.write(f"**MSE:** {mean_squared_error(y_test, y_pred):.4f}")

        # Plot actual vs predicted
        st.subheader("Actual vs Predicted Risk")
        fig, ax = plt.subplots()
        ax.scatter(y_test, y_pred, alpha=0.7)
        ax.set_xlabel("Actual Risk")
        ax.set_ylabel("Predicted Risk")
        st.pyplot(fig)

        # Feature importance
        st.subheader("Feature Importance")
        importances = regressor.feature_importances_
        fig, ax = plt.subplots()
        ax.barh(X.columns, importances)
        st.pyplot(fig)

    # ---------------- Classification ----------------
    with tab2:
        y_class = np.where(y > 0.5, 1, 0)
        X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_class, test_size=0.2, random_state=42)

        classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        classifier.fit(X_train_c, y_train_c)
        y_pred_c = classifier.predict(X_test_c)

        st.subheader("Model Performance")
        st.write(f"**Accuracy:** {accuracy_score(y_test_c, y_pred_c):.2f}")
        st.text("Classification Report")
        st.text(classification_report(y_test_c, y_pred_c))

        # Feature importance
        st.subheader("Feature Importance")
        importances_c = classifier.feature_importances_
        fig, ax = plt.subplots()
        ax.barh(X.columns, importances_c)
        st.pyplot(fig)

    # ---------------- Prediction Input ----------------
    st.sidebar.header("🔮 Predict New Data")
    load = st.sidebar.slider("Load (%)", 60, 100, 80)
    temp = st.sidebar.slider("Temperature (°C)", 55, 85, 70)
    vib = st.sidebar.slider("Vibration (mm/s)", 1, 5, 2)
    humidity = st.sidebar.slider("Humidity (%)", 30, 70, 45)
    oil = st.sidebar.slider("Oil Quality Index", 70, 100, 90)

    input_data = pd.DataFrame([[load, temp, vib, humidity, oil]],
                              columns=X.columns)

    pred_risk = regressor.predict(input_data)[0]
    st.sidebar.subheader("Predicted Failure Risk")
    st.sidebar.write(f"⚠️ Risk Score: **{pred_risk:.2f}**")

else:
    st.info("👆 Please upload a dataset to begin.")
