#!/usr/bin/env python
# nasa2gfs.py
# create a netCDF file that looks like a gaussian
# netCDF GFS history file but contains data from
# NASA GEOS-CF model output
import netCDF4 as nc
import numpy as np
import argparse

# below is ak/bk for GEOS L72

ak = np.array([ 1, 2.00000023841858, 3.27000045776367, 4.75850105285645,
    6.60000133514404, 8.93450164794922, 11.9703016281128, 15.9495029449463,
    21.1349029541016, 27.8526058197021, 36.5041084289551, 47.5806083679199,
    61.6779098510742, 79.5134124755859, 101.944023132324, 130.051025390625,
    165.079025268555, 208.497039794922, 262.021057128906, 327.64306640625,
    407.657104492188, 504.680114746094, 621.680114746094, 761.984191894531,
    929.294189453125, 1127.69018554688, 1364.34020996094, 1645.71032714844,
    1979.16040039062, 2373.04052734375, 2836.78051757812, 3381.00073242188,
    4017.541015625, 4764.39111328125, 5638.791015625, 6660.34130859375,
    7851.2314453125, 9236.572265625, 10866.3017578125, 12783.703125,
    15039.302734375, 17693.00390625, 20119.201171875, 21686.501953125,
    22436.30078125, 22389.80078125, 21877.59765625, 21214.998046875,
    20325.8984375, 19309.6953125, 18161.896484375, 16960.896484375,
    15625.99609375, 14290.9951171875, 12869.59375, 11895.8623046875,
    10918.1708984375, 9936.521484375, 8909.9921875, 7883.421875,
    7062.1982421875, 6436.263671875, 5805.3212890625, 5169.61083984375,
    4533.90087890625, 3898.20092773438, 3257.08081054688, 2609.20068359375,
    1961.310546875, 1313.48034667969, 659.375244140625, 4.80482578277588, 0])

bk = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8.17541323527848e-09,
    0.00696002459153533, 0.0280100405216217, 0.0637200623750687,
    0.113602079451084, 0.156224086880684, 0.200350105762482,
    0.246741116046906, 0.294403105974197, 0.343381136655807,
    0.392891138792038, 0.44374018907547, 0.494590193033218,
    0.546304166316986, 0.581041514873505, 0.615818440914154,
    0.650634944438934, 0.685899913311005, 0.721165955066681,
    0.749378204345703, 0.770637512207031, 0.791946947574615,
    0.81330394744873, 0.834660947322845, 0.856018006801605,
    0.877429008483887, 0.898908019065857, 0.920387029647827,
    0.941865026950836, 0.963406026363373, 0.984951972961426, 1])

def nasa2gfs(inputfile, gfsfile, outputfile, tracers):
    # take data from inputdata and variables/dimensions
    # from gfsfile and write to outputfile
    # tracers is a list of variables to read from inputfile
    # first open new file for writing
    ofile = nc.Dataset(outputfile, 'w', format="NETCDF4")
    # open the input data file to get dimensions
    ifile = nc.Dataset(inputfile)
    nx = len(ifile.dimensions['lon'])
    ny = len(ifile.dimensions['lat'])
    nz = len(ifile.dimensions['lev'])
    # create dimensions
    xdim = ofile.createDimension("grid_xt", nx)
    ydim = ofile.createDimension("grid_yt", ny)
    zdim = ofile.createDimension("pfull", nz)
    zidim = ofile.createDimension("phalf", nz+1)
    tdim = ofile.createDimension("time", None)
    # open the GFS file to get variables, etc.
    gfile = nc.Dataset(gfsfile)
    # add all variables in the GFS file to the output file
    for name,gfsvar in gfile.variables.items():
        ofile.createVariable(name, gfsvar.dtype, gfsvar.dimensions)
    # add all tracers specified to the output file
    for t in tracers:
        ofile.createVariable(t.lower(), "f4", ("time", "pfull", "grid_yt", "grid_xt"))
    # add necessary global attributes to output file
    ofile.ncnsto = np.int32(gfile.ncnsto + len(tracers))
    ofile.im = np.int32(nx)
    ofile.jm = np.int32(ny)
    ofile.source = "FV3GFS"
    ofile.grid = "gaussian"
    ofile.hydrostatic = "non-hydrostatic"
    # do not think we need ak/bk but leaving not here just in case
    # for each variable in the GFS file, first lets just fill a mean value in the array
    for name,var in gfile.variables.items():
        vmean = np.nanmean(var[:])
        vout = ofile.variables[var.name]
        vshape = list(vout.shape)
        if vshape[0] == 0:
            vshape[0] = 1
        vshape = tuple(vshape)
        vout[:] = np.ones((vshape))*vmean
    # now for the fields in the NASA file, need to replace necessary fields
    gfsvars = ['grid_xt', 'grid_yt', 'pfull', 'dpres', 'hgtsfc', 'pressfc']
    nasavars = ['lon', 'lat', 'lev', 'DELP', 'PHIS', 'PS']
    for gv, nv in zip(gfsvars, nasavars):
        vdata = ifile.variables[nv][:]
        vdataout = ofile.variables[gv]
        vdataout[:] = vdata
    # handle lon and lat
    xdata = ifile.variables['lon'][:]
    ydata = ifile.variables['lat'][:]
    lons, lats = np.meshgrid(xdata, ydata)
    xdataout = ofile.variables['lon']
    ydataout = ofile.variables['lat']
    xdataout[:] = lons
    ydataout[:] = lats
    # need to handle phalf, not in input file...
    phalf = ak + bk * 1000.
    vdataout = ofile.variables['phalf']
    vdataout[:] = phalf
    # now add in the tracers
    for t in tracers:
        vdata = ifile.variables[t][:] * 1000000. # mol/mol to ppm
        vdataout = ofile.variables[t.lower()]
        vdataout[:] = vdata


if __name__ == '__main__':
    # get command line arguments
    parser = argparse.ArgumentParser(description=('Creates a netCDF file ',
                                                  'that looks like a GFS ',
                                                  'Gaussian Grid netCDF file ',
                                                  'from an input NASA GEOS-CF ',
                                                  'netCDF history file'))
    parser.add_argument('-i', '--inputfile',
                        help='path to input NASA GEOS-CF file',
                        type=str, required=True)
    parser.add_argument('-g', '--gfsfile',
                        help='path to template GFS netCDF Gaussian file',
                        type=str, required=True)
    parser.add_argument('-o', '--outputfile',
                        help='path to output file',
                        type=str, required=True)
    parser.add_argument('-t', '--tracers',
                        help='list of tracers to grab from inputdata',
                        type=str, nargs='+', required=False, default=['NO2'])
    args = parser.parse_args()
    # call main function
    nasa2gfs(args.inputfile, args.gfsfile, args.outputfile, args.tracers)
