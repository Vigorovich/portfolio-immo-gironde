"""
Analyse DVF Gironde 2025 — pipeline complet
Source des données : Demandes de valeurs foncières géolocalisées (data.gouv.fr / DGFiP)
https://www.data.gouv.fr/datasets/demandes-de-valeurs-foncieres-geolocalisees
Licence Ouverte 2.0

Usage : télécharger 33.csv.gz depuis
https://files.data.gouv.fr/geo-dvf/latest/csv/2025/departements/33.csv.gz
puis lancer ce script.
"""
import pandas as pd

# 1. Chargement -----------------------------------------------------------
df = pd.read_csv("33.csv.gz", compression="gzip", low_memory=False)

# 2. Nettoyage --------------------------------------------------------------
# Ventes classiques de logements uniquement (hors VEFA, échanges, expropriations)
df = df[df["nature_mutation"] == "Vente"]
df = df[df["type_local"].isin(["Maison", "Appartement"])]

# Une mutation avec plusieurs lots fausse le prix au m² -> on ne garde
# que les mutations à un seul bien
counts = df.groupby("id_mutation")["id_mutation"].transform("count")
df = df[counts == 1]

df["valeur_fonciere"] = pd.to_numeric(df["valeur_fonciere"], errors="coerce")
df["surface_reelle_bati"] = pd.to_numeric(df["surface_reelle_bati"], errors="coerce")
df = df.dropna(subset=["valeur_fonciere", "surface_reelle_bati"])
df = df[(df["surface_reelle_bati"] >= 9) & (df["valeur_fonciere"] >= 5000)]

df["prix_m2"] = df["valeur_fonciere"] / df["surface_reelle_bati"]

# Valeurs aberrantes : on retire le 1er et le 99e centile
lo, hi = df["prix_m2"].quantile([0.01, 0.99])
df = df[(df["prix_m2"] >= lo) & (df["prix_m2"] <= hi)]

df["date_mutation"] = pd.to_datetime(df["date_mutation"])
df["mois"] = df["date_mutation"].dt.to_period("M").astype(str)

print(f"{len(df)} ventes exploitables")

# 3. Où acheter moins cher : agrégat par commune -----------------------------
# Jamais d'adresse ni de vente individuelle affichée : uniquement des médianes
# par commune, avec un seuil minimum de ventes pour la fiabilité statistique.
communes = (
    df.groupby("nom_commune")
    .agg(
        n=("prix_m2", "size"),
        prix_m2=("prix_m2", "median"),
        lat=("latitude", "median"),
        lon=("longitude", "median"),
    )
    .reset_index()
)
communes_fiables = communes[communes.n >= 10]

# 4. Quand acheter : agrégat par mois ----------------------------------------
mensuel = (
    df.groupby("mois")
    .agg(n=("prix_m2", "size"), prix_m2=("prix_m2", "median"))
    .reset_index()
)

# 5. Quel bien pour quel budget ----------------------------------------------
par_type = (
    df.groupby("type_local")
    .agg(n=("prix_m2", "size"), prix_m2=("prix_m2", "median"), surface=("surface_reelle_bati", "median"))
)

zones = {
    "Bordeaux": ["Bordeaux"],
    "Bassin d'Arcachon": ["Arcachon", "Lège-Cap-Ferret", "La Teste-de-Buch", "Andernos-les-Bains"],
    "Libournais (rural)": ["Libourne", "Castillon-la-Bataille", "Sainte-Foy-la-Grande"],
}
for zone, communes_zone in zones.items():
    sub = df[df.nom_commune.isin(communes_zone)]
    prix_m2_median = sub["prix_m2"].median()
    surface_250k = 250_000 / prix_m2_median
    print(f"{zone}: {prix_m2_median:.0f} €/m², {surface_250k:.0f} m² pour 250 000 €")
