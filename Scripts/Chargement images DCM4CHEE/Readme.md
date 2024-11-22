# Script

## Chargement ordonnées d'instances DICOM au sein de DCM4CHEE


### Description

Ce script permet d'effectuer un chargement ordonné d'un grand nombre d'instances DICOM au sein de l'outil DCM4CHEE. Par "ordonné", il est entendu que les instances seront transmises à DCM4CHEE selon un ordre croissant basé sur la dénomination des fichiers correspondant. Si l'on prend l'exemple d'un répertoire comportant trois instances DICOM, respectivement nommées I0, I1 et I2, le script assurera d'abord la transmission de l'instance I0, puis I1 et enfin I2. 


### Prérequis

Préalablement à l'exécution du script, l'utilisateur doit avoir connaissance des informations suivantes :
- Adresse du répertoire contenant les images à charger au sein de DCM4CHEE
- Hostname/IP et port associés au DCM4CHEE au sein duquel doit être effectué le chargement  
- Niveau d'encodage des instances DICOM à charger au sein de DCM4CHEE (attribut 0002,0010))

