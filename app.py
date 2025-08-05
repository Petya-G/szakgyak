import streamlit as st
import pandas as pd

testing = true

df = pd.read_json("partners.json", orient="records")
if(testing):
    df = df.head(10)
    
df = df.drop(['status', 'sumTopicsCount', 'departmentTopicsCount', 'isPremium'], axis=1)
df.to_json("columnsRemoved.json", orient="records")

_ = st.title("BME AUT Internship partners")

for col in df.select_dtypes(include=['object']).columns:
    search = st.text_input(f"Search {col}")
    if search:
        df = df[df[col].str.contains(search, case=False, na=False)]

_ = st.dataframe(df)
