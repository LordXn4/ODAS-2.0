from pydantic import BaseModel


class PerformanceSettings(BaseModel):
    # Prioridade: baixa latência e baixo consumo de RAM.
    max_context_tokens: int = 1024
    threads: int = 4
    max_model_size_mb: int = 3072
    low_memory: bool = True
