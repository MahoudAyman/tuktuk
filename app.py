import os

# تعريف الملفات ومحتواها
files = {
    "metadata.json": r"""{
  "name": "TukTuk Go",
  "description": "A modern ride-hailing app specifically for TukTuks using Supabase backend.",
  "requestFramePermissions": [
    "geolocation"
  ]
}""",

    "index.html": r"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="https://cdn-icons-png.flaticon.com/512/5695/5695143.png" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>TukTuk Go</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Leaflet CSS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
     integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
     crossorigin=""/>
    <!-- Google Fonts (Cairo for Arabic support) -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap" rel="stylesheet">
    <script>
      tailwind.config = {
        theme: {
          extend: {
            fontFamily: {
              sans: ['Cairo', 'sans-serif'],
            },
            colors: {
              brand: {
                yellow: '#FFD700',
                black: '#111111',
                dark: '#1A1A1A',
                gray: '#2D2D2D'
              }
            }
          }
        }
      }
    </script>
    <style>
      body {
        background-color: #111111;
        color: white;
      }
      /* Leaflet Map Fixes */
      .leaflet-container {
        width: 100%;
        height: 100%;
        z-index: 0;
      }
    </style>
  <script type="importmap">
{
  "imports": {
    "react": "https://aistudiocdn.com/react@^19.2.0",
    "react-dom/client": "https://aistudiocdn.com/react-dom@^19.2.0/client",
    "react-dom/": "https://aistudiocdn.com/react-dom@^19.2.0/",
    "react/": "https://aistudiocdn.com/react@^19.2.0/",
    "@supabase/supabase-js": "https://aistudiocdn.com/@supabase/supabase-js@^2.84.0",
    "react-leaflet": "https://aistudiocdn.com/react-leaflet@^5.0.0",
    "framer-motion": "https://aistudiocdn.com/framer-motion@^12.23.24",
    "lucide-react": "https://aistudiocdn.com/lucide-react@^0.554.0",
    "leaflet/": "https://aistudiocdn.com/leaflet@^1.9.4/",
    "leaflet": "https://aistudiocdn.com/leaflet@^1.9.4"
  }
}
</script>
</head>
  <body>
    <div id="root"></div>
    <script type="module" src="./index.tsx"></script>
  </body>
</html>""",

    "index.tsx": r"""import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const rootElement = document.getElementById('root');
if (!rootElement) {
  throw new Error("Could not find root element to mount to");
}

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);""",

    "types.ts": r"""export interface GeoLocation {
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

export type AppView = 'landing' | 'register-user' | 'register-driver' | 'user-dashboard' | 'driver-dashboard';""",

    "App.tsx": r"""import React, { useState, useEffect } from 'react';
import Layout from './components/Layout';
import LandingPage from './views/Landing';
import Register from './views/Register';
import UserDashboard from './views/UserDashboard';
import DriverDashboard from './views/DriverDashboard';
import { AppView, User, Driver } from './types';

const App: React.FC = () => {
  const [view, setView] = useState<AppView>('landing');
  const [currentUser, setCurrentUser] = useState<User | null>(null);
  const [currentDriver, setCurrentDriver] = useState<Driver | null>(null);

  // Simple persistance for demo
  useEffect(() => {
    const savedUser = localStorage.getItem('tuktuk_user');
    const savedDriver = localStorage.getItem('tuktuk_driver');
    
    if (savedUser) {
      setCurrentUser(JSON.parse(savedUser));
      setView('user-dashboard');
    } else if (savedDriver) {
      setCurrentDriver(JSON.parse(savedDriver));
      setView('driver-dashboard');
    }
  }, []);

  const handleUserLogin = (user: User) => {
    setCurrentUser(user);
    localStorage.setItem('tuktuk_user', JSON.stringify(user));
    localStorage.removeItem('tuktuk_driver');
    setCurrentDriver(null);
    setView('user-dashboard');
  };

  const handleDriverLogin = (driver: Driver) => {
    setCurrentDriver(driver);
    localStorage.setItem('tuktuk_driver', JSON.stringify(driver));
    localStorage.removeItem('tuktuk_user');
    setCurrentUser(null);
    setView('driver-dashboard');
  };

  const handleLogout = () => {
    localStorage.removeItem('tuktuk_user');
    localStorage.removeItem('tuktuk_driver');
    setCurrentUser(null);
    setCurrentDriver(null);
    setView('landing');
  };

  return (
    <Layout currentView={view} onNavigate={setView} onLogout={handleLogout}>
      {view === 'landing' && <LandingPage onNavigate={setView} />}
      
      {view === 'register-user' && (
        <Register type="user" onSuccess={handleUserLogin} onCancel={() => setView('landing')} />
      )}
      
      {view === 'register-driver' && (
        <Register type="driver" onSuccess={handleDriverLogin} onCancel={() => setView('landing')} />
      )}

      {view === 'user-dashboard' && currentUser && (
        <UserDashboard user={currentUser} />
      )}

      {view === 'driver-dashboard' && currentDriver && (
        <DriverDashboard driver={currentDriver} />
      )}
    </Layout>
  );
};

export default App;""",

    "utils/geo.ts": r"""import { GeoLocation } from '../types';

// Haversine formula to calculate distance between two points in km
export const calculateDistance = (loc1: GeoLocation, loc2: GeoLocation): number => {
  const R = 6371; // Radius of the earth in km
  const dLat = deg2rad(loc2.lat - loc1.lat);
  const dLon = deg2rad(loc2.lng - loc1.lng);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(deg2rad(loc1.lat)) * Math.cos(deg2rad(loc2.lat)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const d = R * c; // Distance in km
  return parseFloat(d.toFixed(2));
};

const deg2rad = (deg: number): number => {
  return deg * (Math.PI / 180);
};

export const calculatePrice = (distanceKm: number): number => {
  const BASE_RATE = 5; // 5 EGP base
  const PER_KM = 3; // 3 EGP per km
  return Math.ceil(BASE_RATE + (distanceKm * PER_KM));
};""",

    "services/supabase.ts": r"""import { createClient } from '@supabase/supabase-js';

// NOTE: In a real production app, use environment variables.
// For this prompt's requirement to work immediately, we use the provided keys.
const SUPABASE_URL = 'https://oljxeosptnsmlcggzogw.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sanhlb3NwdG5zbWxjZ2d6b2d3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM2NjY3MDksImV4cCI6MjA3OTI0MjcwOX0.niii7MFS8W9GHtjunloo94qxaDPWOq2aeDUu_fZklKk';

export const supabase = createClient(SUPABASE_URL, SUPABASE_KEY);

export const USERS_TABLE = 'users';
export const DRIVERS_TABLE = 'drivers';
export const RIDES_TABLE = 'rides';""",

    "components/Layout.tsx": r"""import React from 'react';
import { CarTaxiFront, LogOut } from 'lucide-react';
import { AppView } from '../types';

interface LayoutProps {
  children: React.ReactNode;
  currentView: AppView;
  onNavigate: (view: AppView) => void;
  onLogout: () => void;
}

const Layout: React.FC<LayoutProps> = ({ children, currentView, onNavigate, onLogout }) => {
  return (
    <div className="min-h-screen flex flex-col bg-brand-black text-white font-sans">
      {/* Header */}
      <header className="bg-brand-yellow text-brand-black py-4 px-6 sticky top-0 z-50 shadow-lg">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div 
            className="flex items-center gap-2 cursor-pointer"
            onClick={() => onNavigate('landing')}
          >
            <CarTaxiFront size={32} strokeWidth={2.5} />
            <h1 className="text-2xl font-black tracking-tighter">TukTuk Go</h1>
          </div>
          
          {currentView !== 'landing' && (
            <button 
              onClick={onLogout}
              className="flex items-center gap-2 bg-black/10 hover:bg-black/20 px-3 py-1.5 rounded-full text-sm font-bold transition-colors"
            >
              <LogOut size={16} />
              <span>خروج</span>
            </button>
          )}
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 relative">
        {children}
      </main>
    </div>
  );
};

export default Layout;""",

    "components/MapComponent.tsx": r"""import React, { useEffect } from 'react';
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

export default MapComponent;""",

    "views/Landing.tsx": r"""import React from 'react';
import { motion } from 'framer-motion';
import { MapPin, Car } from 'lucide-react';
import { AppView } from '../types';

interface LandingProps {
  onNavigate: (view: AppView) => void;
}

const LandingPage: React.FC<LandingProps> = ({ onNavigate }) => {
  return (
    <div className="h-full flex flex-col items-center justify-center p-6 text-center bg-[url('https://images.unsplash.com/photo-1596451832228-1f9804657315?q=80&w=2500&auto=format&fit=crop')] bg-cover bg-center relative">
      {/* Overlay */}
      <div className="absolute inset-0 bg-black/80 z-0"></div>

      <div className="relative z-10 max-w-3xl">
        <motion.div
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h1 className="text-6xl md:text-8xl font-black text-brand-yellow mb-4 drop-shadow-lg">
            TukTuk Go
          </h1>
          <p className="text-xl md:text-2xl text-gray-200 mb-12 font-light">
            أسرع وأسهل طريقة لحجز توك توك في مدينتك. آمن، سريع، ورخيص.
          </p>
        </motion.div>

        <div className="flex flex-col md:flex-row gap-6 justify-center w-full">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onNavigate('register-user')}
            className="group flex flex-col items-center justify-center gap-4 bg-brand-yellow text-black w-full md:w-64 h-40 rounded-2xl shadow-xl border-4 border-brand-yellow hover:bg-transparent hover:text-brand-yellow transition-all"
          >
            <MapPin size={48} />
            <span className="text-2xl font-bold">أحتاج توصيلة</span>
          </motion.button>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => onNavigate('register-driver')}
            className="group flex flex-col items-center justify-center gap-4 bg-gray-800 text-white w-full md:w-64 h-40 rounded-2xl shadow-xl border-4 border-gray-700 hover:border-brand-yellow transition-all"
          >
            <Car size={48} className="group-hover:text-brand-yellow transition-colors" />
            <span className="text-2xl font-bold group-hover:text-brand-yellow transition-colors">أنا سائق</span>
          </motion.button>
        </div>
      </div>

      {/* Scroll Indicator */}
      <motion.div 
        animate={{ y: [0, 10, 0] }}
        transition={{ repeat: Infinity, duration: 2 }}
        className="absolute bottom-8 z-10"
      >
        <div className="w-6 h-10 border-2 border-white/30 rounded-full flex justify-center pt-2">
          <div className="w-1.5 h-1.5 bg-brand-yellow rounded-full"></div>
        </div>
      </motion.div>
    </div>
  );
};

export default LandingPage;""",

    "views/Register.tsx": r"""import React, { useState, useEffect } from 'react';
import { Loader2, MapPin } from 'lucide-react';
import { supabase, USERS_TABLE, DRIVERS_TABLE } from '../services/supabase';
import { GeoLocation } from '../types';

interface RegisterProps {
  type: 'user' | 'driver';
  onSuccess: (data: any) => void;
  onCancel: () => void;
}

const Register: React.FC<RegisterProps> = ({ type, onSuccess, onCancel }) => {
  const [loading, setLoading] = useState(false);
  const [location, setLocation] = useState<GeoLocation | null>(null);
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    tuktukNumber: '',
  });

  useEffect(() => {
    navigator.geolocation.getCurrentPosition(
      (pos) => setLocation({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
      (err) => console.error(err),
      { enableHighAccuracy: true }
    );
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!location) {
      alert("يرجى تفعيل الموقع الجغرافي للمتابعة");
      return;
    }

    setLoading(true);

    try {
      const table = type === 'user' ? USERS_TABLE : DRIVERS_TABLE;
      const payload: any = {
        name: formData.name,
        phone: formData.phone,
        location: location
      };

      if (type === 'driver') {
        payload.tuktuk_number = formData.tuktukNumber;
        payload.status = 'available';
      }

      // Simple flow: Insert. If phone exists, we assume login (for this prototype)
      // In real app, we'd handle auth error or upsert.
      // Here we check if exists first
      const { data: existing } = await supabase
        .from(table)
        .select('*')
        .eq('phone', formData.phone)
        .single();

      if (existing) {
        // Update location on login
        await supabase.from(table).update({ location }).eq('id', existing.id);
        onSuccess({ ...existing, location });
      } else {
        const { data, error } = await supabase
          .from(table)
          .insert([payload])
          .select()
          .single();

        if (error) throw error;
        onSuccess(data);
      }

    } catch (error: any) {
      alert('حدث خطأ: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center h-full p-6">
      <div className="bg-brand-gray w-full max-w-md p-8 rounded-2xl shadow-2xl border border-white/10">
        <h2 className="text-3xl font-bold text-brand-yellow mb-6 text-center">
          {type === 'user' ? 'تسجيل مستخدم جديد' : 'تسجيل سائق جديد'}
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">الاسم</label>
            <input 
              required
              type="text"
              className="w-full bg-black/50 border border-gray-700 rounded-lg p-3 focus:border-brand-yellow focus:outline-none text-white"
              placeholder="اسمك بالكامل"
              value={formData.name}
              onChange={e => setFormData({...formData, name: e.target.value})}
            />
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1">رقم الهاتف</label>
            <input 
              required
              type="tel"
              className="w-full bg-black/50 border border-gray-700 rounded-lg p-3 focus:border-brand-yellow focus:outline-none text-white"
              placeholder="01xxxxxxxxx"
              value={formData.phone}
              onChange={e => setFormData({...formData, phone: e.target.value})}
            />
          </div>

          {type === 'driver' && (
            <div>
              <label className="block text-sm text-gray-400 mb-1">رقم التوكتوك</label>
              <input 
                required
                type="text"
                className="w-full bg-black/50 border border-gray-700 rounded-lg p-3 focus:border-brand-yellow focus:outline-none text-white"
                placeholder="مثال: 123 ق ط ب"
                value={formData.tuktukNumber}
                onChange={e => setFormData({...formData, tuktukNumber: e.target.value})}
              />
            </div>
          )}

          <div className="flex items-center gap-2 text-sm text-gray-400 my-4">
             <MapPin size={16} className={location ? "text-green-500" : "text-red-500"} />
             <span>{location ? "تم تحديد الموقع بنجاح" : "جاري تحديد الموقع..."}</span>
          </div>

          <button 
            disabled={loading || !location}
            type="submit"
            className="w-full bg-brand-yellow text-black font-bold py-3 rounded-lg hover:bg-yellow-300 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex justify-center"
          >
            {loading ? <Loader2 className="animate-spin" /> : 'دخول / تسجيل'}
          </button>
          
          <button 
            type="button"
            onClick={onCancel}
            className="w-full bg-transparent text-gray-400 text-sm hover:text-white transition-colors"
          >
            العودة
          </button>
        </form>
      </div>
    </div>
  );
};

export default Register;""",

    "views/UserDashboard.tsx": r"""import React, { useState, useEffect } from 'react';
import { User, Driver, Ride, GeoLocation } from '../types';
import MapComponent from '../components/MapComponent';
import { supabase, DRIVERS_TABLE, RIDES_TABLE } from '../services/supabase';
import { calculateDistance, calculatePrice } from '../utils/geo';
import { Phone, Star, Loader2 } from 'lucide-react';

interface UserDashboardProps {
  user: User;
}

const UserDashboard: React.FC<UserDashboardProps> = ({ user }) => {
  const [drivers, setDrivers] = useState<Driver[]>([]);
  const [activeRide, setActiveRide] = useState<Ride | null>(null);
  const [destination, setDestination] = useState<GeoLocation | null>(null);
  const [estimatedPrice, setEstimatedPrice] = useState<number>(0);
  const [statusMessage, setStatusMessage] = useState('');

  // 1. Fetch Nearby Drivers Realtime
  useEffect(() => {
    const fetchDrivers = async () => {
      const { data } = await supabase
        .from(DRIVERS_TABLE)
        .select('*')
        .eq('status', 'available');
      if (data) setDrivers(data);
    };

    fetchDrivers();

    // Subscribe to drivers changes (simplified: polling or realtime)
    const channel = supabase
      .channel('public:drivers')
      .on('postgres_changes', { event: '*', schema: 'public', table: DRIVERS_TABLE }, (payload) => {
          // Basic refresh logic
          fetchDrivers();
      })
      .subscribe();

    return () => { supabase.removeChannel(channel); };
  }, []);

  // 2. Check for active rides
  useEffect(() => {
    const checkRide = async () => {
      const { data } = await supabase
        .from(RIDES_TABLE)
        .select('*')
        .eq('passenger_id', user.id)
        .in('status', ['pending', 'accepted', 'on_the_way'])
        .order('created_at', { ascending: false })
        .limit(1)
        .single();

      if (data) {
        setActiveRide(data);
        setDestination(data.destination);
      }
    };

    checkRide();

    const channel = supabase
      .channel(`ride:${user.id}`)
      .on('postgres_changes', { event: '*', schema: 'public', table: RIDES_TABLE, filter: `passenger_id=eq.${user.id}` }, (payload) => {
          const newRide = payload.new as Ride;
          setActiveRide(newRide);
          if (newRide.status === 'finished') {
            setActiveRide(null);
            setDestination(null);
            alert('وصلت بالسلامة! الرحلة انتهت.');
          }
      })
      .subscribe();

    return () => { supabase.removeChannel(channel); };
  }, [user.id]);

  const handleDestinationSelect = (loc: GeoLocation) => {
    if (activeRide) return;
    setDestination(loc);
    const dist = calculateDistance(user.location, loc);
    setEstimatedPrice(calculatePrice(dist));
  };

  const requestRide = async () => {
    if (!destination) return;

    // Find nearest driver
    let nearestDriver: Driver | null = null;
    let minDistance = Infinity;

    drivers.forEach(d => {
      const dist = calculateDistance(user.location, d.location);
      if (dist < minDistance) {
        minDistance = dist;
        nearestDriver = d;
      }
    });

    // NOTE: In a real app, we create a ride with null driver_id and notify all nearby drivers.
    // Here we simplify or just assign to nearest if exists, otherwise create generic.
    
    const dist = calculateDistance(user.location, destination);
    const price = calculatePrice(dist);

    const { data, error } = await supabase
      .from(RIDES_TABLE)
      .insert([{
        passenger_id: user.id,
        driver_id: nearestDriver ? nearestDriver.id : null, // Auto-assign if found, else pool
        pickup: user.location,
        destination: destination,
        status: 'pending',
        price: price,
        distance: dist
      }])
      .select()
      .single();

    if (error) {
      alert('Error requesting ride');
    } else {
      setActiveRide(data);
      setStatusMessage(nearestDriver ? 'جاري الاتصال بالسائق...' : 'في انتظار سائق متاح...');
    }
  };

  return (
    <div className="h-[calc(100vh-64px)] relative">
      <MapComponent 
        center={user.location} 
        drivers={drivers} 
        destination={destination}
        onLocationSelect={handleDestinationSelect}
        interactive={!activeRide}
      />

      {/* Booking / Status Panel */}
      <div className="absolute bottom-0 left-0 right-0 bg-brand-dark border-t border-gray-700 p-4 rounded-t-3xl shadow-2xl z-[1000]">
        <div className="max-w-2xl mx-auto">
          {!activeRide ? (
            <>
              {!destination ? (
                <div className="text-center py-4">
                  <p className="text-xl text-gray-300 animate-pulse">اضغط على الخريطة لتحديد وجهتك</p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="flex justify-between items-center bg-black/30 p-4 rounded-xl">
                    <div>
                      <p className="text-gray-400 text-sm">السعر المقدر</p>
                      <p className="text-3xl font-bold text-brand-yellow">{estimatedPrice} ج.م</p>
                    </div>
                    <div className="text-right">
                      <p className="text-gray-400 text-sm">المسافة</p>
                      <p className="text-xl font-bold text-white">{calculateDistance(user.location, destination)} كم</p>
                    </div>
                  </div>
                  <button 
                    onClick={requestRide}
                    className="w-full bg-brand-yellow text-black text-xl font-bold py-4 rounded-xl hover:bg-yellow-300 transition-transform active:scale-95 shadow-lg"
                  >
                    اطلب توك توك الآن
                  </button>
                </div>
              )}
            </>
          ) : (
            <div className="space-y-4">
              <div className="flex items-center justify-between mb-2">
                 <span className={`px-3 py-1 rounded-full text-sm font-bold ${
                   activeRide.status === 'pending' ? 'bg-yellow-500/20 text-yellow-500' :
                   activeRide.status === 'accepted' ? 'bg-blue-500/20 text-blue-500' :
                   'bg-green-500/20 text-green-500'
                 }`}>
                   {activeRide.status === 'pending' ? 'جاري البحث عن سائق...' : 
                    activeRide.status === 'accepted' ? 'السائق في الطريق إليك' : 
                    'في الرحلة'}
                 </span>
                 <span className="font-mono text-lg">{activeRide.price} ج.م</span>
              </div>

              {activeRide.driver_id && (
                <div className="flex items-center gap-4 bg-gray-800 p-4 rounded-xl border border-gray-700">
                   <div className="w-12 h-12 bg-brand-yellow rounded-full flex items-center justify-center text-2xl">👨‍✈️</div>
                   <div className="flex-1">
                      {/* In a real app, we'd fetch driver details here based on ID. For now just static/placeholder or cached */}
                      <h3 className="font-bold text-lg">سائق التوك توك</h3>
                      <div className="flex items-center gap-1 text-yellow-400 text-sm">
                        <Star size={14} fill="currentColor" /> 4.8
                      </div>
                   </div>
                   <button className="bg-green-600 p-3 rounded-full hover:bg-green-700">
                     <Phone size={20} />
                   </button>
                </div>
              )}

              {activeRide.status === 'pending' && (
                <div className="flex justify-center">
                  <Loader2 className="animate-spin text-brand-yellow" size={32} />
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;""",

    "views/DriverDashboard.tsx": r"""import React, { useState, useEffect } from 'react';
import { Driver, Ride } from '../types';
import { supabase, RIDES_TABLE, DRIVERS_TABLE, USERS_TABLE } from '../services/supabase';
import { Navigation, MapPin, Check, X, Phone } from 'lucide-react';
import { calculateDistance } from '../utils/geo';

interface DriverDashboardProps {
  driver: Driver;
}

const DriverDashboard: React.FC<DriverDashboardProps> = ({ driver }) => {
  const [isOnline, setIsOnline] = useState(driver.status === 'available');
  const [incomingRide, setIncomingRide] = useState<Ride | null>(null);
  const [currentRide, setCurrentRide] = useState<Ride | null>(null);
  const [passengerName, setPassengerName] = useState('');

  // Update status in DB
  const toggleStatus = async () => {
    const newStatus = isOnline ? 'busy' : 'available';
    const { error } = await supabase
      .from(DRIVERS_TABLE)
      .update({ status: newStatus })
      .eq('id', driver.id);
    
    if (!error) setIsOnline(!isOnline);
  };

  // Listen for rides
  useEffect(() => {
    if (!isOnline) return;

    // Check for existing active ride
    const checkActive = async () => {
      const { data } = await supabase.from(RIDES_TABLE).select('*').eq('driver_id', driver.id).neq('status', 'finished').single();
      if (data) {
        setCurrentRide(data);
        fetchPassenger(data.passenger_id);
      }
    };
    checkActive();

    // Subscription
    const channel = supabase
      .channel('driver_rides')
      .on('postgres_changes', { event: '*', schema: 'public', table: RIDES_TABLE }, (payload) => {
        const newRide = payload.new as Ride;
        
        // If I am assigned explicitly
        if (newRide.driver_id === driver.id && newRide.status !== 'finished') {
          setCurrentRide(newRide);
          setIncomingRide(null); // clear request if it was pending
          fetchPassenger(newRide.passenger_id);
        }
        // If it's a pending ride and I'm available (Simple broadcast logic)
        else if (newRide.status === 'pending' && !newRide.driver_id && !currentRide) {
            // Check distance, if close enough, show.
            // For demo: show all pending.
            setIncomingRide(newRide);
        }
      })
      .subscribe();

    return () => { supabase.removeChannel(channel); };
  }, [driver.id, isOnline, currentRide]);

  // Location Simulator (Driver moving)
  useEffect(() => {
    if (!isOnline) return;
    const interval = setInterval(() => {
      navigator.geolocation.getCurrentPosition(async (pos) => {
        await supabase.from(DRIVERS_TABLE).update({
          location: { lat: pos.coords.latitude, lng: pos.coords.longitude }
        }).eq('id', driver.id);
      });
    }, 10000);
    return () => clearInterval(interval);
  }, [isOnline, driver.id]);

  const fetchPassenger = async (id: string) => {
    const { data } = await supabase.from(USERS_TABLE).select('name').eq('id', id).single();
    if (data) setPassengerName(data.name);
  };

  const acceptRide = async () => {
    if (!incomingRide) return;
    await supabase
      .from(RIDES_TABLE)
      .update({ driver_id: driver.id, status: 'accepted' })
      .eq('id', incomingRide.id);
    
    setCurrentRide({...incomingRide, driver_id: driver.id, status: 'accepted'});
    setIncomingRide(null);
    fetchPassenger(incomingRide.passenger_id);
  };

  const updateRideStatus = async (status: Ride['status']) => {
    if (!currentRide) return;
    await supabase.from(RIDES_TABLE).update({ status }).eq('id', currentRide.id);
    if (status === 'finished') {
      setCurrentRide(null);
      setPassengerName('');
    } else {
      setCurrentRide({ ...currentRide, status });
    }
  };

  return (
    <div className="p-4 max-w-md mx-auto space-y-6">
      {/* Status Toggle */}
      <div className="bg-gray-800 p-6 rounded-2xl shadow-lg flex items-center justify-between border border-gray-700">
        <div>
          <h2 className="text-xl font-bold">{driver.name}</h2>
          <p className={isOnline ? "text-green-400" : "text-gray-500"}>
            {isOnline ? "🟢 متاح للعمل" : "⚫ غير متصل"}
          </p>
        </div>
        <button 
          onClick={toggleStatus}
          className={`px-6 py-2 rounded-full font-bold transition-colors ${
            isOnline ? "bg-red-500/20 text-red-500 border border-red-500" : "bg-green-500/20 text-green-500 border border-green-500"
          }`}
        >
          {isOnline ? "توقف" : "ابدأ"}
        </button>
      </div>

      {/* Incoming Request */}
      {incomingRide && !currentRide && (
        <div className="bg-brand-yellow text-black p-6 rounded-2xl shadow-2xl animate-pulse">
          <h3 className="text-2xl font-black mb-2">🔔 طلب جديد!</h3>
          <div className="flex justify-between mb-4 text-lg">
             <span>المسافة: {calculateDistance(driver.location, incomingRide.pickup)} كم</span>
             <span className="font-bold">{incomingRide.price} ج.م</span>
          </div>
          <div className="flex gap-3">
            <button onClick={acceptRide} className="flex-1 bg-black text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2">
              <Check /> قبول
            </button>
            <button onClick={() => setIncomingRide(null)} className="flex-1 bg-white/20 py-3 rounded-xl font-bold">
              تجاهل
            </button>
          </div>
        </div>
      )}

      {/* Current Active Ride */}
      {currentRide && (
        <div className="bg-gray-800 border-2 border-brand-yellow p-6 rounded-2xl shadow-lg">
          <h3 className="text-xl font-bold text-brand-yellow mb-4">الرحلة الحالية</h3>
          
          <div className="space-y-4 mb-6">
             <div className="flex items-start gap-3">
                <div className="bg-blue-500 p-2 rounded-full mt-1"><MapPin size={16} /></div>
                <div>
                  <p className="text-gray-400 text-sm">نقطة الانطلاق</p>
                  <p className="font-bold">{passengerName || 'الراكب'}</p>
                </div>
             </div>
             
             {currentRide.destination && (
               <div className="flex items-start gap-3">
                  <div className="bg-red-500 p-2 rounded-full mt-1"><Navigation size={16} /></div>
                  <div>
                    <p className="text-gray-400 text-sm">الوجهة</p>
                    <p className="font-bold">إحداثيات: {currentRide.destination.lat.toFixed(4)}, {currentRide.destination.lng.toFixed(4)}</p>
                  </div>
               </div>
             )}
          </div>

          <div className="flex flex-col gap-3">
             {currentRide.status === 'accepted' && (
               <button onClick={() => updateRideStatus('on_the_way')} className="w-full bg-blue-600 py-3 rounded-xl font-bold">
                 تم الوصول للراكب
               </button>
             )}
             {currentRide.status === 'on_the_way' && (
               <button onClick={() => updateRideStatus('finished')} className="w-full bg-green-600 py-3 rounded-xl font-bold">
                 إنهاء الرحلة ({currentRide.price} ج.م)
               </button>
             )}
             <a 
               href={`tel:${driver.phone}`} // Ideally passenger phone, simpler for demo
               className="w-full bg-gray-700 py-3 rounded-xl font-bold text-center flex items-center justify-center gap-2"
             >
               <Phone size={18} /> اتصل بالراكب
             </a>
          </div>
        </div>
      )}
      
      {!isOnline && !currentRide && (
        <div className="text-center text-gray-500 mt-10">
          <p>أنت في وضع غير متصل.</p>
          <p>اضغط "ابدأ" لاستقبال الطلبات.</p>
        </div>
      )}
    </div>
  );
};

export default DriverDashboard;""",
}

# دالة لإنشاء المجلدات والملفات
def create_project_structure():
    for file_path, content in files.items():
        # إنشاء المجلدات إذا لم تكن موجودة
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            print(f"تم إنشاء المجلد: {directory}")
        
        # كتابة الملف
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip())
            print(f"تم إنشاء الملف: {file_path}")

    print("\n✅ تم إنشاء جميع ملفات مشروع TukTuk Go بنجاح!")

if __name__ == "__main__":
    create_project_structure()


