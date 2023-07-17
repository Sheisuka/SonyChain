from math import log2


def round_to_2_power(number: int) -> int:
    """Возращает x, такой, что x это ближайшая степень 2 и x >= number. Пример: 4 -> 4, 3 -> 4, 5 -> 8"""
    tx_log = log2(number)
    tx_round = round(tx_log + 0.5)
    return 2 ** tx_round


def padd_to_2_power(list_: list) -> list:
    """Дополняет list_ последним элементом, так, чтобы его длина стала степенью 2"""
    list_len = len(list_)
    last_element = list_[list_len - 1]
    padded_list = list_[:]
    round_len = round_to_2_power(list_len)
    for i in range(round_len - list_len):
        padded_list.append(last_element) 
    return padded_list