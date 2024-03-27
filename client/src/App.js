import React, { useEffect, useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import StreamForm from './components/StreamForm/StreamForm';
import SignIn from './components/SignIn'; // Ensure you have this SignIn component
import { auth } from './firebaseConfig'; // Adjust this import based on your file structure
import { onAuthStateChanged } from "firebase/auth";

// If you have other components to include, import them here
// For example: import HomePage from './components/HomePage';

// Define styles for the layout
const useStyles = makeStyles({
  root: {
    display: 'flex',
    flexDirection: 'row', // Align children side by side
    height: '100vh', // Full height of the viewport
    padding: '20px',
  },
  streamFormSection: {
    flexBasis: '33%', // StreamForm takes up 1/3 of the space
    paddingRight: '20px', // Optional spacing between the form and the charts
  },
  chartsSection: {
    flex: 1, // Charts take up the remaining space
  },
});

function App() {
  const [user, setUser] = useState(null);
  const classes = useStyles();

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user); // Set user if signed in or null if not
    });

    return () => unsubscribe(); // Clean up the subscription
  }, []);

  return (
    <div className={classes.root}>
      {user ? (
        <React.Fragment>
          <div className={classes.streamFormSection}>
            <StreamForm />
          </div>
          <div className={classes.chartsSection}>
            {/* <ChartsComponent /> // Your charts or other content goes here */}
          </div>
        </React.Fragment>
      ) : (
        <SignIn />
      )}
    </div>
  );
}

export default App;
