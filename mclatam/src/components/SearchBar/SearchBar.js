import React, { useState, useEffect } from 'react';
import './SearchBar.css';
import { collection, getDocs, query, where } from "firebase/firestore";
import { db } from '../../firebase/firebase';

const SearchBar = ({ searchTerm, setSearchTerm, setExpedientes }) => {
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    if (searchTerm === "") return;

    const searchInFirebase = async () => {
      setIsSearching(true);
      const expedientesRef = collection(db, "crm");
      const q = query(
        expedientesRef, 
        where("algún_campo", "==", searchTerm),
        where("Fecha_revisado", "!=", null)  
      );
    
      const querySnapshot = await getDocs(q);
      const expedientesData = [];
      querySnapshot.forEach((doc) => {
        expedientesData.push({ id: doc.id, ...doc.data() });
      });
      if (expedientesData.length > 0) {
        setExpedientes(expedientesData);
      }
    
      setIsSearching(false);
    };

    searchInFirebase();
  }, [searchTerm]);

  return (
    <div className="search-container">
      <input
        className="search-input"
        type="text"
        placeholder="Buscar expediente..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      {isSearching && <span>Buscando...</span>}
    </div>
  );
};

export default SearchBar;
