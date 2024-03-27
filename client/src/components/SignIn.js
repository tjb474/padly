import React from 'react';
import { auth } from '../firebaseConfig'; // Go up two levels
import { GoogleAuthProvider, signInWithPopup } from "firebase/auth";

const SignIn = () => {
  const signInWithGoogle = () => {
    const provider = new GoogleAuthProvider();
    signInWithPopup(auth, provider)
    .then((result) => {
      // This gives you a Google Access Token. You can use it to access the Google API.
      console.log(result);
    }).catch((error) => {
      // Handle Errors here.
      console.error(error);
    });
  };

  return (
    <button onClick={signInWithGoogle}>Sign in with Google</button>
  );
};

export default SignIn;
