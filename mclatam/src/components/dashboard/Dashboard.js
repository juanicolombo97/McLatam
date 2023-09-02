import React, { useState, useEffect } from 'react';
import { getAuth, onAuthStateChanged } from "firebase/auth";
import Tabla from '../Tabla/Tabla';
import SearchBar from '../SearchBar/SearchBar'; // Importa el nuevo componente
import { collection, getDocs } from "firebase/firestore";
import { db } from '../../firebase/firebase';

const Dashboard = () => {
  const [expedientes, setExpedientes] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");

  const filteredExpedientes = expedientes.filter(expediente => {
    return Object.values(expediente).some(value =>
      value.toString().toLowerCase().includes(searchTerm.toLowerCase())
    );
  });

  const auth = getAuth();
  onAuthStateChanged(auth, (user) => {
    if (user) {
      const uid = user.uid;
      console.log('uid', uid);
    } else {
      console.log('No hay usuario');
    }
  });

  useEffect(() => {
    const loadExpedientes = async () => {
      const querySnapshot = await getDocs(collection(db, "crm"));
      const expedientesData = [];
      querySnapshot.forEach((doc) => {
        expedientesData.push({ id: doc.id, ...doc.data() });
      });
      setExpedientes(expedientesData);
    };

    loadExpedientes();
  }, []);

  return (
    <div className="dashboard-container">
      <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
      <Tabla expedientes={filteredExpedientes} />
    </div>
  );
};

export default Dashboard;
