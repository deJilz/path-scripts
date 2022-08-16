#!/usr/bin/python3

# built in 
import os
import sys
import argparse

# 3rd party imports
import tabula

__author__ = "Connor DeJohn"
__version__ = "0.1"
"""
July 2022

script to convert pdf to excel, doc, txt depending on user input

Includes options to:

"""

if __name__=="__main__":
	# instantiate arg parser
    parser = argparse.ArgumentParser(description='convert pdf to another format')
    parser.add_argument('--target', action='store_true',
                        help='target file to convert from pdf. needs to be in working directory')
    parser.add_argument('--ftype', type=str,
                        help='An optional flag to specify the output file type. file type is xlsx by default')
    parser.add_argument('--recur', action='store_true',
                        help='An optional flag to convert files in all subdirectories')
    parser.add_argument('--top', action='store_true',
                        help='An optional flag to convert all files in top directory')
    args = parser.parse_args()
    cur_dir = os.getcwd()
    
    if not args.top or not args.recur:
        # we are not doing the top folder and we are not recuring
        if not args.target or os.path.splitext(f)[1] != ".pdf": # no target or target is not pdf file
            print("A pdf source in the current directory is required")
            quit()
    
    # figure out ext, fix it up - doc,docx,txt
    ext = rgs.ftype.replace(".","")
    
    if not args.source in [f for f in os.listdir(cur_dir) if os.path.isfile(os.path.join(cur_dir, f))]:
        print("[*] The source file was not found. Please check the spelling or the current directory.")
        quit()
    
    # convert
    if args.recur or args.top: # more than one file
        print("[*] more than one file is not implemented yet")
    else: # only one file
        df = tabula.read_pdf(args.target, pages='all')
        tabula.convert_into(df, output_format=ext, pages='all', stream=True)
    