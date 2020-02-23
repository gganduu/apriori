import argparse
import re
from itertools import combinations, groupby
from collections import OrderedDict

def generate_transaction(file):
    '''
    this function is to generate a transaction list from a file
    :param file: file path plus file name
    :return: a transaction list, each item is a set
    '''
    with open(file) as f:
        content = f.readlines()
    transaction = list()
    for line in content:
        transaction.append(frozenset(re.split("[, ]+", line.strip())))
    return transaction

def items_statistics(transaction):
    '''
    this function is to gather item statistics
    :param transaction: transaction database, patten is a list, each item is a set
    :return: total items and total item numbers
    '''
    item_set = set()
    max_len = 0
    for item in transaction:
        if max_len < len(item):
            max_len = len(item)
        item_set.update(item)
    return item_set, max_len

def generate_one_item_set(transaction, min_sup):
    '''
    this function is to generate one item set
    :param transaction: transaction database, patten is a list, each item is a set
    :param min_sup: give min support rate
    :return: return a item set, it's set to be a dictionary
    '''
    total_item, max_len = items_statistics(transaction)
    item_set = dict()
    for item in total_item:
        if item == '':
            continue
        counter = 0
        for tranc_item in transaction:
            if item in tranc_item:
                counter += 1
        if counter/len(transaction) >= min_sup:
            temp_list = list()
            # should use a list to wrap the string, otherwise the frozenset will store each letter
            temp_list.append(item)
            item_set[frozenset(temp_list)] = counter/len(transaction)
    return item_set, max_len

def link_self_to_k_item_candidates(k_minus_one_items, k_item_candidate):
    '''
    this function is to link self to generate k item candidate set, using recursive method to do it
    :param k_minus_one_items: k-1 frequent item set
    :param k_item_candidate: use function input parameter to realize parameter delivery in recursive method
                             the initial value should be a []
    :return: generated k item candidate list
    '''
    #False,0,'',[],{},() all mean False
    if k_minus_one_items:
        self_item, _ = k_minus_one_items.popitem()
        for item, _ in k_minus_one_items.items():
            temp = set(self_item)
            temp.update(item)
            if len(temp) == len(item) + 1:
                k_item_candidate.append(temp)
        link_self_to_k_item_candidates(k_minus_one_items, k_item_candidate)
    return k_item_candidate

def cut_less_than_min_support_rate(k_item_candidate, transaction, min_sup):
    '''
    this function is to cut any item set which is not satisfy with given min_support
    :param k_item_candidate: k item candidate list
    :param transaction: transaction database, patten is a list, each item is a set
    :param min_sup: given min support rate
    :return: the real k item set
    '''
    k_item = dict()
    for candi_item in k_item_candidate:
        counter = 0
        for tranc_item in transaction:
            if candi_item.issubset(tranc_item):
                counter += 1
        if counter/len(transaction) >= min_sup:
            k_item[frozenset(candi_item)] = counter/len(transaction)
    return k_item

def get_fp_set(transaction, min_sup):
    '''
    this function is to mining all frequent pattern item set
    :param transaction: transaction database, patten is a list, each item is a set
    :param min_sup: min_sup: given min support rate
    :return: all frequent pattern set
    '''
    fp_set = dict()
    temp_set, max_len = generate_one_item_set(transaction, min_sup)
    one_item_set = temp_set.copy()
    for i in range(max_len):
        temp_set = link_self_to_k_item_candidates(temp_set, [])
        temp_set = cut_less_than_min_support_rate(temp_set, transaction, min_sup)
        fp_set.update(temp_set)
    fp_set.update(one_item_set)
    return fp_set

def generate_rules(fp_set, min_conf):
    '''
    this function is to generate rules based on fp set and min confidence ratio;
    mining rules is just to iterate all frequent pattern which size is large than 2;
    and judge bi-direction set
    :param fp_set: all frequent pattern set
    :param min_conf: give min confidence ratio
    :return: return rules
    '''
    assert(fp_set)
    rules = dict()
    for key_set in fp_set.keys():
        if len(key_set) < 2:
            continue
        comb_list = list()
        if len(key_set)//2 == 1:
            comb_list.append(list(combinations(key_set, 1)))
        else:
            for i in range(1, len(key_set)//2):
                comb_list.append(list(combinations(key_set, i)))
        for inner_list in comb_list:
            for inner_key in inner_list:
                inner_key = frozenset(inner_key)
                p_inner_key = fp_set.get(inner_key)
                inner_key_insec = key_set.difference(inner_key)
                p_inner_key_insec = fp_set.get(inner_key_insec)
                if fp_set.get(key_set)/p_inner_key >= min_conf:
                    rules[str(inner_key) + "-->" + str(inner_key_insec)] = fp_set.get(key_set)/p_inner_key
                if fp_set.get(key_set)/p_inner_key_insec >= min_conf:
                    rules[str(inner_key_insec) + "-->" + str(inner_key)] = fp_set.get(key_set)/p_inner_key_insec
    return rules

def print_result(fp_set, rules):
    '''
    this function is to print final results
    :param fp_set: total frequent pattern set
    :param rules: total mining rules
    :return: no return
    '''
    for key, groups in groupby(fp_set, lambda x: len(x)):
        print("**{}-frequent pattern**".format(key))
        for group in groups:
            print(str(group)+"-->"+str(fp_set.get(group)))
        print()
    print("Rules:")
    for rule in rules.items():
        print(rule)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", required=True, type=float, help="minimum support ratio", dest="min_sup")
    parser.add_argument("-c", required=True, type=float, help="minimum confidence ratio", dest="min_conf")
    parser.add_argument("-f", required=True, help="input file path plus file name", dest="input_file")
    args = parser.parse_args()
    print(args)
    transaction = generate_transaction(args.input_file)
    fp_set = get_fp_set(transaction, args.min_sup)
    rules = generate_rules(fp_set, args.min_conf)
    print_result(fp_set, rules)


