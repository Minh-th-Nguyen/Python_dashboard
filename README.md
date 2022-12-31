# Python_dashboard

L'objectif du projet est de créer un dashboard dynamique et interactif sur un sujet d'intérêt général, les données sont publics et accesible à tous

## Description

J'ai choisi de traiter les données sur les écoles élémentaires et pré-élémentaire française.

Le jeu de donnée utilisé provient du site [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/effectifs-deleves-par-niveau-et-nombre-de-classes-par-ecole-date-dobservation-au-debut-du-mois-doctobre-chaque-annee/).

## Installation et premier démarrage

Pour installer le projet sur votre machine personnelle il suffit d'entrer l'instruction suivante dans un terminal : 
git clone https://github.com/Minh-th-Nguyen/Python_dashboard

Se déplacer dans le folder Python_dashboard :
cd Python_dashboard

Installer les packages nécessaire :
python -m pip install -r requirements.txt

Finalement exécuter le fichier main.py :
python main.py

Le premier démarrage sera long car le jeu de données est téléchargé pour la première fois pour être à jour au moment du premier lancement du dashboard, les prochaines exécutions du dashboard seront plus rapide.

Il est possible de remettre à jour le dashboard en éxécutant le fichier Data.py présent dans le dossier resources.

## La problématique 

**le désengorgement des écoles et des classes promis par le gouvernement durant ces dernières années à t'il été respecté ?**

## Analyse

Nous pouvons tirer plusieurs conclusion

Nous remarquons que plus nous avançons dans les années moins il y a d'élève par école et par classe, la politique de réduire le nombre d'élève par classe / école porte donc ses fruits, cependant il y a tout de même une grande disparité entre les régions/département. 

Par exemple les départements d'outre-mer ont beaucoup plus d'élève par école / classe qu'en métropole (un exemple mayotte avec en moyenne 308 élève par école)

Nous remarquons aussi que le nombre d'élèves diminue légèrement mais tout de meme de manière significative en quelques années et qu'une relativement grande partie des élèves sont en école privé

## User guide

Une fois le programme main.py éxecuté un lien apparaîtra dans la console, récupèrer le lien URL et collez le dans le navigateur de votre choix, le dashboard devrait maintenant être visible.

Le dashboard est intéractif, toutes les figures présentent dessus ont des pop up lorsque que l'on passe dessus avec la souris, des informations ne sont donc visible que lorsque l'on passe notre souris par dessus ; par exemple les valeurs pour la carte ne sont présent que sur un pop up.

Tout en haut de la page en dessous du titre se trouve un slider, celui-ci permet de choisir l'année qui sera utilisé pour les données, le slider met à jour tous les éléments du dashboard.

les 4 indicateurs varient en fonction de l'année choisi par le slider. De plus le delta apparaissant en dessous dépend des actions de l'utilisateur, il prendra en compte la dernière année sélectionné et l'année courante (par exemple nous étions sur l'année 2019 puis allons sur l'année 2021, le slider donnera l'évolution de l'indicateur en 2021 par rapport à 2019).

La carte peut être vu par région ou par département, une icone situé en haut a droit dans la carte permet de choisir si nous souhaitons voir par département ou par région, il est également possible de choisir si nous souhaitons afficher les pop ups des regions, des départements ou aucun.

L'histograme peut être zoomé avec la souris, se déplacer une fois zoomé et sélectionner des valeurs.

Le camembert donner les valeurs exactes si l'on position sa souris sur l'élément qui nous interesse.

## Architecture du code
 
Le code est structuré en plusieurs fichier. 

Le fichier main.py permet de lancer l'application dash et fais donc tous les callbacks pour mettre à jours les graphiques, carte etc.
les callbacks font tous un appel vers une fonction du fichier figures.py, ce fichier retravail les données et renvoie toutes les figures vers le fichier pour que dash les affiche. Il fais également appelle a Data.py
le fichier layout donne la forme de la page html et la fourni a main.py pour initialiser la page dash.
Le fichier Data.py télécharge les données lors de la première éxecution du dashboard

```mermaid
graph Dashboard;
    A[Main] -->|year| B(figures);
    A--> C(dashboard);
    B -->|map| A;
       B -->|pie chart| A;
          B -->|histogram| A;
             B -->|indicator| A;
    D(Layout) -->|layout| A;
    E(data) --> |data| B ;
```
## Copyright

Je déclare sur l’honneur que le code fourni a été produit par moi même dans sa totatilité.