# Geodesic icosahedron 

Creating geodesic icosahedron given subdivision frequency. 

## Installation
Install the module using ```pip install icosphere``` or clone the repository.

## Use
``` python
from icosphere import icosphere
nu = 5  # or any other integer
vertices, faces = icosphere(nu)
```
## Examples
Check the examples in [icosphere github](https://github.com/vedranaa/icosphere), python script uses matplotlib for visualization, and jupyter notebook uses plotly.

## Why use subdivision frequency?
For a certain subdivision frequency `nu`, each edge of the icosahedron will be split into `nu` segments, and each face will be split into `nu**2` faces.

![](https://github.com/vedranaa/icosphere/raw/main/Figure.png)

This is different than a more common approach which recursively applies a subdivision with `nu = 2`, for example as used in pytorch3d [ico_sphere](https://github.com/facebookresearch/pytorch3d/blob/master/pytorch3d/utils/ico_sphere.py), pymeshlab [sphere](https://pymeshlab.readthedocs.io/en/latest/filter_list.html#sphere), trimesh [icosphere](https://trimsh.org/trimesh.creation.html?highlight=icosahedron#trimesh.creation.icosphere), and PyMesh [generate_icosphere](https://github.com/PyMesh/PyMesh/blob/384ba882b7558ba6e8653ed263c419226c22bddf/python/pymesh/meshutils/generate_icosphere.py).

The advantage of using the subdivision frequency, compared to the recursive subdivision, is in controlling the mesh resolution. Mesh resolution grows quadratically with subdivision frequencies while it grows exponentially with iterations of the recursive subdivision. To be precise, using the recursive subdivision, the number of vertices and faces in the resulting icosphere grows with iterations `iter` as 
`nr_vertex = 12 + 10 * (4**iter -1)` and `nr_face = 10 * 4**iter`
which gives a sequence of mesh vertices

    12, 42, 162, 642, 2562, 10242, 40962, 163842, 655362, 2621442, 10485762... 

Notice for example there is no mesh having between 2562 and 10242 vertices. Using subdivision frequency, the number of vertices and faces grows with `nu` as
Notice for example there is no mesh having between 2562 and 10242 vertices. Using subdivision frequency, the number of vertices and faces grows with `nu` as
 `nr_vertex = 12 + 10 * (nu**2 -1)` and `nr_face = 20 * nu**2`
which gives a sequence of mesh vertices 
    
     12, 42, 92, 162, 252, 362, 492, 642, 812, 1002, 1212, 1442, 1692, 1962, 
     2252, 2562, 2892, 3242, 3612, 4002, 4412, 4842, 5292, 5762, 6252, 6762, 
     7292, 7842, 8412, 9002, 9612, 10242...

Now there is 15 meshes having between 2562 and 10242 vertices. The advantage is even more pronounced when using higher resolutions.

The code was originally developed for [this work](https://ieeexplore.ieee.org/document/7182720).
