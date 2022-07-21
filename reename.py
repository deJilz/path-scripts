import os
import sys
import argparse
from alive_progress import alive_bar
import pandas as pd
import numpy as np

"""
Connor DeJohn
July 2022

script to rename files

Includes options to:
- input a base prefix that will have numbers included

"""

if __name__=="__main__": # ls_to_excel is run from command line
	# instantiate arg parser
    parser = argparse.ArgumentParser(description='rename files in working directory')
    parser.add_argument('--recur', action='store_true',
                        help='An optional flag to rename files in all subdirectories')
    parser.add_argument('--source', type=str,
                        help='add a source file with two columns to match old names to new names. excel file must have header row (titles do not matter, just that first row is cut off) can be txt file with each line of form \"old.jpg,new.jpg\" must be in cur working dir')
    parser.add_argument('--prefix', type=str,
                        help='if no source file, give a starting word to have be the base. every file will change. eg. file -> file1,file2')                    
    args = parser.parse_args()
    cur_dir = os.getcwd()
    
    # check conflict of source and prefix
    if args.source and args.prefix:
        print("There cannot be a prefix and a source. Please enter one or the other.")
        quit()
    
    if not os.path.splitext(args.source)[1]:
        print("Please include a file extension on the source")
        quit()
    
    # source file option
    if args.source:
        if args.source.find(".xl") > 0:
            df = pd.read_excel(cur_dir+"\\"+args.source).to_numpy() # import mapping
            for root, dirs, files in os.walk(cur_dir):
                for f in files:
                    if f == args.source: continue # dont rename the mapping file
                    r = np.where(df[:,0] == f)[0] # find file in mapping
                    if r.size == 0: continue # check if f was found
                    os.rename(os.path.join(root, f), os.path.join(root, str(df[r,1][0]))) # rename old file based on new file
                    r = [] # reset r - not sure if neccessary
                if not args.recur: # break if not recursive check
                    break
        elif args.source.find(".txt") > 0:
            print(".txt is not implemented yet. please use an excel file.")
            quit()
        else:
            if not args.prefix: # if prefix is also empty
                print("The source file was not found. Please check the spelling.")
                quit()
                
                
    # prefix option
    if args.prefix: # prefix given, no source needed to read
        f_prefix = args.prefix
        i = 0
        n_files = len([f for f in os.listdir(cur_dir) if os.path.isfile(os.path.join(cur_dir, f))])
        with alive_bar(n_files,title='renaming files', bar='ruler') as bar: # setup progress bar
            for root, dirs, files in os.walk(cur_dir): # walk through structure
                for f in files: # loop through files
                    os.rename(os.path.join(root, f), os.path.join(root, f_prefix+str(i)+os.path.splitext(f)[1]))
                    i += 1
                if not args.recur: # only loop at top directory (not args.recur) is the replacement when it gets implmented
                    break