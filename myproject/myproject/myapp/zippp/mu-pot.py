import prody as dy
import csv
import numpy as np
import pudb as dbg
import asa 
import molecule
import time

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
    
    typesHash = dict()
    csvReader = csv.reader(open('chen.typ'))
    
    for row in csvReader:
       split_row = row[0].split()
       atom = str(split_row[0])
       AA_3 = str(split_row[1])
       atom_type = int(split_row[2])
       
       typesHash[AA_3+'_'+atom] = atom_type
    
    return typesHash

def getMuPotential():
    csvReader = csv.reader(open('trained.dat'))
    
    mu_pot = np.zeros([28,28])
    
    for row in csvReader:
       row = row[0].split()
       mu_pot[int(row[0]), int(row[1])] = float(row[2])
       mu_pot[int(row[1]), int(row[0])] = float(row[2])
    
    return mu_pot

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

def evalMuPotential(protein, sa_protein, ligand, sa_ligand, max_distance):
   
    # load in trained mu-Potential from file
    muPotential = getMuPotential()
    
    # load atom types 
    types = getTypes()
    dim = len(np.unique(types.values()))

    # initialize counts matrix  
    countArray = np.zeros([dim,dim])
    
    # get iterator over all contact between protein and ligand
    max_pairs_iter = dy.measure.contacts.iterNeighbors(protein, max_distance, ligand)
    
    surface_contact_atoms = []
    surface_contact_tuple = []

    for contact_tuple in max_pairs_iter:
        
        idx_protein = int(contact_tuple[0].getIndex())
        idx_ligand  = int(contact_tuple[1].getIndex())        
        
        if sa_protein[idx_protein] and sa_ligand[idx_ligand]: 
            atom_0_type = getAtomType(contact_tuple[0])
            atom_1_type = getAtomType(contact_tuple[1])

            # unknown atom types are set to -1      
            if atom_0_type >= 0 and atom_1_type >= 0:
                countArray[int(atom_0_type),int(atom_1_type)] += 1
                tttupp = (contact_tuple[0], contact_tuple[1], atom_0_type, atom_1_type, muPotential[atom_0_type,atom_1_type])
                surface_contact_tuple.append(tttupp)

                if atom_0_type >= atom_1_type:
                    atom_type_min = atom_1_type
                    atom_type_max = atom_0_type
                else:
                    atom_type_min = atom_0_type
                    atom_type_max = atom_1_type
                
                surface_contact_atoms.append((contact_tuple[0].getSerial(), contact_tuple[1].getSerial(), atom_type_min, atom_type_max, muPotential[atom_type_min][atom_type_max]))
   
    sct = sortContactTuple(surface_contact_tuple)
    sca = sortContactAtoms(surface_contact_atoms)

    pdb_id = protein.getTitle().split()[0]
    
    contact_file = 'con_' + pdb_id + '.dat'
    #jm_sca = getJMContacts(contact_file)
    
    return  np.dot(muPotential.flatten(), countArray.flatten())

def getJMContacts(contact_file):

    jm = open(contact_file)
    jm_sca = []
    for jj in jm:
        rr = jj.split()
        jm_sca.append((int(rr[0]), int(rr[1].rstrip(':')), int(rr[2]), int(rr[3]), float(rr[4])))
    return jm_sca

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

def getASA(PDB, pdbname):
    
    # returns (numpy) array of asa of atoms in PDB.
    dy.writePDB(pdbname, PDB) 
    mol = molecule.Molecule(pdbname)
    atoms = mol.atoms()
    molecule.add_radii(atoms)
    
    return np.array(asa.calculate_asa(atoms, 1.4))

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

def scoreBenchmark():

    dy.confProDy(verbosity='none')

    resultsFile = open('mu-scores.txt', 'w+')

    csvReader  = csv.reader(open('mu-pot.out', 'rU'))
    csvReader2 = csv.reader(open('kastritis_bench.csv', 'rU'))

    benchmark_data = dict()
    for row in csvReader2:
        benchmark_data[row[0]] = row[1]
    
    # pop off first row of column headings 
    columns= csvReader.next()

    for row in csvReader:
        dbg.set_trace()
        PDB = dy.parsePDB(str(row[0]))

        chains_list = benchmark_data[row[0]].split(':')
        protein, ligand = getChains(PDB, chains_list[0], chains_list[1])
        complex_pdb = getComplex(PDB, chains_list[0], chains_list[1])
       
        tt = getTypes()
        
        protein_ASA = getASA(protein, row[0]+'_'+chains_list[0]+'.pdb')
        protein_ASA_indicator  = determineSurfaceAtoms(protein, protein_ASA, 0.2)

        ligand_ASA  = getASA(ligand, row[0]+'_'+chains_list[1]+'.pdb')
        ligand_ASA_indicator   = determineSurfaceAtoms(ligand, ligand_ASA, 0.2)
        
        radius = 10

        EC = evalMuPotential(protein, protein_ASA_indicator, ligand, ligand_ASA_indicator, radius)
        
        resultsFile.write(str(row[0]) + ' :  ' + str(EC) + '\n')
        print str(row[0]) + ':  ' + str(EC)

def scoreBenchmark2():
    
    dy.confProDy(verbosity='none')

    resultsFile = open('mu-scores.txt', 'w+')
    csvReader  = csv.reader(open('mu-pot.out', 'rU'))

    for row in csvReader:
        rsplit = row[0].split('=')

        PDB_ID = rsplit[0].split()[0]
        jm_score = float(rsplit[1])
        EC = scoreOne(PDB_ID)
        
        if EC != 'not in bench':
            print  PDB_ID + " Diff: " + str( abs(EC - jm_score)) +  "  My score: " + str(EC) + " JM score: " + str(jm_score) 
            if abs(EC-jm_score) > 0.1:
                resultsFile.write(PDB_ID + " Diff: " + str( abs(EC - float(jm_score))) +  "  My score: " + str(EC) + " JM score: " + str(jm_score) + '\n')

    resultsFile.close()


def scoreOne(PDB_FILENAME):
    
    PDB = dy.parsePDB(PDB_FILENAME)
    csvReader2 = csv.reader(open('kastritis_bench.csv', 'rU'))
    
    benchmark_data = dict()
    for row in csvReader2:
        benchmark_data[row[0]] = row[1]

    asa_reader = csv.reader(open(PDB_FILENAME, 'r'))
    asa_array = []

    for row in asa_reader:
        asa_array.append(float(row[0].split()[-1]))
    
    PDB.setMasses(asa_array)
    
    try: 
        benchmark_data[PDB.getTitle()]
        chains_list = sorted(benchmark_data[PDB.getTitle()].split(':'))
    
    except KeyError:
        return 'not in bench'
        #chains_list = ['A','B']

    #dbg.set_trace()
    protein, ligand  = getChains(PDB, chains_list[0], chains_list[1])
    ligand_ASA_indicator   = determineSurfaceAtoms(ligand, ligand.getMasses(), 0.2)
    protein_ASA_indicator  = determineSurfaceAtoms(protein, protein.getMasses(), 0.2)
  
    EC = evalMuPotential(protein, protein_ASA_indicator, ligand, ligand_ASA_indicator, 10)
    return EC 

def main():
    
    scoreBenchmark2()
    #print scoreOne('dimers/2SIC.pdb')
    #plotMuPotential()

if __name__ == "__main__":
    main()

