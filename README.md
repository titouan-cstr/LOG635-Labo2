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
2. Dans `train_model.ipynb`, exécuter toutes les cellules
3. Vérifier le résultat de la Partie 6 : exactitude d'environ 96,6 % et F1 macro d'environ 0,96.

## Tester une image

La dernière cellule de `train_model.ipynb` teste une image avec le modèle final. Pour changer d'image, modifier le chemin relatif :

```python
chemin_photo = "EnsembleA/Cercles/Cercle2/269_Cercle2.jpg"
```

Le notebook affiche la ROI détectée, la classe prédite et la confiance.
