import React, { useState, useEffect } from 'react';
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

export default Register;