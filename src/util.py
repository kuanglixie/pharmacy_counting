#!/usr/bin/env python

'''
    Purpose: help functoin for pharmcy_counting.py

    Usage: python ./src/pharmacy_counting.py ./input/itcont.txt ./output/top_cost_drug.txt
'''

import re


def process_info(line, didx, cidx, pidx):
    """Process one line and return the corresponding drug name and cost.

    Keyword arguments:
    line -- a line from the file.
    didx -- the column index for drug.
    cidx -- the column index for cost.
    pidx -- the column index for patient first name and last name.

    >>> process_info("1000000001,Smith,James,AMBIEN,100", 3, 4, [1, 2])
    ('AMBIEN', 'Smith:James', 100.0)
    >>> process_info("", 0, 0, None)
    (None, None, 0.0)
    >>> process_info("1952310666,A'BODJEDI,ENENGE,ALPRAZOLAM,1964.49", 3, 4, [1,2])
    ('ALPRAZOLAM', "A'BODJEDI:ENENGE", 1964.49)
    """
    if not line:
        return None, None, 0.0

    content = re.split(''',(?=(?:[^"]|"[^"]*")*$)''', line.strip())
    dname = content[didx].strip()
    try:
        cost = float(content[cidx].strip())
    except:
        print(line)
        print(content)
        raise Exception()
    pname = content[pidx[0]] + ":" + content[pidx[1]]
    return dname, pname, cost


def get_output_from_dict(drug_dict):
    """Produce file lines for drug dictionary. the total number of UNIQUE individuals who prescribed the medication, and the total drug cost, which must be listed in descending order based on the total drug cost and if there is a tie, drug name in ascending order.

    Keyword arguments:
    drug_dict -- a dictionary contains drug name, prescribers, and total cost.

    >>> get_output_from_dict({"AMBIEN": [set(["Smith:James", "Lee:High"]), 300]})
    [['AMBIEN', 2, 300]]
    >>> get_output_from_dict({"CCC": [set(["Smith:James", "Lee:High"]), 300],\
    "AMBIEN": [set(["Smith:James", "Lee:High"]), 300]})
    [['AMBIEN', 2, 300], ['CCC', 2, 300]]
    >>> get_output_from_dict({"CCC": [set(["Smith:James", "Lee:High"]), 200],\
    "AMBIEN": [set(["Smith:James", "Lee:High"]), 300]})
    [['AMBIEN', 2, 300], ['CCC', 2, 200]]
    """
    drug_list = []
    for drug, inf in drug_dict.iteritems():
        drug_list.append([drug, len(inf[0]), inf[1]])
    return sorted(drug_list, key=lambda x: (-x[2], x[0]))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
