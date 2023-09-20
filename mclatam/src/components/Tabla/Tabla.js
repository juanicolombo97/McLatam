import React, { useState, useRef, useEffect } from 'react';
import { doc, updateDoc } from "firebase/firestore";
import { db } from '../../firebase/firebase'; 
import Modal from '../Modal/Modal';
import './Tabla.css';

// Lista de filtros de cada columna
const columnas = [
  {
    nombre: 'ID',
    filtros: [
      { etiqueta: '1 - 100', valor: (expediente) => expediente.id >= 1 && expediente.id <= 100 },
      { etiqueta: '101 - 200', valor: (expediente) => expediente.id >= 101 && expediente.id <= 200 },
    ],
  },
  {
    nombre: 'Expediente_id',
    filtros: [
    ],
  },
  {
    nombre: 'Titulo',
    filtros: [
      { etiqueta: 'A - M', valor: (expediente) => /^[A-M]/.test(expediente.Titulo) },
      { etiqueta: 'N - Z', valor: (expediente) => /^[N-Z]/.test(expediente.Titulo) },
    ],
  },
  {
    nombre: 'Estado_expediente',
    filtros: [
      { etiqueta: 'Revisado', valor: (expediente) => expediente.Estado_expediente === 'Revisado' },
      { etiqueta: 'NoRevisado', valor: (expediente) => expediente.Estado_expediente === 'NoRevisado' },
    ],
  },
  {
    nombre: 'Documento',
    filtros: [], // No hay filtros para la columna Documento
  },
  
];

const Tabla = ({expedientes}) => {
  const [modalOpen, setModalOpen] = useState(false);
  const [columnaSeleccionada, setColumnaSeleccionada] = useState(null);
  const [expedientesFiltrados, setExpedientesFiltrados] = useState([]);
  const [modalFilaOpen, setModalFilaOpen] = useState(false);
  const [filaSeleccionada, setFilaSeleccionada] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [dataLoaded, setDataLoaded] = useState(false);

  const itemsPerPage = 15;
  const totalPages = Math.ceil(expedientesFiltrados.length / itemsPerPage);
  const headerRefs = useRef([]);

  // Use effect para cerrar el modal de detalles al precionar afuera o escape
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        setModalFilaOpen(false);
      }
    };

    const handleClick = (e) => {
      if (e.target.classList.contains('modal')) {
        setModalFilaOpen(false);
      }
    };

    document.addEventListener('keydown', handleEscape);
    document.addEventListener('click', handleClick);

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.removeEventListener('click', handleClick);
    };
  }, []);

  // USEefect pra ver si cargaron los datos
  useEffect(() => {
    if (expedientes && expedientes.length > 0) {
        setDataLoaded(true);
        setExpedientesFiltrados(expedientes);
    }
  }, [expedientes]);
  
  const handleColumnClick = (e, columna) => {
    e.preventDefault();
    setColumnaSeleccionada(columna);
    setModalOpen(true);
  };

  const handleFilaClick = (e, fila) => {
    e.preventDefault();
    setFilaSeleccionada(fila);
    setModalFilaOpen(true);
  };

  const handleFilterChange = (e, filtro) => {
    // Si el filtro está chequeado, lo agrega a la lista de filtros aplicados, de lo contrario, lo quita
    if (e.target.checked) {
      setExpedientesFiltrados(expedientesFiltrados.filter(filtro.valor));
    } else {
      setExpedientesFiltrados(expedientesFiltrados.filter(filtro.valor));
    }
  };
  
  const openDocument = (url) => {
    // Abre el documento en una nueva pestaña
    window.open(url, '_blank');
  };
  
  const handlePageChange = (newPage) => {
    // Actualiza el número de página actual
    setCurrentPage(newPage);
  };

  const paginatedExpedientes = expedientesFiltrados.slice((currentPage - 1) * itemsPerPage, currentPage * itemsPerPage);

  const handleResize = (e, index) => {
    const header = headerRefs.current[index];
    const handle = header.querySelector(".resize-handle");
    if (e.target !== handle) return;

    let startWidth = 0;
    let startX = 0;

    startX = e.clientX;
    startWidth = header.offsetWidth;

    const handleMouseMove = (event) => {
      const diff = event.clientX - startX;
      header.style.width = `${startWidth + diff}px`;
    };

    const handleMouseUp = () => {
      document.removeEventListener("mousemove", handleMouseMove);
      document.removeEventListener("mouseup", handleMouseUp);
    };

    document.addEventListener("mousemove", handleMouseMove);
    document.addEventListener("mouseup", handleMouseUp);
  };

  const handleDeleteClick = async (expedienteId) => {
    const expedienteRef = doc(db, 'crm', expedienteId);

    await updateDoc(expedienteRef, {
      "Fecha_revisado": "",
      "Fecha_enviado": "",
      "Encargado": "",
      "Reporte": ""
    });

    // Actualizar el estado local para reflejar los cambios
    const newExpedientes = expedientesFiltrados.map(exp => {
      if (exp.id === expedienteId) {
        return {
          ...exp,
          Fecha_revisado: "",
          Fecha_enviado: "",
          Encargado: "",
          Reporte: ""
        };
      }
      return exp;
    });

    setExpedientesFiltrados(newExpedientes);
  };
  if (!dataLoaded) {
    return (
      <div className="transparent-modal">
        <div className="loading-icon"></div>
      </div>
    );
  }
  return (
    <div className="table-container">
      <table  style={{ tableLayout: 'auto', display: 'inline-table' }}>
        <thead>
          <tr>
            {columnas.map((columna, index) => (
              <th
                key={index}
                ref={(el) => (headerRefs.current[index] = el)}
                onClick={(e) => handleColumnClick(e, columna)}
              >
                {columna.nombre}
                <span
                  className="resize-handle"
                  onMouseDown={(e) => handleResize(e, index)}
                ></span>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {paginatedExpedientes.map((expediente, index) => (
            <tr key={index} onClick={(e) => handleFilaClick(e, expediente)}>
              <td>{expediente.id}</td>
              <td>{expediente.Expediente_id}</td>
              <td>{expediente.Titulo}</td>
              <td>{expediente.Estado_expediente}</td>
              <td>
                <a href={expediente.Documento} target="_blank" rel="noreferrer">
                  Ver Documento
                </a>
              </td>
              <td>
                <button onClick={() => handleDeleteClick(expediente.id)}>
                  <span style={{color: 'red'}}>🗑</span>
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

    {
    modalOpen && (
    <Modal
      onClose={() => setModalOpen(false)}
      style={{
        alignItems: 'flex-start',
        paddingTop: '5rem',
      }}
    >
      <h3>Filtrar por {columnaSeleccionada?.nombre}</h3>
      <ul>
        {columnaSeleccionada?.filtros.map((filtro, index) => (
          <li key={index}>
            <label>
              <input
                type="checkbox"
                onChange={(e) => handleFilterChange(e, filtro)}
              />
              {filtro.etiqueta}
            </label>
          </li>
        ))}
      </ul>
    </Modal>
    )}
    {
  modalFilaOpen && (
    <Modal
      onClose={() => setModalFilaOpen(false)}
      style={{
        alignItems: 'flex-start',
        paddingTop: '5rem',
        width: 'auto',
        maxWidth: '100%',
        minWidth: '500px',
      }}
    >
      <h3>Detalles del expediente</h3>
      <div className="modal-fila-detalles">
        {filaSeleccionada && Object.keys(filaSeleccionada).map((key, index) => (
          key !== 'Documento' && (
            <div className="modal-fila-detalle" key={index}>
              <span className="modal-fila-detalle-nombre">{key}:</span>
              <span className="modal-fila-detalle-valor">
                {typeof filaSeleccionada[key] === 'object' ? JSON.stringify(filaSeleccionada[key]) : filaSeleccionada[key]}
              </span>
            </div>
          )
        ))}
      </div>
      <div className="modal-fila-documento">
        <button
          className="modal-fila-detalle-boton"
          onClick={() => openDocument(filaSeleccionada.Documento || filaSeleccionada.pagina)}
        >
          Ver documento
        </button>
      </div>

    </Modal>
  )
}
       <div className="pagination">
        <button onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>
          Anterior
        </button>
        <span>
          Página {currentPage} de {totalPages}
        </span>
        <button onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages}>
          Siguiente
        </button>
      </div>
      <div className="row-count">
        <p>Total de filas: {expedientesFiltrados.length}</p>
      </div>
    
    </div>

  );
};

export default Tabla;