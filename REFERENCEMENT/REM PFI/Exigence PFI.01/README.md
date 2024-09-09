# DRIM-M_DATA

## Contenu du répertoire
Les jeux de données présents dans ce répertoire sont à destination des éditeurs PFI pour valider l'exigence :
- SC.DB/PFI.01

## Integration avec l'environnement de test du DMP
Dans le cas d'un test d'integration avec l'environnement de DMP de test, vous allez devoir effectuer des modifications sur les exemples mis à disposition.

### Patient
Le patient utilisé dans les exemples est le patient "PAT-TROIS DOMINIQUE".
Ce patient est connu du DMP de test. Il n'y a donc pas de modification à faire dans le document CDA encodé en base64 et le segment PID des messages.

### identifiant du document  CDA
L'identifiant du document CDA se retrouve

 * dans le champs **TXA-12** et dans l'élement **ID** du document CDA pour les **messages MDM**.
 * uniquement dans l'élement **ID** du document CDA pour les **messages ORU**.

Exemple pour un document CDA : 
```XML
<id root="1.2.250.2345.3245.13.58132">
```
#### Instruction

1. Décoder le document CDA
Pour cela il faut récuperer le document CDA qui est dans le champ **OBX-5.4** 
2. Générer un nouvelle identifiant de document
3. Remplacer l'identifiant du document CDA
4. Re-encoder en base 64 le document CDA
5. Remplacer le champ **OBX-5.4** par le nouveau document CDA
6. Modifier la valeur du champ **TXA-12** par le nouvel identifiant **pour les messages MDM**.

#### Cas du remplacement de document
Dans le cas d'un remplacement de document, on retrouve l'identifiant du document à remplacer dans l'élement **relatedDocument" qui correspond à l'identifiant du document remplacé.

Exemple pour un document CDA : 
```XML
<relatedDocument typeCode="RPLC">
<parentDocument>
<id root="1.2.250.2345.3245.13.58132"/>
</parentDocument>
</relatedDocument>
```
#### Instruction

Dans ce cas, il vous faudra modifier l'identifiant du document remplacé dans le document CDA et la valeur du champ **TXA-13**





### Synthése des modifications à effectuer
| Segment  | Champs          | Description | Instruction |
| :--------------- |:---------------| :-----:| :-----|
| MSH  |   MSH-3        |  Application émettrice  | |
| MSH  | MSH-4          |   Organisation émettrice  |  |
| MSH  | MSH-5          |    Application réceptrice  | |
| MSH  | MSH-6          |   Organisation réceptrice | |
| MSH  | MSH-7          |    Date/time du message | |
| MSH  | MSH-10          |   Identifiant du message  | |
| TXA  | TXA-12          |   Identifiant du document  | pour les **messages MDM** |
| TXA  | TXA-13          |   Identifiant du document à remplacer | Dans le cas d'un remplacement et pour les **messages MDM** |
| PRT  | PRT-8.1         |   Nom de l’organisation   | |
| PRT  | PRT-8.10        |  Identifiant de l’organisation destinataire du document   |  FINESS Geographique correspondant au certicat utilisé pour l'alimentation |
| OBX  | OBX-5.4         |  Document CDA encodé en base 64    | |
