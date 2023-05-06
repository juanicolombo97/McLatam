import React from 'react';
import './Expediente.css';

const Expediente = ({ expediente }) => {
    return (
        <div className="expediente-container">
            <h2>Expediente</h2>
            <div className="expediente-data">
                {Object.entries(expediente).map(([titulo, valor], index) => (
                    <div key={index} className="expediente-item">
                        <strong>{titulo}:</strong> {valor}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Expediente;
