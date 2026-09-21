# Où et quand acheter moins cher en Gironde ?

Analyse du marché immobilier girondin à partir des données DVF (Demandes de
valeurs foncières) 2025, publiées par la DGFiP sur data.gouv.fr.

**Version lisible avec graphiques et carte** : (lien Notion / artefact à ajouter ici)

## Question

Où et quand un logement coûte-t-il le moins cher en Gironde, et quel type de
bien (maison ou appartement) permet-il d'optimiser un budget donné ?

## Résultats clés

- Le prix médian au m² va de 988 €/m² à Sainte-Foy-la-Grande (intérieur des
  terres) à 7 318 €/m² à Arcachon (Bassin), soit un facteur 7.
- Les prix restent globalement stables sur 2025 (±3 % autour de 3 400–3 500
  €/m²) : pas de "bon mois" pour négocier un prix nettement plus bas. En
  revanche, juillet et octobre concentrent le plus de ventes (plus de choix).
- Avec 250 000 €, on achète environ 46 m² sur le Bassin d'Arcachon, 59 m² à
  Bordeaux, et 112 m² dans le Libournais rural.

## Données

Source : [Demandes de valeurs foncières géolocalisées](https://www.data.gouv.fr/datasets/demandes-de-valeurs-foncieres-geolocalisees),
data.gouv.fr / DGFiP, Licence Ouverte 2.0.

- `dvf_gironde_clean.csv.gz` : ventes nettoyées utilisées pour l'analyse
  (20 074 lignes ; ventes classiques de maisons/appartements à un seul lot,
  valeurs aberrantes retirées).
- `gironde_communes.csv` : agrégat par commune (prix médian, coordonnées,
  nombre de ventes) utilisé pour la carte.
- `gironde_map.png` : carte des prix par commune.

Aucune adresse ni vente individuelle n'est exposée : toutes les données
publiées ici sont déjà agrégées par commune ou par mois.

## Reproduire l'analyse

```bash
pip install pandas matplotlib
python pipeline_gironde.py
```

Le script part du fichier brut `33.csv.gz`, téléchargeable depuis
[files.data.gouv.fr](https://files.data.gouv.fr/geo-dvf/latest/csv/2025/departements/33.csv.gz).

## Méthodologie

1. Filtrage sur les ventes classiques (hors VEFA, échanges, expropriations)
2. Filtrage sur les biens à un seul lot (prix au m² fiable)
3. Suppression des valeurs aberrantes (1er/99e centile par département)
4. Agrégation par commune, par mois et par type de bien

## Outils

Python, pandas, matplotlib.
