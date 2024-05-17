import pathlib as pl
import site
import rasterio
import geopandas as gpd
import swb_control_file as swb
from utility_functions import create_model_work_dir, read_toml_file

site.addsitedir('.')

from grid_operations import clip_grid_to_geopandas_geometry

base_dir = pl.Path.cwd().parent

control_dict = read_toml_file(filename=base_dir / 'configuration_files/run_control.toml')

gis_dir = base_dir / control_dict['data_directories']['gis_data_dir']
work_dir = base_dir / control_dict['working_directories']['swb_work_dir']

awc_file = gis_dir / control_dict['input_grids']['available_water_capacity_grid']
cdl_file = gis_dir / control_dict['input_grids']['landuse_grid']
hsg_file = gis_dir / control_dict['input_grids']['hydrologic_soil_group_grid']

weather_data_dir = pl.Path(control_dict['weather_data']['weather_data_dir'])
weather_data_proj4_str = control_dict['weather_data']['proj4_str']
precip_file = control_dict['weather_data']['precip_file']
tmax_file = control_dict['weather_data']['tmax_file']
tmin_file = control_dict['weather_data']['tmin_file']

lu_lookup_table = control_dict['input_tables']['lu_lookup_table_name']
irr_lookup_table = control_dict['input_tables']['irr_lookup_table_name']

start_date = control_dict['simulation_control']['start_date']
end_date = control_dict['simulation_control']['end_date']

basins = gis_dir / control_dict['input_shapefiles']['gaging_basins']

basins_gpd = gpd.read_file(basins)


for site_id in basins_gpd.site_no:
    print(f"munging data for site: {site_id}")
    basin = basins_gpd.query(f"site_no=='{site_id}'")

    model_subdir = work_dir / f"gage_{site_id}"

    create_model_work_dir(work_dir=work_dir,
                          sub_dir=f"gage_{site_id}",
                          output_dir='output',
                          logfile_dir='logfile')

    basin_awc_filename = f"AWC_MN__1000m__{site_id}.asc"
    basin_cdl_filename = f"CDL_MN__1000m__{site_id}.asc"
    basin_hsg_filename = f"HSG_MN__1000m__{site_id}.asc"

    nx, ny, xll, yll, resolution, proj4_str = clip_grid_to_geopandas_geometry(grid_filename=awc_file,
                                    gpd_shape=basin,
                                    output_grid_filename=model_subdir / basin_awc_filename,
                                    output_type=rasterio.float32)

    nx, ny, xll, yll, resolution, proj4_str = clip_grid_to_geopandas_geometry(grid_filename=cdl_file,
                                    gpd_shape=basin,
                                    output_grid_filename=model_subdir / basin_cdl_filename,
                                    output_type=rasterio.int32)

    nx, ny, xll, yll, resolution, proj4_str = clip_grid_to_geopandas_geometry(grid_filename=hsg_file,
                                    gpd_shape=basin,
                                    output_grid_filename=model_subdir / basin_hsg_filename,
                                    output_type=rasterio.int32)
    
    with open(model_subdir / f"MN__swb_control_file__gage_{site_id}.ctl",'w') as file:
        file.write(swb.run_details(run_identifier=f"obs_gage_{site_id}"))
        file.write(swb.gridspec(nx, ny, xll, yll, resolution, proj4_str))
        file.write(swb.options())
        file.write(swb.precip_file(precip_file, weather_data_proj4_str))
        file.write(swb.tmax_file(tmax_file, weather_data_proj4_str))
        file.write(swb.tmin_file(tmin_file, weather_data_proj4_str))
        file.write("# Soil and landuse grid specification\n")
        file.write("--------------------------------------\n")
        file.write(swb.awc_grid(basin_awc_filename, proj4_str))
        # f.write(swb_flowdir_grid())
        file.write(swb.landuse_grid(basin_cdl_filename, proj4_str))
        file.write(swb.soils_grid(basin_hsg_filename, proj4_str))  
        file.write(swb.set_init_conditions())   
        file.write(swb.lu_lookup_table(lu_lookup_table)) 
        file.write(swb.irr_lookup_table(irr_lookup_table)) 
        file.write(swb.set_output_options())
        file.write(swb.set_start_and_end_dates(start_date, end_date))
        file.close() 
