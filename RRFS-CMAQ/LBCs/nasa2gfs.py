#!/usr/bin/env python
# nasa2gfs.py
# create a netCDF file that looks like a gaussian
# netCDF GFS history file but contains data from
# NASA GEOS-CF model output
import netDF4 as nc
import argparse

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
    print(nx,ny,nz)

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
