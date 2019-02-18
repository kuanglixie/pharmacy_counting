#!/usr/bin/env python

'''
    Purpose: Summarise input file to an output with drug_name, num_prescriber, and total_cost.

    Input Data: The dataset identifies prescribers by their ID, last name, and first name.  It also describes the specific prescriptions that were dispensed at their direction, listed by drug name and the cost of the medication.

    One example:
        id,prescriber_last_name,prescriber_first_name,drug_name,drug_cost
        1000000001,Smith,James,AMBIEN,100
        1000000002,Garcia,Maria,AMBIEN,200
        1000000003,Johnson,James,CHLORPROMAZINE,1000
        1000000004,Rodriguez,Maria,CHLORPROMAZINE,2000
        1000000005,Smith,David,BENZTROPINE MESYLATE,1500

    Output Data: CSV file with drug_name, num_prescriber, and total_cost

    One example:
        drug_name,num_prescriber,total_cost
        CHLORPROMAZINE,2,3000
        BENZTROPINE MESYLATE,1,1500
        AMBIEN,2,300

    Usage: python ./src/pharmacy_counting.py ./input/itcont.txt ./output/top_cost_drug.txt
'''

import sys
from collections import defaultdict

from util import process_info, get_output_from_dict


def pharmacy_counting(inobj, otobj):
    """Read from inobj input object and write to otobj output object.

    Keyword arguments:
    inobj -- input file object
    otobj -- output file object
    """
    c_res = defaultdict(lambda: [set(), 0])
    fline = True  # whether this is the first line or not
    for line in inobj:
        if fline:
            header = [x.strip().lower() for x in line.split(",")]
            didx = header.index("drug_name")
            pidx1 = header.index("prescriber_first_name")
            pidx2 = header.index("prescriber_last_name")
            cidx = header.index("drug_cost")
            fline = False
            continue
        dname, pname, cost = process_info(line, didx, cidx, [pidx1, pidx2])
        if dname:
            c_res[dname][0].add(pname)
            c_res[dname][1] += cost
    otobj.write("drug_name,num_prescriber,total_cost\n")
    for drug, pnum, tot_cost in get_output_from_dict(c_res):
        tot_cost = str('{0:.2f}'.format(tot_cost).rstrip('0').rstrip('.'))
        if "," in drug:
            drug = "\"" + drug + "\""
        otobj.write(",".join([drug, str(pnum), tot_cost]) + "\n")


if __name__ == "__main__":
    infile = sys.argv[1]
    outfile = sys.argv[2]
    try:
        with open(infile, "r") as iobj, open(outfile, "w") as oobj:
            pharmacy_counting(iobj, oobj)
    except OSError:
        raise OSError("Cannot open " + infile + " or write to " + outfile)
