#!/usr/bin/env python
# replace_lbcs.py
# open a GFS boundary file for read/write and replace
# tracer fields from a second input GFS boundary file
import netCDF4 as nc
import argparse

def replace_lbcs(inputfile, outputfile, tracers):
    # replace the values of tracers in outputfile with
    # the values from inputfile
    # first open output file in append mode
    ofile = nc.Dataset(outputfile, 'a')
    # open the input data file
    ifile = nc.Dataset(inputfile)
    # loop through tracers
    for t in tracers:
        # loop through input file variables
        for name, var in ifile.variables.items():
            if t in var.name:
                print(f'Transferring {var.name}')
                vin = ifile.variables[var.name][:]
                vout = ofile.variables[var.name]
                vout[:] = vin

if __name__ == '__main__':
    # get command line arguments
    parser = argparse.ArgumentParser(description=('replaces fields in a GFS bndy file ',
                                                  'with that of another GFS bndy file ',
                                                  'of the same dimensions'))
    parser.add_argument('-i', '--inputfile',
                        help='path to netCDF file to grab fields from',
                        type=str, required=True)
    parser.add_argument('-o', '--outputfile',
                        help='path to netCDF file to modify',
                        type=str, required=True)
    parser.add_argument('-t', '--tracers',
                        help='list of tracers to grab from inputdata',
                        type=str, nargs='+', required=False, default=['no2'])
    args = parser.parse_args()
    replace_lbcs(args.inputfile, args.outputfile, args.tracers)
