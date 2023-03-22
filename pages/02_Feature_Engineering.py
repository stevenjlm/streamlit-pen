import streamlit as st

from constants import APP_DIR
app_dir=APP_DIR

st.title("Feature Engineering")

st.header("Indicators")

st.write("Some signals in the APM dataset are indicators of whether or not something has occurred in the past hour. \
         Such signals can indicate if components were replaced, if the machine failed, or if there was an error code, for example. \
         In this project I use two models, one where I convolve these indicator signals to say whether or not something occurred in the past 24 hours \
         and one where the convolution is over 48 hours.")
st.image(f"{app_dir}/img/conv.png")
