import streamlit as st

from constants import APP_DIR
app_dir=APP_DIR

st.title("Architecture")

st.markdown("""
The project consists of three components:
 1. The local environment where the code is written and data is parsed.
 2. Sagemaker where the I load training data and train the ML models.
 3. An EC2 instance hosting the streamlit application that serves as the front-end.
""")
st.image(f"{app_dir}/img/arch.png")
