import  func_arbitrage


"""
    step 0: 查找可交易的coin
"""

def step_0():
    url = "https://poloniex.com/public?command=returnTicker"
    coin_json = func_arbitrage.get_coin_tickers(url)

    # 循环遍历每个对象，并从中获取可交易的交易对(排除被冻结或post only（一般是交易对第一次开盘）的交易对)
    coin_list = func_arbitrage.collect_tradeables(coin_json)

    return coin_list



"""Main function"""
if __name__ == '__main__':
    coin_list = step_0()
    print(coin_list)
