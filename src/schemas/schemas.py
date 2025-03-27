from pydantic import BaseModel, Field, SecretStr, computed_field, EmailStr

from enum import Enum

from typing import List, Optional

class ModelChoice(str, Enum):
    OLLAMA = "ollama"
    OPENAI = "openai"
    GEMINI = "gemini"

class OptionsFeedbackSchema(BaseModel):
    model: ModelChoice = Field(default=ModelChoice.OLLAMA)
    api_key: Optional[SecretStr] = Field(default=None)

class UserFeedbackSchema(BaseModel):
    id: str
    feedback: str
    options: OptionsFeedbackSchema = Field(default=OptionsFeedbackSchema(), exclude=True)

class CodeFeature(str, Enum):
    """
    Enum of feature codes

    Args:
        EDITAR_PERFIL: for editing profile
        VISUALIZACAO_PERFIL: for viewing profile
        DELETAR_PERFIL: for deleting profile
        CRIAR_PERFIL: for creating profile
        NOVA_FUNCIONALIDADE: for creating new functionality
    """

    EDITAR_PERFIL = "EDITAR_PERFIL"
    VISUALIZAR_PERFIL = "VISUALIZAR_PERFIL"
    DELETAR_PERFIL = "DELETAR_PERFIL"
    CRIAR_PERFIL = "CRIAR_PERFIL"
    NOVA_FUNCIONALIDADE = "NOVA_FUNCIONALIDADE"

    @classmethod
    def values(cls) -> List[str]:
        return list(map(lambda c: c.value, cls))

class RequestedFeatureSchema(BaseModel):
    """
    Feature Request
    """

    code: CodeFeature = Field(description="Code referring to the feature request")
    reason: str = Field(description="Summary of the reason for the appeal request")

class Sentiment(str, Enum):
    """
    List of possible feelings to be classified

    Args:
        POSITIVO: for positive feedback
        NEGATIVOS: for negative feedback
        INCONCLUSIVO: for incoclusive feedback
    """

    POSITIVO = "POSITIVO"
    NEGATIVO = "NEGATIVO"
    INCONCLUSIVO = "INCONCLUSIVO"

    @classmethod
    def values(cls) -> List[str]:
        return list(map(lambda c: c.value, cls))

class RatedFeedbackSchema(BaseModel):
    """
    Feedback rating
    """

    id: Optional[str] = Field(default=None)
    sentiment: Sentiment = Field(description="Feeling that informed feedback conveys")
    requested_features: List[RequestedFeatureSchema] = Field(description="List of feature requests present in the feedback")

class SentimentStatisticsSchema(BaseModel):
    POSITIVO: int = Field(default=0)
    NEGATIVO: int = Field(default=0)
    INCONCLUSIVO: int = Field(default=0)

    @computed_field
    @property
    def total(self) -> int:
        return self.POSITIVO + self.NEGATIVO + self.INCONCLUSIVO
    
    @computed_field
    @property
    def fields(self) -> List[str]:
        return self.model_fields.keys()

class FeatureStatisticsSchema(BaseModel):
    EDITAR_PERFIL: int = Field(default=0)
    VISUALIZACAO_PERFIL: int = Field(default=0)
    DELETAR_PERFIL: int = Field(default=0)
    CRIAR_PERFIL: int = Field(default=0)
    NOVA_FUNCIONALIDADE: int = Field(default=0)

    @computed_field
    @property
    def total(self) -> int:
        return self.EDITAR_PERFIL + self.VISUALIZACAO_PERFIL + self.DELETAR_PERFIL + self.CRIAR_PERFIL + self.NOVA_FUNCIONALIDADE
    
    @computed_field
    @property
    def fields(self) -> List[str]:
        return self.model_fields.keys()

class EmailSchema(BaseModel):
    id: Optional[int] = Field(default=None) 
    email: EmailStr
    name: str

class ReportSchema(BaseModel):
    main_features: List[str] = Field(description="List of main features")
    main_reasons: List[str] = Field(description="List of top reasons for each new feature")
