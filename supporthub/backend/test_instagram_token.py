"""
supporthub/backend/test_instagram_token.py

Temporary standalone diagnostic script to verify Meta Instagram User Access Tokens (IGAA...).
Uses https://graph.instagram.com for Instagram API with Instagram Login flow.
Strictly redacts tokens and sensitive secrets.
"""

import os
import sys
import json
import httpx

GRAPH_API_HOST = "https://graph.instagram.com"
GRAPH_API_VERSION = "v19.0"

def redact_val(val: str | None) -> str:
    if not val:
        return "NONE"
    if len(val) <= 8:
        return "****"
    return f"{val[:4]}...{val[-4:]}"

def main():
    print("==================================================")
    print("       INSTAGRAM ACCESS TOKEN DIAGNOSTIC TEST     ")
    print("==================================================")
    
    token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    
    # Fallback to .env file if env var not set directly in shell
    if not token and os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("INSTAGRAM_ACCESS_TOKEN="):
                    token = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break

    if not token:
        print("\n❌ RESULT: FAILURE - INSTAGRAM_ACCESS_TOKEN is missing or empty.")
        print("Please export INSTAGRAM_ACCESS_TOKEN or set it in supporthub/backend/.env")
        sys.exit(1)

    print(f"\n[Environment Check]")
    print(f"- INSTAGRAM_ACCESS_TOKEN Found: YES")
    print(f"- Redacted Token Preview: {redact_val(token)}")
    print(f"- HTTP Client: httpx")

    headers = {
        "Authorization": f"Bearer {token}",
    }

    # Meta Instagram Graph API Endpoint for Instagram Login flow
    me_url = f"{GRAPH_API_HOST}/{GRAPH_API_VERSION}/me"
    params = {
        "fields": "id,username,name,account_type"
    }

    print(f"\n[API Request Info]")
    print(f"- Host: {GRAPH_API_HOST}")
    print(f"- Version: {GRAPH_API_VERSION}")
    print(f"- Method: GET")
    print(f"- Target Endpoint: {me_url}")

    print("\nExecuting HTTP request to Instagram Graph API...")
    
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(me_url, headers=headers, params=params)
            
        status_code = response.status_code
        print(f"\n[HTTP Response]")
        print(f"- Status Code: {status_code}")

        try:
            data = response.json()
        except Exception:
            data = {"raw_text": response.text}

        if status_code in (200, 201):
            print("\n==================================================")
            print("  ✅ SUCCESS: Instagram Access Token is VALID")
            print("==================================================")
            
            sanitized = {
                "id": data.get("id"),
                "username": data.get("username"),
                "name": data.get("name"),
                "account_type": data.get("account_type")
            }
            print("\n[Account Information Returned by Instagram API]")
            print(json.dumps(sanitized, indent=2))

        else:
            print("\n==================================================")
            print("  ❌ FAILURE: Instagram API Returned Error")
            print("==================================================")
            error_obj = data.get("error", {})
            err_msg = error_obj.get("message", "Unknown error")
            err_type = error_obj.get("type", "Unknown type")
            err_code = error_obj.get("code", "Unknown code")
            err_subcode = error_obj.get("error_subcode", "None")

            # Redact token if echoed by API error message
            if token in err_msg:
                err_msg = err_msg.replace(token, "[REDACTED_TOKEN]")

            print(f"- Error Message: {err_msg}")
            print(f"- Error Type: {err_type}")
            print(f"- Error Code: {err_code}")
            print(f"- Error Subcode: {err_subcode}")

    except Exception as exc:
        print("\n==================================================")
        print("  ❌ FAILURE: HTTP Transport / Network Exception")
        print("==================================================")
        print(f"Details: {exc}")

if __name__ == "__main__":
    main()
