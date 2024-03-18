// Import necessary React libraries and components
import React, { useState } from 'react';
import IncomeForm from './IncomeForm'; // Importing the IncomeForm component for user input
import IncomeTable from './IncomeTable'; // Importing the IncomeTable component for displaying the table
import './App.css'; // Importing CSS styles for the app

function App() {
  // State to store the income breakdown after form submission
  const [incomeBreakdown, setIncomeBreakdown] = useState(null);

  // This function is called when the form in IncomeForm component is submitted
  const handleFormSubmit = (formData) => {
    console.log(formData); // Log the form data for debugging purposes
    
    // Simulate receiving calculation results from a backend
    // In a real app, you'd make an API call here to get the actual results
    const result = {
      "Gross Income": formData.annualIncome,
      "Pension Contributions": formData.pensionPercentage,
      "Income Tax": "Calculated Value", // Placeholder values for demonstration
      "NI Contributions": "Calculated Value",
      "Student Loan": "Calculated Value",
      "Net Income": "Calculated Value",
    };
    // Update the state with the simulated result
    setIncomeBreakdown(result);
  };

  // Define the columns for the React Table component
  // useMemo is used here to ensure these values are computed once and only recalculated if dependencies change
  const columns = React.useMemo(
    () => [
      {
        Header: 'Category', // Column header
        accessor: 'category', // Accessor matches the key in the data object
      },
      {
        Header: 'Amount', // Column header
        accessor: 'amount', // Accessor matches the key in the data object
      },
    ],
    [] // Empty dependency array means this useMemo hook runs only once when the component mounts
  );

  // Define the data for the React Table component
  // This is placeholder data for demonstration. You can later modify it to use dynamic data from form submission or backend response
  const data = React.useMemo(
    () => [
      {
        category: 'Gross Income', // Category name
        amount: 'Placeholder Amount', // Placeholder amount value
      },
      // You can add more rows here as needed
    ],
    [] // Empty dependency array means this useMemo hook runs only once when the component mounts
  );

  // Render the app UI
  return (
    <div className="App">
      <h1>Income Calculator</h1> {/* Title of the app */}
      {/* IncomeForm component for user inputs. It receives the handleFormSubmit function as a prop */}
      <IncomeForm onSubmit={handleFormSubmit} />
      {/* Conditional rendering: If incomeBreakdown is not null, render a div containing a table of the breakdown */}
      {incomeBreakdown && (
        <div>
          <h2>Income Breakdown</h2> {/* Subtitle for the breakdown section */}
          <table>
            <tbody>
              {/* Mapping through each entry in incomeBreakdown to create table rows */}
              {Object.entries(incomeBreakdown).map(([key, value]) => (
                <tr key={key}>
                  <td>{key}</td> {/* Table cell for the category name */}
                  <td>{value}</td> {/* Table cell for the category value */}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {/* IncomeTable component for displaying the data in a table */}
      <IncomeTable columns={columns} data={data} />
    </div>
  );
}

export default App; // Export the App component for use in other parts of the app
