from providers.data_provider import DataProvider
from engine.market_structure_engine import MarketStructureEngine


def main():

    provider = DataProvider()

    if not provider.connect():
        return

    df = provider.get_market_data(
        symbol="EURUSD",
        timeframe="M5",
        bars=300
    )

    engine = MarketStructureEngine(
        lookback=5
    )

    result = engine.detect(df)

    print("\n========== MARKET STRUCTURE ENGINE ==========\n")

    print("Trend :", result["trend"])

    print()

    if result["last_high"]:

        print(
            "Last Swing High :",
            result["last_high"]["time"],
            round(result["last_high"]["price"], 5)
        )

    else:

        print("Last Swing High : None")

    if result["last_low"]:

        print(
            "Last Swing Low  :",
            result["last_low"]["time"],
            round(result["last_low"]["price"], 5)
        )

    else:

        print("Last Swing Low  : None")

    print()

    print("\n========== PROTECTED SWINGS ==========\n")

    if result["protected_high"]:

     print(
        "Protected High :",
        result["protected_high"]["time"],
        round(result["protected_high"]["price"], 5)
    )

    else:

     print("Protected High : None")

    if result["protected_low"]:

     print(
        "Protected Low  :",
        result["protected_low"]["time"],
        round(result["protected_low"]["price"], 5)
    )

    else:

     print("Protected Low  : None")

    print()

    print("Total Swings :", len(result["swings"]))

    print("\n========== LAST 10 SWINGS ==========\n")    

    for swing in result["swings"][-10:]:

        print(
            swing["type"],
            swing["time"],
            round(swing["price"], 5)
        )
        
    print("\n========== BOS ==========")
    print("Valid       :", result["bos"]["valid"])
    print("Type        :", result["bos"]["type"])
    print("Direction   :", result["bos"]["direction"])
    print("Break Price :", result["bos"]["break_price"]) 

    print("\n========== CHOCH ==========\n")

    print("Valid     :", result["choch"]["valid"])
    print("Direction :", result["choch"]["direction"])

    print("\n========== MSS ==========\n")
    print("Valid     :", result["mss"]["valid"])
    print("Direction :", result["mss"]["direction"])


    print("\n========== SWING ANALYSIS ==========\n")

    swings = result["swings"]

    for i in range(1, len(swings)):

        previous = swings[i - 1]
        current = swings[i]

        print(
            f"{previous['type']:>4} "
            f"{previous['structure']:>2} "
            f"{previous['time']} "
            f"{round(previous['price'],5)}"
            f"  --->  "
            f"{current['type']:>4} "
            f"{current['structure']:>2} "
            f"{current['time']} "
            f"{round(current['price'],5)}"
        )

    provider.shutdown()

if __name__ == "__main__":
    main()
    
 