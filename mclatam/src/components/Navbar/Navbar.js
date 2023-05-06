import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      
      <Link to="/dashboard" className="nav-link">
        Dashboard
      </Link>
      <Link to="/revisar-expedientes" className="nav-link">
        Revisar Expedientes
      </Link>
      <Link to="/estadisticas" className="nav-link">
        Estadísticas
      </Link>
    </nav>
  );
};

export default Navbar;
