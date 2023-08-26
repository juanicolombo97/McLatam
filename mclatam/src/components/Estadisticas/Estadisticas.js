import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Legend, LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';
import { collection, getDocs } from "firebase/firestore";
import { db } from '../../firebase/firebase';
import './Estadisticas.css';

const Estadisticas = () => {
  const [pieNotReviewedData, setPieNotReviewedData] = useState([]);
  const [pieReviewedData, setPieReviewedData] = useState([]);
  const [lineData, setLineData] = useState([]);

  // Función para extraer el nombre de dominio del URL
  const extractDomain = (url) => {
    const match = url.match(/:\/\/(www[0-9]?\.)?(.[^/:]+)/i);
    if (match != null && match.length > 2 && typeof match[2] === 'string' && match[2].length > 0) {
      return match[2].split('.')[0];
    } else {
      return null;
    }
  }

  useEffect(() => {
    const fetchData = async () => {
      const crmRef = collection(db, "crm");
      const allDocs = await getDocs(crmRef);

      const notReviewedPagesData = {};
      const reviewedPagesData = {};

      allDocs.forEach(doc => {
        const data = doc.data();

        const pageName = extractDomain(data.pagina);

        if (data.estado_expediente === 'NoRevisado') {
          notReviewedPagesData[pageName] = (notReviewedPagesData[pageName] || 0) + 1;
        } else {
          reviewedPagesData[pageName] = (reviewedPagesData[pageName] || 0) + 1;
        }
      });

      const pieNotReviewedResults = Object.keys(notReviewedPagesData).map((page, idx) => ({ name: page, value: notReviewedPagesData[page], fill: `#${Math.floor(Math.random()*16777215).toString(16)}` }));
      const pieReviewedResults = Object.keys(reviewedPagesData).map((page, idx) => ({ name: page, value: reviewedPagesData[page], fill: `#${Math.floor(Math.random()*16777215).toString(16)}` }));

      setPieNotReviewedData(pieNotReviewedResults);
      setPieReviewedData(pieReviewedResults);
    };

    fetchData();
  }, []);

  return (
    <div className="stats-container">
      // ... (Mantenemos el código de LineChart aquí)
      <div className="chart-container">
        <h2>Expedientes no revisados por página</h2>
        {pieNotReviewedData.length > 0 ? (
          <PieChart width={400} height={400}>
            <Pie data={pieNotReviewedData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} fill="#8884d8" label />
            <Legend />
          </PieChart>
        ) : (
          <p>Sin expedientes disponibles</p>
        )}
      </div>

      <div className="chart-container">
        <h2>Expedientes revisados por página</h2>
        {pieReviewedData.length > 0 ? (
          <PieChart width={400} height={400}>
            <Pie data={pieReviewedData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} fill="#8884d8" label />
            <Legend />
          </PieChart>
        ) : (
          <p>Sin expedientes disponibles</p>
        )}
      </div>
    </div>
  );
};

export default Estadisticas;
