#!/usr/bin/env python

"""
Routines to calculate the Accessible Surface Area of a set of atoms.
The algorithm is adapted from the Rose lab's chasa.py, which uses
the dot density technique found in:

Shrake, A., and J. A. Rupley. "Environment and Exposure to Solvent
of Protein Atoms. Lysozyme and Insulin." JMB (1973) 79:351-371.
"""

import numpy as np
import math
#import pdb as dbg
from scipy.spatial.distance import cdist


def get_radii_from_prody_pdb(pdb):
    '''
    This is a helper function to avoid using the molecule
    class and handle AtomGroup classes from prody after
    a parsePDB loads a PDB from disk.
    '''

    #Keep import local as prody has lots of junk
    import prody as pr

    #Avoiding another static file in the web app
    atom_radii = { 
    'H': 1.20,
    'N': 1.55,
    'NA': 2.27,
    'CU': 1.40,
    'CL': 1.75,
    'C': 1.70,
    'O': 1.52,
    'I': 1.98,
    'P': 1.80,
    'B': 1.85,
    'BR': 1.85,
    'S': 1.80,
    'SE': 1.90,
    'F': 1.47,
    'FE': 1.80,
    'K':  2.75,
    'MN': 1.73,
    'MG': 1.73,
    'ZN': 1.39,
    'HG': 1.8,
    'XE': 1.8,
    'AU': 1.8,
    'LI': 1.8,
    '.': 1.8
    }

    two_char_elements = [el for el, r in atom_radii.items() if len(el) == 2]

    names = pdb.getNames()

    elements = []

    for name in names:
        element = ''
        for c in name:
            if not c.isdigit() and c != " ":
                element += c
        if element[:2] in two_char_elements:
            element = element[:2]
        else:
            element = element[0]
        elements.append(element)

    radii = []
    for element in elements:
        if element in atom_radii:
            r = atom_radii[element]
        else:
            r = atom_radii['.']
        radii.append(r)

    return(np.array(radii))


def generate_sphere_points(n):
    """
    Returns list of 3d coordinates of points on a sphere using the
    Golden Section Spiral algorithm.
    """
    points = []
    inc = np.pi * (3 - np.sqrt(5))
    offset = 2 / float(n)

    #This should be updated
    for k in xrange(int(n)):
        y = k * offset - 1 + (offset / 2)
        r = math.sqrt(1 - y*y)
        phi = k * inc
        points.append([np.cos(phi)*r, y, np.sin(phi)*r])

    return np.array(points)


def find_neighbor_indices_np(points, radii, probe, k):
    """
    Returns list of indices of atoms within probe distance to atom k
    leveraging numpy for accelerated calculations.  This implementation
    is about 10x faster than the original.
    """

    radius = radii[k] + probe + probe
    radii = (radii + radius) **2

    #computes the squared distance between al atoms and the current atom
    #of interest (kth atom).
    #In fact, for further acceleration, this should be pulled out and done
    #once for all atom pairs  
    dist_sq = np.dot(((points - points[k,:])** 2), np.ones(3))

    dist_sq = (dist_sq < radii)

    #Since the distance to itself should be less than radii, must remove
    #self distance
    dist_sq[k] = False

    return dist_sq

    #alternative implementation but slightly slower than the above
    #neighbor_indices = np.where(dist_sq)[0]
    #neighbor_indices = neighbor_indices[ neighbor_indices!= k]
    #return neighbor_indices 


def find_neighbor_indices_np2(dist_sq, radii, probe, k):
    """
    Returns list of indices of atoms within probe distance to atom k
    leveraging numpy for accelerated calculations.  This implementation
    is about 10x faster than the original.
    """

    radius = radii[k] + probe + probe
    radii = (radii + radius) **2

    #computes the squared distance between al atoms and the current atom
    #of interest (kth atom).
    #In fact, for further acceleration, this should be pulled out and done
    #once for all atom pairs
    #And I have now implemented that (about an 8% speed up)
    #dist_sq = np.dot(((points - points[k,:])** 2), np.ones(3))

    dist_sq = (dist_sq < radii)

    #Since the distance to itself should be less than radii, must remove
    #self distance
    dist_sq[k] = False

    return dist_sq


#@profile
def calculate_asa_np(pdb, probe, n_sphere_point=960):
    """
    Returns list of accessible surface areas of the atoms, using the probe
    and atom radius to define the surface.
    """
    sphere_points = generate_sphere_points(n_sphere_point)

    #points = np.array([ [a.pos.x, a.pos.y, a.pos.z] for a in atoms ])
    points = pdb.getCoords()

    radii = get_radii_from_prody_pdb(pdb)

    #radii = np.array([a.radius for a in atoms])
    radii_plus_probe_sq = (radii + probe)**2

    dist_matrix_sq = cdist(points, points, 'sqeuclidean')

    const = 4.0 * math.pi / n_sphere_point

    areas = np.zeros(len(pdb))

    for i in xrange(0,len(pdb)):

        neighbor_indices = find_neighbor_indices_np2(dist_matrix_sq[i,:], radii, probe, i)

        radius = probe + radii[i]

        point_i = points[i, :]

        test_sphere_points = sphere_points*radius + point_i

        neighbor_points = points[neighbor_indices, :]

        neighbor_radii_sq = radii_plus_probe_sq[neighbor_indices]

        diff_sq = cdist(test_sphere_points, neighbor_points, 'sqeuclidean')

        dist_test = (diff_sq < neighbor_radii_sq)

        #This stupid summation is one of the slowest pieces
        accessible_points = np.sum(dist_test,1)

        #area = sum(accessible_points==0) * const * radius * radius
        area = (n_sphere_point - np.count_nonzero(accessible_points)) * const * radius * radius
        areas[i] = area

        #areas.append(area)

    return areas


def main():
    import sys
    import getopt
    import csv
    import prody as pr


    #usage = \
    """

    Copyright (c) 2007 Bosco Ho

    Calculates the total Accessible Surface Area (ASA) of atoms in a
    PDB file.

    Usage: asa.py -s n_sphere in_pdb [out_pdb]

    - out_pdb    PDB file in which the atomic ASA values are written
                 to the b-factor column.

    -s n_sphere  number of points used in generating the spherical
                 dot-density for the calculation (default=960). The
                 more points, the more accurate (but slower) the
                 calculation.

    """

    #opts, args = getopt.getopt(sys.argv[1:], "n:")
    #if len(args) < 1:
    #    print usage
    #    return



    #mol = molecule.Molecule(args[0])
    #pdb = molecule.Molecule('dimers/1R0R.pdb')
    pdb = pr.parsePDB('dimers/1R0R.pdb')

    #atoms = mol.atoms()
    #molecule.add_radii(atoms)

    data = []

    #for o, a in opts:
    #    if '-n' in o:
    #        n_sphere = int(a)
    #        print "Points on sphere: ", n_sphere
    #
    #n_sphere = [500]
    n_sphere = range(10,2000,10)
    for n in n_sphere:
        asas = calculate_asa_np(pdb, 1.4, n)
        data.append(asas)
        #print "%i, %.1f angstrom squared." % n, sum(asas)
        print(str(n) + ", " + str(sum(asas)) + " angstrom squared.")

    f_test = open('perturbation_analysis.csv','w')
    c = csv.writer(f_test)
    for i in xrange(len(data)):
        c.writerow(data[i])

    #f_test.close()

    #if len(args) > 1:
    #    for asa, atom in zip(asas, atoms):
    #        atom.bfactor = asa
    #    mol.write_pdb(args[1])


if __name__ == "__main__":
    print "in main"
    main()


#Below shows the evolution of each function
#DO NOT DELETE!

'''
def generate_sphere_points_np(n):
    """
    Returns list of 3d coords of points on a sphere using
    the Golden Section Spiral Algorithm as above but
    leveraging the numpy library.
    However, the array is the wrong shape so this code 
    is not used
    """

    inc = np.pi * (3 - np.sqrt(5))
    offset = 2 / float(n)

    k = np.arange(n)
    y = k * offset - 1 + (offset/2)
    r = np.sqrt(1-y*y)
    phi = k * inc

    points = [ np.cos(phi)*r, y, np.sin(phi)*r]

    return(points)
'''

'''
def find_neighbor_indices(atoms, probe, k):
    """
    Returns list of indices of atoms within probe distance to atom k.
    """
    neighbor_indices = []
    atom_k = atoms[k]

    #pulling these out of the inner most loop for performance reasons
    atom_k_pos_x = atom_k.pos.x
    atom_k_pos_y = atom_k.pos.y
    atom_k_pos_z = atom_k.pos.z

    radius = atom_k.radius + probe + probe

    indices = range(k)
    indices.extend(range(k+1, len(atoms)))

    for i in indices:
        atom_i = atoms[i]
        r = radius + atom_i.radius
        #dist = pos_distance(atom_k.pos, atom_i.pos)
        dist_sq = (atom_k_pos_x - atom_i.pos.x)**2 + (atom_k_pos_y - atom_i.pos.y)**2 + (atom_k_pos_z - atom_i.pos.z)**2
        #if dist < radius + atom_i.radius:
        if (dist_sq < (r*r)):
            neighbor_indices.append(i)

    return neighbor_indices
'''

'''
#@profile
def calculate_asa_original(atoms, probe, n_sphere_point=960):
    """
    Returns list of accessible surface areas of the atoms, using the probe
    and atom radius to define the surface.
    """
    sphere_points = generate_sphere_points(n_sphere_point)

    const = 4.0 * math.pi / len(sphere_points)
    #test_point = Vector3d()
    areas = []
    for i, atom_i in enumerate(atoms):

        neighbor_indices = find_neighbor_indices(atoms, probe, i)
        n_neighbor = len(neighbor_indices)
        j_closest_neighbor = 0
        radius = probe + atom_i.radius

        atom_i_pos_x = atom_i.pos.x
        atom_i_pos_y = atom_i.pos.y
        atom_i_pos_z = atom_i.pos.z

        n_accessible_point = 0
        for point in sphere_points:
            is_accessible = True

            test_point_x = point[0]*radius + atom_i_pos_x
            test_point_y = point[1]*radius + atom_i_pos_y
            test_point_z = point[2]*radius + atom_i_pos_z

            cycled_indices = range(j_closest_neighbor, n_neighbor)
            cycled_indices.extend(range(j_closest_neighbor))

            for j in cycled_indices:
                atom_j = atoms[neighbor_indices[j]]
                r = atom_j.radius + probe
                #diff_sq = pos_distance_sq(atom_j.pos, test_point)
                diff_sq = (atom_j.pos.x - test_point_x)**2 + (atom_j.pos.y - test_point_y)**2 + (atom_j.pos.z - test_point_z)**2
                if diff_sq < r*r:
                    j_closest_neighbor = j
                    is_accessible = False
                    break
            if is_accessible:
                n_accessible_point += 1

        area = const*n_accessible_point*radius*radius
        areas.append(area)
    #print str(atom_i.res_num) + " " + atom_i.res_type + " " + str(area)
    return areas
'''

'''
#@profile
def calculate_asa_np_old(atoms, probe, n_sphere_point=960):
    """
    Returns list of accessible surface areas of the atoms, using the probe
    and atom radius to define the surface.
    """
    sphere_points = generate_sphere_points(n_sphere_point)

    radii = np.array([a.radius for a in atoms])
    points = np.array([ [a.pos.x, a.pos.y, a.pos.z] for a in atoms ])


    const = 4.0 * math.pi / len(sphere_points)

    #test_point = Vector3d()
    areas = []
    for i, atom_i in enumerate(atoms):

        neighbor_indices = find_neighbor_indices_np(points, radii, probe, i)

        n_neighbor = len(neighbor_indices)
        j_closest_neighbor = 0
        radius = probe + radii[i]

        #atom_i_pos_x = atom_i.pos.x
        #atom_i_pos_y = atom_i.pos.y
        #atom_i_pos_z = atom_i.pos.z
        point_i = points[i,:]

        n_accessible_point = 0
        for point in sphere_points:
            is_accessible = True

            test_point = point*radius + point_i

            #test_point_x = point[0]*radius + atom_i_pos_x
            #test_point_y = point[1]*radius + atom_i_pos_y
            #test_point_z = point[2]*radius + atom_i_pos_z

            cycled_indices = range(j_closest_neighbor, n_neighbor)
            cycled_indices.extend(range(j_closest_neighbor))


            neighbor_points = points[neighbor_indices, :]
            neighbor_radii_sq = (radii[neighbor_indices] + probe)**2

            diff_sq = np.dot((( neighbor_points - test_point)** 2), np.ones(3))
            dist_test = (diff_sq< neighbor_radii_sq)
            if dist_test.sum()==0:
                n_accessible_point += 1

        area = const*n_accessible_point*radius*radius
        areas.append(area)
    return areas
'''

'''
def calculate_asa_np_fast(atoms, probe, n_sphere_point=960):
    """
    Returns list of accessible surface areas of the atoms, using the probe
    and atom radius to define the surface.
    """
    sphere_points = generate_sphere_points(n_sphere_point)

    radii = np.array([a.radius for a in atoms])
    radii_plus_probe_sq = (radii + probe)**2

    points = np.array([ [a.pos.x, a.pos.y, a.pos.z] for a in atoms ])

    const = 4.0 * math.pi / len(sphere_points)

    #test_point = Vector3d()
    areas = []
    for i, atom_i in enumerate(atoms):

        neighbor_indices = find_neighbor_indices_np(points, radii, probe, i)

        n_neighbor = len(neighbor_indices)
        j_closest_neighbor = 0
        radius = probe + radii[i]

        point_i = points[i, :]

        test_sphere_points = sphere_points*radius + point_i

        neighbor_points = points[neighbor_indices, :]
        neighbor_radii_sq = radii_plus_probe_sq[neighbor_indices]

        n_accessible_point = 0
        #for point in sphere_points:
        for test_point in test_sphere_points:
            diff_sq = np.dot((( neighbor_points - test_point)** 2), np.ones(3))
            dist_test = (diff_sq< neighbor_radii_sq)
            #if dist_test.sum()==0:
            if not(any(dist_test)):
                n_accessible_point += 1

        area = const*n_accessible_point*radius*radius
        areas.append(area)
    return areas
'''
