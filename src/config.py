import yaml
from pathlib import Path
from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings

class AppConfig(BaseModel):
    name: str
    timezone: str
    environment: str

class PathConfig(BaseModel):
    source_excel: str
    raw_data: str
    processed_data: str
    logs: str

class ScraperConfig(BaseModel):
    request_timeout: int
    user_agent: str
    max_retries: int

class LLMConfig(BaseModel):
    provider: str
    model: str
    temperature: float

class AnalysisConfig(BaseModel):
    impact_levels: dict[str, list[str]]

class EmailConfig(BaseModel):
    enabled: bool
    send_high_immediately: bool
    daily_digest_time: str

class NotificationConfig(BaseModel):
    email: EmailConfig

class SchedulerConfig(BaseModel):
    enabled: bool
    run_frequency: str

class Settings(BaseSettings):
    app: AppConfig
    paths: PathConfig
    scraper: ScraperConfig
    llm: LLMConfig
    analysis: AnalysisConfig
    notifications: NotificationConfig
    scheduler: SchedulerConfig

    @classmethod
    def load(cls):
        yaml_path = Path("config/setting.yaml")
        if not yaml_path.exists():
            # Fallback for tests if run from different dir
            yaml_path = Path(__file__).parent.parent / "config" / "setting.yaml"
        
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)

settings = Settings.load()
