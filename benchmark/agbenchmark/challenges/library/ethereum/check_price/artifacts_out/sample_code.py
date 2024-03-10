import requests

def get_ethereum_price(retries=3, delay_seconds=1) -> float:
    for i in range(retries):
        url = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data["ethereum"]["usd"]

        if i < retries - 1:
            print(f"Failed to fetch data. Retrying in {delay_seconds} seconds... (Attempt {i+1}/{retries})")
            time.sleep(delay_seconds)
    
    raise Exception(f"Failed to fetch data after {retries} retries")
