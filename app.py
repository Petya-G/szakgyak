import streamlit as st
import pandas as pd

def main():
    df = pd.read_json("withSite.json", orient="records") 
    _ = st.title("BME AUT Internship partners")

    filtered = df.copy()
    for col in filtered.select_dtypes(include=['object']).columns:
        val = st.text_input(f"Search {col}")
        if val:
            filtered = filtered[filtered[col].str.contains(val, case=False, na=False)]

    def make_clickable(url: str) -> str:
        if not url:
            return ""
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        return f'<a href="{url}" target="_blank">{url}</a>'

    st.write(filtered.to_html(escape=False, formatters={"website": make_clickable}), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
