import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.ndimage import binary_erosion

# File Path
file_location = # Insert File Path Here
script_dir = os.getcwd()
output_dir = os.path.join(script_dir, "outputs")
os.makedirs(output_dir, exist_ok=True)

# Scale pixels to lengths
height_max = 115  # nm
height_min = 0
image_length = 10.98  # μm

# Load image and convert to float array
image = Image.open(file_location).convert('L')
image_array = np.array(image).astype(np.float64)

pixels_z, pixels_x = image_array.shape
dx_nm = (image_length / (pixels_x - 1)) * 1000  # nm

# Coordinates
x = np.linspace(0, image_length, pixels_x)
z = np.linspace(0, image_length, pixels_z)
X, Z = np.meshgrid(x, z)

# Normalize grayscale to height
Y_norm = image_array / image_array.max()
Y_height = Y_norm * (height_max - height_min) + height_min
dy_dx, dy_dz = np.gradient(Y_height, dx_nm)

# Create mask To remove background

mask = np.array(binary_erosion([[val != 0 for val in row] for row in Y_height]))

# Strain components - von Karman Strain Components
epsilon_xx = 0.5 * dy_dx**2
epsilon_zz = 0.5 * dy_dz**2
epsilon_xz = 0.5 * dy_dx * dy_dz
# von Mises Magnitude of 2D strain
strain_profile = np.sqrt(epsilon_xx**2 + epsilon_zz**2 + 2 * epsilon_xz**2)

# Apply the mask

strain_profile[~mask] = 0

# Plot colour map

plt_colour = "hot"

plt.figure(figsize=(8, 6))
plt.imshow(strain_profile, cmap=plt_colour, extent=[0, image_length, 0, image_length], origin='lower', vmax=0.05)
plt.colorbar(label='Estimated Strain')
plt.title('Strain Map')
plt.xlabel('x (μm)')
plt.ylabel('z (μm)')
plt.tight_layout()

# Output to file

color_map_path = os.path.join(output_dir, "strain_map.png")
plt.savefig(color_map_path, dpi=300)
plt.show()
plt.close()

# # Plot 3D map

# fig = plt.figure(figsize=(10, 8))
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_surface(X, Z, strain_profile, cmap=plt_colour, linewidth=0, antialiased=False)
# ax.set_title('Strain map')
# ax.set_xlabel('x (μm)')
# ax.set_ylabel('z (μm)')
# ax.set_zlabel('Estimated Strain')
# plt.tight_layout()

# # Output to file

# surface_plot_path = os.path.join(output_dir, "height_map_3D.png")
# plt.savefig(surface_plot_path, dpi=300)
# plt.show()
# plt.close()
