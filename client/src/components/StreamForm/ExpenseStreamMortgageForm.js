import React, { useState } from 'react';
import './ExpenseStreamMortgageForm.css'; // Import the CSS styles

function ExpenseStreamMortgageForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    streamType: 'expense',
    principal: '',
    annualInterestRate: '',
    years: '',
    startDateStr: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prevData => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="expense-stream-form">
      <div className="form-field">
        <label htmlFor="principal">Principal Amount:</label>
        <input
          type="number"
          id="principal"
          name="principal"
          value={formData.principal}
          onChange={handleChange}
          required
          placeholder="e.g. 250000"
        />
      </div>
      <div className="form-field">
        <label htmlFor="annualInterestRate">Annual Interest Rate (%):</label>
        <input
          type="number"
          id="annualInterestRate"
          name="annualInterestRate"
          step="0.01"
          value={formData.annualInterestRate}
          onChange={handleChange}
          required
          placeholder="e.g. 5"
        />
      </div>
      <div className="form-field">
        <label htmlFor="years">Loan Term (Years):</label>
        <input
          type="number"
          id="years"
          name="years"
          value={formData.years}
          onChange={handleChange}
          required
          placeholder="e.g. 25"
        />
      </div>
      <div className="form-field">
        <label htmlFor="startDateStr">Start Date:</label>
        <input
          type="text"
          id="startDateStr"
          name="startDateStr"
          value={formData.startDateStr}
          onChange={handleChange}
          required
          placeholder="e.g. 01-01-2024 (dd-mm-yyyy)"
          pattern="\d{2}-\d{2}-\d{4}"
          title="Enter a date in DD-MM-YYYY format."
        />
      </div>
      <button type="submit" className="submit-btn">Add Expense Stream</button>
    </form>
  );
}

export default ExpenseStreamMortgageForm;
