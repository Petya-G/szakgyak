import streamlit as st
import pandas as pd

df = pd.read_json("partners.json", orient="records")

st.title("JSON Table Explorer")
st.dataframe(df)              # interactive table
