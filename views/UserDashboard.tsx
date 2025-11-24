import React, { useState, useEffect } from 'react';
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

export default UserDashboard;