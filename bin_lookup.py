import os
import requests
from typing import Any, Dict

def lookup_bin(bin6: str) -> Dict[str, Any]:
    """
    Panggil Bin Info Checker API via RapidAPI.
    """
    rapid_key = os.getenv("RAPIDAPI_KEY")
    rapid_host = os.getenv("RAPIDAPI_HOST")

    if not rapid_key or not rapid_host:
        return {"error": "Missing RAPIDAPI_KEY or RAPIDAPI_HOST in .env"}

    url = f"https://{rapid_host}/info2?bin={bin6}"
    headers = {
        "x-rapidapi-key": rapid_key,
        "x-rapidapi-host": rapid_host
    }

    print("DEBUG Request:", url)
    print("DEBUG Headers:", headers)

    try:
        r = requests.get(url, headers=headers, timeout=20)
        print("DEBUG Status Code:", r.status_code)

        if r.status_code == 200:
            return r.json()

        return {"error": f"RapidAPI error {r.status_code}", "body": r.text}
    except Exception as e:
        return {"error": str(e)}
