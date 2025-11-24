import React, { useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap, useMapEvents } from 'react-leaflet';
import L from 'leaflet';
import { GeoLocation, Driver } from '../types';

// Custom Icons
const tuktukIcon = new L.DivIcon({
  className: 'custom-icon',
  html: `<div style="background-color: #FFD700; border: 2px solid black; padding: 5px; border-radius: 50%; width: 30px; height: 30px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 5px rgba(0,0,0,0.5);">🛺</div>`,
  iconSize: [30, 30],
  iconAnchor: [15, 15]
});

const userIcon = new L.DivIcon({
  className: 'custom-icon',
  html: `<div style="background-color: black; border: 2px solid white; padding: 5px; border-radius: 50%; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 5px rgba(0,0,0,0.5);">👤</div>`,
  iconSize: [20, 20],
  iconAnchor: [10, 10]
});

const destIcon = new L.DivIcon({
  className: 'custom-icon',
  html: `<div style="background-color: red; border: 2px solid white; padding: 5px; border-radius: 50%; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 5px rgba(0,0,0,0.5);">🏁</div>`,
  iconSize: [20, 20],
  iconAnchor: [10, 10]
});

interface MapComponentProps {
  center: GeoLocation;
  drivers?: Driver[];
  destination?: GeoLocation | null;
  onLocationSelect?: (loc: GeoLocation) => void;
  interactive?: boolean;
}

const MapUpdater: React.FC<{ center: GeoLocation }> = ({ center }) => {
  const map = useMap();
  useEffect(() => {
    map.setView([center.lat, center.lng], map.getZoom());
  }, [center, map]);
  return null;
};

const LocationSelector: React.FC<{ onSelect?: (loc: GeoLocation) => void }> = ({ onSelect }) => {
  useMapEvents({
    click(e) {
      if (onSelect) {
        onSelect({ lat: e.latlng.lat, lng: e.latlng.lng });
      }
    },
  });
  return null;
};

const MapComponent: React.FC<MapComponentProps> = ({ 
  center, 
  drivers = [], 
  destination,
  onLocationSelect,
  interactive = true
}) => {
  return (
    <MapContainer 
      center={[center.lat, center.lng]} 
      zoom={15} 
      scrollWheelZoom={interactive}
      style={{ height: '100%', width: '100%' }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      
      <MapUpdater center={center} />
      <LocationSelector onSelect={onLocationSelect} />

      {/* User Location */}
      <Marker position={[center.lat, center.lng]} icon={userIcon}>
        <Popup>موقعك الحالي</Popup>
      </Marker>

      {/* Destination */}
      {destination && (
        <Marker position={[destination.lat, destination.lng]} icon={destIcon}>
           <Popup>الوجهة</Popup>
        </Marker>
      )}

      {/* Drivers */}
      {drivers.map(driver => (
        <Marker 
          key={driver.id} 
          position={[driver.location.lat, driver.location.lng]} 
          icon={tuktukIcon}
        >
          <Popup>
            <div className="text-black text-right">
              <p className="font-bold">{driver.name}</p>
              <p>⭐ {driver.rating}</p>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default MapComponent;