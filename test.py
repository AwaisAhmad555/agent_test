import requests
import json
import logging
from datetime import datetime

# UPDATED LOGGING: Now includes Line Number and Function Name
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [Line: %(lineno)d] - %(message)s',
    handlers=[
        logging.FileHandler("app_troubleshooting.log"),
        logging.StreamHandler()
    ]
)


def generate_crypto_report():
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
        logging.info("Starting data fetch from CoinMarketCap...")
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()

        # Save JSON output
        with open("crypto_report.json", "w", encoding="utf-8") as jf:
            json.dump(data, jf, indent=4)

        # --- INTENTIONAL ERROR FOR TESTING ---
        # TO TEST: Uncomment the next two lines.
        # The log will now show the exact line number where 'test_trigger' fails.
        logging.info("Attempting to verify data integrity...")
        test_trigger = data['invalid_key_for_testing']
        # --------------------------------------

        crypto_list = data.get('data', {}).get('cryptoCurrencyList', [])

        report = []
        report.append(f"--- CRYPTO REPORT ({datetime.now().strftime('%Y-%m-%d')}) ---")
        report.append(f"{'Rank':<5} {'Name':<15} {'Price':<12} {'24h %':<8}")
        report.append("-" * 45)

        for coin in crypto_list:
            rank = coin.get('rank', 'N/A')
            name = coin.get('name', 'Unknown')
            quotes = coin.get('quotes', [])
            price_val = quotes[0].get('price') if quotes else None
            change_val = quotes[0].get('percentChange24h') if quotes else None

            p_str = f"${price_val:,.2f}" if price_val is not None else "N/A"
            c_str = f"{change_val:+.2f}%" if change_val is not None else "N/A"
            report.append(f"{rank:<5} {name:<15} {p_str:<12} {c_str:<8}")

        content = "\n".join(report)
        with open("crypto_report.txt", "w") as f:
            f.write(content)

        logging.info("Report and JSON generated successfully.")

    except KeyError as error:
        # logging.exception automatically adds the line number and traceback
        logging.exception(f"INTENTIONAL TEST ERROR: Key access failed. key : {error}")
    except Exception:
        logging.exception("CRITICAL: An unexpected error occurred.")


if __name__ == "__main__":
    generate_crypto_report()
