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
                EI: Nombre de la Consultoría
                <input type="text" name="consultoria" value={formValues.consultoria} onChange={handleChange} />
            </label>
            <label>
                Lugar
                <input type="text" name="lugar" value={formValues.lugar} onChange={handleChange} />
            </label>
            <label>
                Tipo de Consultoría
                <input type="text" name="tipo" value={formValues.tipo} onChange={handleChange} />
            </label>
            <label>
                Código del Proceso/Prestamo
                <input type="text" name="codigoProceso" value={formValues.codigoProceso} onChange={handleChange} />
            </label>
            <label>
                Código Completo
                <input type="text" name="codigoCompleto" value={formValues.codigoCompleto} onChange={handleChange} />
            </label>
            <label>
                Proyecto
                <input type="text" name="proyecto" value={formValues.proyecto} onChange={handleChange} />
            </label>
            <label>
                Deadline
                <input type="text" name="deadline" value={formValues.deadline} onChange={handleChange} />
            </label>
            <label>
                Plazo
                <input type="text" name="plazo" value={formValues.plazo} onChange={handleChange} />
            </label>
            <label>
                Presupuesto
                <input type="text" name="presupuesto" value={formValues.presupuesto} onChange={handleChange} />
            </label>
            <label>
                Objetivos
                <textarea name="objetivos" value={formValues.objetivos} onChange={handleChange}></textarea>
            </label>
            <label>
                Objetivo Específico
                <textarea name="objetivoEspecifico" value={formValues.objetivoEspecifico} onChange={handleChange}></textarea>
            </label>
            <label>
                Alcance
                <textarea name="alcance" value={formValues.alcance} onChange={handleChange}></textarea>
            </label>
            <label>
                Experiencia
                <textarea name="experiencia" value={formValues.experiencia} onChange={handleChange}></textarea>
            </label>

        </form>
    );
};

export default ExpedienteForm;
