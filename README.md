# LOG635-Labo2

# Guide d'utilisation

## Prérequis

- Python 3.8 ou plus
- Jupyter Notebook ou JupyterLab
- Bibliothèques Python :

```bash
pip install numpy opencv-python imutils matplotlib scikit-learn pandas jupyter
```

- Le dossier `EnsembleA` à la racine du projet
- Jupyter lancé depuis la racine du projet

## Utilisation

1. Dans `creation_dataset.ipynb`, exécuter toutes les cellules. Cela génère `X1.pickle` et `y1.pickle` (1 566 images).
2. Dans `train_model.ipynb`, ne pas utiliser « Run All », car l'ancienne cellule de l'Étape 6 s'arrête sur une erreur. Exécuter dans cet ordre :
   - la première cellule de code ;
   - la cellule de code de l'Étape 1 ;
   - la cellule de code de l'Étape 3 ;
   - les 6 cellules de code sous l'Étape 9, de haut en bas (environ 5 minutes).
3. Vérifier le résultat dans la dernière cellule : exactitude d'environ 96,6 % et F1 macro d'environ 0,96.

## Tester une image

Après les cellules des Étapes 1 et 3, exécuter la cellule située sous « Correction du bug d'évaluation », puis la cellule de l'Étape 8. Pour changer d'image, modifier le chemin relatif :

```python
chemin_photo = "EnsembleA/Cercles/Cercle2/269_Cercle2.jpg"
```

Le notebook affiche la ROI détectée, la classe prédite et la confiance.
