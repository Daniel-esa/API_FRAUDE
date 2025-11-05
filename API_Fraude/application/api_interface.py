"""
Interface de mon API
"""
import pandas as pd
from fastapi import FastAPI, UploadFile, File, Request, Query
from fastapi.responses import JSONResponse
from io import StringIO

from contextlib import asynccontextmanager
from API_Fraude.domain.detect_fraud import predict_from_dataframe
from API_Fraude.infrastructure.loading import load_model_pickle
from API_Fraude.domain import fraud_rules

@asynccontextmanager #<- générateur qui gère une entrée et une sortie dans un contexte
async def lifespan(app: FastAPI):
    """
    Loads the machine learning model into FastAPI's application state during startup.

    This asynchronous context manager ensures that the model is loaded once at 
    application launch and is available throughout the app's lifetime via 
    `app.state.model_pack`.

    Parameters
    ----------
    app : fastapi.FastAPI
        The FastAPI application instance.

    Yields
    ------
    None
        Control is passed back to FastAPI to handle incoming requests.
    
    Side Effects
    ------------
    - Sets `app.state.model_pack` with the model and associated metadata.
    - Prints a startup and shutdown message to the console.
    """
    print("Chargement du modèle au démarrage...")
    app.state.model_pack = load_model_pickle.load_pickle()
    yield # <- générateur
    print("API arrêtée.")

app = FastAPI(
    title="API Score Fraude",
    description="API de détection de fraude avec FastAPI",
    version="1.0.0",    
    contact={"name": "Daniel"},
    lifespan=lifespan
)


@app.post("/predict/")
async def predict_from_json_file(file: UploadFile = File(...),
                                    request: Request = None, cutoff_threshold : float = Query(fraud_rules.FRAUD_RATE_THRESHOLD)):
    """
    Endpoint for fraud prediction from a JSON file upload.

    Accepts a JSON or JSON Lines (NDJSON) file containing a batch of input data, 
    parses it into a pandas DataFrame, and returns fraud predictions, scores, 
    and classification results.

    Parameters
    ----------
    file : UploadFile
        A JSON or NDJSON file uploaded by the client containing feature data.
    request : fastapi.Request, optional
        FastAPI request object providing access to the app's model in `app.state`.

    Returns
    -------
    List[dict]
        A list of prediction results for each row in the input, with keys:
        - 'fraud_proba': predicted fraud probability,
        - 'fraud_score': fraud score (scaled),
        - 'is_fraud': binary classification (0 or 1),
        - 'fraude': original label (if present),
        - 'score_cutoff': threshold used for scoring,
        - 'cutoff': probability threshold used for classification.

    Raises
    ------
    JSONResponse
        If any error occurs during file reading, parsing, or prediction,
        returns a 500 error with an appropriate message.

    Notes
    -----
    - Attempts to parse both standard JSON and JSON Lines formats.
    - Requires the model to be loaded in `app.state.model_pack` via the lifespan context.
    """
    try:
        contents = await file.read()
        decoded = contents.decode('utf-8')  # bytes -> str

        # Convertir le contenu JSON en DataFrame
        try:
            # 1. Essayer avec format classique
            df = pd.read_json(StringIO(decoded))
        except ValueError:
            # 2. Essayer JSON Lines (format NDJSON)
            df = pd.read_json(StringIO(decoded), lines=True)

        print("DEBUG :", request.app.state.model_pack.keys(), "cutoff:", request.app.state.model_pack['cutoff'], "score_cutoff:", request.app.state.model_pack['score_cutoff'])
        
        result_df = predict_from_dataframe(df, request = request, cutoff_model=cutoff_threshold)
        results = result_df[["fraud_proba", "fraud_score", "is_fraud", "fraude", "score_cutoff", "cutoff"]]

        return results.to_dict(orient="records")

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erreur lors de la prédiction : {str(e)}"}
        )
