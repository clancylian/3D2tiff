from flask import Flask, request, jsonify
import json
import numpy as np
import rasterio
from rasterio.transform import from_bounds
import os

app = Flask(__name__)

@app.route("/3d2tiff", methods=['POST'])
def tiff():
    data = request.get_json()
    fileurl = data.get('fileurl')
    if fileurl is None:
        return { 'status' : 400, 'message' : 'fileurl is empty', 'data': {}},400

    pixel_size = data.get('pixelsize')
    if pixel_size is None or pixel_size=='' or pixel_size <= 0:
        pixel_size = 0.000576639388

    # 从文件中读取JSON数据
    try:
        with open(fileurl, 'r') as file:
            json_data = json.load(file)
    except Exception as e:
        return { 'status' : 400, 'message' : 'open file failed', 'data': {}},400

    # 初始化x, y, z列表
    x = []
    y = []
    z = []

    try:
        # 遍历features并提取坐标
        for feature in json_data["features"]:
            coordinates = feature["geometry"]["coordinates"]
            x.append(coordinates[0])
            y.append(coordinates[1])
            z.append(coordinates[2])
    except Exception as e:
        return { 'status' : 400, 'message' : 'read data file failed', 'data': {}},400

    pixel_size = 0.000576639388
    nx = int((max(x) - min(x)) / pixel_size)
    ny = int((max(y) - min(y)) / pixel_size)

    # 打印结果
    # 创建网格点
    x_grid = np.linspace(min(x), max(x), nx)
    y_grid = np.linspace(min(y), max(y), ny)
    x_grid, y_grid = np.meshgrid(x_grid, y_grid)

    # 通过插值法计算网格点上的高度值
    from scipy.interpolate import griddata
    z_grid = griddata((x, y), z, (x_grid, y_grid), method='linear')
    z_grid = np.nan_to_num(z_grid, 0)

    height=z_grid.shape[0]
    width=z_grid.shape[1]

    z_grid = z_grid.astype(np.int16)
    z_grid = -z_grid

    outputfile = os.path.dirname(fileurl)
    full_filename = os.path.basename(fileurl)
    filename, _ = os.path.splitext(full_filename)
    #print(outputfile)
    outputfile = outputfile + "/" + filename + ".tif"
    #print(outputfile)
    #transform = from_origin(min(x_grid[0]), max(y_grid[:,0]), (max(x_grid[0]) - min(x_grid[0])) / (len(x_grid[0])-1), -((max(y_grid[:,0]) - min(y_grid[:,0])) / (len(y_grid[:,0]) -1)))
    transform = from_bounds(min(x_grid[0]), min(y_grid[:,0]), max(x_grid[0]), max(y_grid[:,0]), width, height)
    with rasterio.open(
        outputfile,
        'w',
        driver='GTiff',
        height=z_grid.shape[0],
        width=z_grid.shape[1],
        count=1,
        dtype=z_grid.dtype,
        crs='EPSG:4326',
        compress='LZW',
        tiled=True,
        blockxsize=128,
        blockysize=128,
        transform=transform,
        nodata=0
    ) as dst:
        #dst.update_tags(DataType='Generic')
        dst.set_band_description(1, 'Band 1')
        dst.update_tags(AREA_OR_POINT='Area', Band_1='Band 1')
        #dst.update_tags(1, RepresentationType='ATHEMATIC')
        dst.write(z_grid, 1)
    
    return { 'status' : 200, 'message' : 'ok', 'data': {"outputurl": outputfile}},200
    

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=13200)