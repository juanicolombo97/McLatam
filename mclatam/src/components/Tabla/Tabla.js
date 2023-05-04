import React, { useState } from 'react';
import Modal from '../Modal/Modal';
import './Tabla.css';

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
];

const expedientes = [
  { ID: 1, Nombre: 'Expediente A', Estado: 'Abierto' },
  { ID: 2, Nombre: 'Expediente B', Estado: 'Cerrado' },
  { ID: 3, Nombre: 'Expediente C', Estado: 'Abierto' },
  // ...
];

const Tabla = () => {
  const [modalOpen, setModalOpen] = useState(false);
  const [columnaSeleccionada, setColumnaSeleccionada] = useState(null);
  const [expedientesFiltrados, setExpedientesFiltrados] = useState(expedientes);

  const handleColumnClick = (e, columna) => {
    e.preventDefault();
    setColumnaSeleccionada(columna);
    setModalOpen(true);
  };

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
            <tr key={index}>
              {columnas.map((columna, colIndex) => (
                <td key={colIndex}>{expediente[columna.nombre]}</td>
              ))}
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
</div>
);
};

export default Tabla;


