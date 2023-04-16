import React from 'react';
import { getAuth, onAuthStateChanged } from "firebase/auth";


const Dashboard = () => {

  const auth = getAuth();
  onAuthStateChanged(auth, (user) => {
    if (user) {
      // User is signed in, see docs for a list of available properties
      // https://firebase.google.com/docs/reference/js/firebase.User
      const uid = user.uid;
      console.log('uid', uid)
      // ...
    } else {
      // User is signed out
      // ...
      console.log('No hay usuario')
    }
  });
  
  return (
    <div>
      <h1>Dashboard</h1>
      <p>Bienvenido</p>
    </div>
  );
};

export default Dashboard;
