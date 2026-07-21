from providers.mt5_provider import MT5Provider

mt5 = MT5Provider()

if mt5.connect():

    mt5.shutdown()