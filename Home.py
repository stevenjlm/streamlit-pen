import streamlit as st

st.title("Azure Predictive Maintenance Challenge")

st.write("Steven Munn, Feb 11th 2023")

with st.expander("Overview"):
    st.write("Using the kaggle data-set for \
    [Azure Predictive Maintenance Challenge](https://www.kaggle.com/datasets/arnabbiswas1/microsoft-azure-predictive-maintenance) \
         this project explores ways to model and predict failures for component 2.")

with st.expander("Predicitve Models"):
    st.write("See model predicitions in the Day Model Predictions or Two Day Model Predictions tabs.")

with st.expander("Visualizations"):
    st.write("Inspect data before a failure in the Equipment Failure Visualizations tab.")
