// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAxPoSTVR3uDXLXzihNd04WYnsS9flKDBk",
  authDomain: "mclatam-d6fdb.firebaseapp.com",
  projectId: "mclatam-d6fdb",
  storageBucket: "mclatam-d6fdb.appspot.com",
  messagingSenderId: "585010686503",
  appId: "1:585010686503:web:f54ccc078140f44736bc02",
  measurementId: "G-Y2QYJHJ67K"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication and get a reference to the service
export const auth = getAuth(app);