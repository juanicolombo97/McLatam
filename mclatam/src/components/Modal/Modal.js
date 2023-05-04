import React from 'react';
import './Modal.css';

const Modal = ({ children, onClose, style }) => {
  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <div className="modal-overlay" onClick={handleOverlayClick} style={style}>
      <div className="modal-content">{children}</div>
    </div>
  );
};

export default Modal;
