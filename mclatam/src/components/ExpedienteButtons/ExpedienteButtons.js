import React from 'react';
import './ExpedienteButtons.css';

const ExpedienteButtons = ({ onEnviar, onNoSirve, onAnterior, onAvanzar, handleEnviarReporte }) => {
    return (
        <div className="buttons-container">
            <button className="button enviar" onClick={onEnviar}>Enviar</button>
            <button className="button no-sirve" onClick={onNoSirve}>No Sirve</button>
            <button className="button avanzar" onClick={onAnterior}>Anterior</button>
            <button className="button avanzar" onClick={onAvanzar}>
                Siguiente
            </button>
            <button className="button enviar_reporte" onClick={handleEnviarReporte}>
                Enviar Reporte
            </button>
        </div>
    );
};

export default ExpedienteButtons;
