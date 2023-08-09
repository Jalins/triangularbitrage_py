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


def structure_triangular_pairs(coin_list):
    triangular_pairs_list = []
    remove_duplicate_list = []
    pairs_list = coin_list

    # 获取交易对A
    for pair_a in pairs_list:
        pair_a_split = pair_a.split('_')
        a_base = pair_a_split[0]
        a_quote = pair_a_split[1]

        a_pair_box = [a_base, a_quote]

        # 获取交易对B
        for pair_b in pairs_list:
            pair_b_split = pair_b.split('_')
            b_base = pair_b_split[0]
            b_quote = pair_b_split[1]

            if pair_b != pair_a:
                if b_base in a_pair_box or b_quote in a_pair_box:

                    # 获取交易对C
                    for pair_c in pairs_list:
                        pair_c_split = pair_c.split('_')
                        c_base = pair_c_split[0]
                        c_quote = pair_c_split[1]

                        if pair_c != pair_b and pair_c != pair_a:
                            combine_all = [pair_a, pair_b, pair_c]
                            pair_box = [a_base, a_quote, b_base, b_quote, c_base, c_quote]
                            count_c_base = 0
                            for i in pair_box:
                                if i == c_base:
                                    count_c_base += 1

                            count_c_quote = 0
                            for i in pair_box:
                                if i == c_quote:
                                    count_c_quote += 1

                            if count_c_base == 2 and count_c_quote == 2 and c_base != c_quote:
                                combined = pair_a + "," + pair_b + "," + pair_c

                                # 去除重复的三角套利组合
                                # 使用sorted()函数，将字符串中的字符按照字母顺序排序，保证每个三角套利组合的顺序一致
                                unique_item = ''.join(sorted(combine_all))

                                if unique_item not in remove_duplicate_list:
                                    # 将去重后的三角套利组合添加到重复列表中，用于后续的比较
                                    remove_duplicate_list.append(unique_item)

                                    match_dict= {
                                        'pair_a': pair_a,
                                        'pair_b': pair_b,
                                        'pair_c': pair_c,
                                        'a_base': a_base,
                                        'a_quote': a_quote,
                                        'b_base': b_base,
                                        'b_quote': b_quote,
                                        'c_base': c_base,
                                        'c_quote': c_quote,
                                        'combined': combined,
                                    }
                                    triangular_pairs_list.append(match_dict)
    return triangular_pairs_list