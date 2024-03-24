import React, { useState } from 'react';
import './StreamForm.css'; // Ensure you've created and imported this CSS file
import IncomeStreamSalaryForm from './IncomeStreamSalaryForm';
import ExpenseStreamMortgageForm from './ExpenseStreamMortgageForm';
// Import other specific form components as needed

function StreamForm() {
  const [streamType, setStreamType] = useState('income');
  const [streamCategory, setStreamCategory] = useState('');

  // Function to render the appropriate form based on stream type and category
  const renderForm = () => {
    // Example conditional rendering for 'income' stream type
    if (streamType === 'income') {
      switch (streamCategory) {
        case 'salary':
          return <IncomeStreamSalaryForm />;
        case 'investment':
          // Return the investment form component once defined
          break;
        // Add more cases for other income categories
        default:
          return null;
      }
    } 
    // Example conditional rendering for 'expense' stream type
    else if (streamType === 'expense') {
      switch (streamCategory) {
        case 'mortgage':
          return <ExpenseStreamMortgageForm />;
        // Add more cases for other expense categories
        default:
          return null;
      }
    }
  };

  return (
    <div className="stream-form-container">
      <div className="stream-form-selection">
        <label>Stream Type:</label>
        <select onChange={(e) => setStreamType(e.target.value)} value={streamType}>
          <option value="income">Income</option>
          <option value="expense">Expense</option>
        </select>
      </div>

      {streamType && (
        <div className="stream-form-selection">
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
