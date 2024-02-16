import React from 'react';
import './ExpedienteForm.css';

const ExpedienteForm = ({ values, onChange }) => {
    const handleChange = (event) => {
        onChange(event);
    };
    
    
    return (
        <form className="expediente-form">
            <label>
                <span>Nombre de la Consultoría</span>
                <input type="text" name="consultoria" value={values.consultoria} onChange={handleChange} required/>
            </label>
            <label>
                <span>País</span>
                <input type="text" name="lugar" value={values.lugar} onChange={handleChange} required/>
            </label>
            <label>
                <span>Tipo de Consultoría</span>
                <input type="text" name="tipo" value={values.tipo} onChange={handleChange} required/>
            </label>
            <label>
                <span>Código del Proceso/Prestamo</span>
                <input type="text" name="codigoProceso" value={values.codigoProceso} onChange={handleChange} required/>
            </label>
            <label>
                <span>Código Completo</span>
                <input type="text" name="codigoCompleto" value={values.codigoCompleto} onChange={handleChange} required />
            </label>
            <label>
                <span>Proyecto</span>
                <input type="text" name="proyecto" value={values.proyecto} onChange={handleChange} required />
            </label>
            <label>
                <span>Deadline</span>
                <input type="text" name="deadline" value={values.deadline} onChange={handleChange} required/>
            </label>
            <label>
                <span>Plazo</span>
                <input type="text" name="plazo" value={values.plazo} onChange={handleChange} required/>
            </label>
            <label>
                <span>Presupuesto</span>
                <input type="text" name="presupuesto" value={values.presupuesto} onChange={handleChange} required/>
            </label>
            <label>
                <span>Objetivos</span>
                <textarea name="objetivos" value={values.objetivos} onChange={handleChange} required></textarea>
            </label>
            <label>
                <span>Objetivo Específico</span>
                <textarea name="objetivoEspecifico" value={values.objetivoEspecifico} onChange={handleChange} required></textarea>
            </label>
            <label>
                <span>Alcance</span>
                <textarea name="alcance" value={values.alcance} onChange={handleChange} required></textarea>
            </label>
            <label>
                <span>Experiencia</span>
                <textarea name="experiencia" value={values.experiencia} onChange={handleChange} required></textarea>
            </label>

        </form>
    );
};


export default ExpedienteForm;
