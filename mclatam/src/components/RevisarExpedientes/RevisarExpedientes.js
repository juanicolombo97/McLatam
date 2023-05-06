import React from 'react'
import Expediente from '../Expediente/Expediente'
export const RevisarExpedientes = () => {
  const expedienteData = {
    'Número': '12345',
    'Nombre': 'Juan Pérez',
    'Fecha de Ingreso': '01-01-2023',
    'Estado': 'Pendiente'
};

return (
    <div>
        <Expediente expediente={expedienteData} />
    </div>
);
}

export default RevisarExpedientes