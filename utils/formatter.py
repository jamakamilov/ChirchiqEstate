def format_price(amount: float, currency: str = "UZS"):
    try:
        return f"{int(amount):,} {currency}"
    except:
        return f"{amount} {currency}"
