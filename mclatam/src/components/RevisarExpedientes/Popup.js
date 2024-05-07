import './Popup.css';
import React from 'react';
const Popup = ({ text }) => {

  return (
    <div className="popup" style={{ background: '#4CBB17', opacity: 0.7, color: 'white', padding: '10px', marginTop: '10px', borderRadius: '5px' }}>
        {text}
    </div>
  );
};

export default Popup;