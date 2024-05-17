import rasterio
import geopandas as gpd
from rasterio.mask import mask
#import matplotlib.pyplot as plt

# shp = '../gis/observation_basins.shp'
# cdl_grd = '../gis/cdl__MN__2019-2023_mode.asc'
# aws_grd = '../gis/AWS_grid_MN__1000m.asc'

# data = rasterio.open(grd)
# profile = data.profile

# basins = gpd.read_file(shp)

# with rasterio.open(grd) as src:
#     out_image, out_transform = rasterio.mask.mask(src, shapes[4], crop=True)
#     out_meta = src.meta

# basin = basins.query("site_no=='4015438'")

# output_grid, output_transform = mask(data, basin.geometry, invert=False, crop=True, pad=True, pad_width=2)

# mygrid = output_grid[0,:,:]
# height, width = mygrid.shape

# output_profile = profile
# output_profile.update(width=width, 
#                     height=height,
#                     transform=output_transform)

# with rasterio.open('cdl__MN__2019-2023_mode__04015438.asc', 'w', **output_profile) as dst:
#     dst.write(mygrid.astype(rasterio.int32), 1)


def clip_grid_to_geopandas_geometry(grid_filename, 
                                    gpd_shape, 
                                    output_grid_filename, 
                                    output_type=rasterio.int32,
                                    decimal_precision=3):
    """Clip a raster grid to the bounds of a single polygon, provided as a geopandas geometry entry.

    If no output_type is provided, the results will be written as integers. If the output_type is 'rasterio.float32',
    the resulting output precision will be limited to the value of 'decimal_precision', which defaults to 3.

    Args:
        grid_filename (str): text string defining the grid filename to clip
        gpd_shape (Geopandas dataframe entry): single entry, with geometry, defining shape bounds
        output_grid_filename (str): path and name for the output file. 
        output_type (rasterio type, optional): data type for use in writing output. Defaults to rasterio.int32.
    """
    grid = rasterio.open(grid_filename)
    profile = grid.profile

    output_grid, output_transform = mask(grid, gpd_shape.geometry,
                                         invert=False, 
                                         crop=True, 
                                         pad=True, 
                                         pad_width=2)
    
    height, width = output_grid[0,:,:].shape

    output_profile = profile

    if output_type == rasterio.float32:        
        output_profile.update(width=width, 
                              height=height,
                              transform=output_transform,
                              decimal_precision=decimal_precision)
    else:
        output_profile.update(width=width, 
                              height=height,
                              transform=output_transform)

    with rasterio.open(output_grid_filename, 'w', **output_profile) as dst:
        dst.write(output_grid[0,:,:].astype(output_type), 1)

    # GRID nx, ny, llx, lly, resolution; proj4_str
    return (width, height, output_profile['transform'][2],output_profile['transform'][5],
            output_profile['transform'][0],output_profile['crs'].to_proj4())
