export interface GeoLocation {
  lat: number;
  lng: number;
}

export interface User {
  id: string;
  name: string;
  phone: string;
  location: GeoLocation;
  created_at?: string;
}

export interface Driver {
  id: string;
  name: string;
  phone: string;
  tuktuk_number: string;
  status: 'available' | 'busy';
  rating: number;
  total_rides: number;
  location: GeoLocation;
  created_at?: string;
}

export interface Ride {
  id: string;
  passenger_id: string;
  driver_id: string | null;
  pickup: GeoLocation;
  destination: GeoLocation | null;
  status: 'pending' | 'accepted' | 'on_the_way' | 'finished';
  price: number;
  distance: number;
  created_at?: string;
}

export type AppView = 'landing' | 'register-user' | 'register-driver' | 'user-dashboard' | 'driver-dashboard';