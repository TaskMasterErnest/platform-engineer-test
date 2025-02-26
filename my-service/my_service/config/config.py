from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pydantic import AnyHttpUrl, computed_field


class Settings(BaseSettings):
    BACKEND_ORIGINS: List[AnyHttpUrl] = []
    FASTAPI_PROJECT_NAME: str = "my-service"
    LOG_LEVEL: str = "DEBUG"
    
    # ArgoCD Config defaults
    ARGOCD_SERVER: str = "<ARGOCD_SERVER>"
    ARGOCD_PORT: str = "<ARGOCD_PORT>"
    ARGOCD_PASSWORD: str = "<ARGOCD_ADMIN_USER_PASSWORD>"
    ARGOCD_USERNAME: str = "<ARGOCD_USERNAME>"                              # default argocd user
    TOKEN_CACHE_TTL: int = 600
    
    @computed_field
    def ARGOCD_URL(self) -> str:
        return f"{self.ARGOCD_SERVER}:{self.ARGOCD_PORT}"
    
    model_config = SettingsConfigDict(env_nested_delimiter='__')

settings = Settings(_env_file=".env")