import React, { useEffect, useState } from 'react';
import './App.css';
import SignIn
from './components/auth/SignIn';
import { getAuth, signOut } from 'firebase/auth';
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Protected from './components/auth/Protected';
import Estadisticas from './components/Estadisticas/Estadisticas';
import RevisarExpedientes from './components/RevisarExpedientes/RevisarExpedientes';
import Navbar from './components/Navbar/Navbar';
import Dashboard from './components/dashboard/Dashboard';
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

function App() {
  
  // Estados para ver si esta loggeado
  const [isSignedIn, setIsSignedIn] = useState(null)

  // Funciones para cambiar el estado a loggeado
  const signin = () => {
    setIsSignedIn(true)
  }
  // Función para cerrar sesión
  const signout = () => {
    setIsSignedIn(false)
  }

  return (
    <div className="App">
      
      <BrowserRouter>
      
        <Navbar  />
        <Routes>
          <Route path='/' element={<SignIn isSignedIn={isSignedIn} setIsSignedIn={setIsSignedIn} />} />
          <Route
            path="/dashboard"
            element={
              <Protected isSignedIn={isSignedIn}>
                <Dashboard />
              </Protected>
            }
          />
          <Route
            path="/revisar-expedientes"
            element={
              <Protected isSignedIn={isSignedIn}>
                <RevisarExpedientes />
              </Protected>
            }
          />
          <Route
            path="/estadisticas"
            element={
              <Protected isSignedIn={isSignedIn}>
                <Estadisticas />
              </Protected>
            }
          />
        </Routes>
      </BrowserRouter>
     </div>
  );
}

export default App;
