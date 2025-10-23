import tomllib
from functools import lru_cache
from pathlib import Path
from typing import Self

from pydantic import Field
from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    """Application Settings."""

    name: str = Field(...)
    version: str = Field(...)

    @classmethod
    def from_pyproject(cls) -> Self:
        """Load values from pyproject.toml."""
        pyproject = Path(__file__).resolve().parent / 'pyproject.toml'

        with pyproject.open('rb') as file:
            data = tomllib.load(file)

        return cls(name=data['project']['name'], version=data['project']['version'])


class GeneralSettings(BaseSettings):
    """Concatenate all settings."""

    application: ApplicationSettings = ApplicationSettings.from_pyproject()


@lru_cache
def get_settings() -> GeneralSettings:
    """Load application settings."""
    return GeneralSettings()
