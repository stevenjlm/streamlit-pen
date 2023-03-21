import streamlit as st

st.title("Predictive Maintenance Tool")

st.write("Steven Munn, March 20th 2023")

with st.expander("Overview"):
    st.write("Using the Kaggle data-set for \
    [Azure Predictive Maintenance Challenge](https://www.kaggle.com/datasets/arnabbiswas1/microsoft-azure-predictive-maintenance) \
         this project explores ways to model and predict failures for component 2.")

with st.expander("Predictive Models"):
    st.write("See model predictions in the Day Model Predictions or Two Day Model Predictions tabs.")

with st.expander("Visualizations"):
    st.write("Inspect data before a failure in the Equipment Failure Visualizations tab.")
