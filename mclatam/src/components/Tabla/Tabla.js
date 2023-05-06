import React, { useState, useRef } from 'react';
import Modal from '../Modal/Modal';
import './Tabla.css';

// Lista de filtros de cada columna
const columnas = [
  {
    nombre: 'ID',
    filtros: [
      { etiqueta: '1 - 100', valor: (expediente) => expediente.ID >= 1 && expediente.ID <= 100 },
      { etiqueta: '101 - 200', valor: (expediente) => expediente.ID >= 101 && expediente.ID <= 200 },
    ],
  },
  {
    nombre: 'Nombre',
    filtros: [
      { etiqueta: 'A - M', valor: (expediente) => /^[A-M]/.test(expediente.Nombre) },
      { etiqueta: 'N - Z', valor: (expediente) => /^[N-Z]/.test(expediente.Nombre) },
    ],
  },
  {
    nombre: 'Estado',
    filtros: [
      { etiqueta: 'Abierto', valor: (expediente) => expediente.Estado === 'Abierto' },
      { etiqueta: 'Cerrado', valor: (expediente) => expediente.Estado === 'Cerrado' },
    ],
  },
  {
    nombre: 'Documento',
    filtros: [], // No hay filtros para la columna Documento
  },
];

// Lista expedientes para poblar tabla
const expedientes = [
  { ID: 1, Nombre: 'Expediente A', Estado: 'Abierto', Documento: 'https://google.com' },
  { ID: 2, Nombre: 'Expediente B', Estado: 'Cerrado', Documento: 'https://google.com' },
  { ID: 3, Nombre: 'Expediente C', Estado: 'Abierto', Documento: 'https://google.com' },
  { ID: 1, Nombre: 'Expediente A', Estado: 'Abierto', Documento: 'https://google.com' },
  { ID: 2, Nombre: 'Expediente B', Estado: 'Cerrado', Documento: 'https://google.com' },
  { ID: 3, Nombre: 'Expediente C', Estado: 'Abierto', Documento: 'https://google.com' },
  { ID: 1, Nombre: 'Expediente A', Estado: 'Abierto', Documento: 'https://google.com' },
  { ID: 2, Nombre: 'Expediente B', Estado: 'Cerrado', Documento: 'https://google.com' },
  { ID: 3, Nombre: 'Expediente C', Estado: 'Abierto', Documento: 'https://google.com' },
  { ID: 1, Nombre: 'Expediente A', Estado: 'Abierto', Documento: 'https://google.com' },
  { ID: 2, Nombre: 'Expediente B', Estado: 'Cerrado', Documento: 'https://google.com' },
  { ID: 3, Nombre: 'Expediente C', Estado: 'Abierto', Documento: 'https://google.com' },
  { ID: 1, Nombre: 'Expediente A', Estado: 'Abierto', Documento: 'https://google.com' },
  { ID: 2, Nombre: 'Expediente B', Estado: 'Cerrado', Documento: 'https://google.com' },
  { ID: 3, Nombre: 'Expediente C', Estado: 'Abierto', Documento: 'https://google.com' },
  { ID: 1, Nombre: 'Expediente A', Estado: 'Abierto', Documento: 'https://google.com' },
  { ID: 2, Nombre: 'Expediente B', Estado: 'Cerrado', Documento: 'https://google.com' },
  { ID: 3, Nombre: 'Expediente C', Estado: 'Abierto', Documento: 'https://google.com' },
  
];

const Tabla = () => {
  const [modalOpen, setModalOpen] = useState(false);
  const [columnaSeleccionada, setColumnaSeleccionada] = useState(null);
  const [expedientesFiltrados, setExpedientesFiltrados] = useState(expedientes);
  const [modalFilaOpen, setModalFilaOpen] = useState(false);
  const [filaSeleccionada, setFilaSeleccionada] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;
  const totalPages = Math.ceil(expedientesFiltrados.length / itemsPerPage);
  const headerRefs = useRef([]);

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

  const handleFilterChange = (e, filtro) => { /* Tu función handleFilterChange */ };
  const openDocument = (url) => { /* Tu función openDocument */ };
  const handlePageChange = (newPage) => { /* Tu función handlePageChange */ };

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

  

  return (
    <div className="table-container">
      <table>
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
              {columnas.map((columna, colIndex) => (
                <td key={colIndex}>{expediente[columna.nombre]}</td>
              ))}
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
            justifyContent: 'center',
            paddingTop: '5rem',
          }}
        >
          <h3>Detalles del expediente</h3>
          <div className="modal-fila-detalles">
            {columnas.map((columna, index) => (
              columna.nombre !== 'Documento' && (
                <div className="modal-fila-detalle" key={index}>
                  <span className="modal-fila-detalle-nombre">{columna.nombre}:</span>
                  <span className="modal-fila-detalle-valor">{filaSeleccionada[columna.nombre]}</span>
                </div>
              )
            ))}
          </div>
          <div className="modal-fila-documento">
            <button
              className="modal-fila-detalle-boton"
              onClick={() => openDocument(filaSeleccionada.Documento)}
            >
              Ver documento
            </button>
          </div>
        </Modal>
    )}
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