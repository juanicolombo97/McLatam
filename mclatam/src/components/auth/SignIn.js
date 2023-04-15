import React, {useState} from 'react'
import './SignIn.css'
export const SignIn = () => {

    // Estados de los inputs
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

  return (
    <div className='sign-in-container'>
        <form className='sign-in-form'>
            <h2 className='sign-in-title'>Sign In</h2>
            <div className='sign-in-inputs'>
                <div className='input-container'>
                    <label htmlFor='email' >Email</label>
                    <input type='email' id='email'  placeholder='Enter your email' value={email}/>
                </div>
                <div className='input-container'>
                    <label htmlFor='password' >Password</label>
                    <input type='password' id='password' placeholder='Enter your password' value={password} />
                </div>
               
                <button className='sign-in-button'>Sign In</button>

            </div>
        </form>
    </div>
  )
}

export default SignIn