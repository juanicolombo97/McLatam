import React, { useState, useEffect } from 'react';
import { PieChart, Pie, Legend, LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip } from 'recharts';
import { collection, getDocs, query, where } from "firebase/firestore";
import { db } from '../../firebase/firebase';
import './Estadisticas.css';

const Estadisticas = () => {
  const [pieNotReviewedData, setPieNotReviewedData] = useState([]);
  const [pieReviewedData, setPieReviewedData] = useState([]);
  const [lineData, setLineData] = useState([]);

  const extractDomain = (url) => {
    const match = url.match(/:\/\/(www[0-9]?\.)?(.[^/:]+)/i);
    if (match != null && match.length > 2 && typeof match[2] === 'string' && match[2].length > 0) {
      return match[2].split('.')[0];
    } else {
      return null;
    }
  }

  // Nuevas funciones adicionales
  const getWeekNumber = (d) => {
    d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
    var yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    var weekNo = Math.ceil(( ( (d - yearStart) / 86400000) + 1)/7);
    return weekNo;
  }

  const processLineData = (data) => {
    let processedData = {};

    data.forEach(expediente => {
      let week = getWeekNumber(new Date(expediente.Fecha_revisado));
      let year = new Date(expediente.Fecha_revisado).getFullYear();
      let key = `${year}-W${week}`;

      if (!processedData[key]) {
        processedData[key] = {};
      }
      
      if (!processedData[key][expediente.encargado]) {
        processedData[key][expediente.encargado] = 0;
      }

      processedData[key][expediente.encargado]++;
    });

    const finalData = Object.keys(processedData).map(key => {
      return { name: key, ...processedData[key] };
    });

    setLineData(finalData);
  };

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

      // Obtener los datos para el gráfico de líneas de los últimos 3 meses
      const threeMonthsAgo = new Date();
      threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);

      const q = query(crmRef, where("Fecha_revisado", ">=", threeMonthsAgo));
      const snapshot = await getDocs(q);

      const lineChartData = snapshot.docs.map(doc => doc.data());
      processLineData(lineChartData);
    };

    fetchData();
  }, []);

  return (
    <div className="stats-container">
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

      <div className="chart-container">
        <h2>Cantidad de expedientes revisados por semana y por encargado</h2>
        <LineChart width={600} height={400} data={lineData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          {
            Object.keys(lineData[0] || {}).filter(key => key !== 'name').map((encargado, index) => (
              <Line key={encargado} dataKey={encargado} stroke={`#${Math.floor(Math.random()*16777215).toString(16)}`} />
            ))
          }
        </LineChart>
      </div>
    </div>
  );
};

export default Estadisticas;
