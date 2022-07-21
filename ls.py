#!/usr/bin/python3

# built in
import os
import sys
import argparse

# 3rd party imports
import xlsxwriter

__author__ = "Connor DeJohn"
__version__ = "0.1"
"""
July 2022

Similar script to ls but translating to python.

Includes options to:
- check recursively
- will always dump to txt
- has option to also dump to excel file
"""
def ls_to_table(c_filename,xname):
    #c_filename = os.getcwd() + "\\# 
    ROW = 1
    path = ""
    workbook = xlsxwriter.Workbook(xname)
    worksheet = workbook.add_worksheet()
    files = []
    
    # read in the ls file
    with open(c_filename) as f:
        lines = f.readlines()
        
    # go through each line
    for line in lines:
        line = line.strip()
        # trigger when a block ends
        if line == '': 
            # write the TAG
            k = path.split("\\")[-1]
            if k != '' and k[-1] == ':':
                k = k[:-1]
            worksheet.write(ROW,1,k)
            # write the PATH
            worksheet.write(ROW,0,'\\'.join(path.split("\\")[:-1] + [k])[1:])
            
            # write the files
            try: 
                for i,p in enumerate(files):
                    worksheet.write(ROW,4+i,p)
            except:
                worksheet.write(ROW,10,','.join(files))
                
            ROW = ROW + 1
            files = []
            continue # new block
        if line[0] == '.' and line[1] != ':':
            path = line
            continue
        files.append(line)
    workbook.close()


if __name__=="__main__": # ls_to_excel is run from command line
	# instantiate arg parser
    parser = argparse.ArgumentParser(description='translation of ls to python for cmd executation.\nIt will walk the current working directory and, by default, create a txt file and an excel file.')
    parser.add_argument('--top', action='store_true',
                        help='An optional flag to only walk top directory')
    parser.add_argument('--noex', action='store_true',
                        help='An optional flag to halt the dumping of the txt file to an excel file')
    parser.add_argument('--fname', type=str,
                        help='An optional file name for txt file')
    args = parser.parse_args()
    cur_dir = os.getcwd()
    # allow user to specify a specific filename
    if args.fname is None:
        txt_f = cur_dir + "\\ls.txt"
        xname = "ls.xlsx"
    else:
        if args.fname.find(".txt") > 0:
            txt_f = cur_dir + "\\" + args.fname
            xname = args.fname.replace(".txt",".xlsx")
        else:
            txt_f = cur_dir + "\\" + args.fname + ".txt"
            xname = args.fname + ".xlsx"
    
    
    # loop through folders
    with open(txt_f,'w') as fp:
        fp.write(".:\n")
        for root, dirs, files in os.walk(cur_dir):
            header = root.replace(cur_dir,".")
            if header == ".":
                fp.write("{0}:\n".format(cur_dir))
            else:
                fp.write("{0}:\n".format(header))
                
            for d in dirs: # list out sub directories
                fp.write("{0}\\\n".format(d))
            for f in files: # list out files in folder
                fp.write("{0}\n".format(f))
            if args.top: # if we only want the top level
                break # fall out
            else:
                fp.write("\n")
    
    # how to put out results
    if not args.noex:
        ls_to_table(txt_f,xname)