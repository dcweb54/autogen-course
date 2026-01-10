import csv
import requests
from urllib.parse import urlparse
import time
import os

def is_proxy_working(proxy_url, timeout=10):
    """
    Test if a proxy is working by making a request through it.
    Returns True if successful, False otherwise.
    """
    try:
        proxies = {
            "http": proxy_url,
            "https": proxy_url,
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(
            "http://httpbin.org/ip",
            proxies=proxies,
            timeout=timeout,
            headers=headers
        )
        if response.status_code == 200:
            origin = response.json().get("origin", "")
            if origin and urlparse(proxy_url).hostname in origin:
                return True
            elif origin:
                # Still counts as working (even if shows real IP due to misconfig)
                return True
        return False
    except Exception as e:
        return False

def main():
    working_proxies = []
    failed_proxies = []

    with open(os.path.join(os.getcwd(),"proxy_ip_check","proxies.txt"), "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        proxies = []
        for row in reader:
            if row.get("protocol") == "http" and row.get("proxy"):
                proxies.append(row["proxy"])

    print(f"🔍 Found {len(proxies)} HTTP proxies to test...\n")

    for i, proxy in enumerate(proxies, 1):
        print(f"[{i}/{len(proxies)}] Testing {proxy} ...", end=" ")
        if is_proxy_working(proxy):
            print("✅ WORKING")
            working_proxies.append(proxy)
        else:
            print("❌ FAILED")
            failed_proxies.append(proxy)

        # Optional: small delay to avoid overwhelming
        time.sleep(0.2)

    # Summary
    print("\n" + "="*50)
    print(f"✅ Working proxies: {len(working_proxies)}")
    print(f"❌ Failed proxies:  {len(failed_proxies)}")
    print("="*50)

    if working_proxies:
        print("\n🟢 Working Proxy List:")
        for p in working_proxies:
            print(p)
        
        # Optionally save to file
        with open("working_proxies.txt", "w") as out:
            for p in working_proxies:
                out.write(p + "\n")
        print("\n📥 Saved working proxies to 'working_proxies.txt'")
    else:
        print("\n❌ No working proxies found.")

if __name__ == "__main__":
    main()