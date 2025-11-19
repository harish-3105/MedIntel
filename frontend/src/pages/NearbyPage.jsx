// Nearby Medical Facilities with GPS/Geolocation
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { useEffect, useRef, useState } from 'react';

function NearbyPage() {
  const [userLocation, setUserLocation] = useState(null);
  const [facilities, setFacilities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [locationInput, setLocationInput] = useState('');
  const [filters, setFilters] = useState({
    hospital: true,
    clinic: true,
    pharmacy: true,
  });

  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const userMarkerRef = useRef(null);
  const facilitiesMarkersRef = useRef([]);

  // Initialize map
  useEffect(() => {
    if (!mapInstanceRef.current && mapRef.current) {
      // Initialize Leaflet map
      mapInstanceRef.current = L.map(mapRef.current).setView([20.5937, 78.9629], 5);

      // Add OpenStreetMap tiles
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19,
      }).addTo(mapInstanceRef.current);
    }

    return () => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.remove();
        mapInstanceRef.current = null;
      }
    };
  }, []);

  // Get current location using GPS
  const getCurrentLocation = () => {
    if (!navigator.geolocation) {
      alert('Geolocation is not supported by your browser');
      return;
    }

    setLoading(true);

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const location = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };

        setUserLocation(location);
        updateMapView(location);
        searchNearbyFacilities(location);
      },
      (error) => {
        console.error('Geolocation error:', error);
        alert('Could not get your location. Please enter manually.');
        setLoading(false);
      }
    );
  };

  // Search location by address
  const searchLocationByAddress = async () => {
    if (!locationInput.trim()) {
      alert('Please enter a location');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(locationInput)}&limit=1`
      );

      const data = await response.json();

      if (data.length === 0) {
        alert('Location not found. Please try a different address.');
        setLoading(false);
        return;
      }

      const location = {
        lat: parseFloat(data[0].lat),
        lng: parseFloat(data[0].lon),
      };

      setUserLocation(location);
      updateMapView(location);
      searchNearbyFacilities(location);
    } catch (error) {
      console.error('Geocoding error:', error);
      alert('Error searching location. Please try again.');
      setLoading(false);
    }
  };

  // Update map view with user location
  const updateMapView = (location) => {
    if (!mapInstanceRef.current) return;

    mapInstanceRef.current.setView([location.lat, location.lng], 14);

    // Remove old user marker
    if (userMarkerRef.current) {
      mapInstanceRef.current.removeLayer(userMarkerRef.current);
    }

    // Add new user marker
    userMarkerRef.current = L.marker([location.lat, location.lng], {
      icon: L.divIcon({
        className: 'user-location-marker',
        html: '<div style="background: #3b82f6; width: 16px; height: 16px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(59,130,246,0.5);"></div>',
        iconSize: [20, 20],
      }),
    }).addTo(mapInstanceRef.current);

    userMarkerRef.current.bindPopup('<strong>Your Location</strong>').openPopup();
  };

  // Search nearby facilities using Overpass API
  const searchNearbyFacilities = async (location) => {
    // Clear existing markers
    facilitiesMarkersRef.current.forEach((marker) => mapInstanceRef.current.removeLayer(marker));
    facilitiesMarkersRef.current = [];

    const allFacilities = [];

    try {
      if (filters.hospital) {
        const hospitals = await searchOverpassAPI(location, 'hospital');
        allFacilities.push(...hospitals.map((f) => ({ ...f, type: 'hospital' })));
      }

      if (filters.clinic) {
        const clinics = await searchOverpassAPI(location, 'clinic');
        allFacilities.push(...clinics.map((f) => ({ ...f, type: 'clinic' })));
      }

      if (filters.pharmacy) {
        const pharmacies = await searchOverpassAPI(location, 'pharmacy');
        allFacilities.push(...pharmacies.map((f) => ({ ...f, type: 'pharmacy' })));
      }

      // Sort by distance
      allFacilities.forEach((f) => {
        f.distance = calculateDistance(location.lat, location.lng, f.lat, f.lng);
      });
      allFacilities.sort((a, b) => a.distance - b.distance);

      setFacilities(allFacilities);
      addMarkersToMap(allFacilities);
      setLoading(false);
    } catch (error) {
      console.error('Error searching facilities:', error);
      setLoading(false);
    }
  };

  // Search Overpass API for specific facility type
  const searchOverpassAPI = async (location, type) => {
    const radius = 5000; // 5km
    const query = `
      [out:json];
      (
        node["amenity"="${type}"](around:${radius},${location.lat},${location.lng});
        way["amenity"="${type}"](around:${radius},${location.lat},${location.lng});
      );
      out center;
    `;

    const response = await fetch('https://overpass-api.de/api/interpreter', {
      method: 'POST',
      body: query,
    });

    const data = await response.json();

    return data.elements.map((element) => ({
      id: element.id,
      name: element.tags?.name || `Unnamed ${type}`,
      lat: element.lat || element.center?.lat,
      lng: element.lon || element.center?.lon,
      phone: element.tags?.phone || 'N/A',
      address: formatAddress(element.tags),
      openingHours: element.tags?.opening_hours || 'N/A',
    }));
  };

  // Add markers to map
  const addMarkersToMap = (facilities) => {
    if (!mapInstanceRef.current) return;

    facilities.forEach((facility) => {
      const iconColor = facility.type === 'hospital' ? '#ef4444' : facility.type === 'clinic' ? '#3b82f6' : '#10b981';

      const marker = L.marker([facility.lat, facility.lng], {
        icon: L.divIcon({
          className: 'facility-marker',
          html: `<div style="background: ${iconColor}; color: white; width: 30px; height: 30px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 16px; border: 2px solid white; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
            ${facility.type === 'hospital' ? '🏥' : facility.type === 'clinic' ? '🏥' : '💊'}
          </div>`,
          iconSize: [30, 30],
        }),
      }).addTo(mapInstanceRef.current);

      marker.bindPopup(`
        <div style="min-width: 200px;">
          <strong style="font-size: 14px;">${facility.name}</strong><br/>
          <small style="color: #666;">📍 ${facility.distance.toFixed(2)} km away</small><br/>
          <small>${facility.address}</small><br/>
          <small>📞 ${facility.phone}</small><br/>
          <small>🕒 ${facility.openingHours}</small><br/>
          <button onclick="window.open('https://www.google.com/maps/dir/${userLocation.lat},${userLocation.lng}/${facility.lat},${facility.lng}', '_blank')" 
            style="margin-top: 8px; padding: 6px 12px; background: #3b82f6; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">
            Get Directions
          </button>
        </div>
      `);

      facilitiesMarkersRef.current.push(marker);
    });
  };

  // Calculate distance between two points (Haversine formula)
  const calculateDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371; // Earth's radius in km
    const dLat = ((lat2 - lat1) * Math.PI) / 180;
    const dLon = ((lon2 - lon1) * Math.PI) / 180;
    const a =
      Math.sin(dLat / 2) * Math.sin(dLat / 2) +
      Math.cos((lat1 * Math.PI) / 180) *
        Math.cos((lat2 * Math.PI) / 180) *
        Math.sin(dLon / 2) *
        Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
  };

  // Format address from tags
  const formatAddress = (tags) => {
    if (!tags) return 'Address not available';
    const parts = [tags['addr:street'], tags['addr:city'], tags['addr:postcode']].filter(Boolean);
    return parts.length > 0 ? parts.join(', ') : 'Address not available';
  };

  // Focus on facility
  const focusFacility = (facility) => {
    if (!mapInstanceRef.current) return;
    mapInstanceRef.current.setView([facility.lat, facility.lng], 16);
  };

  // Open directions in Google Maps
  const openDirections = (facility) => {
    if (userLocation) {
      window.open(`https://www.google.com/maps/dir/${userLocation.lat},${userLocation.lng}/${facility.lat},${facility.lng}`, '_blank');
    } else {
      window.open(`https://www.google.com/maps/search/?api=1&query=${facility.lat},${facility.lng}`, '_blank');
    }
  };

  return (
    <div className="flex h-screen w-full flex-col overflow-hidden bg-gradient-to-br from-background via-background to-background/95">
      {/* Header */}
      <div className="border-b border-white/10 bg-white/5 p-6 backdrop-blur-xl">
        <h1 className="mb-2 text-3xl font-bold text-white">🗺️ Find Nearby Medical Facilities</h1>
        <p className="text-white/60">Locate hospitals, clinics, and pharmacies near you</p>
      </div>

      {/* Content */}
      <div className="flex flex-1 gap-4 overflow-hidden p-6">
        {/* Map Section */}
        <div className="flex flex-[2] flex-col gap-4">
          {/* Search Controls */}
          <div className="glass-card p-4">
            <div className="mb-3 flex gap-3">
              <div className="relative flex-1">
                <input
                  type="text"
                  value={locationInput}
                  onChange={(e) => setLocationInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && searchLocationByAddress()}
                  placeholder="Enter your location or address..."
                  className="w-full rounded-xl border border-white/20 bg-white/5 px-4 py-3 pl-10 text-white placeholder-white/40 focus:border-primary focus:outline-none"
                />
                <span className="absolute left-3 top-3.5 text-white/60">📍</span>
              </div>
              <button
                onClick={getCurrentLocation}
                disabled={loading}
                className="rounded-xl border border-primary/30 bg-primary/10 px-4 py-3 text-primary hover:bg-primary/20 disabled:opacity-50"
              >
                📍 Current Location
              </button>
              <button
                onClick={searchLocationByAddress}
                disabled={loading}
                className="rounded-xl bg-primary px-6 py-3 font-semibold text-background hover:bg-primary/90 disabled:opacity-50"
              >
                🔍 Search
              </button>
            </div>

            {/* Filters */}
            <div className="flex gap-4">
              <label className="flex cursor-pointer items-center gap-2 text-white/80">
                <input
                  type="checkbox"
                  checked={filters.hospital}
                  onChange={(e) => setFilters({ ...filters, hospital: e.target.checked })}
                  className="h-4 w-4 rounded border-white/20 bg-white/10 text-primary focus:ring-primary"
                />
                🏥 Hospitals
              </label>
              <label className="flex cursor-pointer items-center gap-2 text-white/80">
                <input
                  type="checkbox"
                  checked={filters.clinic}
                  onChange={(e) => setFilters({ ...filters, clinic: e.target.checked })}
                  className="h-4 w-4 rounded border-white/20 bg-white/10 text-primary focus:ring-primary"
                />
                🏥 Clinics
              </label>
              <label className="flex cursor-pointer items-center gap-2 text-white/80">
                <input
                  type="checkbox"
                  checked={filters.pharmacy}
                  onChange={(e) => setFilters({ ...filters, pharmacy: e.target.checked })}
                  className="h-4 w-4 rounded border-white/20 bg-white/10 text-primary focus:ring-primary"
                />
                💊 Pharmacies
              </label>
            </div>
          </div>

          {/* Map */}
          <div ref={mapRef} className="glass-card flex-1 overflow-hidden rounded-2xl" />

          {loading && (
            <div className="glass-card p-4 text-center text-white/60">
              <div className="mb-2 inline-block h-8 w-8 animate-spin rounded-full border-4 border-primary/30 border-t-primary"></div>
              <p>Searching for medical facilities...</p>
            </div>
          )}
        </div>

        {/* Facilities List */}
        <div className="flex flex-1 flex-col gap-3 overflow-y-auto">
          <div className="glass-card p-4">
            <h2 className="mb-2 text-xl font-bold text-white">
              Nearby Facilities {facilities.length > 0 && `(${facilities.length})`}
            </h2>
            <p className="text-sm text-white/60">Click to view on map or get directions</p>
          </div>

          {facilities.length === 0 && !loading && (
            <div className="glass-card p-8 text-center">
              <div className="mb-4 text-6xl">🗺️</div>
              <p className="text-white/60">
                {userLocation ? 'No facilities found nearby. Try different filters.' : 'Search or use your location to find medical facilities'}
              </p>
            </div>
          )}

          {facilities.map((facility, idx) => (
            <div key={idx} className="glass-card p-4 hover:border-primary/50">
              <div className="mb-2 flex items-start justify-between">
                <div>
                  <h3 className="font-semibold text-white">{facility.name}</h3>
                  <p className="text-xs text-white/60">
                    {facility.type === 'hospital' ? '🏥 Hospital' : facility.type === 'clinic' ? '🏥 Clinic' : '💊 Pharmacy'}
                  </p>
                </div>
                <span className="rounded-full bg-primary/20 px-2 py-1 text-xs font-semibold text-primary">
                  {facility.distance.toFixed(2)} km
                </span>
              </div>

              <p className="mb-1 text-sm text-white/70">📍 {facility.address}</p>
              <p className="mb-1 text-sm text-white/70">📞 {facility.phone}</p>
              <p className="mb-3 text-sm text-white/70">🕒 {facility.openingHours}</p>

              <div className="flex gap-2">
                <button
                  onClick={() => focusFacility(facility)}
                  className="flex-1 rounded-lg border border-white/20 bg-white/5 py-2 text-sm text-white hover:bg-white/10"
                >
                  📍 View on Map
                </button>
                <button
                  onClick={() => openDirections(facility)}
                  className="flex-1 rounded-lg bg-primary/20 py-2 text-sm text-primary hover:bg-primary/30"
                >
                  🗺️ Directions
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default NearbyPage;
