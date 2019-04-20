# Projet de Licence L3 : Algorithme Evolutionniste
Ce projet consiste en l'implémentation d'un algorithme génétique avec pour model d'entrainement un robot balance.


## Installation :
Pour l'installation, vous aurez besoins de plusieurs package, vous pouvez les installer en utilisant :

#### Pour windows

Pour l'installation de pybulle, vous risquez d'avoir besoin d'installer Visual Studio.
Pybullet necessite certains composants installés avec.

Vous devez lancer la commande en étant administrateur :
```zsh
pip install pybullet numpy
```

puis

```bash
git clone https://github.com/MatheoDumont/L3_Projet.git
```

#### Pour Linux

```bash
sudo pip3 install pybullet numpy
```

```bash
git clone https://github.com/MatheoDumont/L3_Projet.git
```


## Utilisation
Pour utiliser l'algorithme déjà entrainé
Assurez vous d'être dans le bon répertoire :
```zsh
cd L3_projet
```

Utiliser cette commande pour lancer lancer l'algo:
```bash
python main.py [1] [2] [3]
```
1. boolean : Affichage graphique : True, sinon ligne de commande
2. integer : Nombre d'individus pour la simulation, nous vous conseillons 10, autrement cela risque de ne pas marcher.
3. boolean : Charger une sauvegarde d'un réseau de neurones antérieur.
