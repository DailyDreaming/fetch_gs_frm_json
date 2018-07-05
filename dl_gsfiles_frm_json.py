import os
import subprocess
import sys

def strip_gsfiles_from_json_n_dl_locally(input_json, outputdir='.'):
    gs_list_filename = 'gs_files.txt'
    with open(input_json, 'r') as f1:
        for line in f1:
            if '"gs://' in line:
                edited_line = line[line.find('gs://'):].strip().strip(',').strip('"')
                print(edited_line)
                with open(gs_list_filename, 'a+') as f2:
                    f2.write(edited_line)
                    f2.write('\n')
    print('Importing gs files from: ' + str(sys.argv[1]))
    print('Into the cwd: ' + str(os.getcwd()))

    # fetch everything with gsutil
    cmd = 'cat {} | gsutil -m cp -I {}'.format(gs_list_filename, outputdir)

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate() # block until done
    with open('gsutil_stderr.log', 'w') as f:
        f.write(stdout)
        f.write('\n\n\n')
        f.write(stderr)

strip_gsfiles_from_json_n_dl_locally(sys.argv[1])
