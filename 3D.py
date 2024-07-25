# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import numpy as np

# # 示例数据：三维点坐标
# # 你可以用你自己的数据替换这些示例数据
# x = np.random.rand(100) * 10
# y = np.random.rand(100) * 10
# z = np.random.rand(100) * 10

# print(x)

# # 创建网格点
# x_grid = np.linspace(min(x), max(x), 50)
# y_grid = np.linspace(min(y), max(y), 50)
# x_grid, y_grid = np.meshgrid(x_grid, y_grid)

# #print(x_grid)

# # 通过插值法计算网格点上的高度值
# from scipy.interpolate import griddata
# z_grid = griddata((x, y), z, (x_grid, y_grid), method='cubic')

# # 绘制三维地形图
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # 绘制地形图
# ax.plot_surface(x_grid, y_grid, z_grid, cmap='viridis')

# # 添加散点图
# ax.scatter(x, y, z, color='r')

# # 设置轴标签
# ax.set_xlabel('X axis')
# ax.set_ylabel('Y axis')
# ax.set_zlabel('Z axis')

# plt.show()


# import matplotlib.pyplot as plt
# from osgeo import gdal

# dataset = gdal.Open('terrain.tif')

# band = dataset.GetRasterBand(1)
# data = band.ReadAsArray()

# plt.imshow(data, cmap='viridis')
# plt.colorbar()
# plt.title("ssda")
# iplt.imshow()


import rasterio
import matplotlib.pyplot as plt

with rasterio.open('terrain.tif') as dataset:

    data = dataset.read()

print(data)
print(data.shape)

# 可视化数据
# plt.imshow(data, cmap='viridis')
# plt.colorbar()
# plt.title('Terrain Data')
# plt.show()


middle_slice = data[0, :, :]
plt.imshow(middle_slice, cmap='viridis')
plt.colorbar()
plt.title("111")
plt.show()


from mayavi import mlab

volume = data

print(volume.shape)

mlab.figure(size=(100,100))
mlab.volume_slice(volume, plane_orientation='x_axes', slice_index=volume.shape[0])
mlab.volume_slice(volume, plane_orientation='y_axes', slice_index=volume.shape[1])
mlab.volume_slice(volume, plane_orientation='z_axes', slice_index=volume.shape[2])
mlab.colorbar(title="saca", orientation="vertical")
mlab.show()

# import pyvista as pv
# import numpy as np

# volume = data[0]
# print(volume)

# grid = pv.UniformGrid()
# grid.dimensions = 2
# grid.origin = (0,0,0)
# grid.spacing = (1,1,1)
# grid.point_arrays['values'] = volume.flatten(ordder='F')

# plotter = pv.Plotter()
# plotter.add_volume(grid, cmap='viridis')
# plotter.show()