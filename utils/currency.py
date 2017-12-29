from forex_python.converter import CurrencyCodes, CurrencyRates

cc = CurrencyCodes()
cr = CurrencyRates(force_decimal=True)


def check_currency(currency, default=None):
    if currency is None:
        return default

    currency = currency.upper()

    if cc.get_currency_name(currency):
        return currency
    else:
        return None


def available_currencies():
    currencies = "USD, " + ", ".join(cr.get_rates("USD").keys())
    return "No such currency. Available currencies:\n%s" % currencies
