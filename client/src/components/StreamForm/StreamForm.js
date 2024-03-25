import React, { useState } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import IncomeStreamSalaryForm from './IncomeStreamSalaryForm';
import ExpenseStreamMortgageForm from './ExpenseStreamMortgageForm';
// Import other specific form components as needed

// Define your component-specific styles
const useStyles = makeStyles({
  formContainer: {
    display: 'flex',
    flexDirection: 'column',
    margin: '20px auto',
    padding: '20px',
    maxWidth: '600px',
    background: '#f9f9f9',
    borderRadius: '8px',
    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
  },
  formHeading: {
    color: '#007bff',
    marginBottom: '20px',
  },
  formSelection: {
    marginBottom: '20px',
    '& label': {
      marginRight: '10px',
    },
    '& select': {
      padding: '10px',
      borderRadius: '5px',
      border: '1px solid #ccc',
    },
  },
  // Additional styles can be added here
});

function StreamForm() {
  const [streamType, setStreamType] = useState('income');
  const [streamCategory, setStreamCategory] = useState('');
  const classes = useStyles(); // Use the styles defined

  const renderForm = () => {
    if (streamType === 'income') {
      switch (streamCategory) {
        case 'salary':
          return <IncomeStreamSalaryForm />;
        case 'investment':
          // Return the investment form component once defined
          break;
        default:
          return null;
      }
    } else if (streamType === 'expense') {
      switch (streamCategory) {
        case 'mortgage':
          return <ExpenseStreamMortgageForm />;
        default:
          return null;
      }
    }
  };

  return (
    <div className={classes.formContainer}>
      <h2 className={classes.formHeading}>Add New Stream</h2>

      <div className={classes.formSelection}>
        <label>Stream Type:</label>
        <select onChange={(e) => setStreamType(e.target.value)} value={streamType}>
          <option value="income">Income</option>
          <option value="expense">Expense</option>
        </select>
      </div>

      {streamType && (
        <div className={classes.formSelection}>
          <label>Category:</label>
          {streamType === 'income' ? (
            <select onChange={(e) => setStreamCategory(e.target.value)} value={streamCategory}>
              <option value="">Select Category</option>
              <option value="salary">Salary</option>
              <option value="investment">Investment</option>
              {/* Add more income categories as needed */}
            </select>
          ) : (
            <select onChange={(e) => setStreamCategory(e.target.value)} value={streamCategory}>
              <option value="">Select Category</option>
              <option value="mortgage">Mortgage</option>
              {/* Add more expense categories as needed */}
            </select>
          )}
        </div>
      )}

      {streamCategory && renderForm()}
    </div>
  );
}

export default StreamForm;
