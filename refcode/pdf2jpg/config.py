"""Configuration module for PDF to JPG Converter.

Handles loading and validation of settings from settings.json.
"""

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

logger = logging.getLogger(__name__)


@dataclass
class CropSettings:
    """Crop settings for image output.
    
    Values are percentages (0-100) indicating the crop region.
    """
    enabled: bool = False
    horizontal_start: float = 0.0
    horizontal_end: float = 100.0
    vertical_start: float = 0.0
    vertical_end: float = 100.0

    def __post_init__(self) -> None:
        """Validate crop values are within 0-100 range."""
        for attr in ['horizontal_start', 'horizontal_end', 'vertical_start', 'vertical_end']:
            value = getattr(self, attr)
            if not (0 <= value <= 100):
                raise ValueError(f"{attr} must be between 0 and 100, got {value}")
        
        if self.horizontal_start >= self.horizontal_end:
            raise ValueError(f"horizontal_start ({self.horizontal_start}) must be less than horizontal_end ({self.horizontal_end})")
        if self.vertical_start >= self.vertical_end:
            raise ValueError(f"vertical_start ({self.vertical_start}) must be less than vertical_end ({self.vertical_end})")


@dataclass
class Settings:
    """Application settings loaded from settings.json."""

    input_folder: Path = field(default_factory=lambda: Path("./input"))
    output_folder: Path = field(default_factory=lambda: Path("./output"))
    dpi: int = 300
    format: Literal["jpg", "png"] = "jpg"
    jpg_quality: int = 90
    colorspace: Literal["rgb", "gray"] = "rgb"
    overwrite: bool = False
    skip_if_exists: bool = True
    max_pages_per_pdf: int = 0  # 0 = no limit
    fail_fast: bool = False
    log_file: Path | None = None
    crop: CropSettings = field(default_factory=CropSettings)

    def __post_init__(self) -> None:
        """Validate and convert path strings to Path objects."""
        if isinstance(self.input_folder, str):
            self.input_folder = Path(self.input_folder)
        if isinstance(self.output_folder, str):
            self.output_folder = Path(self.output_folder)
        if isinstance(self.log_file, str):
            self.log_file = Path(self.log_file) if self.log_file else None

        # Validate dpi
        if not (72 <= self.dpi <= 1200):
            logger.warning(f"DPI {self.dpi} is unusual. Recommended: 72-600.")

        # Validate jpg_quality
        if not (1 <= self.jpg_quality <= 100):
            raise ValueError(f"jpg_quality must be 1-100, got {self.jpg_quality}")


def load_settings(settings_path: Path | None = None) -> Settings:
    """Load settings from JSON file.

    Args:
        settings_path: Path to settings.json. If None, uses default location.

    Returns:
        Settings object with loaded or default values.

    Raises:
        FileNotFoundError: If settings file doesn't exist.
        json.JSONDecodeError: If settings file is invalid JSON.
    """
    if settings_path is None:
        # Default: look for settings.json next to the executable/script
        settings_path = Path("settings.json")

    if not settings_path.exists():
        logger.warning(f"Settings file not found: {settings_path}. Using defaults.")
        return Settings()

    logger.info(f"Loading settings from: {settings_path}")

    with open(settings_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Parse crop settings
    crop_data = data.get("crop", {})
    crop_settings = CropSettings(
        enabled=crop_data.get("enabled", False),
        horizontal_start=crop_data.get("horizontal", {}).get("start", 0.0),
        horizontal_end=crop_data.get("horizontal", {}).get("end", 100.0),
        vertical_start=crop_data.get("vertical", {}).get("start", 0.0),
        vertical_end=crop_data.get("vertical", {}).get("end", 100.0),
    )

    # Map JSON keys to Settings fields
    return Settings(
        input_folder=data.get("input_folder", "./input"),
        output_folder=data.get("output_folder", "./output"),
        dpi=data.get("dpi", 300),
        format=data.get("format", "jpg"),
        jpg_quality=data.get("jpg_quality", 90),
        colorspace=data.get("colorspace", "rgb"),
        overwrite=data.get("overwrite", False),
        skip_if_exists=data.get("skip_if_exists", True),
        max_pages_per_pdf=data.get("max_pages_per_pdf", 0),
        fail_fast=data.get("fail_fast", False),
        log_file=data.get("log_file"),
        crop=crop_settings,
    )


def setup_logging(settings: Settings) -> None:
    """Configure logging based on settings.

    Args:
        settings: Application settings.
    """
    handlers: list[logging.Handler] = []

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s - %(message)s", datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    handlers.append(console_handler)

    # File handler (if configured)
    if settings.log_file:
        file_handler = logging.FileHandler(settings.log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)

    # Configure root logger
    logging.basicConfig(level=logging.DEBUG, handlers=handlers, force=True)

    logger.info("Logging configured.")
