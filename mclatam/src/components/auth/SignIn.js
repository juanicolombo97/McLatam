import React, {useState} from 'react'
import './SignIn.css'
import LogoImg from '../../assets/images/logo.jpeg'
import {signInWithEmailAndPassword} from "firebase/auth";
import {auth} from '../../firebase'
import { useNavigate } from 'react-router-dom';

export const SignIn = ({isSignedIn, setIsSignedIn}) => {

    // Estados de los inputs
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    // Estado de error
    const [error, setError] = useState('')

    // Hook useNavigate
    const navigate = useNavigate();
    // Función para iniciar sesión
    const signIn = (e) => {

        // Prevenimos que se recargue la página
        e.preventDefault()
        console.log(email, password)

        // Iniciamos sesión
        signInWithEmailAndPassword(auth, email, password).then(
            (userCredential) => {
            // Signed in
            const user = userCredential.user;
            console.log(user)

            // Setteamos que este logueado
            setIsSignedIn(true)
            
            // Redireccionamos a dashboard
            navigate('/dashboard')
            
            }
        ).catch((error) => {
            setError('Usuario incorrecto');
            console.log(error)
        }  
        )
    }

  return (
    <div className='sign-in-container'>
        <form className='sign-in-form' onSubmit={signIn}>
            <img src={LogoImg} alt="Descripción de la imagen"  className='img-logo'/>
            <h2 className='sign-in-title'>Sign In</h2>
            <div className='sign-in-inputs'>
                <div className='input-container'>
                    <label htmlFor='email' >Email</label>
                    <input 
                        type='email' 
                        id='email'  
                        placeholder='Enter your email' 
                        value={email}
                        onChange={(e) => {
                            setEmail(e.target.value)
                            setError('')
                        }}
                    />
                </div>
                <div className='input-container'>
                    <label htmlFor='password' >Password</label>
                    <input 
                        type='password' 
                        id='password' 
                        placeholder='Enter your password' 
                        value={password} 
                        onChange={(e) => {
                            setPassword(e.target.value)
                            setError('')
                        }}
                    />
                </div>
                {error && <p>{error}</p>}
                <button className='sign-in-button'>Sign In</button>

            </div>
        </form>
    </div>
  )
}

export default SignIn