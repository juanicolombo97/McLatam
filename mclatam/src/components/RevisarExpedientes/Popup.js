import './Popup.css';
import React, { useState } from 'react';
const Popup = ({ onClose }) => {

  return (
    <div className="popup">
        <p>Email enviado</p>
        <button className="close-button-black" onClick={onClose}>
              &times;
        </button>
    </div>
  );
};

export default Popup;