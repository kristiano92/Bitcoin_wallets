import csv
from collections import defaultdict

def create_wallets(file):
    '''Reads csv file, groups addresses as wallets and writes results to csv file'''

    # read csv file with hashes of transactions and addresses
    reader = csv.reader(open(file, 'r'))
    header = next(reader)
    d = defaultdict(list)    # {tx1:[adr1,adr2,...],tx2:[adr2, adr3,...]}
    for row in reader:
       k, v = row
       d[k].append(v)

    # create inverse dictionary: addresses as keys and hashes of transactions as values
    inverse = {item: [key for key,ls in d.items() if item in ls]
               for item in set(sum(d.values(),[]))}                     # {adr1:[tx1,tx5,...], adr2:[tx1,tx3,...]}

    # create wallets dictionary with initial ids and hashes of transactions from inverse dictionary
    wallets = dict()            # {1:[tx1,tx5,...], 2:[tx1,tx3,...]}
    id = 1
    for v in inverse.values():
        wallets[id] = v
        id += 1

    # change wallets transactions on proper addresses from d(dict)
    for k1,v1 in d.items():
        for k2,v2 in wallets.items():
            if k1 in v2:
                wallets[k2]=v1             #{1:[adr1,adr4,adr5,...],2:[adr4,adr8,...]}

    # create list of lists with addresses
    values_list = []
    for v in wallets.values():
        values_list.append(v)

    # compare lists between one another to group addresses without duplicates
    group_addresses = []
    while len(values_list) > 0:
        first, *rest = values_list
        first = set(first)

        lf = -1
        while len(first)>lf:
            lf = len(first)

            rest2 = []
            for r in rest:
                if len(first.intersection(set(r)))>0:
                    first |= set(r)
                else:
                    rest2.append(r)
            rest = rest2

        group_addresses.append(list(first))
        values_list = rest

    # add grouped addresses to wallet ids
    final_wallets = dict()
    final_id = 100000
    for w in group_addresses:
        final_wallets[final_id] = w
        final_id += 1

    # write results to csv file
    with open("final_results.csv", "w", newline='') as final:
        csv_output = csv.writer(final)
        csv_output.writerow(['wallet', 'address'])
        for key in final_wallets.keys():
            csv_output.writerow([key] + final_wallets[key])

create_wallets('Transactions-In-Test.csv')
