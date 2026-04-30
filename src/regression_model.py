import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression


@st.cache_resource
def train_regression_model(df: pd.DataFrame) -> LinearRegression:
    X = df[["fov", "table_position"]]
    y = df["arrow_1"]

    model = LinearRegression()
    model.fit(X, y)
    return model
