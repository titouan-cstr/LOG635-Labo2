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

Tout le laboratoire est dans un seul notebook : `LOG635_Lab2.ipynb`.

1. Exécuter toutes les cellules dans l'ordre.
2. La Partie 4 génère `X1.pickle` et `y1.pickle` (1 566 images) ainsi que le dossier `EnsembleB/` : les 1 514 ROI uniques en PNG 64×64, classées par étiquette (à remettre dans le .zip).
3. Vérifier le résultat de la Partie 6 : exactitude moyenne d'environ 95,1 % et F1 macro d'environ 0,948.

Le rapport est dans `Rapport_Lab2.md` (figures dans `rapport_images/`).

## Tester une image

La section « Complément : tester une image brute » (après la Partie 6) teste une image avec le modèle final. Pour changer d'image, modifier le chemin relatif :

```python
chemin_photo = "EnsembleA/Cercles/Cercle2/269_Cercle2.jpg"
```

Le notebook affiche la ROI détectée, la classe prédite et la confiance.
