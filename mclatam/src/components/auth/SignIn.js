import React, {useState} from 'react'

export const SignIn = () => {
  return (
    <div className='sign-in-container'>
        <form className='sign-in-form'>
            <h2 className='sign-in-title'>Sign In</h2>
            <div className='sign-in-inputs'>

                <label htmlFor='email' placeholder='Enter your email'>Email</label>
                <input type='email' id='email' />

                <label htmlFor='password' placeholder='Enter your password'>Password</label>
                <input type='password' id='password' />

                <button className='sign-in-button'>Sign In</button>

            </div>
        </form>
    </div>
  )
}

export default SignIn