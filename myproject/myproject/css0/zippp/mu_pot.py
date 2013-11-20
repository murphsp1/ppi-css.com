import prody as dy
import csv
import numpy as np
#import pudb as dbg
import asa_np 
import time
#import mu_pot



# define residue ASA reference, store in dict
ASA_REF = dict()

ASA_REF['ALA']= 121.93
ASA_REF['CYS']= 173.46
ASA_REF['ASP']= 163.81
ASA_REF['GLU']= 207.33
ASA_REF['PHE']= 236.16
ASA_REF['GLY']= 92.5
ASA_REF['HIS']= 211.05
ASA_REF['ILE']= 220.13
ASA_REF['LYS']= 247.02
ASA_REF['LEU']= 207.26
ASA_REF['MET']= 221.3
ASA_REF['ASN']= 176.74
ASA_REF['PRO']= 173.45
ASA_REF['GLN']= 212.42
ASA_REF['ARG']= 260.07
ASA_REF['SER']= 154.56
ASA_REF['THR']= 198.38
ASA_REF['VAL']= 208.23
ASA_REF['TRP']= 278.45
ASA_REF['TYR']= 250.6


##########################


def getTypes():
    typesHash = {'ALA_CB': 1,
         'ARG_CB': 15,
         'ARG_CD': 16,
         'ARG_CG': 16,
         'ARG_CZ': 18,
         'ARG_NE': 19,
         'ARG_NH1': 17,
         'ARG_NH2': 17,
         'ASN_CB': 10,
         'ASN_CG': 13,
         'ASN_ND2': 14,
         'ASN_OD1': 11,
         'ASP_CB': 20,
         'ASP_CG': 21,
         'ASP_OD1': 22,
         'ASP_OD2': 22,
         'CYS_CB': 1,
         'CYS_SG': 4,
         'GLN_CB': 10,
         'GLN_CD': 13,
         'GLN_CG': 12,
         'GLN_NE2': 14,
         'GLN_OE1': 11,
         'GLU_CB': 20,
         'GLU_CD': 21,
         'GLU_CG': 20,
         'GLU_OE1': 22,
         'GLU_OE2': 22,
         'GLY_CA': 0,
         'HIS_CB': 5,
         'HIS_CD2': 6,
         'HIS_CE1': 6,
         'HIS_CG': 6,
         'HIS_ND1': 9,
         'HIS_NE2': 9,
         'ILE_CB': 1,
         'ILE_CD': 2,
         'ILE_CD1': 2,
         'ILE_CG1': 2,
         'ILE_CG2': 2,
         'LEU_CB': 1,
         'LEU_CD1': 2,
         'LEU_CD2': 2,
         'LEU_CG': 2,
         'LYS_CB': 15,
         'LYS_CD': 16,
         'LYS_CE': 16,
         'LYS_CG': 16,
         'LYS_NZ': 17,
         'MET_CB': 1,
         'MET_CE': 2,
         'MET_CG': 2,
         'MET_SD': 3,
         'PHE_CB': 5,
         'PHE_CD1': 6,
         'PHE_CD2': 6,
         'PHE_CE1': 6,
         'PHE_CE2': 6,
         'PHE_CG': 6,
         'PHE_CZ': 6,
         'PRO_CB': 23,
         'PRO_CD': 23,
         'PRO_CG': 23,
         'SER_CB': 10,
         'SER_OG': 11,
         'THR_CB': 10,
         'THR_CG2': 12,
         'THR_OG1': 11,
         'TRP_CB': 5,
         'TRP_CD1': 6,
         'TRP_CD2': 6,
         'TRP_CE2': 6,
         'TRP_CE3': 6,
         'TRP_CG': 6,
         'TRP_CH2': 6,
         'TRP_CZ2': 6,
         'TRP_CZ3': 6,
         'TRP_NE1': 7,
         'TYR_CB': 5,
         'TYR_CD1': 6,
         'TYR_CD2': 6,
         'TYR_CE1': 6,
         'TYR_CE2': 6,
         'TYR_CG': 6,
         'TYR_CZ': 6,
         'TYR_OH': 8,
         'VAL_CB': 1,
         'VAL_CG1': 2,
         'VAL_CG2': 2,
         'XXX_C': 26,
         'XXX_CA': 25,
         'XXX_N': 24,
         'XXX_O': 27,
         'XXX_OCT': 27,
         'XXX_OXT': 27}
    return(typesHash)

'''
def getTypes():
    
    typesHash = dict()
    csvReader = csv.reader(open('chen.typ'))
    
    for row in csvReader:
       split_row = row[0].split()
       atom = str(split_row[0])
       AA_3 = str(split_row[1])
       atom_type = int(split_row[2])
       
       typesHash[AA_3+'_'+atom] = atom_type
    
    return typesHash
'''

def getMuPotential():
    #Hard coded version to avoid file read

    mu_pot =[[  6.73990000e-02,   7.61900000e-03,  -8.08560000e-02,
         -1.45657000e-01,  -4.00617000e-01,  -1.17511000e-01,
         -2.25774000e-01,  -2.46113000e-01,  -3.03289000e-01,
          2.86130000e-02,   1.68628000e-01,   1.38989000e-01,
          1.36041000e-01,   2.21910000e-02,   7.79000000e-04,
          2.52966000e-01,   2.15528000e-01,   1.24504000e-01,
          1.09375000e-01,   1.36467000e-01,   3.22538000e-01,
          2.71164000e-01,   2.52852000e-01,   1.11958000e-01,
          1.89847000e-01,   1.70766000e-01,   1.81964000e-01,
          1.77348000e-01],
       [  7.61900000e-03,  -3.48106000e-01,  -4.36488000e-01,
         -4.11371000e-01,  -4.88671000e-01,  -3.59635000e-01,
         -4.22153000e-01,  -4.69935000e-01,  -3.70816000e-01,
         -9.40280000e-02,  -2.17720000e-02,  -3.75360000e-02,
         -3.07010000e-02,  -5.67000000e-03,  -1.65040000e-02,
          1.05535000e-01,   1.30726000e-01,   7.19130000e-02,
          1.26860000e-02,   2.00650000e-02,   1.37978000e-01,
          1.53633000e-01,   1.55201000e-01,  -3.51600000e-02,
         -9.72770000e-02,  -1.08008000e-01,  -1.01520000e-01,
         -1.01089000e-01],
       [ -8.08560000e-02,  -4.36488000e-01,  -5.03711000e-01,
         -4.62096000e-01,  -4.30706000e-01,  -4.36160000e-01,
         -4.73317000e-01,  -5.40213000e-01,  -4.02799000e-01,
         -1.29399000e-01,  -1.27001000e-01,  -1.15208000e-01,
         -1.44369000e-01,  -8.10270000e-02,  -7.84320000e-02,
         -1.73750000e-02,   5.40410000e-02,   2.27000000e-02,
         -3.59130000e-02,  -3.56000000e-02,   2.57640000e-02,
          7.97870000e-02,   9.03070000e-02,  -9.08820000e-02,
         -2.18090000e-01,  -2.24066000e-01,  -2.19856000e-01,
         -2.16302000e-01],
       [ -1.45657000e-01,  -4.11371000e-01,  -4.62096000e-01,
         -5.31100000e-01,  -2.62445000e-01,  -4.45192000e-01,
         -4.72076000e-01,  -5.22389000e-01,  -4.14674000e-01,
         -2.04895000e-01,  -8.51850000e-02,  -8.64600000e-02,
         -1.11777000e-01,  -4.14980000e-02,  -2.65060000e-02,
         -6.01810000e-02,   2.34490000e-02,  -8.18800000e-03,
         -7.23780000e-02,  -7.96760000e-02,   8.59080000e-02,
          1.26987000e-01,   1.34049000e-01,  -1.14208000e-01,
         -2.02837000e-01,  -2.04029000e-01,  -1.98360000e-01,
         -1.92829000e-01],
       [ -4.00617000e-01,  -4.88671000e-01,  -4.30706000e-01,
         -2.62445000e-01,  -8.86145000e-01,  -4.32150000e-01,
         -4.43318000e-01,  -3.96594000e-01,  -3.30370000e-01,
         -3.91355000e-01,  -2.61427000e-01,  -2.40193000e-01,
         -2.04854000e-01,  -2.53238000e-01,  -2.25891000e-01,
         -2.24796000e-01,  -1.86530000e-01,  -1.67818000e-01,
         -2.24065000e-01,  -2.17794000e-01,  -9.82260000e-02,
         -7.23920000e-02,  -7.45510000e-02,  -3.71525000e-01,
         -3.32963000e-01,  -3.27974000e-01,  -3.38900000e-01,
         -3.44134000e-01],
       [ -1.17511000e-01,  -3.59635000e-01,  -4.36160000e-01,
         -4.45192000e-01,  -4.32150000e-01,  -4.89383000e-01,
         -5.54329000e-01,  -6.84584000e-01,  -4.79506000e-01,
         -2.15591000e-01,  -1.29790000e-01,  -1.32601000e-01,
         -1.52988000e-01,  -1.14393000e-01,  -1.22417000e-01,
          5.12280000e-02,   8.22510000e-02,   1.83190000e-02,
         -7.20010000e-02,  -6.22570000e-02,   5.18120000e-02,
          4.97330000e-02,   4.29420000e-02,  -2.32652000e-01,
         -1.60789000e-01,  -1.77747000e-01,  -1.60285000e-01,
         -1.57072000e-01],
       [ -2.25774000e-01,  -4.22153000e-01,  -4.73317000e-01,
         -4.72076000e-01,  -4.43318000e-01,  -5.54329000e-01,
         -6.10587000e-01,  -7.52797000e-01,  -5.22999000e-01,
         -2.57530000e-01,  -2.21324000e-01,  -2.08934000e-01,
         -2.36814000e-01,  -1.91663000e-01,  -1.89856000e-01,
         -6.65080000e-02,   2.88900000e-03,  -4.21880000e-02,
         -1.36655000e-01,  -1.33742000e-01,  -5.15650000e-02,
         -2.46010000e-02,  -1.67670000e-02,  -2.95709000e-01,
         -2.81330000e-01,  -2.87642000e-01,  -2.78825000e-01,
         -2.72912000e-01],
       [ -2.46113000e-01,  -4.69935000e-01,  -5.40213000e-01,
         -5.22389000e-01,  -3.96594000e-01,  -6.84584000e-01,
         -7.52797000e-01,  -7.93602000e-01,  -6.83120000e-01,
         -3.40628000e-01,  -2.08443000e-01,  -1.59401000e-01,
         -2.09092000e-01,  -2.62650000e-01,  -2.74152000e-01,
         -2.00140000e-01,  -1.52853000e-01,  -1.39376000e-01,
         -2.31910000e-01,  -2.74491000e-01,  -9.91470000e-02,
         -7.44190000e-02,  -7.76540000e-02,  -5.39364000e-01,
         -3.55084000e-01,  -3.60652000e-01,  -3.56094000e-01,
         -3.53131000e-01],
       [ -3.03289000e-01,  -3.70816000e-01,  -4.02799000e-01,
         -4.14674000e-01,  -3.30370000e-01,  -4.79506000e-01,
         -5.22999000e-01,  -6.83120000e-01,  -5.32144000e-01,
         -2.64625000e-01,  -1.63957000e-01,  -1.61187000e-01,
         -2.13911000e-01,  -1.72173000e-01,  -1.71631000e-01,
         -9.28570000e-02,  -3.78290000e-02,  -6.84820000e-02,
         -1.57300000e-01,  -1.72127000e-01,  -9.13580000e-02,
         -6.37790000e-02,  -5.68090000e-02,  -2.30791000e-01,
         -2.53879000e-01,  -2.49503000e-01,  -2.44321000e-01,
         -2.36760000e-01],
       [  2.86130000e-02,  -9.40280000e-02,  -1.29399000e-01,
         -2.04895000e-01,  -3.91355000e-01,  -2.15591000e-01,
         -2.57530000e-01,  -3.40628000e-01,  -2.64625000e-01,
         -8.47200000e-02,  -4.01990000e-02,  -5.13580000e-02,
          6.01300000e-03,  -3.59620000e-02,  -3.58970000e-02,
          2.01368000e-01,   2.10136000e-01,   1.38736000e-01,
          8.54020000e-02,   1.05132000e-01,   6.27570000e-02,
          1.56410000e-02,   1.64300000e-02,   5.29050000e-02,
         -1.74000000e-03,  -8.16500000e-03,   1.24200000e-03,
          9.39500000e-03],
       [  1.68628000e-01,  -2.17720000e-02,  -1.27001000e-01,
         -8.51850000e-02,  -2.61427000e-01,  -1.29790000e-01,
         -2.21324000e-01,  -2.08443000e-01,  -1.63957000e-01,
         -4.01990000e-02,   1.52589000e-01,   1.21176000e-01,
          7.75480000e-02,   1.33562000e-01,   1.14696000e-01,
          3.01862000e-01,   2.47231000e-01,   1.79157000e-01,
          1.67323000e-01,   1.82610000e-01,   3.27425000e-01,
          2.97648000e-01,   2.88860000e-01,   1.22926000e-01,
          1.94560000e-01,   1.77110000e-01,   1.92922000e-01,
          1.84182000e-01],
       [  1.38989000e-01,  -3.75360000e-02,  -1.15208000e-01,
         -8.64600000e-02,  -2.40193000e-01,  -1.32601000e-01,
         -2.08934000e-01,  -1.59401000e-01,  -1.61187000e-01,
         -5.13580000e-02,   1.21176000e-01,   1.03012000e-01,
          5.92830000e-02,   1.05156000e-01,   9.32710000e-02,
          2.60880000e-01,   2.23743000e-01,   1.70612000e-01,
          1.56200000e-01,   1.71317000e-01,   2.92152000e-01,
          2.64200000e-01,   2.55598000e-01,   1.08039000e-01,
          1.50154000e-01,   1.35417000e-01,   1.50878000e-01,
          1.44903000e-01],
       [  1.36041000e-01,  -3.07010000e-02,  -1.44369000e-01,
         -1.11777000e-01,  -2.04854000e-01,  -1.52988000e-01,
         -2.36814000e-01,  -2.09092000e-01,  -2.13911000e-01,
          6.01300000e-03,   7.75480000e-02,   5.92830000e-02,
          1.82170000e-02,   5.35420000e-02,   4.40820000e-02,
          2.88899000e-01,   2.48899000e-01,   1.87611000e-01,
          1.88114000e-01,   2.01560000e-01,   3.24980000e-01,
          2.99847000e-01,   2.90504000e-01,   1.37318000e-01,
          1.47761000e-01,   1.35799000e-01,   1.50039000e-01,
          1.47344000e-01],
       [  2.21910000e-02,  -5.67000000e-03,  -8.10270000e-02,
         -4.14980000e-02,  -2.53238000e-01,  -1.14393000e-01,
         -1.91663000e-01,  -2.62650000e-01,  -1.72173000e-01,
         -3.59620000e-02,   1.33562000e-01,   1.05156000e-01,
          5.35420000e-02,   1.03990000e-01,   9.98860000e-02,
          2.95185000e-01,   2.69107000e-01,   1.90359000e-01,
          1.60293000e-01,   1.65898000e-01,   3.12543000e-01,
          2.85346000e-01,   2.80917000e-01,   1.21579000e-01,
          1.49889000e-01,   1.46650000e-01,   1.43340000e-01,
          1.44481000e-01],
       [  7.79000000e-04,  -1.65040000e-02,  -7.84320000e-02,
         -2.65060000e-02,  -2.25891000e-01,  -1.22417000e-01,
         -1.89856000e-01,  -2.74152000e-01,  -1.71631000e-01,
         -3.58970000e-02,   1.14696000e-01,   9.32710000e-02,
          4.40820000e-02,   9.98860000e-02,   7.98980000e-02,
          2.80367000e-01,   2.55466000e-01,   1.86236000e-01,
          1.45258000e-01,   1.64832000e-01,   2.93843000e-01,
          2.71750000e-01,   2.66380000e-01,   1.06597000e-01,
          1.27652000e-01,   1.26652000e-01,   1.27476000e-01,
          1.31161000e-01],
       [  2.52966000e-01,   1.05535000e-01,  -1.73750000e-02,
         -6.01810000e-02,  -2.24796000e-01,   5.12280000e-02,
         -6.65080000e-02,  -2.00140000e-01,  -9.28570000e-02,
          2.01368000e-01,   3.01862000e-01,   2.60880000e-01,
          2.88899000e-01,   2.95185000e-01,   2.80367000e-01,
          4.80512000e-01,   4.51464000e-01,   3.37426000e-01,
          2.79388000e-01,   3.11760000e-01,   2.78088000e-01,
          2.41010000e-01,   2.29861000e-01,   2.77528000e-01,
          3.23213000e-01,   2.97680000e-01,   3.13566000e-01,
          3.03427000e-01],
       [  2.15528000e-01,   1.30726000e-01,   5.40410000e-02,
          2.34490000e-02,  -1.86530000e-01,   8.22510000e-02,
          2.88900000e-03,  -1.52853000e-01,  -3.78290000e-02,
          2.10136000e-01,   2.47231000e-01,   2.23743000e-01,
          2.48899000e-01,   2.69107000e-01,   2.55466000e-01,
          4.51464000e-01,   4.28212000e-01,   3.33540000e-01,
          2.94842000e-01,   3.20744000e-01,   2.27652000e-01,
          2.08118000e-01,   2.00714000e-01,   2.59716000e-01,
          2.70298000e-01,   2.56619000e-01,   2.62825000e-01,
          2.55882000e-01],
       [  1.24504000e-01,   7.19130000e-02,   2.27000000e-02,
         -8.18800000e-03,  -1.67818000e-01,   1.83190000e-02,
         -4.21880000e-02,  -1.39376000e-01,  -6.84820000e-02,
          1.38736000e-01,   1.79157000e-01,   1.70612000e-01,
          1.87611000e-01,   1.90359000e-01,   1.86236000e-01,
          3.37426000e-01,   3.33540000e-01,   2.55484000e-01,
          2.15382000e-01,   2.27049000e-01,   1.34520000e-01,
          1.27316000e-01,   1.21265000e-01,   1.85705000e-01,
          1.70158000e-01,   1.63801000e-01,   1.67931000e-01,
          1.65401000e-01],
       [  1.09375000e-01,   1.26860000e-02,  -3.59130000e-02,
         -7.23780000e-02,  -2.24065000e-01,  -7.20010000e-02,
         -1.36655000e-01,  -2.31910000e-01,  -1.57300000e-01,
          8.54020000e-02,   1.67323000e-01,   1.56200000e-01,
          1.88114000e-01,   1.60293000e-01,   1.45258000e-01,
          2.79388000e-01,   2.94842000e-01,   2.15382000e-01,
          1.61169000e-01,   1.61170000e-01,   1.02174000e-01,
          8.20950000e-02,   8.46550000e-02,   1.54822000e-01,
          1.17288000e-01,   1.10215000e-01,   1.13954000e-01,
          1.13881000e-01],
       [  1.36467000e-01,   2.00650000e-02,  -3.56000000e-02,
         -7.96760000e-02,  -2.17794000e-01,  -6.22570000e-02,
         -1.33742000e-01,  -2.74491000e-01,  -1.72127000e-01,
          1.05132000e-01,   1.82610000e-01,   1.71317000e-01,
          2.01560000e-01,   1.65898000e-01,   1.64832000e-01,
          3.11760000e-01,   3.20744000e-01,   2.27049000e-01,
          1.61170000e-01,   1.71615000e-01,   1.18951000e-01,
          1.05797000e-01,   1.06015000e-01,   1.71352000e-01,
          1.40824000e-01,   1.30073000e-01,   1.35573000e-01,
          1.29703000e-01],
       [  3.22538000e-01,   1.37978000e-01,   2.57640000e-02,
          8.59080000e-02,  -9.82260000e-02,   5.18120000e-02,
         -5.15650000e-02,  -9.91470000e-02,  -9.13580000e-02,
          6.27570000e-02,   3.27425000e-01,   2.92152000e-01,
          3.24980000e-01,   3.12543000e-01,   2.93843000e-01,
          2.78088000e-01,   2.27652000e-01,   1.34520000e-01,
          1.02174000e-01,   1.18951000e-01,   4.92972000e-01,
          4.44065000e-01,   4.25884000e-01,   2.23553000e-01,
          3.46969000e-01,   3.20717000e-01,   3.47092000e-01,
          3.35500000e-01],
       [  2.71164000e-01,   1.53633000e-01,   7.97870000e-02,
          1.26987000e-01,  -7.23920000e-02,   4.97330000e-02,
         -2.46010000e-02,  -7.44190000e-02,  -6.37790000e-02,
          1.56410000e-02,   2.97648000e-01,   2.64200000e-01,
          2.99847000e-01,   2.85346000e-01,   2.71750000e-01,
          2.41010000e-01,   2.08118000e-01,   1.27316000e-01,
          8.20950000e-02,   1.05797000e-01,   4.44065000e-01,
          3.95006000e-01,   3.79191000e-01,   2.21562000e-01,
          3.09574000e-01,   2.90681000e-01,   3.04238000e-01,
          3.01326000e-01],
       [  2.52852000e-01,   1.55201000e-01,   9.03070000e-02,
          1.34049000e-01,  -7.45510000e-02,   4.29420000e-02,
         -1.67670000e-02,  -7.76540000e-02,  -5.68090000e-02,
          1.64300000e-02,   2.88860000e-01,   2.55598000e-01,
          2.90504000e-01,   2.80917000e-01,   2.66380000e-01,
          2.29861000e-01,   2.00714000e-01,   1.21265000e-01,
          8.46550000e-02,   1.06015000e-01,   4.25884000e-01,
          3.79191000e-01,   3.66276000e-01,   2.21943000e-01,
          2.94400000e-01,   2.78778000e-01,   2.92398000e-01,
          2.86702000e-01],
       [  1.11958000e-01,  -3.51600000e-02,  -9.08820000e-02,
         -1.14208000e-01,  -3.71525000e-01,  -2.32652000e-01,
         -2.95709000e-01,  -5.39364000e-01,  -2.30791000e-01,
          5.29050000e-02,   1.22926000e-01,   1.08039000e-01,
          1.37318000e-01,   1.21579000e-01,   1.06597000e-01,
          2.77528000e-01,   2.59716000e-01,   1.85705000e-01,
          1.54822000e-01,   1.71352000e-01,   2.23553000e-01,
          2.21562000e-01,   2.21943000e-01,   3.75560000e-02,
          1.01579000e-01,   8.50600000e-02,   8.91730000e-02,
          9.10560000e-02],
       [  1.89847000e-01,  -9.72770000e-02,  -2.18090000e-01,
         -2.02837000e-01,  -3.32963000e-01,  -1.60789000e-01,
         -2.81330000e-01,  -3.55084000e-01,  -2.53879000e-01,
         -1.74000000e-03,   1.94560000e-01,   1.50154000e-01,
          1.47761000e-01,   1.49889000e-01,   1.27652000e-01,
          3.23213000e-01,   2.70298000e-01,   1.70158000e-01,
          1.17288000e-01,   1.40824000e-01,   3.46969000e-01,
          3.09574000e-01,   2.94400000e-01,   1.01579000e-01,
          2.05554000e-01,   1.76138000e-01,   2.00967000e-01,
          1.86826000e-01],
       [  1.70766000e-01,  -1.08008000e-01,  -2.24066000e-01,
         -2.04029000e-01,  -3.27974000e-01,  -1.77747000e-01,
         -2.87642000e-01,  -3.60652000e-01,  -2.49503000e-01,
         -8.16500000e-03,   1.77110000e-01,   1.35417000e-01,
          1.35799000e-01,   1.46650000e-01,   1.26652000e-01,
          2.97680000e-01,   2.56619000e-01,   1.63801000e-01,
          1.10215000e-01,   1.30073000e-01,   3.20717000e-01,
          2.90681000e-01,   2.78778000e-01,   8.50600000e-02,
          1.76138000e-01,   1.49362000e-01,   1.68853000e-01,
          1.59142000e-01],
       [  1.81964000e-01,  -1.01520000e-01,  -2.19856000e-01,
         -1.98360000e-01,  -3.38900000e-01,  -1.60285000e-01,
         -2.78825000e-01,  -3.56094000e-01,  -2.44321000e-01,
          1.24200000e-03,   1.92922000e-01,   1.50878000e-01,
          1.50039000e-01,   1.43340000e-01,   1.27476000e-01,
          3.13566000e-01,   2.62825000e-01,   1.67931000e-01,
          1.13954000e-01,   1.35573000e-01,   3.47092000e-01,
          3.04238000e-01,   2.92398000e-01,   8.91730000e-02,
          2.00967000e-01,   1.68853000e-01,   1.93302000e-01,
          1.84669000e-01],
       [  1.77348000e-01,  -1.01089000e-01,  -2.16302000e-01,
         -1.92829000e-01,  -3.44134000e-01,  -1.57072000e-01,
         -2.72912000e-01,  -3.53131000e-01,  -2.36760000e-01,
          9.39500000e-03,   1.84182000e-01,   1.44903000e-01,
          1.47344000e-01,   1.44481000e-01,   1.31161000e-01,
          3.03427000e-01,   2.55882000e-01,   1.65401000e-01,
          1.13881000e-01,   1.29703000e-01,   3.35500000e-01,
          3.01326000e-01,   2.86702000e-01,   9.10560000e-02,
          1.86826000e-01,   1.59142000e-01,   1.84669000e-01,
          1.78443000e-01]]

    return(np.array(mu_pot))

'''
def getMuPotentialFromFile():
    csvReader = csv.reader(open('trained_final2.dat'))
    
    mu_pot = np.zeros([28,28])
    
    for row in csvReader:
       row = row[0].split()
       mu_pot[int(row[0]), int(row[1])] = float(row[2])
       mu_pot[int(row[1]), int(row[0])] = float(row[2])
    
    return mu_pot
'''

def plotMuPotential():

    X = getMuPotential()
    [nr,nc]= np.shape(X)

    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    fig = plt.figure()
    ax = fig.add_subplot(111)
    imgplot = ax.imshow(X, cmap=cm.jet, interpolation='nearest')

    numrows, numcols = X.shape
    def format_coord(x, y):
        col = int(x+0.5)
        row = int(y+0.5)
        if col>=0 and col<numcols and row>=0 and row<numrows:
            z = X[row,col]
            return 'x=%1.4f, y=%1.4f, z=%1.4f'%(x, y, z)
        else:
            return 'x=%1.4f, y=%1.4f'%(x, y)

    ax.format_coord = format_coord
    #fig.colorbar(imgplot)
    font = {'family' : 'serif',
        'color'  : 'darkblue',
        'weight' : 'normal',
        'size'   : 16,
        }
    plt.ylabel('Protein A Atom Types', fontdict=font)
    plt.xlabel('Protein B Atom Types', fontdict=font)
    plt.show()

def getAtomType(atom):
    
    types = getTypes()
    bbAtoms = ['CA','O','N','C','OXT','OCT']    
    
    atom_0_str = ''

    if atom.getName() not in bbAtoms:
        atom_0_str = str(atom.getResname()) + '_' + str(atom.getName())
    
    else:
        if atom.getName() == 'CA' and atom.getResname() == 'GLY':
            atom_0_str = str(atom.getResname()) + '_' + str(atom.getName())
        else:
            atom_0_str = 'XXX' + '_' + str(atom.getName())
    try:
        atom_type = types[atom_0_str]
    
    except KeyError:
        atom_type = -1
        #print "Key error: " + atom_0_str
    
    return int(atom_type)


def evalMuPotential(complex, protein, sa_protein, ligand, sa_ligand, max_distance):
   
    # load in trained mu-Potential from file
    muPotential = getMuPotential()
    
    # load atom types 
    types = getTypes()
    dim = len(np.unique(types.values()))

    # get chids from complex
    chids = np.unique(complex.getChids())

    # initialize counts matrix  
    countArray = np.zeros([dim,dim])
    
    # get iterator over all contact between protein and ligand
    max_pairs_iter = dy.measure.contacts.iterNeighbors(protein, max_distance, ligand)
    
    #surface_contact_atoms = []

    # delta ASA sums 
    solvation_terms = dict()
    solvation_terms['TYR'] = 0.0
    solvation_terms['CYS'] = 0.0
    solvation_terms['SER'] = 0.0

    # lists of atom serial numbers that have already been counted. 
    solvation_lists = dict()
    solvation_lists['TYR'] = [] 
    solvation_lists['CYS'] = [] 
    solvation_lists['SER'] = [] 

    lig_solvation_lists = dict(solvation_lists)
    # pull np arrays of ASA values
    # note: ASA is stored in Mass field. 
    # now we index these with 'index'

    complex_ASA = complex.getMasses()
    protein_ASA = protein.getMasses()
    ligand_ASA  = ligand.getMasses()

    pro_chain_complex = complex.select('chain ' + str(chids[0])).copy()
    lig_chain_complex_= complex.select('chain ' + str(chids[1])).copy()


    for contact_tuple in max_pairs_iter:
        
        pro_index = int(contact_tuple[0].getIndex())
        lig_index = int(contact_tuple[1].getIndex())        

        if sa_protein[pro_index] and sa_ligand[lig_index]: 
            pro_atom_type = getAtomType(contact_tuple[0])
            lig_atom_type = getAtomType(contact_tuple[1])

            
            # unknown atom types are set to -1      
            if pro_atom_type >= 0 and lig_atom_type >= 0:

                # increment count array
                countArray[int(pro_atom_type),int(lig_atom_type)] += 1
    
    return  np.dot(muPotential.flatten(), countArray.flatten())

def sortContactAtoms(contact_tuples):
    return sorted(contact_tuples, key=lambda tup: (tup[0], tup[1]))

def sortContactTuple(contact_tuples):
    return sorted(contact_tuples, key=lambda tup: (tup[0].getSerial(), tup[1].getSerial()))

def printAtomContacts(atom_contacts):
    return 1 

def getChains(pdb, chains1, chains2):

    protein = pdb.select('chain ' + chains1[0]).copy()
    ligand  = pdb.select('chain ' + chains2[0]).copy()

    if len(chains1) > 1:
        for ch in range(1,len(chains1)):
            protein = protein + pdb.select('chain ' + chains1[ch]).copy()

    if len(chains2) > 1:
        for ch in range(1,len(chains2)):
            ligand = ligand +  pdb.select('chain ' + chains2[ch]).copy()
    
    return (protein, ligand)

def getComplex(pdb, chains1, chains2):

    # need to do this, since the complex may be just a subset of chains. 
    com = pdb.select('chain ' + chains1[0]).copy()
    com = com + pdb.select('chain ' + chains2[0]).copy()

    if len(chains1) > 1:
        for ch in range(1,len(chains1)):
            com = com + pdb.select('chain ' + chains1[ch]).copy()

    if len(chains2) > 1:
        for ch in range(1,len(chains2)):
            com = com +  pdb.select('chain ' + chains2[ch]).copy()

    return com 

def determineSurfaceAtoms(PDB, PDB_ASA, ref_percent=0.2):
    
    # return a binary vector: 1 if atom is on surface, 0 ow
    surface_indicator = np.zeros(np.shape(PDB_ASA))

    res_iter = PDB.iterResidues()
    for res in res_iter:
        atoms_noh = res.select('noh')
        idx_a = [int(a.getIndex()) for a in atoms_noh]
        residueASA = np.sum(PDB_ASA[idx_a])
        
        # there may be a strange residue in there 
        try:
            ASA_REF[res.getResname()]
            if residueASA > ref_percent*float(ASA_REF[res.getResname()]):
                surface_indicator[idx_a] = np.ones(len(idx_a))

        except KeyError:
            continue

    return surface_indicator 


def scoreBenchmark2():
    
    dy.confProDy(verbosity='none')

    resultsFile = open('mu-solv-scores.txt', 'w+')
    csvWriter = csv.writer(resultsFile)
    csvWriter.writerow(['name', 'mu', 'TYR', 'SER', 'CYS' ])

    csvReader  = csv.reader(open('train_dG_est.csv', 'rU'))
    csvReader.next()
    headers = csvReader.next()

    for row in csvReader:

        PDB_ID = row[0]
        mu_pot_score = float(row[1])
        dASA_tyr = float(row[2])
        dASA_ser = float(row[3])
        dASA_cys = float(row[4])
        dG_est   = float(row[5])

        feature_vector = scoreOne(PDB_ID)
        results = [PDB_ID]
        map(results.append, feature_vector)
        print results
        csvWriter.writerow(results)

    resultsFile.close()


def getKastritisData():

    try:
        open('kastritis_bench', 'rU')
        csvReader2 = csv.reader(open('kastritis_bench.csv', 'rU'))
        benchmark_data = dict()
        for row in csvReader2:
            benchmark_data[row[0]] = row[1]
    except:
        IOError
        print 'file not found'

    return benchmark_data

def scoreOne(PDB_FILENAME):
    
    PDB = dy.parsePDB(PDB_FILENAME)
    #PDB = dy.parsePDB('./dimers/'+ PDB_FILENAME + '.pdb')

    PDB_ID = PDB.getTitle()

    PDB = PDB.select('stdaa and noh').copy()

    chains_list = np.unique(PDB.getChids())

    if chains_list[0] != PDB.getChids()[0]:
        chains_list = [chains_list[idx] for idx in [1,0]]

    # chains
    protein, ligand  = getChains(PDB, chains_list[0], chains_list[1])
    
    # complex with ASA values of proteins in complex
    complex_pdb = protein + ligand

    # get asa for complex and each chain 
    asa_complex = asa_np.calculate_asa_np(complex_pdb, 1.4, 960) 
    asa_protein = asa_np.calculate_asa_np(protein, 1.4, 960) 
    asa_ligand  = asa_np.calculate_asa_np(ligand,  1.4, 960) 

    # round asa values
    asa_complex = [round(asa_complex[idx],2) for idx in range(len(asa_complex))]
    asa_protein = [round(asa_protein[idx],2) for idx in range(len(asa_protein))]
    asa_ligand  = [round(asa_ligand[idx],2) for idx in range(len(asa_ligand))]

    # store ASA values in mass field
    complex_pdb.setMasses(asa_complex)
    protein.setMasses(asa_protein)
    ligand.setMasses(asa_ligand)
    
    # overwrite PDB with disassociated ASAs stored in masses field.
    # used in desolvation terms calculation.
    PDB = protein + ligand

    # determine surface atoms, ###_ASA_indicator is number of atoms length binary vector.
    protein_ASA_indicator  = determineSurfaceAtoms(protein, protein.getMasses(), 0.2)
    ligand_ASA_indicator   = determineSurfaceAtoms(ligand,  ligand.getMasses(),  0.2)

    # get mu potential score     
    mu = evalMuPotential(complex_pdb, protein, protein_ASA_indicator, ligand, ligand_ASA_indicator, 10)
    mu = round(mu,2)

    # compute desolvation terms
    deltaASA_Tyr = 0.0
    deltaASA_Ser = 0.0
    deltaASA_Cys = 0.0

    if complex_pdb.select('resname TYR') is not None:
        deltaASA_Tyr = round(np.sum(complex_pdb.select('resname TYR').select('sc').getMasses() - PDB.select('resname TYR').select('sc').getMasses()),2)

    if complex_pdb.select('resname SER') is not None:
        deltaASA_Ser = round(np.sum(complex_pdb.select('resname SER').select('sc').getMasses() - PDB.select('resname SER').select('sc').getMasses()),2)

    if complex_pdb.select('resname CYS') is not None:
        deltaASA_Cys = round(np.sum(complex_pdb.select('resname CYS').select('sc').getMasses() - PDB.select('resname CYS').select('sc').getMasses()),2)

    # arrange features and set fitted weights 
    feature_vector = np.array([mu, deltaASA_Tyr, deltaASA_Ser, deltaASA_Cys])

    #Old
    #weights_vector = [0.001607683, 0.006278654, 0.016471769, 0.026061642]
    #bias = -9.168165335

    #New - 
    weights_vector = [0.00160383620921846, 0.00638908613212121, 0.0176168750693056, 0.0263422755351373]
    bias = -9.08150020679505

    #return feature_vector
    #return np.dot(feature_vector, weights_vector) + bias

    ddg_est =  np.dot(feature_vector, weights_vector) + bias
    return_tuple = (PDB_ID, str(chains_list[0] + ':' + chains_list[1]), str(ddg_est) )
    return(return_tuple)
    

def main():
    
    #scoreBenchmark2()
    ddg = scoreOne('1YVB')
    print ddg

if __name__ == "__main__":
    main()







