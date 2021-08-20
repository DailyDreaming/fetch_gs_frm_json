import os
import sys
import subprocess
import json
from six import iteritems

"""
Call this on a json containing gs:// bucket paths and it will download them all
locally and produce a new json file (alongside the old one) containing local
paths to those files instead.

Store this script somewhere intuitive, for example:
/usr/local/bin/dl_gsfiles_frm_json.py

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
    Replaces the input's gs:// paths with paths local to cwd and returns the modified input.

    Expects a json-like dictionary as input.
    These gs:// paths are stored as a list for later downloading.
    """
    if isinstance(input, basestring):
        if input.startswith('gs://'):
            return new_local_path(input)
    if isinstance(input, list):
        j = []
        for i in input:
            j.append(gs_to_local(i))
        return j
    elif isinstance(input, dict):
        for k, v in iteritems(input):
            input[k] = gs_to_local(v)
    return input

def strip_gsfiles_from_json_n_dl_locally(input_json, project=None):
    """
    Opens a json, finds and downloads all gs:// filepaths within it, and creates a new json
    containing local paths to the newly downloaded gs:// files.
    """
    outputdir='.'
    with open(input_json, 'r') as json_data:
        json_dict = json.load(json_data)
        new_json = gs_to_local(json_dict)

    with open(input_json + '.new', 'w') as f:
        json.dump(new_json, f)

    gs_list_filename = os.path.join(os.getcwd(), 'gs_fetch_file.txt')
    with open(gs_list_filename, 'w') as f:
        for g in set(gs_filelist):
            f.write(g)
            f.write('\n')
    print('\n')
    print('Importing gs files from: ' + str(input_json))
    print('Into the cwd: ' + str(os.getcwd()))

    # fetch everything with gsutil
    if project==None:
        cmd = 'cat {} | gsutil -m cp -I {}'.format(gs_list_filename, outputdir)
    else:
        cmd = 'cat {} | gsutil -m -u {} cp -I {}'.format(gs_list_filename, project, outputdir)
    print('With the command: ' + str(cmd))
    print('New json with local paths created: ' + str(input_json + '.new'))
    print('\n')
    subprocess.call(cmd, shell=True)

try:
    strip_gsfiles_from_json_n_dl_locally(input_json=sys.argv[1], project=sys.argv[2])
except IndexError:
    strip_gsfiles_from_json_n_dl_locally(input_json=sys.argv[1])


