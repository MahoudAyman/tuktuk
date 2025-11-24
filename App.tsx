import React, { useState, useEffect } from 'react';
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

export default App;