from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """All config comes from environment variables, nothing hardcoded."""

    server_port: int = 8000
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "orbit"
    db_user: str = "orbit"
    db_password: str = "orbit"
    
    # URL of interns-api; used to validate intern exists before creating task
    interns_api_url: str = "http://localhost:8080"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
