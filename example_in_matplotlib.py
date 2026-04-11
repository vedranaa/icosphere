'''
An example of using icosphere module. Plots the icosphere in matplotlib showing
with color the original icosahedron faces.

'''
from icosphere import icosphere
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure()
light_source = matplotlib.colors.LightSource(azdeg=60, altdeg=30)

for nu in range(1, 7):

    vertices, faces = icosphere(nu=nu)

    # Basic mesh colors divided in 20 groups (one for each original face).
    colors = matplotlib.cm.tab20(np.linspace(0, 1, 20))[:, :3]
    colors = np.tile(colors, (1, faces.shape[0] // 20)).reshape(faces.shape[0], 1, 3)

    # Compute face shading intensity from normalized face normals.
    face_normals = np.cross(
        vertices[faces[:, 1]] - vertices[faces[:, 0]],
        vertices[faces[:, 2]] - vertices[faces[:, 0]],
    )
    face_normals /= np.linalg.norm(face_normals, axis=1, keepdims=True)
    intensity = light_source.shade_normals(face_normals)

    # Blend base colors with shading and add alpha channel.
    rgb = light_source.blend_hsv(rgb=colors, intensity=intensity.reshape(-1, 1, 1))
    alpha = np.full((rgb.shape[0], 1, 1), 0.9)
    rgba = np.concatenate((rgb, alpha), axis=2)

    poly = Poly3DCollection(vertices[faces])
    poly.set_facecolor(rgba.reshape(-1, 4))
    poly.set_edgecolor('black')
    poly.set_linewidth(0.25)

    ax = fig.add_subplot(2, 3, nu, projection='3d')

    ax.add_collection3d(poly)

    ax.set(xlim=(-1, 1), ylim=(-1, 1), zlim=(-1, 1))

    ax.set(xticks=[-1, 0, 1], yticks=[-1, 0, 1], zticks=[-1, 0, 1])
    ax.set_box_aspect((1, 1, 1))

    ax.set_title(f'nu={nu}')

fig.suptitle('Icospheres with different subdivision frequency')
plt.tight_layout()
plt.subplots_adjust(hspace=0.4)
# fig.savefig('Figure.png', dpi=150, bbox_inches='tight')  # TODO: remove
plt.show()



