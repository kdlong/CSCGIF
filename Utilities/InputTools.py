import argparse
import itertools
import glob
import os

def getDefaultParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--files", required=True, 
            type=lambda x: [i.strip() for i in x.split(",")],
            help="List of files of data files, separated by"
            "commas. Unix wildcards will be expanded"
    )
    parser.add_argument("-s", "--subtract_files", default=[], 
            type=lambda x: [i.strip() for i in x.split(",")],
            help="List of files of data files, separated by"
            "commas. Unix wildcards will be expanded. Values from "
            "file 2 will be subtracted from file 1"
    )
    parser.add_argument("-p", "--data_path", type=str,
        default="/afs/cern.ch/cms/MUON/csc/fast1-test-ISR/IVmeasurements/", 
        help="Append this path to data files"
    )
    return parser
def getFileList(files, data_path):
    file_path = lambda x: x if os.path.exists(x.split("/")[0]) \
        else "/".join([data_path.rstrip("/"), x])
    file_list = itertools.chain(
        *[glob.glob(file_path(i)) for i in files]
    )
    return file_list
