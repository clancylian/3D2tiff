import json
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.transform import from_bounds

# 从文件中读取JSON数据
with open('data.json', 'r') as file:
    json_data = json.load(file)

# 初始化x, y, z列表
x = []
y = []
z = []

# 遍历features并提取坐标
for feature in json_data["features"]:
    coordinates = feature["geometry"]["coordinates"]
    x.append(coordinates[0])
    y.append(coordinates[1])
    z.append(coordinates[2])

# 打印结果
# 创建网格点
x_grid = np.linspace(min(x), max(x), 100)
y_grid = np.linspace(min(y), max(y), 100)
x_grid, y_grid = np.meshgrid(x_grid, y_grid)

# 通过插值法计算网格点上的高度值
from scipy.interpolate import griddata
z_grid = griddata((x, y), z, (x_grid, y_grid), method='linear')
z_grid = np.nan_to_num(z_grid, 0)

nan_mask = np.isnan(z_grid)

height=z_grid.shape[0]
width=z_grid.shape[1]

z_grid = z_grid.astype(np.int16)
z_grid = -z_grid

#transform = from_origin(min(x_grid[0]), max(y_grid[:,0]), (max(x_grid[0]) - min(x_grid[0])) / (len(x_grid[0])-1), -((max(y_grid[:,0]) - min(y_grid[:,0])) / (len(y_grid[:,0]) -1)))
transform = from_bounds(min(x_grid[0]), min(y_grid[:,0]), max(x_grid[0]), max(y_grid[:,0]), width, height)
with rasterio.open(
    'terrain.tif',
    'w',
    driver='GTiff',
    height=z_grid.shape[0],
    width=z_grid.shape[1],
    count=1,
    dtype=z_grid.dtype,
    crs='EPSG:4326',
    compress='LZW',
    tiled=True,
    blockxsize=256,
    blockysize=256,
    transform=transform,
    nodata=-10000
) as dst:
    #dst.update_tags(DataType='Generic')
    dst.set_band_description(1, 'Band 1')
    dst.update_tags(AREA_OR_POINT='Area', Band_1='Band 1')
    #dst.update_tags(1, RepresentationType='ATHEMATIC')
    dst.write(z_grid, 1)

# 绘制三维地形图
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')


surf = ax.plot_surface(x_grid, y_grid, z_grid, facecolors=plt.cm.viridis(z_grid / np.max(z_grid)), antialiased=True)

m = plt.cm.ScalarMappable(cmap=plt.cm.viridis)
m.set_array(z_grid)
fig.colorbar(m)

sc = ax.scatter(x, y, z, c=z, cmap='viridis', marker='o')

fig.colorbar(sc, ax=ax, shrink=0.5, aspect=5)

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')

plt.show()



