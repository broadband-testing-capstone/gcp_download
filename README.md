# gcp_download
## Steps:
1. Open google cloud shell inside gcp
2. Run the following command:
```gsutil -m cp "gs://[bucket name]/*" [download location] ```
replace [bucket name] with the name of the bucket you want to copy from and [download location] with the location you want to download the files to inside google shell.
3. Click more (the three dots) in google shell and then select download, it will have you select the location of the folder or file you want to download and then have you select the download location.
4. Run json2csv.py for m_lab json files and txt2csv.py for netrics txt files. You can use -i and -o options to specify input and output files. If you don't specify either it will be in the current directory.