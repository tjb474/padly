import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import StreamForm from './components/StreamForm/StreamForm';

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
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <div className={classes.streamFormSection}>
        <StreamForm />
      </div>
      <div className={classes.chartsSection}>
        {/* <ChartsComponent /> // Your charts or other content goes here */}
      </div>
    </div>
  );
}

export default App;
