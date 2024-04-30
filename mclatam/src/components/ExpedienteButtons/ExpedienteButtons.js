import React from 'react';
import './ExpedienteButtons.css';

const ExpedienteButtons = ({ onEnviar, onNoSirve, onAnterior, onAvanzar }) => {
    return (
        <div className="buttons-container">
            <button className="button enviar" onClick={onEnviar}>Seleccionar</button>
            <button className="button no-sirve" onClick={onNoSirve}>No Sirve</button>
            <button className="button avanzar" onClick={onAnterior}>Anterior</button>
            <button className="button avanzar" onClick={onAvanzar}>
                Siguiente
            </button>
        </div>
    );
};

export default ExpedienteButtons;
