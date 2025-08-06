import os
import requests
import time
from typing import Optional
import pandas as pd
from pandas import DataFrame
from dotenv import load_dotenv

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

    hostname = response["web"]["results"][0]["meta_url"]["hostname"]
    print(hostname)

    time.sleep(1)
    return hostname

def addWebsites(
    df: pd.DataFrame,
    fetch: bool = False,
    batch_size: Optional[int] = None
) -> None:
    if "website" not in df.columns:
        df["website"] = ""

    if fetch:
        mask = df["website"].eq("") & df["name"].ne("")
        empty_idx = df.index[mask]

        if batch_size is not None:
            empty_idx = empty_idx[:batch_size]

        if len(empty_idx):
            df.loc[empty_idx, "website"] = df.loc[empty_idx, "name"].apply(getWebsite)

    df.to_json("withSite.json", orient="records")
def setupJSON() -> None:
    partners = pd.read_json("partners.json", orient="records")
        
    partners = partners.drop(['status', 'sumTopicsCount', 'departmentTopicsCount', 'isPremium'], axis=1)
    addWebsites(partners)

def main():
    #setupJSON()
    withWebsite = pd.read_json("withSite.json", orient="records")

    fasz = 3        
    addWebsites(withWebsite, True, fasz)

if __name__ == "__main__":
    main()   
