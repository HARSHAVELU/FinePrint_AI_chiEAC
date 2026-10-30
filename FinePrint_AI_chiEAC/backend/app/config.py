import os
from dataclasses import dataclass
os.environ['LANGSMITH_TRACING'] = 'false'
os.environ['LANGCHAIN_TRACING_V2'] = 'false'
@dataclass(frozen=True)
class Settings:
    mode: str = os.getenv('FINEPRINT_MODE', 'demo')
    model: str = os.getenv('FINEPRINT_MODEL', 'claude-haiku-4-5')
    retrieval: str = os.getenv('FINEPRINT_RETRIEVAL', 'lexical')
    redaction: str = os.getenv('FINEPRINT_REDACTION', 'regex')
    ttl: int = int(os.getenv('FINEPRINT_TTL', '1800'))
    max_bytes: int = 5 * 1024 * 1024
    max_rows: int = 400
    threshold: float = float(os.getenv('FINEPRINT_THRESHOLD', '.18'))
settings = Settings()
