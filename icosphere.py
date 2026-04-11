'''
Creates a geodesic icosahedron for a given (integer) subdivision frequency,
rather than by recursively applying Loop-like subdivision.

The main advantage of subdivision frequency over recursive subdivision is
better control of mesh resolution. With subdivision frequency, mesh resolution
grows quadratically with nu; with recursive subdivision, it grows
exponentially with the number of iterations.

More precisely, for recursive subdivision (where each iteration corresponds to
nu = 2), the number of vertices after i iterations is
    [12 + 10 * (2**i + 1) * (2**i - 1) for i in range(10)]
which gives
    [12, 42, 162, 642, 2562, 10242, 40962, 163842, 655362, 2621442].
Notice, for example, that there is no mesh with a vertex count between 2562
and 10242.

Using subdivision frequency directly, the number of vertices for a given nu is
    [12 + 10 * (nu + 1) * (nu - 1) for nu in range(1, 33)]
which gives
    [12, 42, 92, 162, 252, 362, 492, 642, 812, 1002, 1212, 1442, 1692, 1962,
     2252, 2562, 2892, 3242, 3612, 4002, 4412, 4842, 5292, 5762, 6252, 6762,
     7292, 7842, 8412, 9002, 9612, 10242]
where nu = 32 gives 10242 vertices, and there are 15 meshes with a vertex count
between 2562 and 10242. The advantage becomes even more pronounced at higher
resolutions.

Author: vand@dtu.dk, 2014, 2017, 2021.
Originally developed in connection with
https://ieeexplore.ieee.org/document/7182720

'''

import numpy as np


def icosphere(nu=1, nr_verts=None):
    '''
    Return a geodesic icosahedron for subdivision frequency `nu`.

    Frequency `nu = 1` returns a regular unit icosahedron, and `nu > 1`
    performs subdivision. If `nr_verts` is given, `nu` is adjusted so the
    generated icosphere contains at least `nr_verts` vertices. Returned faces
    are zero-indexed.

    Parameters
    ----------
    nu : subdivision frequency, integer (larger than 1 to subdivide).
    nr_verts : desired number of mesh vertices; if given, `nu` may be increased.

    Returns
    -------
    vertices : vertex list, numpy array of shape (12 + 10 * (nu+1) * (nu-1), 3)
    faces : face list, numpy array of shape (20 * nu**2, 3)

    '''

    # Unit icosahedron
    vertices, faces = icosahedron()

    # If nr_verts given, computing appropriate subdivision frequency nu.
    # We know nr_verts = 12 + 10 * (nu + 1) * (nu - 1)
    if nr_verts is not None:
        nu_min = int(np.ceil(np.sqrt(max(1 + (nr_verts - 12) / 10, 1))))
        nu = int(max(nu, nu_min))

    # Subdividing
    if nu > 1:
        vertices, faces = subdivide_mesh(vertices, faces, nu)
        vertices = vertices / np.sqrt(np.sum(vertices ** 2, axis=1, keepdims=True))

    return vertices, faces


def icosahedron():
    ''' Regular unit icosahedron. '''

    # 12 principal directions in 3D space: points on a unit icosahedron
    phi = (1 + np.sqrt(5)) / 2
    scale = np.sqrt(1 + phi ** 2)
    vertices = np.array([
        [0, 1, phi], [0, -1, phi], [1, phi, 0],
        [-1, phi, 0], [phi, 0, 1], [-phi, 0, 1]]) / scale
    vertices = np.vstack([vertices, -vertices])

    # 20 faces
    faces = np.array([
        [0, 5, 1], [0, 3, 5], [0, 2, 3], [0, 4, 2], [0, 1, 4],
        [1, 5, 8], [5, 3, 10], [3, 2, 7], [2, 4, 11], [4, 1, 9],
        [7, 11, 6], [11, 9, 6], [9, 8, 6], [8, 10, 6], [10, 7, 6],
        [2, 11, 7], [4, 9, 11], [1, 8, 9], [5, 10, 8], [3, 7, 10]])

    return vertices, faces


def subdivide_mesh(vertices, faces, nu):
    '''
    Subdivides mesh by adding vertices on mesh edges and faces. Each edge
    will be divided in nu segments. (For example, for nu=2 one vertex is added
    on each mesh edge, for nu=3 two vertices are added on each mesh edge and
    one vertex is added on each face.) If V and F are number of mesh vertices
    and number of mesh faces for the input mesh, the subdivided mesh contains
    V + F*(nu+1)*(nu-1)/2 vertices and F*nu^2 faces.

    Parameters
    ----------
    vertices : vertex list, numpy array of shape (V, 3)
    faces : face list, numpy array of shape (F, 3). Zero indexed.
    nu : subdivision frequency, integer (larger than 1 to make a change).

    Returns
    -------
    subvertices : vertex list, numpy array of shape (V + F*(nu+1)*(nu-1)/2, 3)
    subfaces : face list, numpy array of shape (F*nu**2, 3)

    Author: vand at dtu.dk, 8.12.2017. Translated to python 6.4.2021. Cleaned
    code without changing the algorithm 9.4.2026.

    '''

    edges = np.vstack([faces[:, :-1], faces[:, 1:], faces[:, [0, 2]]])
    edges = np.unique(np.sort(edges, axis=1), axis=0)
    num_faces = faces.shape[0]
    num_vertices = vertices.shape[0]
    num_edges = edges.shape[0]
    subfaces = np.empty((num_faces * nu ** 2, 3), dtype=int)
    subvertices = np.empty(
        (num_vertices + num_edges * (nu - 1) + num_faces * (nu - 1) * (nu - 2) // 2, 3)
    )

    subvertices[:num_vertices] = vertices

    # Dictionary for accessing edge index from indices of edge vertices.
    edge_indices = dict()
    for i in range(num_vertices):
        edge_indices[i] = dict()
    for i, edge in enumerate(edges, start=1):
        edge_indices[edge[0]][edge[1]] = i
        edge_indices[edge[1]][edge[0]] = -i

    template = faces_template(nu)
    ordering = vertex_ordering(nu)
    reordered_template = ordering[template]

    # At this point, we have num_vertices vertices, and now we add (nu-1) vertex per edge
    # (on-edge vertices).
    w = np.arange(1, nu) / nu  # interpolation weights
    for e, edge in enumerate(edges):
        for k in range(nu - 1):
            subvertices[num_vertices + e * (nu - 1) + k] = (w[-1 - k] * vertices[edge[0]]
                                                             + w[k] * vertices[edge[1]])

    # At this point we have num_edges(nu-1)+num_vertices vertices, and we add (nu-1)*(nu-2)/2
    # vertices per face (on-face vertices).
    r = np.arange(nu - 1)
    for f in range(num_faces):
        # First, fixing connectivity. We get hold of the indices of all
        # vertices involved in this subface: original, on-edges and on-faces.
        T = np.arange(
            f * (nu - 1) * (nu - 2) // 2 + num_edges * (nu - 1) + num_vertices,
            (f + 1) * (nu - 1) * (nu - 2) // 2 + num_edges * (nu - 1) + num_vertices,
        )
        eAB = edge_indices[faces[f, 0]][faces[f, 1]]
        eAC = edge_indices[faces[f, 0]][faces[f, 2]]
        eBC = edge_indices[faces[f, 1]][faces[f, 2]]
        AB = (abs(eAB) - 1) * (nu - 1) + num_vertices + r
        if eAB < 0:
            AB = AB[::-1]
        AC = (abs(eAC) - 1) * (nu - 1) + num_vertices + r
        if eAC < 0:
            AC = AC[::-1]
        BC = (abs(eBC) - 1) * (nu - 1) + num_vertices + r
        if eBC < 0:
            BC = BC[::-1]
        VEF = np.concatenate([faces[f], AB, AC, BC, T])
        subfaces[f * nu ** 2:(f + 1) * nu ** 2, :] = VEF[reordered_template]
        # Now geometry, computing positions of face vertices.
        subvertices[T, :] = inside_points(subvertices[AB, :], subvertices[AC, :])

    return subvertices, subfaces


def faces_template(nu):
    '''
    Template for linking subfaces                  0
    in a subdivision of a face.                   / \
    Returns faces with vertex                    1---2
    indexing given by reading order             / \ / \
    (as illustrated).                          3---4---5
                                              / \ / \ / \
                                             6---7---8---9
                                            / \ / \ / \ / \
                                           10--11--12--13--14
    '''

    faces = []
    # looping in layers of triangles
    for i in range(nu):
        vertex0 = i * (i + 1) // 2
        skip = i + 1
        for j in range(i):  # adding pairs of triangles, will not run for i==0
            faces.append([j + vertex0, j + vertex0 + skip, j + vertex0 + skip + 1])
            faces.append([j + vertex0, j + vertex0 + skip + 1, j + vertex0 + 1])
        # adding the last (unpaired, rightmost) triangle
        faces.append([i + vertex0, i + vertex0 + skip, i + vertex0 + skip + 1])

    return np.array(faces)


def vertex_ordering(nu):
    '''
    Permutation for ordering of                    0
    face vertices which transforms                / \
    reading-order indexing into indexing         3---6
    first corners vertices, then on-edges       / \ / \
    vertices, and then on-face vertices        4---12--7
    (as illustrated).                         / \ / \ / \
                                             5---13--14--8
                                            / \ / \ / \ / \
                                           1---9--10--11---2
    '''

    left = list(range(3, nu + 2))
    right = list(range(nu + 2, 2 * nu + 1))
    bottom = list(range(2 * nu + 1, 3 * nu))
    inside = list(range(3 * nu, (nu + 1) * (nu + 2) // 2))

    o = [0]  # topmost corner
    for i in range(nu - 1):
        o.append(left[i])
        o = o + inside[i * (i - 1) // 2:i * (i + 1) // 2]
        o.append(right[i])
    o = o + [1] + bottom + [2]

    return np.array(o)


def inside_points(vAB, vAC):
    '''
    Returns coordinates of the inside                 .
    (on-face) vertices (marked by star)              / \
    for subdivision of the face ABC when         vAB0---vAC0
    given coordinates of the on-edge               / \ / \
    vertices  AB[i] and AC[i].                 vAB1---*---vAC1
                                                 / \ / \ / \
                                             vAB2---*---*---vAC2
                                               / \ / \ / \ / \
                                              .---.---.---.---.
    '''

    out = []
    u = vAB.shape[0]
    for i in range(0 if u == 1 else 1, u):
        # Interpolate points on the segment between vAB[i] and vAC[i], excluding endpoints.
        j = i + 1
        interp = (np.arange(1, j) / j)[:, None]
        out.append(
            np.multiply(interp, vAC[i, None])
            + np.multiply(1 - interp, vAB[i, None])
        )

    return np.concatenate(out)
