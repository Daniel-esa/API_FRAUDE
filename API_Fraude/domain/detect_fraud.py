"""
Prediction des nouvelles données communiqués à l'API
"""

from fastapi import Request


from API_Fraude.infrastructure.data_modification import preprocessing
from API_Fraude.config import settings, settings_score
from API_Fraude.domain import score_mapper, fraud_rules
from API_Fraude.application.train_and_saves import train_model
from API_Fraude.infrastructure.loading import load_model_pickle

# print(settings.MODEL_PATH)



def predict_from_dataframe(df_input, request: Request, cutoff_model: float):
    
    """
    Performs fraud prediction on a given input DataFrame.

    The function uses a preloaded model and its associated metadata (min/max logit,
    score thresholds, etc.) accessed via the FastAPI application state. It applies
    preprocessing to the input data, computes fraud probabilities, converts them 
    into normalized scores, and classifies entries as fraudulent or not.

    Args
    ----------
    df_input : pandas.DataFrame
        Input data containing the features needed for prediction.
    request : fastapi.Request
        FastAPI request object containing access to the application state, 
        including the loaded model and its metadata.
    cutoff_model : float, optional
        Probability threshold for classifying an entry as fraudulent. Defaults to 0.3. Best value in our tests
    Returns
    -------
    pandas.DataFrame
        A copy of the input DataFrame with additional columns:
        - 'fraud_proba': predicted fraud probability,
        - 'fraud_score': fraud score scaled using the model’s logit bounds,
        - 'is_fraud': binary classification result (1 if fraudulent, 0 otherwise),
        - 'Fraude réelle': original label (if available),
        - 'cutoff': raw probability threshold for classification,
        - 'score_cutoff': corresponding score threshold.

    Notes
    -----
    This function expects the following to be present in the FastAPI app state:
    - 'model_pack': dictionary containing:
        - 'model': a fitted classifier with `predict_proba`,
        - 'min_logit', 'max_logit': used for score normalization,
        - 'cutoff': probability threshold for classification,
        - 'score_cutoff': score threshold for reference.

    Preprocessing is applied via `preprocessing.preprocess_input` and 
    `preprocessing.dummy_data`, and configuration constants are read from
    `settings` and `settings_score`.
    """
    # model_pack = load_model_pickle.load_pickle()
    model_pack = request.app.state.model_pack
    df_processed = preprocessing.preprocess_input(df_input=df_input, columns_to_drop=settings.COLUMNS_TO_DROP, columns_to_clean=settings.COLUMNS_TO_CLEAN, columns_to_int=settings.COLUMNS_TO_INT, hour_column=settings.HOUR_COLUMN)
    x_train_dummy = train_model.dummy_data(df_processed.drop(columns=[settings.TARGET], errors='ignore'))
    
    model = model_pack["model"]
    probas = model.predict_proba(x_train_dummy)[:, 1]

    # Scoring
    scores = score_mapper.compute_score(
        probas,
        model_pack["min_logit"],
        model_pack["max_logit"],
        min_score=settings_score.MIN_SCORE,
        max_score=settings_score.MAX_SCORE
    )

    # Détection selon seuil optimal
    cutoff = cutoff_model #model_pack["cutoff"]
    score_cutoff = score_mapper.compute_score(
        cutoff_model,
        model_pack["min_logit"],
        model_pack["max_logit"],
        min_score=settings_score.MIN_SCORE,
        max_score=settings_score.MAX_SCORE
    )
    is_fraud = (probas >= cutoff).astype(int)

    results = df_input.copy()
    results["fraud_proba"] = probas
    results["fraud_score"] = scores
    results["is_fraud"] = is_fraud
    results["Fraude réelle"] = df_input["fraude"]
    results["cutoff"] = cutoff
    results["score_cutoff"] = score_cutoff
    
    #coucou
    
    return results


