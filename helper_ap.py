
from zipfile import ZipFile
import gzip
import shutil

#unzip the dataset
def unzip(filename):
'''unzips as .zip given file_name'''
  with ZipFile(filename, 'r') as zipObj:
    zipObj.extractall()


def ungz(fname_gz, fname):
  '''ungz given .gz filename
  fname_gz: file.csv.gz
  fanme: file.csv
  '''
  with gzip.open(fname_gz, 'rb') as f_in:
    with open('fname.tsv', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
