import uvicorn

from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Form

from models.titanic import Passenger, PredictionResponse
from libs.model import predict_survival


BASE_DIR = Path(__file__).resolve(strict=True).parent
MODEL_DIR = BASE_DIR / "models_ml"


app = FastAPI(
    title="Titanic Survival API",
    description="API do predykcji przeżycia pasażera Titanica na podstawie modelu ML.",
    version="1.0.0"
)


@app.get("/", tags=["intro"])
async def index():
    return {
        "message": "Titanic Survival Prediction API",
        "docs": "/docs"
    }


@app.get("/health", tags=["intro"])
async def health():
    return {
        "status": "OK"
    }


@app.get("/model/info", tags=["model"])
async def model_info(model_name: str = "our_model"):
    model_file = MODEL_DIR / f"{model_name}.pkl"

    return {
        "model_name": model_name,
        "model_path": str(model_file),
        "model_exists": model_file.exists(),
        "expected_features": [
            "Pclass",
            "Age",
            "SibSp",
            "Parch",
            "Fare",
            "male",
            "Q",
            "S"
        ]
    }


@app.post(
    "/titanic/predict",
    tags=["titanic"],
    response_model=PredictionResponse,
    status_code=200
)
async def predict_titanic(data: Passenger, model_name: str = "our_model"):
    model_file = MODEL_DIR / f"{model_name}.pkl"

    if not model_file.exists():
        raise HTTPException(
            status_code=400,
            detail=f"Model not found: {model_file}"
        )

    try:
        survived, probability = predict_survival(data, model_file)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(error)}"
        )

    survived_label = "Survived" if survived == 1 else "Did not survive"

    return {
        "survived": survived,
        "survived_label": survived_label,
        "probability": probability
    }


@app.post(
    "/titanic/predict-form",
    tags=["titanic"],
    response_model=PredictionResponse,
    status_code=200
)
async def predict_titanic_form(
    pclass: Annotated[int, Form()],
    sex: Annotated[str, Form()],
    age: Annotated[float, Form()],
    sibsp: Annotated[int, Form()] = 0,
    parch: Annotated[int, Form()] = 0,
    fare: Annotated[float, Form()] = 0,
    embarked: Annotated[str, Form()] = "S",
    model_name: str = "our_model"
):
    data = Passenger(
        pclass=pclass,
        sex=sex,
        age=age,
        sibsp=sibsp,
        parch=parch,
        fare=fare,
        embarked=embarked
    )

    model_file = MODEL_DIR / f"{model_name}.pkl"

    if not model_file.exists():
        raise HTTPException(
            status_code=400,
            detail=f"Model not found: {model_file}"
        )

    try:
        survived, probability = predict_survival(data, model_file)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(error)}"
        )

    survived_label = "Survived" if survived == 1 else "Did not survive"

    return {
        "survived": survived,
        "survived_label": survived_label,
        "probability": probability
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8008)
