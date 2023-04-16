import React, { useEffect } from 'react';
import './App.css';
import SignIn
from './components/auth/SignIn';
import { getAuth, signOut } from 'firebase/auth';

function App() {
  
  // Funcion para cerrar sesión al cerrar la ventana
  useEffect(() => {
    const handleBeforeUnload = async () => {
      const auth = getAuth();
      if (auth.currentUser) {
        await signOut(auth);
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);

  
  return (
    <div className="App">
      <SignIn />
    </div>
  );
}

export default App;
