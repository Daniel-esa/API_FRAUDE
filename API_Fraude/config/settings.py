"""
Appel de mes chemins et de mes variables globales
"""

# Chemins vers les fichiers importants

MODEL_PATH = "API_Fraude/data/fraud_model.pkl"
DATA_PATH = "API_Fraude/data/autorisations.sas7bdat"

# Chemin pour les tests
TEST_PATH = "API_Fraude/data/tests"

# Variables à supprimer

COLUMNS_TO_DROP = [
        'FM_Difference_Pays_12', 'FM_Difference_Pays_24',
        'FM_Difference_Pays_3', 'FM_Difference_Pays_6', 'Montant',
        'FM_Redondance_MCC_12', 'FM_Redondance_MCC_24', 'FM_Redondance_MCC_6',
        'FM_Sum_12', 'FM_Sum_3', 'FM_Sum_6', 'FM_Velocity_Condition_12',"Carte", "dateheure", "CodeRep"] 

# Colonnes à clean

COLUMNS_TO_CLEAN = ['MCC', 'Pays', 'Heure']

# Colonnes à transformer en entier

COLUMNS_TO_INT = ["Heure", "fraude"] # on verra ça après

# Variable cible
TARGET = "fraude"

# Date pour split

DATE_COLUMN = "Date"

# Colonne heure. utiliser pour un traitement spécifique
HOUR_COLUMN = "Heure"

# Variable avec traitement particulier 

#Split date pour train/test
SPLIT_DATE = "2004-04-01"

# SEED

SEED = 42


