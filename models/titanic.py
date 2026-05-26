from pydantic import BaseModel, Field
from typing import Literal, Optional


class Passenger(BaseModel):
    pclass: int = Field(..., ge=1, le=3, description="Passenger class: 1, 2 or 3")
    sex: Literal["male", "female"] = Field(..., description="Passenger sex")
    age: float = Field(..., ge=0, description="Passenger age")
    sibsp: int = Field(0, ge=0, description="Number of siblings/spouses aboard")
    parch: int = Field(0, ge=0, description="Number of parents/children aboard")
    fare: float = Field(0, ge=0, description="Ticket fare")
    embarked: Literal["C", "Q", "S"] = Field("S", description="Port of embarkation: C, Q or S")


class PredictionResponse(BaseModel):
    survived: int
    survived_label: str
    probability: Optional[float] = None
