import streamlit as st
import s3fs
import os
from io import StringIO
import pandas as pd

st.write("Note: These reports are not meant to be standalone.")

st.write('[Exploration and Data Discovery](http://marching-penguin-reports.s3-website-us-west-1.amazonaws.com/explore.html)')
st.write('[24h Model Construction Notes](http://marching-penguin-reports.s3-website-us-west-1.amazonaws.com)')
st.write('[Github Repo for Models](https://github.com/stevenjlm/marching-penguin)')
st.write('[Github Repo for front-end](https://github.com/stevenjlm/streamlit-pen)')
