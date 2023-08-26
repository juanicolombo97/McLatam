import React, { useState, useEffect } from 'react';
import { getAuth, onAuthStateChanged } from "firebase/auth";
import Tabla from '../Tabla/Tabla';

const Dashboard = () => {
  const [expedientes, setExpedientes] = useState([]);

  useEffect(() => {
  
    const expedientesData = [
      { id: 1, nombre: 'Juan', apellido: 'Perez', edad: 25 },
      { id: 2, nombre: 'Maria', apellido: 'Garcia', edad: 30 },
      { id: 3, nombre: 'Carlos', apellido: 'Lopez', edad: 35 },
    ];

    setExpedientes(expedientesData);
  }, []);

  const auth = getAuth();
  onAuthStateChanged(auth, (user) => {
    if (user) {
      const uid = user.uid;
      console.log('uid', uid);
    } else {
      console.log('No hay usuario');
    }
  });

  return (
    <div className="dashboard-container">
      <Tabla expedientes={expedientes} />
    </div>
  );
};

export default Dashboard;