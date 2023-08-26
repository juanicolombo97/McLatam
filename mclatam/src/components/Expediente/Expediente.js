import React, { useState } from 'react';
import Modal from '../Modal/Modal';
import './Expediente.css';

const Expediente = ({ expediente }) => {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [modalContent, setModalContent] = useState('');
    const [titulo, ...contenidoArr] = modalContent.split(":");
    const contenido = contenidoArr.join(":"); 
    
        const handleModalOpen = (titulo, valor) => {
        setModalContent(`${titulo}: ${valor}`);
        setIsModalOpen(true);
    };

    return (
        <div className="expediente-container">
            <h2>Expediente</h2>
            <div className="expediente-data">
                {Object.entries(expediente).map(([titulo, valor], index) => (
                    <div key={index} className="expediente-item" onClick={() => handleModalOpen(titulo, valor)}>
                        <strong>{titulo}: </strong> 
                        {valor.length > 50 
                            ? <span>{`${valor.substring(0, 50)}...`}</span> 
                            : valor
                        }
                    </div>
                ))}
            </div>
            {
            isModalOpen && (
            <Modal
              onClose={() => setIsModalOpen(false)}
              style={{
                alignItems: 'flex-start',
                paddingTop: '5rem',
                width: 'auto',
                maxWidth: '100%',
                minWidth: '500px',
              }}
            >
              <div className="modal-fila-detalles">
                <span className="modal-fila-detalle-nombre">{titulo}</span>
                <span className="modal-fila-detalle-valor">{contenido}</span>
              </div>
            </Modal>
            )}
        </div>
    );
};

export default Expediente;