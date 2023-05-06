import React, { useState } from 'react';
import './ExpedienteForm.css';

const ExpedienteForm = ({handleEnviar }) => {

    const [formValues, setFormValues] = useState({
        consultoria: '',
        lugar: '',
        tipo: '',
        codigoProceso: '',
        codigoCompleto: '',
        proyecto: '',
        deadline: '',
        plazo: '',
        presupuesto: '',
        objetivos: '',
        objetivoEspecifico: '',
        alcance: '',
        experiencia: ''
    });

    const handleChange = (event) => {
        const { name, value } = event.target;
        setFormValues((prevValues) => ({ ...prevValues, [name]: value }));
    };

    return (
        <form className="expediente-form" onSubmit={handleEnviar}>
            <label>
                <span>EI: Nombre de la Consultoría</span>
                <input type="text" name="consultoria" value={formValues.consultoria} onChange={handleChange} />
            </label>
            <label>
                <span>Lugar</span>
                <input type="text" name="lugar" value={formValues.lugar} onChange={handleChange} />
            </label>
            <label>
                <span>Tipo de Consultoría</span>
                <input type="text" name="tipo" value={formValues.tipo} onChange={handleChange} />
            </label>
            <label>
                <span>Código del Proceso/Prestamo</span>
                <input type="text" name="codigoProceso" value={formValues.codigoProceso} onChange={handleChange} />
            </label>
            <label>
                <span>Código Completo</span>
                <input type="text" name="codigoCompleto" value={formValues.codigoCompleto} onChange={handleChange} />
            </label>
            <label>
                <span>Proyecto</span>
                <input type="text" name="proyecto" value={formValues.proyecto} onChange={handleChange} />
            </label>
            <label>
                <span>Deadline</span>
                <input type="text" name="deadline" value={formValues.deadline} onChange={handleChange} />
            </label>
            <label>
                <span>Plazo</span>
                <input type="text" name="plazo" value={formValues.plazo} onChange={handleChange} />
            </label>
            <label>
                <span>Presupuesto</span>
                <input type="text" name="presupuesto" value={formValues.presupuesto} onChange={handleChange} />
            </label>
            <label>
                <span>Objetivos</span>
                <textarea name="objetivos" value={formValues.objetivos} onChange={handleChange}></textarea>
            </label>
            <label>
                <span>Objetivo Específico</span>
                <textarea name="objetivoEspecifico" value={formValues.objetivoEspecifico} onChange={handleChange}></textarea>
            </label>
            <label>
                <span>Alcance</span>
                <textarea name="alcance" value={formValues.alcance} onChange={handleChange}></textarea>
            </label>
            <label>
                <span>Experiencia</span>
                <textarea name="experiencia" value={formValues.experiencia} onChange={handleChange}></textarea>
            </label>
        </form>
    );
};


export default ExpedienteForm;
