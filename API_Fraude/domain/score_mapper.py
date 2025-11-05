import numpy as np

def compute_score(probability, min_logit, max_logit, min_score=0, max_score=1000):
    """
    Converts a probability into a normalized score using the logit function.

    The probability is transformed into a logit (log-odds), then scaled linearly to 
    a score within the range [min_score, max_score], based on the provided 
    logit bounds (min_logit and max_logit).

    Args
    ----------
    probability : float
        A probability value between 0 and 1 (excluding exact 0 and 1).
    min_logit : float
        Minimum expected logit value used for normalization.
    max_logit : float
        Maximum expected logit value used for normalization.
    min_score : float, optional
        Minimum value of the output score range. Default is 0.
    max_score : float, optional
        Maximum value of the output score range. Default is 1000.

    Returns
    -------
    float
        A score scaled to the specified range, rounded to the nearest integer.

    Notes
    -----
    This function assumes the existence of a `log_odd(probability)` function that 
    safely computes the logit of a probability. Probabilities close to 0 or 1 
    should be clipped before applying the logit to avoid infinite values.
    """
    # Clip la proba pour éviter les infs (0 et 1 extrêmes)
    
    logit = log_odd(probability)
    score = ((logit - min_logit) * (max_score - min_score) / (max_logit - min_logit)) + min_score
    
    return np.round(score)

def log_odd(p):
    """
    Computes the log-odds (logit) of a probability value.

    The input probability is first clipped to avoid extreme values (0 and 1),
    which would otherwise result in infinite log-odds. The logit is then 
    computed as log(p / (1 - p)).

    Args
    ----------
    p : float or array-like
        Probability value(s) in the range [0, 1].

    Returns
    -------
    float or ndarray
        Log-odds corresponding to the input probability.

    Notes
    -----
    Clipping is applied using a small epsilon (1e-6) to avoid division by zero 
    or taking the logarithm of zero.
    """
    p_clipped = np.clip(p, 1e-6, 1 - 1e-6)
    log_odds = np.log(p_clipped / (1 - p_clipped))
    
    return log_odds

# def n_approved(probas, thresholds):
#     return np.sum(probas >= thresholds)