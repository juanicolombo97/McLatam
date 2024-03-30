import React, { useState, useEffect } from 'react';
import { getAuth, onAuthStateChanged } from "firebase/auth";
import Tabla from '../Tabla/Tabla';
import SearchBar from '../SearchBar/SearchBar';
import { collection, getDocs, query, orderBy, limit, where } from "firebase/firestore";
import { db } from '../../firebase/firebase';

const Dashboard = () => {
  const [expedientes, setExpedientes] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(true);

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
      const expedientesRef = collection(db, "crm");

      const q = query(
        expedientesRef,
        where("Estado_expediente", "==", 'Enviar'),
        orderBy("Pagina", "asc"),
        orderBy("FechaPublicacion", "desc")
      );

      const querySnapshot = await getDocs(q);
      const expedientesData = [];
      querySnapshot.forEach((doc) => {
        expedientesData.push({ id: doc.id, ...doc.data() });
      });

      setExpedientes(expedientesData);
      setIsLoading(false);
    };
  
    loadExpedientes();
  }, []);
  

  const filteredExpedientes = expedientes.filter(expediente => {
    return Object.values(expediente).some(value =>
      value.toString().toLowerCase().includes(searchTerm.toLowerCase())
    );
  });

  return (
        <div className="expedientes-container">
          {isLoading ? (
            <div className="transparent-modal">
              <div className="loading-icon"></div>
            </div>
          ) : filteredExpedientes.length === 0 ? (
            <div className="sin-expediente-container">
                <div>No se enviaron expedientes.</div>
            </div>
          ) : (
            <>
              <SearchBar searchTerm={searchTerm} setSearchTerm={setSearchTerm} />
              <Tabla expedientes={filteredExpedientes} />
            </>
          )}
        </div>
  );
};

export default Dashboard;
