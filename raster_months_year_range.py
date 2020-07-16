import pandas as pd
import os
import glob
from PIL import Image
import numpy as np

# import WA+ modules
import watools.General.data_conversions as DC
import watools.General.raster_conversions as RC

os.chdir(r"D:\chapter3analysis\precipitation")
state_date = '2007-10-01'
end_date = '2008-09-01'
in_files = '*monthly*.tif'
out_file = '2007_2008_new.tif'

def monthly_to_yearly(state_date, end_date, in_files, out_file):
    
    month_range = pd.date_range(start= state_date, end= end_date, freq= 'MS').strftime("%Y.%m").tolist()
    #print(month_range)
    files_list = []
    data = []

    files = glob.glob(in_files)
    #print(files)

    # Get array information and define projection
    geo_out, proj, size_X, size_Y = RC.Open_array_info(files[0])
    if int(proj.split('"')[-2]) == 4326:
        proj = "WGS84"

    for i in month_range:
        if 'P_CHIRPS.v2.0_mm-month-1_monthly_'+i+'.01.tif' in files:
            files_list.append('P_CHIRPS.v2.0_mm-month-1_monthly_'+i+'.01.tif')
        else:
            print("No such file")

    for j in files_list:
        photo = Image.open(j)
        month = np.array(photo)
        data.append(month)

    #print(data)
    arr_year = np.array(data)

    #print(year_sum)

    year_sum = arr_year.sum(axis=0)

    # Save tiff file
    DC.Save_as_tiff(out_file, year_sum, geo_out, proj)


monthly_to_yearly(state_date, end_date, in_files, out_file)
