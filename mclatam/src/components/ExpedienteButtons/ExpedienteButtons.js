import React from 'react';
import './ExpedienteButtons.css';

const ExpedienteButtons = ({ onEnviar, onNoSirve, onAvanzar }) => {
    return (
        <div className="buttons-container">
            <button className="button enviar" onClick={onEnviar}>
                Enviar
            </button>
            <button className="button no-sirve" onClick={onNoSirve}>
                No Sirve
            </button>
            <button className="button avanzar" onClick={onAvanzar}>
                Avanzar
            </button>
        </div>
    );
};

export default ExpedienteButtons;
