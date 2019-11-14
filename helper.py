from zipfile import ZipFile

#unzip the dataset
def unzip(filename):

  with ZipFile(filename, 'r') as zipObj:
    zipObj.extractall()
