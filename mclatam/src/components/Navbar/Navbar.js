import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <NavLink to="/dashboard" className="nav-link" activeClassName="active">
        Dashboard
      </NavLink>
      <NavLink to="/revisar-expedientes" className="nav-link" activeClassName="active">
        Revisar Expedientes
      </NavLink>
      <NavLink to="/estadisticas" className="nav-link" activeClassName="active">
        Estadísticas
      </NavLink>
    </nav>
  );
};

export default Navbar;
