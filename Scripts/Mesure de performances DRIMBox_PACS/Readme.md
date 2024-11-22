# Outils

## SpeedTest

Ce script permet de mesurer les performances d'un système PACS associé à une DRIMBox. Initialement construit afin de fournir un exemple d'implémentation de l'exigence DB.SO.102 issue de la spécification projet DRIMBox, il peut être utilisé aussi bien dans le cadre du processus d'homologation qu'en exploitation. 

Le fonctionnement du script implique le déclenchement une requête C-MOVE (par défaut sur le StudyInstanceUID de l'examen de référence ANS: 1.2.250.1.213.4.5.2.1.199) à destination du système PACS et une interprétation de la réponse émise en retour.
Le script récupère alors:
-  une mesure de temps associée à la réception de la première image
-  la quantité de données transférée
-  le temps total de récupération de l'examen, duquel peut être déduit le débit offert par le système PACS.

Le contenu des images reçues en provenance du PACS est ignoré par le script.

### Prérequis

```bash
 pip install pydicom
 pip install -U pynetdicom
```

### Usage

```bash
python3 ./speedtest.py [options] host port aec


optional arguments:
  -h, --help            show this help message and exit

Parameters:
  host                  Hostname of DICOM peer
  port                  TCP/IP port number to listen on
  aec                   Called AE title

General Options:
  --version             print version information and exit
  -q, --quiet           quiet mode, print no warnings and errors
  -v, --verbose         verbose mode, print processing details
  -d, --debug           debug mode, print debug information
  -ll [l], --log-level [l]
                        use level l for the logger (critical, error, warn, info, debug)

Network Options:
  -aet [a]etitle, --ae-title [a]etitle
                        set my AE title (default: STORESCP)
  -p [p]port, --cstore-port [p]port
                        set my STORECSP port (default: 9999)
  -ta [s]econds, --acse-timeout [s]econds
                        timeout for ACSE messages (default: 30 s)
  -td [s]econds, --dimse-timeout [s]econds
                        timeout for DIMSE messages (default: 30 s)
  -tn [s]econds, --network-timeout [s]econds
                        timeout for the network (default: 30 s)
  -pdu [n]umber of bytes, --max-pdu [n]umber of bytes
                        set max receive pdu to n bytes (0 for unlimited, default: 16382)
  -ba [a]ddress, --bind-address [a]ddress
                        The address of the network interface to listen on. If unset, listen on all interfaces.

Preferred Transfer Syntaxes:
  -x=, --prefer-uncompr
                        prefer explicit VR local byte order
  -xe, --prefer-little  prefer explicit VR little endian TS
  -xb, --prefer-big     prefer explicit VR big endian TS
  -xi, --implicit       accept implicit VR little endian TS only

Miscellaneous Options:
  --no-echo             don't act as a verification SCP
  -s [s]tudy, --study [s]tudy
                        StudyInstanceUID to retrieve default: 1.2.250.1.213.4.5.2.1.199
  -pid [p]patientid, --patientid [p]patientid
                        PatientID to retrieve default: 199
```

### Résultats

Les résultats du script sont présentés sous la forme suivante:

```bash
-----RESULTS-------------------------------------------------------------------------
Start time: 2024-07-25 11:11:44.133268
End time: 2024-07-25 11:11:56.151701
First image received at: 2024-07-25 11:11:44.574870

Transfer Syntax received: 1.2.840.10008.1.2.4.80
Total bytes transfered: 209.577218 MB
/!\ WARNING: If this is not what you expected, there must have have been some TS conversion from the PACS
Please consider these results carefully.
(Study 1.2.250.1.213.4.5.2.1.199 is initially encoded in 1.2.840.10008.1.2.4.80)

Latency (first image): 0:00:00.441602
Throughput: 139.50385578552545 Mbps
------------------------------------------------------------------------------------
```

