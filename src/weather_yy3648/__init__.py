# read version from installed package
from importlib.metadata import version
__version__ = version("weather_yy3648")

from .weather_yy3648 import (
    celsius_to_fahrenheit,
    summarize_temperatures,
    clean_readings,
)