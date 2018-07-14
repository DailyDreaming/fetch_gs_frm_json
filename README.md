# fetch_gs_frm_json
For a json containing gs:// bucket paths, for example:

```
{
    "input_file": {
        "class": "File",
        "path": "gs://topmed_workflow_testing/topmed_aligner/input_files/NWD176325.0005.recab.cram"
    },
    "reference_genome": {
        "class": "File",
        "path": "gs://topmed_workflow_testing/topmed_variant_caller/reference_files/hg38/hs38DH.fa"
    }
}
```

This script will:
1. Download all google bucket files into the current directory (using `gsutil`).
2. Output a new json modified to contain the new local paths.

To run:
    `python dl_gsfiles_frm_json.py <path-to-json-file>`

If the path to this script is:
    `/usr/local/bin/dl_gsfiles_frm_json.py`

A convenient alias can be created in '~/.bashrc' by adding:
    `gs_json() { python /usr/local/bin/dl_gsfiles_frm_json.py "$1"; }`

Then simple run anytime using:
    `gs_json <path-to-json-file>`
