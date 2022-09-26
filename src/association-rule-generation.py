import copy
import csv
import itertools
import sys
from collections import defaultdict
import numpy as np
import pandas as pd

def main():
    input_file = str(sys.argv[1])
    min_supp = float(sys.argv[2])
    min_conf = float(sys.argv[3])

    # input_file = "Integrated_Dataset.csv"
    # min_supp = 0.1
    # min_conf = 0.5
    num_of_transactions = 0

    categories = list()
    itemsetscount = defaultdict(lambda:0)

    print(input_file)
    df = pd.read_csv(str(input_file))
    # print(df)
    df = df.fillna('NA')
    D = df.values.tolist()
    # print(D)
    # categories = list(df.columns.values)
    # all_transactions = df.values.tolist()
    num_of_transactions = len(D)
    global_itemset = []
    support = defaultdict(lambda:0)

    # for transactions in all_transactions:
    #     basket = [i for i in transactions if (i != 0 or i != 0.0)]
    #     D.add(frozenset(basket))

    global_itemset, support = itemset_generation( D, min_supp, num_of_transactions, itemsetscount, global_itemset, support)
    # print(global_itemset)
    association_rules = association_rule_generation(global_itemset, itemsetscount, min_conf, support)
    # print(association_rules)
    for rule in association_rules:
        print(rule)
    # g_item = [(y, support[y]) for y in global_itemset]
    # g_item = sorted(g_item, reverse=True)
    # for g in g_item:
    #     print("",g,"",support[g[0]]*100)

    with open('example-run.txt', "a+") as file:
        file.write("\nFrequent Global Itemsets :\n")
        for i in range(len(global_itemset)):
            file.write("{}, {} \n ".format(list(global_itemset[i]), round(support[global_itemset[i]], 2)))
        file.write("\nAssociation Rules: \n")
        association_rules = sorted(association_rules, key=lambda x: x[1], reverse=True)
        for rule in association_rules:
            file.write("{} =====> {}, {}\n".format(rule[0][0], rule[0][1], round(rule[1], 2)))


def itemset_generation( D, min_supp, num_of_transactions, itemsetcount, global_itemset, support):
    categories = get_categories(D)
    # print(categories)
    lk_1 = []
    for item in categories:
        itemsetcount[frozenset([item])] = 0
        for transaction in D:
            if item in transaction:
                itemsetcount[frozenset([item])] += 1
        support[frozenset([item])] = itemsetcount[frozenset([item])] / num_of_transactions
        if support[frozenset([item])] >= min_supp:
            lk_1.append(frozenset([item]))
    global_itemset.extend(lk_1)

    k=2
    while lk_1 and k<=(len(categories)+1):
        c_k = candidate_generation(lk_1, k)
        lk_1 = list()
        for c in c_k:
            for transaction in D:
                if set(c).intersection(set(transaction))==set(c):
                    itemsetcount[(c)] += 1
            support[c] = itemsetcount[c] / num_of_transactions
            if support[c] >= min_supp:
                lk_1.append(c)
        global_itemset.extend(lk_1)
        k = k + 1

    return global_itemset, support


def get_categories(D):
    categories = set()
    for row in D:
        for item in row:
            if item != 'NA' and item != 'N/A':
                # item = [item]
                # tup = tuple(item)
                categories.add(item)
    return categories


def candidate_generation(lk_1, k):
    lk_1 = set(lk_1)
    c_k = get_union(lk_1, k)
    c_k = prune(c_k, lk_1, k)
    return c_k

def get_union(lk_1, k):
    union_set = set()
    for item1 in lk_1:
        for item2 in lk_1:
            if len(item1.union(item2))==len(item2)+1:
                union_set.add(item1.union(item2))
    return union_set


def prune(c_k, lk_1, k):
    c_k_temp = copy.deepcopy(c_k)
    ret = set()
    for itemset in c_k_temp:
        flag = True
        for item in itemset:
            temp_itemset = copy.deepcopy(itemset)
            temp_itemset = set(temp_itemset)
            temp_itemset.remove(item)
            if temp_itemset not in lk_1:
                flag = False
                break
        if flag:
            ret.add(itemset)
    return ret


def get_subset(c_k, transactions):
    subset = []
    for c_t in c_k:
        if set(c_t).intersection(set(transactions)) == set(c_t):
            subset.append(c_t)
    return subset


def association_rule_generation(global_itemset, itemsetscount, min_conf, support):
    rules = []
    for itemset in global_itemset:
        for right in itemset:
            left = set(itemset.copy())
            left.remove(right)
            subsets = itertools.chain.from_iterable(itertools.combinations(list(left), r) for r in range(len(list(left)) + 1))
            for s in subsets:
                conf = 0
                s = frozenset(s)
                if s in itemsetscount:
                    conf = support[itemset]/support[s]
                if conf >= min_conf:
                    item = (left,right)
                    if [item, conf] not in rules:
                        rules.append([item, conf])
    return rules


if __name__ == "__main__":
    main()
