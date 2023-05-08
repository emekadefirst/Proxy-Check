import requests

MAX_RETRIES = 3  # Maximum number of times to retry a failed proxy

with open("valid_proxies.csv", "r") as f:
    proxies = f.read().split("\n")

# Remove empty lines from the proxies list
proxies = [p for p in proxies if p.strip()]

sites_to_check = [
    "http://ipinfo.io/json",
    "http://httpbin.org/ip",
    "https://www.google.com",
]

for proxy in proxies:
    success = False
    num_retries = 0
    
    while not success and num_retries < MAX_RETRIES:
        try:
            print(f"USING THE PROXY: {proxy}")
            res = requests.get(sites_to_check[0], proxies={"http": proxy, "https": proxy})
            res.raise_for_status()  # Raise an error if the response is not OK
            success = True
        except Exception as e:
            print(f"Proxy {proxy} failed: {e}")
            num_retries += 1
            continue
        
        for site in sites_to_check[1:]:
            try:
                res = requests.get(site, proxies={"http": proxy, "https": proxy})
                res.raise_for_status()  # Raise an error if the response is not OK
            except Exception as e:
                print(f"Proxy {proxy} failed: {e}")
                success = False
                break
                
        if not success:
            num_retries += 1
            
    if not success:
        print(f"Proxy {proxy} failed after {MAX_RETRIES} retries")
    else:
        print(f"Proxy {proxy} succeeded!")
    
    # Close the requests to avoid memory leaks
    res.close()
