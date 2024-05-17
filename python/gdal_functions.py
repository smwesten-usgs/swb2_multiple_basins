import os
from osgeo import gdal
from osgeo_utils.gdal_fillnodata import *
import rasterio as rio
import json

# example GDAL error handler function
def gdal_error_handler(err_class, err_num, err_msg):
    errtype = {
            gdal.CE_None:'None',
            gdal.CE_Debug:'Debug',
            gdal.CE_Warning:'Warning',
            gdal.CE_Failure:'Failure',
            gdal.CE_Fatal:'Fatal'
    }
    err_msg = err_msg.replace('\n',' ')
    err_class = errtype.get(err_class, 'None')
    print('Error Number: %s' % (err_num))
    print('Error Type: %s' % (err_class))
    print('Error Message: %s' % (err_msg))

# install error handler
gdal.PushErrorHandler(gdal_error_handler)

def get_extents(filename):
    myopts = gdal.InfoOptions(options = ['-json'], reportProj4=True)
    myinfo = gdal.Info(filename,options=myopts)
    corner_coordinates = myinfo.get('cornerCoordinates')
    return corner_coordinates

def get_proj4(filename):
    myopts = gdal.InfoOptions(options = ['-json'], reportProj4=True)
    myinfo = gdal.Info(filename,options=myopts)
    proj4 = myinfo.get('coordinateSystem').get('proj4')
    return proj4

def get_wkt(filename):
    myopts = gdal.InfoOptions(options = ['-json'])
    myinfo = gdal.Info(filename,options=myopts)
    wkt = myinfo.get('coordinateSystem').get('wkt')
    return wkt

def get_nx_ny(filename):
    myopts = gdal.InfoOptions(options = ['-json'], reportProj4=True)
    myinfo = gdal.Info(filename,options=myopts)
    (nx, ny) = myjson['size']
    (nx,ny) = myinfo.get('coordinateSystem').get('size')
    return (nx, ny)

def gdalwarp(src_file, dst_file, src_proj4, dst_proj4, nx, ny, xll, yll, xur, yur, output_type, resample_algorithm):

    warp_options = gdal.WarpOptions(dstSRS=dst_proj4, 
                                    srcSRS=src_proj4,
                                    outputBounds=(xll,yll,xur,yur),
                                    width=nx,
                                    height=ny,
                                    outputBoundsSRS=dst_proj4,
                                    setColorInterpretation=True,
                                    outputType=output_type,
                                    resampleAlg=resample_algorithm)

    res = gdal.Warp(destNameOrDestDS=dst_file,
                    srcDSOrSrcDSTab=src_file,
                    options=warp_options)
    res = None

def gdal_translate( dst_file, src_file='temp.img', output_type=gdal.GDT_Float32, gdal_format='AAIGrid',nodata=-9999.):
    if output_type == gdal.GDT_Float32:
      translate_options = gdal.TranslateOptions(format=gdal_format, 
                                                outputType=output_type,
                                                creationOptions=["SIGNIFICANT_DIGITS=5,FORCE_CELLSIZE=TRUE"],
                                                noData=nodata)
    else:
      translate_options = gdal.TranslateOptions(format=gdal_format, 
                                                outputType=output_type,
                                                creationOptions=["FORCE_CELLSIZE=TRUE"],
                                                noData=nodata)
    
    res=gdal.Translate(dst_file,src_file,options=translate_options)
    res=None

def gdal_rasterize( dst_file, src_file, dst_proj4, resolution, xll, yll, xur, yur,
                    layer='', attribute='', gdal_format='HFA',
                    output_type=gdal.GDT_Float32, nodata=-9999):

    rasterize_options = gdal.RasterizeOptions(
                              outputSRS=dst_proj4,
                              format=gdal_format,
                              outputType=output_type,
                              outputBounds=(xll,yll,xur,yur),
                              initValues=0,
                              xRes=resolution,
                              yRes=resolution,
                              attribute=attribute)
    res=gdal.Rasterize( dst_file,
                        src_file,
                        options=rasterize_options)
    res=None
