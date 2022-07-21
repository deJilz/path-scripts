#!/usr/bin/python3

# built in 
import os
import sys
import argparse

# 3rd party imports
from alive_progress import alive_bar
from multiprocessing import Process
from PyPDF2 import PdfFileReader, PdfMerger
import pathlib

__author__ = "Connor DeJohn"
__version__ = "0.1"
"""
July 2022

script to merge pdfs in cwd

Includes options to:
- check recursively
- use folder names or maintain structure
- choose how to sort the files
"""


def thread_it(SAVING_FLDR_NAME,files,root,smethod):
    '''
    fpath - 
    d - directory name
    fs - list of file names in d directory
    '''
    merger = PdfMerger()
    # get folder name for merged file name
    dir_name = os.path.basename(root)
    
    match smethod:
        case 0: # alphabetical
            f_sorted = sorted(files)
        case 1: # sort by modified date
            f_sorted = sorted(pathlib.Path(root).iterdir(), key=os.path.getmtime)
            '''
            this doesnt work yet. it ends up spitting out stuff like this which doesnt work for my purpuse.
            i need the file names only
            [WindowsPath('C:/Users/dejohncm/OneDrive - Air Products and Chemicals, Inc/Appraisals/FY21/Instructions.docx'), 
            WindowsPath('C:/Users/dejohncm/OneDrive - Air Products and Chemicals, Inc/Appraisals/FY21/Individual Career Planning.docx'), 
            WindowsPath('C:/Users/dejohncm/OneDrive - Air Products and Chemicals, Inc/Appraisals/FY21/Performance Development form - FY21 - DEJOHNCM.docx'), 
            WindowsPath('C:/Users/dejohncm/OneDrive - Air Products and Chemicals, Inc/Appraisals/FY21/some feedback notes from pascal.txt'), WindowsPath('C:
            '''
    
    for f in f_sorted: # sort the files
        try:
            if f.find(".pdf")>0:
                merger.append(PdfFileReader(open(root+"\\"+f, 'rb')))
        except:
            print("\n[*] Probable error with tag %s."%(dir_name))
            
    os.makedirs(SAVING_FLDR_NAME, exist_ok=True) # mkdir if not there, suppresses error if there
    merger.write(SAVING_FLDR_NAME +"\\"+ dir_name + ".pdf")

if __name__=="__main__": # ls_to_excel is run from command line
	# instantiate arg parser
    parser = argparse.ArgumentParser(description='merge pdfs in the current working directory. option flags for top folder, all subdirectories')
    parser.add_argument('--recur', action='store_true',
                        help='An optional flag to merge recursively.')
    # parser.add_argument('--noex', action='store_true',
                        # help='An optional flag to halt the dumping of the txt file to an excel file')
    parser.add_argument('--sortby', type=str,
                        help='how to sort merged pdfs: a for alphabetical, d for last modified date')
    args = parser.parse_args()
    cur_dir = os.getcwd()
    
    # create folder for merged files
    SAVING_FLDR_NAME = cur_dir + "\\MERGED"
    os.makedirs(SAVING_FLDR_NAME, exist_ok=True) # mkdir if not there, suppresses error if there
    BATCH_SIZE = 18
    match args.sortby:
        case "a":
            sortmethod = 0
        case "d":
            sortmethod = 0
            if input("[*] not implemented yet. will merge by alphabetical. press 'n' to quit, anything else to continue: ") == "n":
                quit()
        case _:
            sortmethod = 0
    
    # get number of folders
    n_dirs = -1
    for root, dirs, files in os.walk(cur_dir):
        n_dirs += len(dirs)
        if not args.recur: # fall out if only top
            break
    
    
    if n_dirs in [0] and not args.recur:
        quit()
        
    # 
    i = 0
    with alive_bar(n_dirs,title='pdfs merging', bar='ruler') as bar: # setup progress bar
        for root, dirs, files in os.walk(cur_dir): # walk through structure
            # do current directory files
            if "MERGED" in root:
                continue
            p = Process(target=thread_it,args=(os.path.join(SAVING_FLDR_NAME+root.replace(cur_dir,"\\")), files, root, sortmethod))
            p.start()
            i += 1
            if (i+1)%BATCH_SIZE == 0 or i == n_dirs: # batches of 5 and joins the last one
                p.join()
            bar()
            if not args.recur:
                break
        p.join()
    
    
    