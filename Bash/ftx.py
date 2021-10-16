import ccxt
import os
import datetime
import json
import sys

exchange = ccxt.ftx()
exc_name = exchange.name.replace(" ", "")
symbolForThis = ""
 
def main():
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python CcxtData.py <SYMBOL>")

    symbolForThis = sys.argv[1]+'-PERP'
    print(getTickerPrice(symbolForThis))
    currYMD = datetime.datetime.now().strftime('%Y%m%d')
    fileName = f'{os.getcwd()}/{currYMD}_CCXT_{exc_name}_{symbolForThis.replace("/","").replace("-","")}.jsonl'
    print(f'{fileName}')

# TODO: if fresh start, add a log statement to the start of file 
def getTickerPrice(symbol):
    try:            
        return (str(json.dumps(exchange.fetch_ticker(symbol))))
    except ccxt.errors.BadSymbol:
        return (str(json.dumps(exchange.fetch_ticker(sys.argv[1]+'/USD'))))
    except ccxt.NetworkError as netError:
        # TODO: if error then show the error.
        return f"Network Error {netError.args} [DateTime: {datetime.datetime.now()}]"


if __name__ == '__main__':
    main()
