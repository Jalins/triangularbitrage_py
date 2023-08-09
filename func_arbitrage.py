import requests
import json

def get_coin_tickers(url):
    # 从交易所中获取coin列表与价格
    req = requests.get(url)
    coin_json = json.loads(req.text)
    return coin_json

def collect_tradeables(coin_json):
    # 从coin列表中获取可交易的交易对
    coin_list = []
    for coin in coin_json:
        is_frozen = coin_json[coin]['isFrozen']
        is_post_only = coin_json[coin]['postOnly']
        if int(is_frozen) == 0 and int(is_post_only) == 0:
            coin_list.append(coin)
    return coin_list
