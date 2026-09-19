from ..models import ProviderSettings
from .base import Provider
from .ollama import OllamaProvider
from .openai_compat import OpenAICompatibleProvider


def get_provider(settings: ProviderSettings) -> Provider:
    if settings.provider == "ollama":
        return OllamaProvider(settings.base_url, settings.api_key, settings.model)
    return OpenAICompatibleProvider(settings.base_url, settings.api_key, settings.model)
