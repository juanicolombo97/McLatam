import React, { useState, useEffect } from 'react';
import { collection, getDocs, query, where } from "firebase/firestore";
import { db } from '../../firebase/firebase';  // Asegúrate de tener la ruta correcta a tu archivo firebase
import Expediente from '../Expediente/Expediente';
import ExpedienteButtons from '../ExpedienteButtons/ExpedienteButtons';
import ExpedienteForm from '../ExpedienteForm/ExpedienteForm';

export const RevisarExpedientes = () => {
  
  const [expedientes, setExpedientes] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  
  useEffect(() => {
    const loadExpedientes = async () => {
      const expedientesRef = collection(db, "crm"); // Asegúrate de cambiar "crm" por el nombre de tu colección
      const q = query(expedientesRef, where("Estado_expediente", "==", "NoRevisado"));
      const querySnapshot = await getDocs(q);
      const expedientesData = [];
      querySnapshot.forEach((doc) => {
        expedientesData.push({ id: doc.id, ...doc.data() });
      });
      setExpedientes(expedientesData);
    };

    loadExpedientes();
  }, []);

  // Boton enviar
  const handleEnviar = () => {
        // Realizar updates en la base de datos y avanzar al siguiente expediente
        console.log('Enviar');
        setCurrentIndex((prevIndex) => (prevIndex + 1) % expedientes.length);
  };

  // Boton no sirve
  const handleNoSirve = () => {
        // Realizar updates en la base de datos y avanzar al siguiente expediente
        console.log('No Sirve');
        setCurrentIndex((prevIndex) => (prevIndex + 1) % expedientes.length);
  };

  // Boton avanzar
  const handleAvanzar = () => {
        // Avanzar al siguiente expediente
        console.log('Avanzar');
        setCurrentIndex((prevIndex) => (prevIndex + 1) % expedientes.length);
  };



  return (
    <div>
        <ExpedienteButtons
            onEnviar={handleEnviar} 
            onNoSirve={handleNoSirve}
            onAvanzar={handleAvanzar}
        />
        {expedientes.length > 0 && <Expediente expediente={expedientes[currentIndex]} />}
        <ExpedienteForm handleEnviar={handleEnviar} />
    </div>
  );
};

export default RevisarExpedientes;