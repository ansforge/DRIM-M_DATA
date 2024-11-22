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

print ("Argument List:", str(sys.argv))

def cstoreFile(folder, file):
    print("Storing file : " + file )
    # Indiquer le hostname/ip + port du serveur récepteur des objets DICOM
    # Si les images sont encodées avec la Transfer Syntax 1.2.840.10008.1.2.4.80, indiquer "-xt"
    # Si les images sont encodées avec la Transfer Syntax 1.2.840.10008.1.2, indiquer "-xi"
    # Si les images sont encodées avec la Transfer Syntax 1.2.840.10008.1.2.4.50, indiquer "-xy"
    # Si les images sont encodées avec la Transfer Syntax 1.2.840.10008.1.2.1, indiquer "-x="
    # Si les images sont encodées avec la Transfer Syntax 1.2.840.10008.1.2.4.70, indiquer "-xs"
    os.system('cd ' + folder + ' &&  storescu hostname_or_ip port -v -xt -aec DCM4CHEE ' + file)

inputArgs = sys.argv
folder = inputArgs[1]
    
lst = natsort.natsorted(os.listdir(folder))
for tmp in lst:
    cstoreFile(folder, tmp)
    time.sleep(0.1)

