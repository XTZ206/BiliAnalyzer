import json
from pathlib import Path
from typing import Optional
from bilibili_api import Credential

def login_from_cookies(sessdata: Optional[str] = None, bili_jct: Optional[str] = None) -> Credential:
    #Create a Credential object from cookies
    if not sessdata or not bili_jct:
        raise ValueError("sessdata and bili_jct are required")
    return Credential(sessdata=sessdata, bili_jct=bili_jct)

def login_from_file(filepath: Path) -> Credential:
    #Load authentication information from a file
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return login_from_cookies(
            sessdata=data.get("sessdata"),
            bili_jct=data.get("bili_jct")
        )
    except Exception as e:
        print(f"Failed to load credentials from {filepath}: {e}")
        return None

def login_from_stored(fake: bool = False) -> Credential:
    #Load authentication information from stored file or create fake credentials
    if fake:
        return Credential(sessdata="", bili_jct="", buvid3="")
    try:
        return login_from_file(Path("credential.json"))
    except Exception:
        print("Warning: No valid credentials found, using fake credentials (limited access)")
        return Credential(sessdata="", bili_jct="", buvid3="")

def check() -> str:
    #Check authentication status
    try:
        credential = login_from_stored()
        if credential.sessdata and credential.bili_jct:
            return "Authenticated"
        else:
            return "Not Authenticated"
    except Exception:
        return "Not Authenticated"

def logout() -> None:
    #Clear authentication information
    try:
        Path("credential.json").unlink()
        print("Credentials deleted")
    except FileNotFoundError:
        print("No credentials found")