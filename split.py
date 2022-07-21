#!/usr/bin/python3

# built in
import os
import sys
import argparse

# 3rd party imports
import numpy as np
import pandas as pd
from PyPDF2 import PdfFileReader, PdfFileWriter

__author__ = "Connor DeJohn"
__version__ = "0.1"
"""
July 2022

script to split a pdf into the individual sheets

Includes options to:
- use a default - PG N format 
- include a mapping document the maps pg 1 to row 1
"""

if __name__=="__main__": # ls_to_excel is run from command line
	# instantiate arg parser
    parser = argparse.ArgumentParser(description='split a selected pdf into pages. defaults to suffix \" - PG\"')
    # parser.add_argument('--recur', action='store_true',
                        # help='An optional flag to rename files in all subdirectories')
    parser.add_argument('--source', type=str,
                        help='source pdf to split. include .pdf')
    parser.add_argument('--mapping', type=str,
                        help='add a source file with one column specifying the name for the page. excel file must have header row (titles do not matter, just that first row is cut off) must be in cur working dir')
    # parser.add_argument('--suffix', type=str,
                        # help='if no source file, give a starting word to have be the base. every file will change. eg. file -> file1,file2')                    
    args = parser.parse_args()
    cur_dir = os.getcwd()
    
    if not args.source:
        print("A source in the current directory is required")
        quit()
    
    if not os.path.splitext(args.source)[1]:
        print("Please include a file extension on the source")
        quit()
    
    inputpdf = PdfFileReader(open(cur_dir+"\\"+args.source, "rb")) # read in source pdf
    outputpdf = ""
    
    # source file option
    if args.mapping:
        if args.source.find(".xl") > 0:
            print("[*] Not done yet. only the default is ready")
            quit()
            
            df = pd.read_excel(cur_dir+"\\"+args.source).to_numpy() # import mapping
            # these ps need to be toyed with, it may be 1 or so rows off
            for p in range(inputpdf.numPages):
                output = PdfFileWriter()
                output.addPage(inputpdf.getPage(p))
                outname = df[p]
                with open(outname, "wb") as outputStream:
                    output.write(outputStream)
        elif args.source.find(".txt") > 0:
            print("[*] .txt is not implemented yet. please use an excel file.")
            quit()
        else:
            print("[*] The source file was not found. Please check the spelling.")
            quit()
    else:
        f_suffix = " - PG "
        for p in range(inputpdf.numPages):
            output = PdfFileWriter()
            output.addPage(inputpdf.getPage(p))
            outname = os.path.splitext(args.source)[0] + f_suffix + p + ".pdf" #ORIGINAL_PDF.split('.')[0] + ' SH' + str(df[i,1])
            with open(outname, "wb") as outputStream:
                output.write(outputStream)