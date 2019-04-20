# Projet de Licence L3 : Algorithme Evolutionniste
Ce projet consiste en l'implémentation d'un algorithme génétique avec pour modèle d'entrainement un robot balance.
Nous utilisons comme moteur physique Pybullet.

## Installation :
Pour l'installation, vous aurez besoins de plusieurs packages, vous pouvez les installer en utilisant :

#### Avec windows

Pour l'installation de Pybullet, vous risquez d'avoir besoin d'installer Visual Studio.
Pybullet nécessite certains composants installés avec.

Vous devez lancer la commande en tant qu'administrateur :
```bash
pip install pybullet numpy
```

puis

```bash
git clone https://github.com/MatheoDumont/L3_Projet.git
```

#### Avec Linux

```bash
pip3 install -U pybullet numpy
```
puis
```bash
git clone https://github.com/MatheoDumont/L3_Projet.git
```


## Utilisation

Assurez vous d'être dans le bon répertoire :
```zsh
cd /votre/chemin/L3_projet
```

Utiliser cette commande pour lancer lancer l'algo:
```bash
python main.py [1] [2] [3]
```
1. boolean : Affichage graphique sinon ligne de commande
2. integer : Nombre d'individus pour la simulation, nous vous conseillons 10, autrement cela risque de ne pas marcher.
3. boolean : Charge le dernier réseau de neurones sauvegardé

Pour utiliser l'algorithme déjà entrainé, il faut donc mettre le 3ème argument à ```True```.

Pour sauvegarder et manipuler plus d'un réseau de neurones à la fois, 
ça se passe dans gen_algo.py avec les méthodes ```load_genes_from_disk``` et ```save_to_disk``` que vous devrez manipuler.
