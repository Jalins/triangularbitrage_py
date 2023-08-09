import  func_arbitrage
import  json

url = "https://poloniex.com/public?command=returnTicker"
"""
    step 0: 查找可交易的coin
"""

def step_0():

    coin_json = func_arbitrage.get_coin_tickers(url)

    # 循环遍历每个对象，并从中获取可交易的交易对(排除被冻结或post only（一般是交易对第一次开盘）的交易对)
    coin_list = func_arbitrage.collect_tradeables(coin_json)

    return coin_list

"""
    在交易列表中寻找可进行三角套利的三个交易对
    每三个交易对为一组，计算三角套利的收益率
"""
def step_1(coin_list):

    structured_list = func_arbitrage.structure_triangular_pairs(coin_list)

    with open('structured_triangular_list.json', 'w') as fp:
        json.dump(structured_list, fp)

    print(structured_list)

"""
   计算三角套利的收益率
"""
def step_2():
    with open('structured_triangular_list.json', 'r') as fp:
        structured_list = json.load(fp)

    # 获取最新的价格
    price_json = func_arbitrage.get_coin_tickers(url)

    for t_pair in structured_list:
        price_dict = func_arbitrage.get_price_for_t_pair(t_pair, price_json)
        func_arbitrage.calculate_triangulat_arb_surface_rate(t_pair, price_dict)





"""Main function"""
if __name__ == '__main__':
    # coin_list = step_0()
    # step_1(coin_list)
    step_2()
