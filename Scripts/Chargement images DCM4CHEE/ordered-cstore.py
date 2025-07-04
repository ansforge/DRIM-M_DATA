##############
# Envoi d'objets DICOM de manière ordonnée au moyen de transactions C-STORE
# Usage :  python3 ordered-cstore.py folder
##############

# to install natsort:
# pip install natsort

# Import des bibliopthèques associées au script
import os
import sys
import natsort
import time
import pydicom

print ("Argument List:", str(sys.argv))

def cstoreFile(folder, file, transferSyntax):
    print("Storing file : " + file )
    
    # Choix de la Transfer Syntax à mentionner au sein de la commande C-STORE
    if "1.2.840.10008.1.2.4.80" == str(transferSyntax) :
        print("Syntaxe de transfert associée aux images : 1.2.840.10008.1.2.4.80")
        transferSyntaxCode = "-xt"
        
    elif "1.2.840.10008.1.2" == str(transferSyntax) :
        print("Syntaxe de transfert associée aux images : 1.2.840.10008.1.2")
        transferSyntaxCode = "-xi"

    elif "1.2.840.10008.1.2.4.50" == str(transferSyntax) :
        print("Syntaxe de transfert associée aux images : 1.2.840.10008.1.2.4.50")
        transferSyntaxCode = "-xy"

    elif "1.2.840.10008.1.2.1" == str(transferSyntax) :
        print("Syntaxe de transfert associée aux images : 1.2.840.10008.1.2.1")
        transferSyntaxCode = "-x="

    elif "1.2.840.10008.1.2.4.70" == str(transferSyntax) :
        print("Syntaxe de transfert associée aux images : 1.2.840.10008.1.2.4.70")
        transferSyntaxCode = "-xs"

    # Indiquer le hostname/ip + port du serveur récepteur des objets DICOM
    print(transferSyntaxCode)
    os.system('cd ' + folder + ' &&  storescu acceptance.ihe-catalyst.net 11112 -v ' + transferSyntaxCode + ' -aec DCM4CHEE ' + file)

inputArgs = sys.argv
folder = inputArgs[1]
    
lst = natsort.natsorted(os.listdir(folder))

# Détermination de la transfer syntax associée aux images
FirstInstance = pydicom.filereader.read_file_meta_info((folder + '/' + str(lst[0])))
transferSyntaxValue = FirstInstance[0x0002,0x0010].value

for tmp in lst:
    cstoreFile(folder, tmp, transferSyntaxValue)
    time.sleep(0.1)

