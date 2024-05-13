Ce répertoire contient une liste blanche répertoriant un ensemble d'URL et Certificats de DRIMbox fictives.


La liste blanche a été signée à l'aide d'un certificat ORG SIGN de l'offre organisation de l'AC IGC Santé environnement TEST.
la signature utilisée est de type enveloppée, elle est conforme aux spécifications DRIMbox.

le certificat de signature utilisé par l'ANS pour signer la liste blanche est issu de l'infrastructure de gestion de la confiance "IGC-SANTE" Environnement TEST.
http://igc-sante.esante.gouv.fr/PC%20TEST/

La gamme utilisée est : Elementaire Test
Domaine : Racine pour l'autorité et Organisation pour le certificat Signature.

Cette liste blanche est mise à disposition par l'ANS à destination des éditeurs afin qu'ils puissent faire leurs vérifications de signature conformes aux exigences et scénarios rédigés.

Notamment 
- les vérificatons cryptographiques à partir des certificats Racine et Intermédiaire.
- la vérification du contenu du certificat de signature utilisé (Vérification CN et OU) avec le contrôle de sa validité
Enfin la vérification de non révocation du certificat à partir du fichier CRL accessible sur le site de l'IGC Sante.

Le contenu du certificat de signature utilisé pour signer le fichier est : 
CN=Liste Blanche DRIM-M,OU=318751275100020


A noter que l'ANS recommande l'implémententation de l'outil Esign pour réaliser les vérifications.
https://github.com/ansforge/esignsante

Si un outil tiers est utilisé il sera nécessaire de créer un keystore avec les certificats racine et intermédiaire.
Si l'outil EsignSanté de l'ANS est utilisé la vérification à l'aide de cette commande produira un fichier encodé.
Exemple : curl -X POST "http://10.3.26.30/esignsante/v1/validation/signatures/xadesbaselineb" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "idVerifSignConf=1" -F "file=@c:\test\listeblanche_INFORMATIFSIGNE.xml;type=text/xml" > c:\test\listeblanche_INFORMATIQUESIGNE.log
Le fichier log est dans le répertoire listeblanche pour interprétation.
L'avantage est que l'outil Esign Santé peut charger directement les donnée de l'infrastructure IGC-SANTE
A noter dans l'exemple le statut True qui permet de signifier la vérification et validation de la signature.
