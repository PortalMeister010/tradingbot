def brier_score(predictions: list[float], outcomes: list[int]) -> float:
    if not predictions or len(predictions) != len(outcomes):
        return 0.0
    return sum((p - o) ** 2 for p, o in zip(predictions, outcomes)) / len(predictions)
