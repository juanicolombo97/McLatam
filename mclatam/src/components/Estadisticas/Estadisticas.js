import React from 'react';
import { PieChart, Pie, Legend, LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';
import './Estadisticas.css';

const Estadisticas = () => {
  // Datos para el PieChart
  const pieData = [
    { name: 'Página 1', value: 30, fill: '#8884d8' },
    { name: 'Página 2', value: 15, fill: '#83a6ed' },
    { name: 'Página 3', value: 25, fill: '#8dd1e1' },
    { name: 'Página 4', value: 20, fill: '#82ca9d' },
    { name: 'Página 5', value: 10, fill: '#a4de6c' }
  ];

  // Datos para el LineChart
  const lineData = [
    { name: 'Semana 1', Encargado_1: 10, Encargado_2: 5, Encargado_3: 20 },
    { name: 'Semana 2', Encargado_1: 20, Encargado_2: 15, Encargado_3: 25 },
    { name: 'Semana 3', Encargado_1: 15, Encargado_2: 10, Encargado_3: 30 },
    { name: 'Semana 4', Encargado_1: 30, Encargado_2: 20, Encargado_3: 25 },
  ];

  return (
    <div className="stats-container">

      <h2>Cantidad de expedientes revisados por semana y por encargado</h2>
      <div className="chart-container">
      <LineChart width={600} height={400} data={lineData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip />
        <Line dataKey="Encargado_1" stroke="#8884d8" />
        <Line dataKey="Encargado_2" stroke="#82ca9d" />
        <Line dataKey="Encargado_3" stroke="#ffc658" />
      </LineChart>
      </div>
      <h2>Cantidad de expedientes por página</h2>
      <div className="chart-container">
        <PieChart width={400} height={400}>
          <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} fill="#8884d8" label />
          <Legend />
        </PieChart>
      </div>
  
      
    </div>
  );

};

export default Estadisticas;