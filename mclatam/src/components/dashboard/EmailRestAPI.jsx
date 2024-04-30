import axios from 'axios';
import React, { useState } from 'react'

const EmailRestAPI = ({expedientes}) => {

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log(expedientes)

    const serviceId = 'service_13g2x8b';
    const templateId = 'template_5d93i2v';
    const publicKey = '2V3D22_QeInH8FIm3';

    const formatearExpedientes = expedientes.map(expediente => {
      return `Titulo: ${expediente.Titulo}\nDocumento: ${expediente.Documento}\nPagina: ${expediente.Pagina}\nPais: ${expediente.Pais}\n\n`;
    }).join('\n');

    const data = {
      service_id: serviceId,
      template_id: templateId,
      user_id: publicKey,
      template_params: {
        from_name: name,
        from_email: email,
        message: formatearExpedientes,
      }
    };

    try {
      const res = await axios.post("https://api.emailjs.com/api/v1.0/email/send", data);
      console.log(res.data);
      setName('McLatam');
      setEmail('concamicky@gmail.com');
    } catch (error) {
      console.error(error);
    }
  }

  return (
    <div>
        <form onSubmit={handleSubmit} className='emailForm'>
          <button type="submit">Enviar Reporte</button>
        </form>
    </div>
  )
}

export default EmailRestAPI