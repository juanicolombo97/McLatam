import React, { useState, useEffect } from 'react';
import { collection, getDocs, query, where, doc, updateDoc,serverTimestamp } from "firebase/firestore";
import { db } from '../../firebase/firebase';  // Asegúrate de tener la ruta correcta a tu archivo firebase
import Expediente from '../Expediente/Expediente';
import ExpedienteButtons from '../ExpedienteButtons/ExpedienteButtons';
import ExpedienteForm from '../ExpedienteForm/ExpedienteForm';
import {auth} from '../../firebase/firebase'
import Popup from "./Popup";

export const RevisarExpedientes = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [expedientes, setExpedientes] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [noExpedientes, setNoExpedientes] = useState(false);
  const [isPopupVisible, setPopupVisibility] = useState(false);

  // Formulario de reporte 
  const initialFormValues = {
    consultoria: '',
    lugar: '',
    tipo: '',
    codigoProceso: '',
    codigoCompleto: '',
    proyecto: '',
    deadline: '',
    plazo: '',
    presupuesto: '',
    objetivos: '',
    objetivoEspecifico: '',
    alcance: '',
    experiencia: '',
    encargado: '',
  };
  
  const [formValues, setFormValues] = useState(initialFormValues);

    
  useEffect(() => {
    const loadExpedientes = async () => {
      const expedientesRef = collection(db, "crm"); 
      const q = query(expedientesRef, where("Estado_expediente", "==", "NoRevisado"));
      const querySnapshot = await getDocs(q);
      const expedientesData = [];
      querySnapshot.forEach((doc) => {
        expedientesData.push({ id: doc.id, ...doc.data() });
      });
      console.log('Expedientes: ', expedientesData);
      if(expedientesData.length === 0){
        setNoExpedientes(true);
      } else {
        setExpedientes(expedientesData);
        setNoExpedientes(false);
      }
      setIsLoading(false);

    };

    loadExpedientes();
  }, []);


  const handleEnviar = async () => {
    setIsLoading(true);
    console.log("formValues")
    console.log(Object.values(formValues))
    // obtenemos el mail del usuario de firebase
    const user = auth.currentUser;
    const email = user.email;
    console.log('EMAIL: ', email);

    // Agregamos el mail del usuario al formulario
    formValues.encargado = email;
    const allFieldsFilled = Object.values(formValues).every(field => field !== '');
    if (!allFieldsFilled) {
      alert("Por favor, completa todos los campos antes de enviar.");
      setIsLoading(false);
      return;
    }

    // Formatear los datos del formulario para el reporte
    const formattedReport = Object.entries(formValues).map(([key, value]) => `${key}: ${value}`).join('\n');
  
    // Realizar updates en la base de datos y avanzar al siguiente expediente
    const expedienteRef = doc(db, "crm", expedientes[currentIndex].id);
    
    await updateDoc(expedienteRef, {
      Estado_expediente: "Enviar",
      Reporte: formattedReport,
      Fecha_revisado: serverTimestamp(),
      Encargado: email,
    });
  
    if (expedientes.length > 0) {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % expedientes.length);
    }
    setIsLoading(false);
    setFormValues(initialFormValues);
    setPopupVisibility(true);
    setTimeout(() => {
      setPopupVisibility(false);
    }, 2000);

  };
  
  // Boton no sirve
  const handleNoSirve = async () => {
    setIsLoading(true);

    // Realizar updates en la base de datos y avanzar al siguiente expediente
    const expedienteRef = doc(db, "crm", expedientes[currentIndex].id);
    
    await updateDoc(expedienteRef, {
      Estado_expediente: "NoSirve",
      Fecha_revisado: serverTimestamp()
    });

    if (expedientes.length > 0) {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % expedientes.length);
    }
    setIsLoading(false);
    setFormValues(initialFormValues);

  };

  // Boton anterior
  const handleAnterior = () => {
    setIsLoading(true);

        // Retroceder al expediente anterior
    console.log('Anterior');
    if (expedientes.length > 0) {
      setCurrentIndex((prevIndex) => (prevIndex - 1) % expedientes.length);
    }
    setIsLoading(false);
    setFormValues(initialFormValues);

  };

  // Boton avanzar
  const handleAvanzar = () => {
    setIsLoading(true);

        // Avanzar al siguiente expediente
    console.log('Avanzar');
    if (expedientes.length > 0) {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % expedientes.length);
    }        
    setIsLoading(false);
    setFormValues(initialFormValues);

  };

  const handleEnviarReporte = async () => {
    console.log('Enviar reporte');

  }

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormValues((prevValues) => ({ ...prevValues, [name]: value }));
  };

  const handleClosePopup = () => {
    setPopupVisibility(false);
  };

  return (
    <div>
        {isLoading ? (
            <div className="transparent-modal">
              <div className="loading-icon"></div>
            </div>
        ) :
        expedientes.length === 0 ? (
            <Expediente expediente={null} />
        ) : (
            <>
              {isPopupVisible && <Popup onClose={handleClosePopup} />}
              <ExpedienteButtons
                    onEnviar={handleEnviar}
                    onNoSirve={handleNoSirve}
                    onAnterior={handleAnterior}
                    onAvanzar={handleAvanzar}
                    handleEnviarReporte={handleEnviarReporte}
                />
                <Expediente expediente={expedientes[currentIndex]} />
                <ExpedienteForm values={formValues} onChange={handleChange} />
            </>
        )}
    </div>
);

};

export default RevisarExpedientes;