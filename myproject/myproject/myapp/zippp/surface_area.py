import prody as dy
import numpy as np
import math

def getRadiiDict():

    return {
     'H': 1.20, 'N': 1.55, 'NA': 2.27,'CU': 1.40,
     'CL': 1.75, 'C': 1.70, 'O': 1.52, 'I': 1.98, 'P': 1.80,
     'B': 1.85, 'BR': 1.85, 'S': 1.80, 'SE': 1.90, 'F': 1.47,
     'FE': 1.80, 'K':  2.75, 'MN': 1.73, 'MG': 1.73, 'ZN': 1.39,
     'HG': 1.8, 'XE': 1.8, 'AU': 1.8, 'LI': 1.8, '.': 1.8
    }

def getAtomRadii(AG):

    radii = getRadiiDict()
    pdb_radii =[]

    for a in AG:
        try:
            r = radii[a.getElement()]
        except KeyError:
            print a.getElement()
            r = radii['.']
        pdb_radii.append(r)

    # return [radii[a.getElement()] for a in pdb]
    return pdb_radii

def generate_sphere_points(n):
    """
    Returns list of 3d coordinates of points on a sphere using the
    Golden Section Spiral algorithm.
    """
    points = []
    inc = math.pi * (3 - math.sqrt(5))
    offset = 2 / float(n)
    for k in range(int(n)):
        y = k * offset - 1 + (offset / 2)
        r = math.sqrt(1 - y*y)
        phi = k * inc
        points.append([math.cos(phi)*r, y, math.sin(phi)*r])
    return points

def find_neighbor_indices(atoms, probe, k):
    """
    Returns list of indices of atoms within probe distance to atom k.
    """
    coords_all = atoms.getCoords()
    neighbor_indices = []
    atom_k = atoms[k]
    radius = atom_k.getRadius() + probe + probe

    indices = range(k)
    indices.extend(range(k+1, len(atoms)))

    for i in indices:
	dist = pos_distance(coords_all[k], coords_all[i])
	#dist = np.linalg.norm(coords_all[k] -  coords_all[i])
	if dist < radius + atoms[i].getRadius():
            neighbor_indices.append(i)

    return neighbor_indices

def pos_distance(p1, p2):
    return math.sqrt(pos_distance_sq(p2, p1))

def pos_distance_sq(p1, p2):
    x = p1[0] - p2[0]
    y = p1[1] - p2[1]
    z = p1[2] - p2[2]
    return x*x + y*y + z*z;

def calcASA(atoms, probe=1.4, n_sphere_point=960):
    """
    Returns list of accessible surface areas of the atoms, using the probe
    and atom radius to define the surface.

    """
    atoms.setRadii(getAtomRadii(atoms))

    sphere_points = generate_sphere_points(n_sphere_point)
    const = 4.0 * math.pi / len(sphere_points)

    test_point = [0.0, 0.0, 0.0]
    areas = []

    coords_all = atoms.getCoords()

    for i, atom_i in enumerate(atoms):

        neighbor_indices = find_neighbor_indices(atoms, probe, i)
        n_neighbor = len(neighbor_indices)
        j_closest_neighbor = 0
        radius = probe + atom_i.getRadius()

        n_accessible_point = 0
        for point in sphere_points:
            is_accessible = True
	    test_point = np.dot(point,radius) + coords_all[i]
            cycled_indices = range(j_closest_neighbor, n_neighbor)
            cycled_indices.extend(range(j_closest_neighbor))

            for j in cycled_indices:
                atom_j = atoms[neighbor_indices[j]]
                r = atom_j.getRadius() + probe
                #diff_sq = np.linalg.norm(coords_all[neighbor_indices[j]] - test_point)
                diff_sq = pos_distance_sq(coords_all[neighbor_indices[j]], test_point)
		if diff_sq < r*r:
                    j_closest_neighbor = j
                    is_accessible = False
                    break
	    if is_accessible:
                n_accessible_point += 1

        area = const*n_accessible_point*radius*radius
        areas.append(area)
	#print str(atom_i.getResnum()) + " " + atom_i.getResname() + " " + str(area)
    return areas



