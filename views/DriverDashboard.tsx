import React, { useState, useEffect } from 'react';
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

export default DriverDashboard;