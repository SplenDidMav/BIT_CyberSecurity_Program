#Kasiski测试法
from math import sqrt
def repeated_seq_pos(text, seq_len):
#找到重复的序列和它们的位置
    seq_pos = {}
    for i, char in enumerate(text):
        next_seq = text[i:i+seq_len]
        #如果序列在文本中出现了两次或以上
        if next_seq in seq_pos.keys():
            seq_pos[next_seq].append(i)
        #如果序列在文本中只出现了一次
        else:
            seq_pos[next_seq] = [i]
    #只保留重复的序列
    repeated = list(filter(lambda x: len(seq_pos[x]) >= 2, seq_pos))
    #返回重复的序列和它们的位置
    rep_seq_pos = [(seq, seq_pos[seq]) for seq in repeated]
    return rep_seq_pos


def get_spacings(positions):
#计算序列之间的间隔
    return [positions[i+1] - positions[i] for i in range(len(positions)-1)]


def _get_factors(number):
#计算一个数的所有因子
    factors = set()
    for i in range(1, int(sqrt(number))+1):
        if number % i == 0:
            factors.add(i)
            factors.add(number//i)
    return sorted(factors)


def candidate_key_lengths(factor_lists, max_key_len):
#获得候选密钥长度
    all_factors = [factor_lists[lst][fac] for lst in range(len(factor_lists)) for fac in range(len(factor_lists[lst]))]
    #排除大于最大密钥长度的因子
    candidate_lengths = list(filter(lambda x:  x <= max_key_len, all_factors))
    #通过频率排序
    sorted_candidates = sorted(set(candidate_lengths), key=lambda x: all_factors.count(x), reverse=True)
    return sorted_candidates


def find_key_length(cyphertext, seq_len, max_key_len):
#找到重复序列的间隔，计算间隔的因子，获得候选密钥长度
    rsp = repeated_seq_pos(cyphertext, seq_len)
    seq_spc = {}
    for seq, positions in rsp:
        seq_spc[seq] = get_spacings(positions)
    #计算间隔的序列因子
    #因子列表
    factor_lists = []
    for spacings in seq_spc.values():
        for space in spacings:
            factor_lists.append(_get_factors(space))
    #根据下降的频率排序公因数
    #获得候选密钥长度
    ckl = candidate_key_lengths(factor_lists, max_key_len)
    key_len = ckl[0]
    return key_len
