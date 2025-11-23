import requests

API_KEY = "c2e51e9e4835d1afc4ce042b"
BASE_CURRENCY = "USD"
SUPPORTED_CURRENCIES = {
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
    "JPY": "Japanese Yen",
    "PHP": "Philippine Peso",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CNY": "Chinese Yuan",
    "HKD": "Hong Kong Dollar",
    "SGD": "Singapore Dollar"
}


def fetch_exchange_rates() -> dict:
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{BASE_CURRENCY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data["result"] != "success":
            raise Exception("Failed to fetch rates: API returned error")
        return data["conversion_rates"]
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error connecting to API: {e} (Check your internet or API key!)")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error fetching rates: {e}")
        exit(1)


def display_supported_currencies():
    print("\n📊 Supported Currencies:")
    for code, name in SUPPORTED_CURRENCIES.items():
        print(f"  - {code}: {name}")


def validate_currency(code: str) -> str:
    code = code.strip().upper()
    if code not in SUPPORTED_CURRENCIES:
        print(f"\n❌ Invalid currency code: {code}")
        print("Check the list of supported currencies above!")
        exit(1)
    return code


def validate_amount(amount: str) -> float:
    try:
        amount = float(amount.strip())
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return amount
    except ValueError as e:
        print(f"\n❌ Invalid amount: {e} (Enter a number like 100 or 50.50)")
        exit(1)


def main():
    print("=====================================")
    print("      💱 TERMINAL CURRENCY CONVERTER  ")
    print("=====================================")

    print("\n🔄 Fetching latest exchange rates...")
    rates = fetch_exchange_rates()

    display_supported_currencies()

    amount = validate_amount(input("\n💵 Enter amount to convert: "))
    from_currency = validate_currency(input("🔄 Convert FROM (currency code): "))
    to_currency = validate_currency(input("🔄 Convert TO (currency code): "))

    rate_from = rates[from_currency]
    rate_to = rates[to_currency]
    converted_amount = (amount / rate_from) * rate_to

    print("\n=====================================")
    print(f"✅ {amount:.2f} {from_currency} = {converted_amount:.2f} {to_currency}")
    print(f"📈 1 {from_currency} = {rate_to / rate_from:.4f} {to_currency}")
    print("=====================================")


if __name__ == "__main__":
    main()
    