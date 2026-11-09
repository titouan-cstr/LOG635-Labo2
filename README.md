# LOG635-Labo2

# Guide d'utilisation

## Prérequis

- Python 3.8 ou plus
- Jupyter Notebook ou JupyterLab
- Bibliothèques Python :

```bash
pip install numpy opencv-python matplotlib jupyter
```

- Le dossier d'images de la base de données, accessible depuis `creation_dataset.ipynb`
- Tous les fichiers du projet dans le même dossier (notebooks et `.pickle`)

## Utilisation

1. Lancer `creation_dataset.ipynb` (toutes les cellules) pour générer `X1.pickle` et `y1.pickle`.
2. Lancer `train_model.ipynb` (toutes les cellules, dans l'ordre) pour entraîner le modèle.
3. Pour tester une image, modifier le chemin dans la **dernière cellule** de `train_model.ipynb` :

```python
# --- EXEMPLE D'UTILISATION ---
chemin_photo = "/Chemin/vers/une/photo/exemple/269_Cercle2.jpg"   # <-- à modifier
predire_image_brute(chemin_photo, nn_evaluated, X_features_mean, X_features_std)
```

Le notebook affiche la ROI détectée, la classe prédite et la confiance.