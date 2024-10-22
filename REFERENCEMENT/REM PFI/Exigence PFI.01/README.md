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
### structure de l'auteur du document CDA
L'identifiant de structure de l'auteur du document CDA se retrouve dans le champs **PRT-8.10** et dans l'élement **author/assignedAuthor/representedOrganization/id** du document CDA.

Exemple pour un document CDA : 
```XML
<author>
<time value="20210409094914.827+0100"></time>
<assignedAuthor>
<id extension="801234564895" root="1.2.250.1.71.4.2.1"></id>
<addr nullFlavor="UNK"></addr>
<telecom nullFlavor="UNK"></telecom>
<assignedPerson>
<name>
<family qualifier="SP">Eric</family>
<given>Thomas</given>
</name>
</assignedPerson>
<representedOrganization>
<id extension="1120456789" root="1.2.250.1.71.4.2.2"></id>
<name>Organisation-Y</name>
<telecom nullFlavor="UNK"></telecom>
<addr nullFlavor="UNK"></addr>
</representedOrganization>
</assignedAuthor>
</author>
```
#### Instruction

1. Décoder le document CDA
Pour cela il faut récuperer le document CDA qui est dans le champ **OBX-5.4** 
2. Générer un nouvelle identifiant de document
3. Remplacer l'identifiant du document CDA
4. Remplacer l'identifiant de la structure de l'auteur du document CDA
5. Re-encoder en base 64 le document CDA
6. Remplacer le champ **OBX-5.4** par le nouveau document CDA
7. Modifier la valeur du champ **TXA-12** par le nouvel identifiant **pour les messages MDM**
8. Modifier la valeur du champ **PRT-8.10** par le nouvel identifiant de la structure de l'auteur


### Synthése des modifications à effectuer dans le message HL7v2

| Segment  | Champs          | Description | Instruction |
| :--------------- |:---------------| :-----:| :-----|
| MSH  |   MSH-3        |  Application émettrice  | |
| MSH  | MSH-4          |   Organisation émettrice  |  |
| MSH  | MSH-5          |    Application réceptrice  | |
| MSH  | MSH-6          |   Organisation réceptrice | |
| MSH  | MSH-7          |    Date/time du message | |
| MSH  | MSH-10          |   Identifiant du message  | |
| TXA  | TXA-12          |   Identifiant du document  | pour les **messages MDM** |
| PRT  | PRT-8.7         |   Type d’identifiant de l’organisation   | pour PRT-4 = ‘SB^Send by^participation’ |
| PRT  | PRT-8.10        |  Identifiant de l’organisation à l’origine de la demande de traitement sur le(s) document(s)   |  pour PRT-4 = ‘SB^Send by^participation’ |
| PRT  | PRT-15.4        |  adresse email de destination   |  pour PRT-4 = ‘RCT^Result Copies To^participation’ |
| OBX  | OBX-5.4         |  Document CDA encodé en base 64    | modifié Id du document principal et/ou du document remplacé et le champ author/assignedAuthor/representedOrganization/id |
