from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime

class GeospatialDataProvider(ABC):
    """
    Common Abstract Interface for Geospatial & Satellite Data Providers.
    Allows seamless hot-swapping between Google Earth Engine (live) and DemoDataProvider (synthetic fallback).
    """

    @abstractmethod
    def get_elevation_grid(self, min_lat: float, min_lon: float, max_lat: float, max_lon: float) -> Dict[str, Any]:
        """Retrieve digital elevation model (DEM) grid data."""
        pass

    @abstractmethod
    def get_satellite_imagery_layer(self, region_id: str, date_str: Optional[str] = None) -> Dict[str, Any]:
        """Retrieve optical or multispectral satellite metadata and tile URL."""
        pass

    @abstractmethod
    def get_land_cover_classification(self, region_id: str) -> Dict[str, Any]:
        """Retrieve land cover classification (urban, wetland, coastal mangrove, agricultural)."""
        pass

    @abstractmethod
    def get_precipitation_accumulation(self, cyclone_id: str) -> Dict[str, Any]:
        """Retrieve satellite/radar precipitation accumulation layer (e.g. GPM / IMERG)."""
        pass

    @abstractmethod
    def get_provider_status(self) -> Dict[str, Any]:
        """Return provider connection state, provenance status, and freshness."""
        pass
