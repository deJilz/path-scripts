#!/usr/bin/python3

# built in 
import os
import sys
import argparse
from datetime import date

__author__ = "Connor DeJohn"
__version__ = "0.1"
"""
July 2022

script to rename file to add " with CMD comments MMDDYYY"

Includes options to:
- do recursively

"""
print("success")
quit()
if __name__=="__main__": # ls_to_excel is run from command line
	# instantiate arg parser
    parser = argparse.ArgumentParser(description='script to add \" with III comments MMDDYY\" to pdf files')
    parser.add_argument('--recur', action='store_true',
                        help='An optional flag to rename files in all subdirectories')
    parser.add_argument('--initials', type=str,
                        help='option to change intials, the script will default to CMD')
    parser.add_argument('--ftype', type=str,
                        help='option to change the file type being looked for')                        
    args = parser.parse_args()
    cur_dir = os.getcwd()
    
    # parse the initials
    if args.initials:
        if len(args.initials) > 5:
            print("Please entire shorter intials.")
            quit()
        usr_initials = args.initials
    else:
        usr_initials = "CMD"
    
    # get the date
    d = date.today().strftime('%m%d%y')
    
    # build the string
    suffix = " with " + usr_initials + " comments " + d
    
    # check file type
    if args.ftype:
        if args.ftype.find(".") > 0:
            f_type = args.ftype
        else:
            f_type = "." + args.type
    else:
        f_type = ".pdf"
    
    # walk through structure
    for root, dirs, files in os.walk(cur_dir):
        for f in files: # loop through files
            if os.path.splitext(f)[1] != f_type: continue # dont rename things that are not pdfs
            
            os.rename(os.path.join(root, f), os.path.join(root, os.path.splitext(f)[0]+suffix+os.path.splitext(f)[1]))
        
        if not args.recur: break # only loop at top directory (not args.recur) is the replacement when it gets implmented  