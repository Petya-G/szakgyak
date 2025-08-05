import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
import requests
import time

_ = load_dotenv()
api_key = os.getenv("API_KEY")
testing = True

def getWebsite(name: str) -> str:
    response = requests.get(
      "https://api.search.brave.com/res/v1/web/search",
      headers={
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "x-subscription-token": api_key
      },
      params={
        "q": name,
        "country": "ALL",
        "search_lang": "hu",
        "count": "1",
        "safesearch": "off",
        "spellcheck": "false",
        "result_filter": "web"
      },
    ).json()

    print(response["web"]["results"][0]["meta_url"]["hostname"])

    hostname = response["web"]["results"][0]["meta_url"]["hostname"]

    time.sleep(1)
    return hostname

df = pd.read_json("partners.json", orient="records")
if(testing):
    df = df.head(10)
    
df = df.drop(['status', 'sumTopicsCount', 'departmentTopicsCount', 'isPremium'], axis=1)

if "website" not in df.columns:
    df["website"] = df["name"].apply(getWebsite)

_ = st.title("BME AUT Internship partners")

filtered = df.copy()
for col in filtered.select_dtypes(include=['object']).columns:
    val = st.text_input(f"Search {col}")
    if val:
        filtered = filtered[filtered[col].str.contains(val, case=False, na=False)]

def make_clickable(url: str) -> str:
    if url:
        return f'<a href="{url}" target="_blank">{url}</a>'
    return ""

st.write(filtered.to_html(escape=False, formatters={"website": make_clickable}), unsafe_allow_html=True)
