import datetime

def run_details(run_identifier):
    result = (f"### AUTO-GENERATED SWB2 CONTROL FILE ###\n"
              f"!   run identifier: {run_identifier}\n"
              f"!   generated on {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n")
    return result


def gridspec(nx, ny, llx, lly, resolution, proj4_str):
    result = (f"# GRID DEFINITION\n"
              f"------------------\n"
              f"GRID {nx} {ny} {llx} {lly} {resolution}\n"
              f"BASE_PROJECTION_DEFINITION {proj4_str}\n\n"
             )
    return result


def options():
    result = """
# MODULE SPECIFICATION
-----------------------
INTERCEPTION_METHOD              BUCKET
EVAPOTRANSPIRATION_METHOD        HARGREAVES
RUNOFF_METHOD                    CURVE_NUMBER
SOIL_MOISTURE_METHOD             FAO56_TWO_STAGE
PRECIPITATION_METHOD             GRIDDED
FOG_METHOD                       NONE
FLOW_ROUTING_METHOD              NONE
IRRIGATION_METHOD                FAO56
CROP_COEFFICIENT_METHOD          FAO56
ROOTING_DEPTH_METHOD             FAO56
DIRECT_NET_INFILTRATION_METHOD   NONE
DIRECT_SOIL_MOISTURE_METHOD      NONE
SOIL_STORAGE_MAX_METHOD          TABLE\n\n"""
    return result

def precip_file(precip_file, precip_proj4_str):
    result = (f"PRECIPITATION NETCDF {precip_file}\n"
              f"PRECIPITATION_GRID_PROJECTION_DEFINITION {precip_proj4_str}\n"
              f"PRECIPITATION_NETCDF_Z_VAR             gross_precipitation\n"
              f"PRECIPITATION_MISSING_VALUES_CODE                  -9999.0\n"
              f"PRECIPITATION_MISSING_VALUES_OPERATOR                   <=\n"
              f"PRECIPITATION_MISSING_VALUES_ACTION                   zero\n\n")
    return result


def tmax_file(tmax_file, tmax_proj4_str):
    result = (f"TMAX NETCDF {tmax_file}\n"
              f"TMAX_GRID_PROJECTION_DEFINITION {tmax_proj4_str}\n"
              f"TMAX_MISSING_VALUES_CODE          -9999.0\n"
              f"TMAX_MISSING_VALUES_OPERATOR           <=\n"
              f"TMAX_MISSING_VALUES_ACTION           mean\n\n")
    return result


def tmin_file(tmin_file, tmin_proj4_str):
    result = (f"TMAX NETCDF {tmin_file}\n"
              f"TMAX_GRID_PROJECTION_DEFINITION {tmin_proj4_str}\n"
              f"TMAX_MISSING_VALUES_CODE          -9999.0\n"
              f"TMAX_MISSING_VALUES_OPERATOR           <=\n"
              f"TMAX_MISSING_VALUES_ACTION           mean\n\n")
    return result


def soils_grid(hsg_file, hsg_proj4_str):
    result = (f"HYDROLOGIC_SOILS_GROUP ARC_GRID {hsg_file}\n"
              f"HYDROLOGIC_SOILS_GROUP_PROJECTION_DEFINITION {hsg_proj4_str}\n\n")
    return result


def awc_grid(awc_file, awc_proj4_str):
    result = (f"AVAILABLE_WATER_CONTENT ARC_GRID {awc_file}\n" 
              f"AVAILABLE_WATER_CONTENT_PROJECTION_DEFINITION {awc_proj4_str}\n\n")
    return result


def landuse_grid(lu_file, lu_proj4_str):
    result = (f"LAND_USE ARC_GRID {lu_file}\n"
              f"LAND_USE_PROJECTION_DEFINITION {lu_proj4_str}\n\n")
    return result


def lu_lookup_table(lu_table_file):
    result = (f"LAND_USE_LOOKUP_TABLE {lu_table_file}\n"
             )
    return result


def irr_lookup_table(irr_table_file):
    result = f"IRRIGATION_LOOKUP_TABLE {irr_table_file}\n\n"
    return result


def set_init_conditions():
    result = """
# Initial conditions
---------------------
INITIAL_CONTINUOUS_FROZEN_GROUND_INDEX   CONSTANT  100.0
UPPER_LIMIT_CFGI 83.
LOWER_LIMIT_CFGI 55.

INITIAL_PERCENT_SOIL_MOISTURE            CONSTANT  70.0
INITIAL_SNOW_COVER_STORAGE               CONSTANT   0.0 \n\n
"""
    return result


def set_output_options():
    result = """
# Output options
-----------------
OUTPUT ENABLE snowmelt snow_storage
OUTPUT DISABLE snowfall runon rainfall 
OUTPUT DISABLE reference_ET0 soil_storage delta_soil_storage surface_storage infiltration
OUTPUT ENABLE tmax tmin gross_precip runoff_outside
OUTPUT ENABLE rejected_net_infiltration net_infiltration\n\n
"""
    return result

def set_start_and_end_dates(start_date, end_date):
    result = (f"# Start and end of simulation\n"
              f"------------------------------\n"
              f"START_DATE {start_date}\n"
              f"END_DATE {end_date}\n\n"
             )
    return result


# def write_swb_control_file():
#     with open(os.path.join(swb_output_dir,'MN__swb_control_file.ctl'),'w') as f:
#         f.write(swb_gridspec() + '\n')
#         f.write(swb_options() + '\n\n')
#         f.write(swb_precip_grid_prism() + '\n\n')
#         f.write(swb_tmax_grid_prism() + '\n\n')
#         f.write(swb_tmin_grid_prism() + '\n\n')
#         f.write(swb_awc_grid() + '\n\n')
#         f.write(swb_flowdir_grid() + '\n\n')
#         f.write(swb_landuse_grid() + '\n\n')
#         f.write(swb_soils_grid() + '\n\n')  
#         f.write(swb_set_init_moisture() + '\n\n')   
#         f.write(swb_lu_lookup_table() + '\n\n') 
#         f.write(swb_irr_lookup_table() + '\n\n') 
#         f.write(swb_set_output_options() + '\n')
#         f.write(swb_set_start_and_end_dates() + '\n')
#         f.close() 