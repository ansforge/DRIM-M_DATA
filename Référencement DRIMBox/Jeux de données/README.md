# Jeux de données - Référencement DRIMBox  

Cet espace est composé d'un ensemble de répertoires associés à la mise à disposition des jeux de données impliqués dans le cadre du processus d'homologation SEGUR vague 2 spécifique aux systèmes DRIMBox. 

Chaque répertoire est nommé en fonction du standard correspondant aux jeux de données qu'il héberge. Ainsi : 
- Répertoire CDA : Comptes-rendus d'imagerie, au format CDA-R2 Niveau 1.
- Répertoire HL7v2 : Messages HL7v2 ORU/MDM véhiculant des comptes-rendus d'imagerie CDA. 
- Répertoire Images DICOM : Instances DICOM correspondant aux images médicales associées à un ensemble d'examens d'imagerie. 
- Répertoire IOCM : Objet KOS-IOCM associé à la suppression d'instances DICOM au sein d'un examen d'imagerie. 
- Répertoire KOS : Documents de références d'objets d'un examen d'imagerie (KOS).
- Répertoire PDF : Comptes-rendus d'imagerie métier, comportant un template d'URL d'accès à la visionneuse d'un système DRIMBox source. 
- Répertoire XDM : Archive XDM à utiliser dans le cadre d'un import de données au sein d'un système DRIMBox.

Afin de déterminer les conditions de mise en œuvre de chacun de ces jeux de données, il est vivement conseillé de se reporter aux scénarios de test associés au processus d'homologation SEGUR vague 2 spécifique aux systèmes DRIMBox. Cela permettra notamment de différencier les jeux de données passants de ceux associés à un cas d'erreur. 

Certains répertoires (CDA, HL7v2, Images DICOM) comportent un dossier dénommé "Annexes". Au sein de ce dossier, l'utilisateur pourra retrouver un ensemble de jeux de données transmis à titre informatif. En effet, à première vue, ces jeux de données ne sont pas indispensables au bon déroulement de la session de test Homologation SEGUR vague 2 spécifique aux systèmes DRIMBox. Cependant, il a été jugé pertinent de tout de même mettre à disposition ces jeux de données afin d'anticiper d'éventuels besoins d'informations complémentaires.  



