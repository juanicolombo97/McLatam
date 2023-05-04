import React, { useState } from 'react';
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
];

const Tabla = () => {
  const [modalOpen, setModalOpen] = useState(false);
  const [columnaSeleccionada, setColumnaSeleccionada] = useState(null);
  const [expedientesFiltrados, setExpedientesFiltrados] = useState(expedientes);

  const [modalFilaOpen, setModalFilaOpen] = useState(false);
  const [filaSeleccionada, setFilaSeleccionada] = useState(null);

  // Funcion que se encarga de abrir el modal de filtros
  const handleColumnClick = (e, columna) => {
    e.preventDefault();
    setColumnaSeleccionada(columna);
    setModalOpen(true);
  };

  // Funcion que se encarga de abrir el documento en una nueva pestaña
  const handleFilaClick = (e, fila) => {
    e.preventDefault();
    setFilaSeleccionada(fila);
    setModalFilaOpen(true);
  };

  // Funcion que se encarga de filtrar los expedientes segun el filtro seleccionado
  const handleFilterChange = (e, filtro) => {
    const checked = e.target.checked;
    let nuevosExpedientesFiltrados;

    if (checked) {
      nuevosExpedientesFiltrados = expedientes.filter(filtro.valor);
    } else {
      nuevosExpedientesFiltrados = expedientes;
    }

    setExpedientesFiltrados(nuevosExpedientesFiltrados);
  };

  // Funcion que se encarga de abrir el documento en una nueva pestaña-
  const openDocument = (url) => {
    window.open(url, '_blank');
  };

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            {columnas.map((columna, index) => (
              <th key={index} onClick={(e) => handleColumnClick(e, columna)}>
                {columna.nombre}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {expedientesFiltrados.map((expediente, index) => (
            <tr key={index} onClick={(e) => handleFilaClick(e, expediente)}>
              {columnas.map((columna, colIndex) => (
                <td key={colIndex}>{expediente[columna.nombre]}</td>))}
            </tr>
            ))}
        </tbody>
    </table>
    {modalOpen && (
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
{modalFilaOpen && (
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
    </div>
  );
};

export default Tabla;