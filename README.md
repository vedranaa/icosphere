# Geodesic Icosahedron
Creates a geodesic icosahedron given a subdivision frequency.

[![PyPI Downloads](https://static.pepy.tech/personalized-badge/icosphere?period=total&units=INTERNATIONAL_SYSTEM&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/icosphere)

## Installation
Install with `pip install icosphere`, or clone this repository.

## Usage
```python
from icosphere import icosphere
nu = 5  # or any other integer
vertices, faces = icosphere(nu)
```

## Examples
See examples in the [icosphere GitHub repository](https://github.com/vedranaa/icosphere):
- `example_in_matplotlib.py` uses matplotlib for visualization.
- `Example_in_plotly.ipynb` uses plotly for interactive visualization.

You can also open the notebooks in Colab:
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vedranaa/icosphere/blob/main/Example_in_plotly.ipynb) - plotly
- [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/vedranaa/icosphere/blob/main/Example_in_matplotlib.ipynb) - matplotlib

## Why use subdivision frequency?
For a certain subdivision frequency `nu`, each edge of the icosahedron will be split into `nu` segments, and each face will be split into `nu**2` faces.
![](https://github.com/vedranaa/icosphere/raw/main/Figure.png)
This is different from a more common approach that recursively applies subdivision with `nu = 2`, as used in pytorch3d [ico_sphere](https://github.com/facebookresearch/pytorch3d/blob/master/pytorch3d/utils/ico_sphere.py), pymeshlab [sphere](https://pymeshlab.readthedocs.io/en/latest/filter_list.html#sphere), trimesh [icosphere](https://trimsh.org/trimesh.creation.html?highlight=icosahedron#trimesh.creation.icosphere), and PyMesh [generate_icosphere](https://github.com/PyMesh/PyMesh/blob/384ba882b7558ba6e8653ed263c419226c22bddf/python/pymesh/meshutils/generate_icosphere.py).

The subdivision-frequency approach gives better control of mesh resolution than recursive subdivision. In this approach, mesh resolution grows quadratically with `nu`, while in recursive subdivision it grows exponentially with the number of iterations. More precisely, under recursive subdivision, the number of vertices and faces in the resulting icosphere grows with iterations `iter` as `nr_vertex = 12 + 10 * (4**iter - 1)` and `nr_face = 10 * 4**iter`, which gives the sequence of vertex counts

    12, 42, 162, 642, 2562, 10242, 40962, 163842, 655362, 2621442, 10485762...
Notice, for example, that there is no mesh with a vertex count between 2562 and 10242. Using subdivision frequency, the number of vertices and faces grows with `nu` as `nr_vertex = 12 + 10 * (nu**2 - 1)` and `nr_face = 20 * nu**2`, which gives the sequence of vertex counts

     12, 42, 92, 162, 252, 362, 492, 642, 812, 1002, 1212, 1442, 1692, 1962,
     2252, 2562, 2892, 3242, 3612, 4002, 4412, 4842, 5292, 5762, 6252, 6762,
     7292, 7842, 8412, 9002, 9612, 10242...
Now there are 15 meshes with vertex counts between 2562 and 10242. The advantage is even more pronounced at higher resolutions.

The code was originally developed for [this work](https://ieeexplore.ieee.org/document/7182720).

## Reference this work
Dahl, V. A., Dahl, A. B., & Larsen, R. (2014). Surface Detection Using Round Cut. 2014 2nd International Conference on 3D Vision. https://doi.org/10.1109/3dv.2014.60

```bibtex
@inproceedings{Dahl_2014,
	doi = {10.1109/3dv.2014.60},
	url = {https://doi.org/10.1109%2F3dv.2014.60},
	year = 2014,
	month = {dec},
	publisher = {{IEEE}},
	author = {Vedrana A. Dahl and Anders B. Dahl and Rasmus Larsen},
	title = {Surface Detection Using Round Cut},
	booktitle = {2014 2nd International Conference on 3D Vision}
}
```
