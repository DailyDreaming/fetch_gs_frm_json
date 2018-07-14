import os
import sys
import subprocess
import json
from six import iteritems

"""
Store this script somewhere intuitive, for example:
sudo nano /usr/local/bin/dl_gsfiles_frm_json.py

Then call anytime by writing the following to '~/.bashrc':
gs_json() { python /usr/local/bin/dl_gsfiles_frm_json.py "$1"; }
"""

gs_filelist = []

def new_local_path(gsfilepath):
    """Stores the gs path in a list and returns a path local to the cwd."""
    gs_filelist.append(gsfilepath)
    return os.path.join(os.getcwd(), os.path.basename(gsfilepath))

def gs_to_local(input):
    """
    Expects a json-like dictionary as input.
    Replaces the input's gs:// paths with paths local to cwd and returns the modified input.
    These gs:// paths are stored as a list for later downloading.
    """
    if isinstance(input, basestring):
        if input.startswith('gs://'):
            return new_local_path(input)
        else:
            return input
    if isinstance(input, list):
        j = []
        for i in input:
            j.append(gs_to_local(i))
        return j
    elif isinstance(input, dict):
        for k, v in iteritems(input):
            input[k] = gs_to_local(v)
        return input

def strip_gsfiles_from_json_n_dl_locally(input_json='/home/quokka/Desktop/deletewes/workflow-service/testdata/topmed-alignment.sample.json', outputdir='.'):
    """
    Opens a json, finds and downloads all gs:// filepaths within it, and creates a new json
    containing local paths to the newly downloaded gs:// files.
    """
    with open(input_json, 'r') as json_data:
        json_dict = json.load(json_data)
        new_json = gs_to_local(json_dict)

    with open(input_json + '.new', 'w') as f:
        f.write(str(new_json))
        f.write('\n')

    gs_list_filename = os.path.join(os.getcwd(), 'gs_fetch_file.txt')
    with open(gs_list_filename, 'w') as f:
        for g in set(gs_filelist):
            f.write(g)
            f.write('\n')

    print('Importing gs files from: ' + str(input_json))
    print('Into the cwd: ' + str(os.getcwd()))

    # fetch everything with gsutil
    cmd = 'cat {} | gsutil -m cp -I {}'.format(gs_list_filename, outputdir)
    print('With the command: ' + str(cmd))
    subprocess.call(cmd, shell=True)

strip_gsfiles_from_json_n_dl_locally(input_json=sys.argv[1])
