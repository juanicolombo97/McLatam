import React, { useState, useEffect } from 'react';
import { getAuth, onAuthStateChanged } from "firebase/auth";
import Tabla from '../Tabla/Tabla';
import { collection, getDocs, query, orderBy, limit, where } from "firebase/firestore";
import { db } from '../../firebase/firebase';
import Popup from "../RevisarExpedientes/Popup";
import EmailRestAPI from "./EmailRestAPI";

const Dashboard = () => {
  const [expedientes, setExpedientes] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isPopupVisible, setPopupVisibility] = useState(false);

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
        orderBy("Pagina", "asc")
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

  const handleClosePopup = () => {
    setPopupVisibility(false);
  };

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
              <div className="container">
                {isPopupVisible && <Popup onClose={handleClosePopup} />}
                <EmailRestAPI expedientes={filteredExpedientes}/>
              </div>
              <Tabla expedientes={filteredExpedientes} />
            </>
          )}
        </div>
  );
};

export default Dashboard;
