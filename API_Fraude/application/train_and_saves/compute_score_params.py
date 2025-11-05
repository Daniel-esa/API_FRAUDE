"""
Fixations des bornes du logit pour la conversiond es probas en score compris entre 0 et 1000
"""
import pandas as pd

from API_Fraude.application.train_and_saves.train_model import modele, x_train_dummy,  X_test, y_test
from API_Fraude.domain.score_mapper import log_odd



## Probabilités tests

X_test_dummy = pd.get_dummies(X_test, drop_first=True).reindex(columns=x_train_dummy.columns, fill_value=0)

probas = modele.predict_proba(X_test_dummy)[:, 1]

## Calcul des log-odds sur les probas du test (pas les seuils ROC)

log_odds = log_odd(probas)

## Fixation des bornes à partir des prédictions test

min_logit, max_logit = log_odds.min(), log_odds.max()


# model: ok
# columns : ok
# min_logit : ok
# max_logit : ok
# cut_off optimal : non
# score optimal : non
## Conversion des probabilités en scores
