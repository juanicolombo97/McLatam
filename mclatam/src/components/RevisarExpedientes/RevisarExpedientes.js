import React, {useState} from 'react'
import Expediente from '../Expediente/Expediente'
import ExpedienteButtons from '../ExpedienteButtons/ExpedienteButtons'
import ExpedienteForm from '../ExpedienteForm/ExpedienteForm';

export const RevisarExpedientes = () => {
  
  // Lista expedientes
  const expedientes = [
    {
        'Número': '12345',
        'Nombre': 'Juan Pérez',
        'Fecha de Ingreso': '01-01-2023',
        'Estado': 'Pendiente'
    },
    {
      'Número': '234rqrqe',
      'Nombre': 'Micky conca',
      'Fecha de Ingreso': '01-01-2023',
      'Estado': 'Activo'
  },
  {
    'Número': '12345',
    'Nombre': 'Pato conca',
    'Fecha de Ingreso': '01-01-2023',
    'Estado': 'fwef'
},
    // ... más expedientes aquí
  ];

  const [currentIndex, setCurrentIndex] = useState(0);

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
        <Expediente expediente={expedientes[currentIndex]} />
        <ExpedienteForm handleEnviar={handleEnviar} />
    </div>
);
};

export default RevisarExpedientes