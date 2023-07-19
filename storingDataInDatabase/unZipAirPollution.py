import os
import zipfile


def getFolder(zipFolder, outputLocation):
    """
    Unzips the given input folder.
    
    zipFolder      : input zip file containing soramame data.
    outputLocation : directory to store unzipped file. 
    
    """
    with zipfile.ZipFile(zipFolder, 'r') as zip_ref:
        zip_ref.extractall(outputLocation + str(zipFolder.split('.')[0]))
    return os.path.join(outputLocation, zipFolder.split('.')[0])


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Error : Incorrect number of input parameters given : " + str(len(sys.argv) - 1))
        print("Input Parameters-> zip folder Path, output Folder Path")
    else:
        unzippedLocation = getFolder(sys.argv[1], sys.argv[2])
