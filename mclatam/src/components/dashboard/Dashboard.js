import React, { useState, useEffect } from 'react';
import { getAuth, onAuthStateChanged } from "firebase/auth";
import './Dashboard.css'; /* Importar el archivo CSS */
import Tabla from '../Tabla/Tabla';

const Dashboard = () => {
  const [columnas, setColumnas] = useState([]);
  const [expedientes, setExpedientes] = useState([]);

  useEffect(() => {
    const columnasData = [
      { nombre: 'id', items: [1, 2, 3] },
      { nombre: 'nombre', items: ['Juan', 'Maria', 'Carlos'] },
      { nombre: 'apellido', items: ['Perez', 'Garcia', 'Lopez'] },
      { nombre: 'edad', items: [25, 30, 35] },
    ];

    const expedientesData = [
      { id: 1, nombre: 'Juan', apellido: 'Perez', edad: 25 },
      { id: 2, nombre: 'Maria', apellido: 'Garcia', edad: 30 },
      { id: 3, nombre: 'Carlos', apellido: 'Lopez', edad: 35 },
    ];

    setColumnas(columnasData);
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
      <h1>Dashboard</h1>
      <Tabla columnas={columnas} expedientes={expedientes} />
    </div>
  );
};

export default Dashboard;