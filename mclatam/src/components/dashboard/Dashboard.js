import React, { useState, useEffect } from 'react';
import { getAuth, onAuthStateChanged } from "firebase/auth";
import Tabla from '../Tabla/Tabla';
import { collection, getDocs } from "firebase/firestore";
import { db } from '../../firebase/firebase';

const Dashboard = () => {
  const [expedientes, setExpedientes] = useState([]);


  const auth = getAuth();
  onAuthStateChanged(auth, (user) => {
    if (user) {
      const uid = user.uid;
      console.log('uid', uid);
    } else {
      console.log('No hay usuario');
    }
  });

  // Carga expedientes desde Firestore
  useEffect(() => {
    const loadExpedientes = async () => {
      const querySnapshot = await getDocs(collection(db, "crm")); // Asegúrate de cambiar "crm" por el nombre de tu colección
      const expedientesData = [];
      querySnapshot.forEach((doc) => {
        expedientesData.push({ id: doc.id, ...doc.data() });
      });
      console.log('expedientesData', expedientesData);
      setExpedientes(expedientesData);
    };

    loadExpedientes();
  }, []);


  return (
    <div className="dashboard-container">
      <Tabla expedientes={expedientes} />
    </div>
  );
};

export default Dashboard;