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
    {
      name: 'Encargado 1',
      data: [
        { name: 'Semana 1', value: 10 },
        { name: 'Semana 2', value: 20 },
        { name: 'Semana 3', value: 15 },
        { name: 'Semana 4', value: 30 }
      ]
    },
    {
      name: 'Encargado 2',
      data: [
        { name: 'Semana 1', value: 5 },
        { name: 'Semana 2', value: 15 },
        { name: 'Semana 3', value: 10 },
        { name: 'Semana 4', value: 20 }
      ]
    },
    {
      name: 'Encargado 3',
      data: [
        { name: 'Semana 1', value: 20 },
        { name: 'Semana 2', value: 25 },
        { name: 'Semana 3', value: 30 },
        { name: 'Semana 4', value: 25 }
      ]
    }
  ];

  return (
    <div className="stats-container">
      <h2>Cantidad de expedientes por página</h2>
      <div className="chart-container">
        <PieChart width={400} height={400}>
          <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} fill="#8884d8" label />
          <Legend />
        </PieChart>
      </div>
  
      <h2>Cantidad de expedientes revisados por semana y por encargado</h2>
      <div className="chart-container">
        <LineChart width={600} height={400} data={lineData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          {lineData.map((data, index) => (
            <Line key={index} dataKey="value" data={data.data} name={data.name} stroke={`#${Math.floor(Math.random() * 16777215).toString(16)}`} />
          ))}
        </LineChart>
      </div>
    </div>
  );

};

export default Estadisticas;