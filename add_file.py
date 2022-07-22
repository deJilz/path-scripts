#!/usr/bin/python3

# built in 
import os
import sys
import argparse
import shutil

# 3rd party imports


__author__ = "Connor DeJohn"
__version__ = "0.1"
"""
July 2022

script to copy file into sub folders

Includes options to:

"""

if __name__=="__main__": # ls_to_excel is run from command line
	# instantiate arg parser
    parser = argparse.ArgumentParser(description='copy a file into subdirectories and include option to delete files inside')
    parser.add_argument('--source', type=str,
                        help='specify file that will be copied')
    parser.add_argument('--replace', type=str,
                        help='add a file that will be found in the subdirectories and will be deleted')
    parser.add_argument('--new_name', type=str,
                        help='add a string to rename the copied file')
    parser.add_argument('--only_rmv', type=str,
                        help='override flag to only delete a specified file from all subdirectories')
    args = parser.parse_args()
    
    # check for source and only_rmv
    if not args.source and not args.only_rmv:
        print("A source file must be included. see -h for help.")
        quit()
    
    cur_dir = os.getcwd()
    
    # check for proper file names
    if args.source:
        if args.replace:
            if not os.path.splitext(args.source)[1] or not os.path.splitext(args.replace)[1]:
                print("Please include a file extension on the source and replacement.")
                quit()
        else:
            if not os.path.splitext(args.source)[1]:
                print("Please include a file extension on the source.")
                quit()
    elif args.only_rmv:
        if not os.path.splitext(args.only_rmv)[1]:
            please("Please enter the file to be removed")
            quit()
        # if the file is good, remove it
        for root, dirs, files in os.walk(cur_dir):
            for f in files: # check for removeable file
                if f == args.only_rmv: os.remove(os.path.join(root,f)) # delete the file if found
        quit()
    
    
    src = os.path.join(cur_dir,args.source)
    for root, dirs, files in os.walk(cur_dir):
        for f in files: # check for removeable file
            if f == args.replace: os.remove(os.path.join(root,f)) # delete the file if found
        for d in dirs:
            shutil.copy2(src, os.path.join(root,d)) # copy into each subdirectory