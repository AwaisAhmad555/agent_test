import requests
import json
from datetime import datetime


def generate_crypto_report():
    # Public internal API endpoint
    url = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing"

    params = {
        "start": 1,
        "limit": 10,
        "sortBy": "market_cap",
        "sortType": "desc",
        "convert": "USD"
    }

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        print("Fetching data...")
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()

        # --- NEW: Save JSON output ---
        with open("crypto_report.json", "w", encoding="utf-8") as jf:
            json.dump(data, jf, indent=4)

        # Navigate the JSON tree carefully
        crypto_list = data.get('data', {}).get('cryptoCurrencyList', [])

        report = []
        report.append(f"--- CRYPTO REPORT ({datetime.now().strftime('%Y-%m-%d')}) ---")
        report.append(f"{'Rank':<5} {'Name':<15} {'Price':<12} {'24h %':<8}")
        report.append("-" * 45)

        for coin in crypto_list:
            rank = coin.get('rank', 'N/A')
            name = coin.get('name', 'Unknown')

            # Safe extraction of nested price data
            quotes = coin.get('quotes', [])
            price_val = quotes[0].get('price') if quotes else None
            change_val = quotes[0].get('percentChange24h') if quotes else None

            # Formatting logic that prevents the "NoneType" error
            p_str = f"${price_val:,.2f}" if price_val is not None else "N/A"
            c_str = f"{change_val:+.2f}%" if change_val is not None else "N/A"

            report.append(f"{rank:<5} {name:<15} {p_str:<12} {c_str:<8}")

        # Final output
        content = "\n".join(report)
        with open("crypto_report.txt", "w") as f:
            f.write(content)

        print("\nSuccess! Preview of report:")
        print(content)
        print("\nFull data also saved to crypto_report.json")

    except Exception as e:
        print(f"Critial Error: {e}")


if __name__ == "__main__":
    generate_crypto_report()