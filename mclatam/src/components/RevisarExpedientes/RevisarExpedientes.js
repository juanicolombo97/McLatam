import React, { useState, useEffect } from 'react';
import { collection, getDocs, query, where, doc, updateDoc,serverTimestamp } from "firebase/firestore";
import { db } from '../../firebase/firebase';  // Asegúrate de tener la ruta correcta a tu archivo firebase
import Expediente from '../Expediente/Expediente';
import ExpedienteButtons from '../ExpedienteButtons/ExpedienteButtons';
import ExpedienteForm from '../ExpedienteForm/ExpedienteForm';

export const RevisarExpedientes = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [expedientes, setExpedientes] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);

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
    experiencia: ''
  };
  const [formValues, setFormValues] = useState(initialFormValues);


  useEffect(() => {
    const loadExpedientes = async () => {
      const expedientesRef = collection(db, "crm"); // Asegúrate de cambiar "crm" por el nombre de tu colección
      const q = query(expedientesRef, where("estado_expediente", "==", "NoRevisado"));
      const querySnapshot = await getDocs(q);
      const expedientesData = [];
      querySnapshot.forEach((doc) => {
        expedientesData.push({ id: doc.id, ...doc.data() });
      });
      setExpedientes(expedientesData);
    };

    loadExpedientes();
  }, []);

  useEffect(() => {
    if (expedientes && expedientes.length > 0) {
      setIsLoading(false);
    }
  }, [expedientes]);

  const handleEnviar = async () => {
    setIsLoading(true);

    const allFieldsFilled = Object.values(formValues).every(field => field !== '');
    if (!allFieldsFilled) {
      alert("Por favor, completa todos los campos antes de enviar.");
      return;
    }

    // Formatear los datos del formulario para el reporte
    const formattedReport = Object.entries(formValues).map(([key, value]) => `${key}: ${value}`).join('\n');
  
    console.log('REPORTE: ', formattedReport);
  
    // Realizar updates en la base de datos y avanzar al siguiente expediente
    const expedienteRef = doc(db, "crm", expedientes[currentIndex].id);
    
    await updateDoc(expedienteRef, {
      Estado_expediente: "Enviar",
      Reporte: formattedReport,
      Fecha_revisado: serverTimestamp()
    });
  
    if (expedientes.length > 0) {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % expedientes.length);
    }
    setIsLoading(false);
    setFormValues(initialFormValues);

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

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormValues((prevValues) => ({ ...prevValues, [name]: value }));
  };


return (
  <div>
     {isLoading && (
        <div className="loading-modal">
          <div className="loading-icon"></div>
        </div>
      )}
   <ExpedienteButtons
      onEnviar={handleEnviar}
      onNoSirve={handleNoSirve}
      onAvanzar={handleAvanzar}
    />
    {expedientes.length > 0 && <Expediente expediente={expedientes[currentIndex]} />}
    <ExpedienteForm values={formValues} onChange={handleChange} />
  </div>
);
};

export default RevisarExpedientes;