
import os
if __name__ == "__main__":
    try:
        f = open('new_fldrs.txt','r')
    except:
        print("file not found") # this may never run, i think open will create the file if nonexistant
        quit()
    new_names = f.read().strip().splitlines()
    for n in new_names:
        os.makedirs(os.path.join(os.getcwd(),n.replace('\t',' ').replace('/','-').replace('\n','')), exist_ok = True)
        print("Made:",n)