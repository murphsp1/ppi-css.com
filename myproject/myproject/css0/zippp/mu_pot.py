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

    mu_pot =[[  6.30320000e-02,   4.36400000e-03,  -8.21090000e-02,
         -1.46445000e-01,  -3.96399000e-01,  -1.23005000e-01,
         -2.31079000e-01,  -2.52237000e-01,  -3.06600000e-01,
          2.53030000e-02,   1.65200000e-01,   1.35683000e-01,
          1.35792000e-01,   2.16140000e-02,  -3.66000000e-04,
          2.50525000e-01,   2.12563000e-01,   1.20144000e-01,
          1.04269000e-01,   1.32487000e-01,   3.18100000e-01,
          2.67057000e-01,   2.48770000e-01,   1.10503000e-01,
          1.86041000e-01,   1.67202000e-01,   1.78034000e-01,
          1.74629000e-01],
       [  4.36400000e-03,  -3.49776000e-01,  -4.37321000e-01,
         -4.14660000e-01,  -4.87235000e-01,  -3.59826000e-01,
         -4.22061000e-01,  -4.68147000e-01,  -3.71333000e-01,
         -9.66500000e-02,  -2.04090000e-02,  -3.56820000e-02,
         -3.06670000e-02,  -4.95900000e-03,  -1.51500000e-02,
          1.05256000e-01,   1.30598000e-01,   7.10240000e-02,
          1.01970000e-02,   1.79120000e-02,   1.36525000e-01,
          1.52042000e-01,   1.53349000e-01,  -3.61730000e-02,
         -9.81140000e-02,  -1.08662000e-01,  -1.02394000e-01,
         -1.01631000e-01],
       [ -8.21090000e-02,  -4.37321000e-01,  -5.04285000e-01,
         -4.64951000e-01,  -4.30753000e-01,  -4.35463000e-01,
         -4.72631000e-01,  -5.37322000e-01,  -4.00861000e-01,
         -1.31144000e-01,  -1.24288000e-01,  -1.12701000e-01,
         -1.42528000e-01,  -7.95290000e-02,  -7.66000000e-02,
         -1.67030000e-02,   5.44110000e-02,   2.21860000e-02,
         -3.82110000e-02,  -3.72690000e-02,   2.53390000e-02,
          7.95900000e-02,   9.01230000e-02,  -9.03250000e-02,
         -2.17868000e-01,  -2.23785000e-01,  -2.19698000e-01,
         -2.15929000e-01],
       [ -1.46445000e-01,  -4.14660000e-01,  -4.64951000e-01,
         -5.35344000e-01,  -2.69711000e-01,  -4.47492000e-01,
         -4.74162000e-01,  -5.21465000e-01,  -4.17674000e-01,
         -2.10993000e-01,  -8.55420000e-02,  -8.52200000e-02,
         -1.12140000e-01,  -4.18880000e-02,  -2.86350000e-02,
         -6.38110000e-02,   2.08810000e-02,  -1.04980000e-02,
         -7.42900000e-02,  -8.16360000e-02,   8.17940000e-02,
          1.23123000e-01,   1.30684000e-01,  -1.12352000e-01,
         -2.05365000e-01,  -2.06810000e-01,  -2.00936000e-01,
         -1.95172000e-01],
       [ -3.96399000e-01,  -4.87235000e-01,  -4.30753000e-01,
         -2.69711000e-01,  -8.84398000e-01,  -4.34730000e-01,
         -4.40939000e-01,  -4.22834000e-01,  -3.22010000e-01,
         -3.89932000e-01,  -2.60297000e-01,  -2.41461000e-01,
         -1.94398000e-01,  -2.49967000e-01,  -2.27248000e-01,
         -2.21608000e-01,  -1.82157000e-01,  -1.59664000e-01,
         -2.20234000e-01,  -2.13756000e-01,  -9.81530000e-02,
         -6.71310000e-02,  -7.21320000e-02,  -3.77188000e-01,
         -3.33370000e-01,  -3.29137000e-01,  -3.38457000e-01,
         -3.39579000e-01],
       [ -1.23005000e-01,  -3.59826000e-01,  -4.35463000e-01,
         -4.47492000e-01,  -4.34730000e-01,  -4.92942000e-01,
         -5.57092000e-01,  -6.85032000e-01,  -4.82959000e-01,
         -2.20678000e-01,  -1.32774000e-01,  -1.35455000e-01,
         -1.54531000e-01,  -1.15485000e-01,  -1.23231000e-01,
          4.80490000e-02,   8.00970000e-02,   1.73430000e-02,
         -7.48260000e-02,  -6.46930000e-02,   4.67100000e-02,
          4.48620000e-02,   3.81530000e-02,  -2.35289000e-01,
         -1.63455000e-01,  -1.80368000e-01,  -1.63072000e-01,
         -1.59599000e-01],
       [ -2.31079000e-01,  -4.22061000e-01,  -4.72631000e-01,
         -4.74162000e-01,  -4.40939000e-01,  -5.57092000e-01,
         -6.12474000e-01,  -7.52950000e-01,  -5.26395000e-01,
         -2.61742000e-01,  -2.23548000e-01,  -2.11458000e-01,
         -2.37346000e-01,  -1.92309000e-01,  -1.90250000e-01,
         -6.87540000e-02,   2.45000000e-04,  -4.35290000e-02,
         -1.39710000e-01,  -1.37604000e-01,  -5.63350000e-02,
         -2.94750000e-02,  -2.17090000e-02,  -2.97462000e-01,
         -2.83424000e-01,  -2.89644000e-01,  -2.81048000e-01,
         -2.74992000e-01],
       [ -2.52237000e-01,  -4.68147000e-01,  -5.37322000e-01,
         -5.21465000e-01,  -4.22834000e-01,  -6.85032000e-01,
         -7.52950000e-01,  -7.90838000e-01,  -6.81470000e-01,
         -3.43428000e-01,  -2.10686000e-01,  -1.62612000e-01,
         -2.04708000e-01,  -2.60986000e-01,  -2.73582000e-01,
         -1.97212000e-01,  -1.51788000e-01,  -1.36816000e-01,
         -2.31705000e-01,  -2.73559000e-01,  -1.05947000e-01,
         -7.84180000e-02,  -8.21040000e-02,  -5.41542000e-01,
         -3.56589000e-01,  -3.61771000e-01,  -3.57277000e-01,
         -3.54318000e-01],
       [ -3.06600000e-01,  -3.71333000e-01,  -4.00861000e-01,
         -4.17674000e-01,  -3.22010000e-01,  -4.82959000e-01,
         -5.26395000e-01,  -6.81470000e-01,  -5.36260000e-01,
         -2.67562000e-01,  -1.71591000e-01,  -1.68218000e-01,
         -2.18144000e-01,  -1.77060000e-01,  -1.77611000e-01,
         -9.68120000e-02,  -4.18150000e-02,  -7.13990000e-02,
         -1.62990000e-01,  -1.77948000e-01,  -9.77260000e-02,
         -7.06390000e-02,  -6.38110000e-02,  -2.30172000e-01,
         -2.57578000e-01,  -2.53423000e-01,  -2.47969000e-01,
         -2.40107000e-01],
       [  2.53030000e-02,  -9.66500000e-02,  -1.31144000e-01,
         -2.10993000e-01,  -3.89932000e-01,  -2.20678000e-01,
         -2.61742000e-01,  -3.43428000e-01,  -2.67562000e-01,
         -9.11280000e-02,  -4.12800000e-02,  -5.31130000e-02,
          2.08100000e-03,  -3.82360000e-02,  -3.82270000e-02,
          1.98445000e-01,   2.07142000e-01,   1.36392000e-01,
          8.16130000e-02,   1.00953000e-01,   5.63300000e-02,
          1.01910000e-02,   1.05330000e-02,   5.49400000e-02,
         -4.80500000e-03,  -1.14610000e-02,  -1.83500000e-03,
          7.29100000e-03],
       [  1.65200000e-01,  -2.04090000e-02,  -1.24288000e-01,
         -8.55420000e-02,  -2.60297000e-01,  -1.32774000e-01,
         -2.23548000e-01,  -2.10686000e-01,  -1.71591000e-01,
         -4.12800000e-02,   1.50174000e-01,   1.19260000e-01,
          7.58520000e-02,   1.31887000e-01,   1.15020000e-01,
          2.99110000e-01,   2.45365000e-01,   1.76519000e-01,
          1.62252000e-01,   1.77419000e-01,   3.23136000e-01,
          2.93650000e-01,   2.85449000e-01,   1.21427000e-01,
          1.92690000e-01,   1.75253000e-01,   1.90915000e-01,
          1.82990000e-01],
       [  1.35683000e-01,  -3.56820000e-02,  -1.12701000e-01,
         -8.52200000e-02,  -2.41461000e-01,  -1.35455000e-01,
         -2.11458000e-01,  -1.62612000e-01,  -1.68218000e-01,
         -5.31130000e-02,   1.19260000e-01,   1.00892000e-01,
          5.78390000e-02,   1.04193000e-01,   9.34360000e-02,
          2.59235000e-01,   2.22340000e-01,   1.68254000e-01,
          1.51627000e-01,   1.67072000e-01,   2.87597000e-01,
          2.60314000e-01,   2.51871000e-01,   1.07139000e-01,
          1.48580000e-01,   1.33778000e-01,   1.48989000e-01,
          1.43919000e-01],
       [  1.35792000e-01,  -3.06670000e-02,  -1.42528000e-01,
         -1.12140000e-01,  -1.94398000e-01,  -1.54531000e-01,
         -2.37346000e-01,  -2.04708000e-01,  -2.18144000e-01,
          2.08100000e-03,   7.58520000e-02,   5.78390000e-02,
          1.59520000e-02,   5.44120000e-02,   4.77300000e-02,
          2.88266000e-01,   2.48352000e-01,   1.85483000e-01,
          1.83672000e-01,   1.97920000e-01,   3.21063000e-01,
          2.95700000e-01,   2.87698000e-01,   1.35052000e-01,
          1.45900000e-01,   1.34502000e-01,   1.48720000e-01,
          1.46058000e-01],
       [  2.16140000e-02,  -4.95900000e-03,  -7.95290000e-02,
         -4.18880000e-02,  -2.49967000e-01,  -1.15485000e-01,
         -1.92309000e-01,  -2.60986000e-01,  -1.77060000e-01,
         -3.82360000e-02,   1.31887000e-01,   1.04193000e-01,
          5.44120000e-02,   1.04354000e-01,   1.01675000e-01,
          2.94268000e-01,   2.68576000e-01,   1.86709000e-01,
          1.54717000e-01,   1.61309000e-01,   3.08183000e-01,
          2.81299000e-01,   2.77338000e-01,   1.20211000e-01,
          1.49480000e-01,   1.45805000e-01,   1.42603000e-01,
          1.44256000e-01],
       [ -3.66000000e-04,  -1.51500000e-02,  -7.66000000e-02,
         -2.86350000e-02,  -2.27248000e-01,  -1.23231000e-01,
         -1.90250000e-01,  -2.73582000e-01,  -1.77611000e-01,
         -3.82270000e-02,   1.15020000e-01,   9.34360000e-02,
          4.77300000e-02,   1.01675000e-01,   8.32610000e-02,
          2.80556000e-01,   2.56121000e-01,   1.83686000e-01,
          1.40967000e-01,   1.61401000e-01,   2.90204000e-01,
          2.67750000e-01,   2.62878000e-01,   1.05682000e-01,
          1.27400000e-01,   1.26429000e-01,   1.26875000e-01,
          1.31166000e-01],
       [  2.50525000e-01,   1.05256000e-01,  -1.67030000e-02,
         -6.38110000e-02,  -2.21608000e-01,   4.80490000e-02,
         -6.87540000e-02,  -1.97212000e-01,  -9.68120000e-02,
          1.98445000e-01,   2.99110000e-01,   2.59235000e-01,
          2.88266000e-01,   2.94268000e-01,   2.80556000e-01,
          4.79618000e-01,   4.50688000e-01,   3.37081000e-01,
          2.76751000e-01,   3.09304000e-01,   2.74661000e-01,
          2.37748000e-01,   2.26713000e-01,   2.74417000e-01,
          3.20370000e-01,   2.94979000e-01,   3.11152000e-01,
          3.01902000e-01],
       [  2.12563000e-01,   1.30598000e-01,   5.44110000e-02,
          2.08810000e-02,  -1.82157000e-01,   8.00970000e-02,
          2.45000000e-04,  -1.51788000e-01,  -4.18150000e-02,
          2.07142000e-01,   2.45365000e-01,   2.22340000e-01,
          2.48352000e-01,   2.68576000e-01,   2.56121000e-01,
          4.50688000e-01,   4.26612000e-01,   3.32738000e-01,
          2.92791000e-01,   3.18748000e-01,   2.24274000e-01,
          2.04671000e-01,   1.97565000e-01,   2.55812000e-01,
          2.68153000e-01,   2.54602000e-01,   2.60781000e-01,
          2.54735000e-01],
       [  1.20144000e-01,   7.10240000e-02,   2.21860000e-02,
         -1.04980000e-02,  -1.59664000e-01,   1.73430000e-02,
         -4.35290000e-02,  -1.36816000e-01,  -7.13990000e-02,
          1.36392000e-01,   1.76519000e-01,   1.68254000e-01,
          1.85483000e-01,   1.86709000e-01,   1.83686000e-01,
          3.37081000e-01,   3.32738000e-01,   2.54368000e-01,
          2.12869000e-01,   2.24698000e-01,   1.31118000e-01,
          1.23991000e-01,   1.18221000e-01,   1.83291000e-01,
          1.68022000e-01,   1.61825000e-01,   1.65680000e-01,
          1.64072000e-01],
       [  1.04269000e-01,   1.01970000e-02,  -3.82110000e-02,
         -7.42900000e-02,  -2.20234000e-01,  -7.48260000e-02,
         -1.39710000e-01,  -2.31705000e-01,  -1.62990000e-01,
          8.16130000e-02,   1.62252000e-01,   1.51627000e-01,
          1.83672000e-01,   1.54717000e-01,   1.40967000e-01,
          2.76751000e-01,   2.92791000e-01,   2.12869000e-01,
          1.57710000e-01,   1.58145000e-01,   9.75900000e-02,
          7.77960000e-02,   8.04140000e-02,   1.48973000e-01,
          1.12905000e-01,   1.06057000e-01,   1.09660000e-01,
          1.10392000e-01],
       [  1.32487000e-01,   1.79120000e-02,  -3.72690000e-02,
         -8.16360000e-02,  -2.13756000e-01,  -6.46930000e-02,
         -1.37604000e-01,  -2.73559000e-01,  -1.77948000e-01,
          1.00953000e-01,   1.77419000e-01,   1.67072000e-01,
          1.97920000e-01,   1.61309000e-01,   1.61401000e-01,
          3.09304000e-01,   3.18748000e-01,   2.24698000e-01,
          1.58145000e-01,   1.68258000e-01,   1.14375000e-01,
          1.01334000e-01,   1.02294000e-01,   1.66215000e-01,
          1.37049000e-01,   1.26308000e-01,   1.31769000e-01,
          1.26309000e-01],
       [  3.18100000e-01,   1.36525000e-01,   2.53390000e-02,
          8.17940000e-02,  -9.81530000e-02,   4.67100000e-02,
         -5.63350000e-02,  -1.05947000e-01,  -9.77260000e-02,
          5.63300000e-02,   3.23136000e-01,   2.87597000e-01,
          3.21063000e-01,   3.08183000e-01,   2.90204000e-01,
          2.74661000e-01,   2.24274000e-01,   1.31118000e-01,
          9.75900000e-02,   1.14375000e-01,   4.87557000e-01,
          4.38819000e-01,   4.20576000e-01,   2.20136000e-01,
          3.43350000e-01,   3.17001000e-01,   3.43460000e-01,
          3.32759000e-01],
       [  2.67057000e-01,   1.52042000e-01,   7.95900000e-02,
          1.23123000e-01,  -6.71310000e-02,   4.48620000e-02,
         -2.94750000e-02,  -7.84180000e-02,  -7.06390000e-02,
          1.01910000e-02,   2.93650000e-01,   2.60314000e-01,
          2.95700000e-01,   2.81299000e-01,   2.67750000e-01,
          2.37748000e-01,   2.04671000e-01,   1.23991000e-01,
          7.77960000e-02,   1.01334000e-01,   4.38819000e-01,
          3.89449000e-01,   3.73928000e-01,   2.18557000e-01,
          3.06033000e-01,   2.87089000e-01,   3.00766000e-01,
          2.98714000e-01],
       [  2.48770000e-01,   1.53349000e-01,   9.01230000e-02,
          1.30684000e-01,  -7.21320000e-02,   3.81530000e-02,
         -2.17090000e-02,  -8.21040000e-02,  -6.38110000e-02,
          1.05330000e-02,   2.85449000e-01,   2.51871000e-01,
          2.87698000e-01,   2.77338000e-01,   2.62878000e-01,
          2.26713000e-01,   1.97565000e-01,   1.18221000e-01,
          8.04140000e-02,   1.02294000e-01,   4.20576000e-01,
          3.73928000e-01,   3.60988000e-01,   2.19703000e-01,
          2.91027000e-01,   2.75491000e-01,   2.89169000e-01,
          2.84376000e-01],
       [  1.10503000e-01,  -3.61730000e-02,  -9.03250000e-02,
         -1.12352000e-01,  -3.77188000e-01,  -2.35289000e-01,
         -2.97462000e-01,  -5.41542000e-01,  -2.30172000e-01,
          5.49400000e-02,   1.21427000e-01,   1.07139000e-01,
          1.35052000e-01,   1.20211000e-01,   1.05682000e-01,
          2.74417000e-01,   2.55812000e-01,   1.83291000e-01,
          1.48973000e-01,   1.66215000e-01,   2.20136000e-01,
          2.18557000e-01,   2.19703000e-01,   3.07330000e-02,
          9.97100000e-02,   8.29990000e-02,   8.71010000e-02,
          9.00510000e-02],
       [  1.86041000e-01,  -9.81140000e-02,  -2.17868000e-01,
         -2.05365000e-01,  -3.33370000e-01,  -1.63455000e-01,
         -2.83424000e-01,  -3.56589000e-01,  -2.57578000e-01,
         -4.80500000e-03,   1.92690000e-01,   1.48580000e-01,
          1.45900000e-01,   1.49480000e-01,   1.27400000e-01,
          3.20370000e-01,   2.68153000e-01,   1.68022000e-01,
          1.12905000e-01,   1.37049000e-01,   3.43350000e-01,
          3.06033000e-01,   2.91027000e-01,   9.97100000e-02,
          2.03079000e-01,   1.73755000e-01,   1.98486000e-01,
          1.85094000e-01],
       [  1.67202000e-01,  -1.08662000e-01,  -2.23785000e-01,
         -2.06810000e-01,  -3.29137000e-01,  -1.80368000e-01,
         -2.89644000e-01,  -3.61771000e-01,  -2.53423000e-01,
         -1.14610000e-02,   1.75253000e-01,   1.33778000e-01,
          1.34502000e-01,   1.45805000e-01,   1.26429000e-01,
          2.94979000e-01,   2.54602000e-01,   1.61825000e-01,
          1.06057000e-01,   1.26308000e-01,   3.17001000e-01,
          2.87089000e-01,   2.75491000e-01,   8.29990000e-02,
          1.73755000e-01,   1.47085000e-01,   1.66521000e-01,
          1.57518000e-01],
       [  1.78034000e-01,  -1.02394000e-01,  -2.19698000e-01,
         -2.00936000e-01,  -3.38457000e-01,  -1.63072000e-01,
         -2.81048000e-01,  -3.57277000e-01,  -2.47969000e-01,
         -1.83500000e-03,   1.90915000e-01,   1.48989000e-01,
          1.48720000e-01,   1.42603000e-01,   1.26875000e-01,
          3.11152000e-01,   2.60781000e-01,   1.65680000e-01,
          1.09660000e-01,   1.31769000e-01,   3.43460000e-01,
          3.00766000e-01,   2.89169000e-01,   8.71010000e-02,
          1.98486000e-01,   1.66521000e-01,   1.90806000e-01,
          1.82873000e-01],
       [  1.74629000e-01,  -1.01631000e-01,  -2.15929000e-01,
         -1.95172000e-01,  -3.39579000e-01,  -1.59599000e-01,
         -2.74992000e-01,  -3.54318000e-01,  -2.40107000e-01,
          7.29100000e-03,   1.82990000e-01,   1.43919000e-01,
          1.46058000e-01,   1.44256000e-01,   1.31166000e-01,
          3.01902000e-01,   2.54735000e-01,   1.64072000e-01,
          1.10392000e-01,   1.26309000e-01,   3.32759000e-01,
          2.98714000e-01,   2.84376000e-01,   9.00510000e-02,
          1.85094000e-01,   1.57518000e-01,   1.82873000e-01,
          1.77431000e-01]]

    return(np.array(mu_pot))
'''
def getMuPotential():
    csvReader = csv.reader(open('trained.dat'))
    
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







