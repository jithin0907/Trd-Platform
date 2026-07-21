from providers.data_provider import DataProvider

provider = DataProvider()

if provider.connect():

    df = provider.get_market_data(
        symbol="EURUSD",
        timeframe="M15",
        bars=100
    )

    print(df.tail())

    provider.shutdown()