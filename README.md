# fetch_gs_frm_json
For a json containing gs:// bucket paths, for example:
```
{
    "bwa_index": {
        "class": "File",
        "path": "gs://topmed_workflow_testing/topmed_aligner/reference_files/hg38/hs38DH.fa.tar"
    },
    "dbsnp": {
        "class": "File",
        "path": "gs://topmed_workflow_testing/topmed_aligner/reference_files/hg38/Homo_sapiens_assembly38.dbsnp138.vcf.gz"
    },
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

This script will download all of these google bucket files using `gsutil` into the current directory, and in addition to creating a new json in current directory modified to contain the new local paths.

If the path to this script is:
    `/usr/local/bin/dl_gsfiles_frm_json.py`

A convenient alias can be created in '~/.bashrc' by adding:
    `gs_json() { python /usr/local/bin/dl_gsfiles_frm_json.py "$1"; }`
