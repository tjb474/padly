import React, { useState } from 'react';
import './IncomeStreamSalaryForm.css'; // Import the CSS styles

function IncomeStreamSalaryForm() {
  const [formData, setFormData] = useState({
    annualIncome: '',
    personalAllowance: '',
    bonus: '',
    pensionPercentage: '',
    planType: 'Plan 1',
    isScottish: false,
    isMarried: false,
    isBlind: false,
    startDate: '',
    endDate: ''
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Assuming your Flask API is running on localhost:5000
    const API_URL = 'http://localhost:5000/add_stream';


    const payload = {
      ...formData,
      user_id: 'user123', // This should be dynamically set based on your application's user context
      stream_type: 'income',
      annual_income: formData.annualIncome,
      personal_allowance: formData.personalAllowance,
      bonus: formData.bonus,
      pension_percentage: formData.pensionPercentage,
      plan_type: formData.planType,
      is_scottish: formData.isScottish,
      is_married: formData.isMarried,
      is_blind: formData.isBlind,
      start_date_str: formData.startDate, // Map startDate to start_date_str
      end_date_str: formData.endDate, // Map endDate to end_date_str
    };

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();
      console.log('Stream added successfully:', result);

      // Optionally, clear the form or provide feedback to the user
    } catch (error) {
      console.error('Error adding stream:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="income-stream-form">
      <div className="form-field">
        <label htmlFor="annualIncome">Annual Income:</label>
        <input
          type="number"
          id="annualIncome"
          name="annualIncome"
          placeholder="e.g. 50000"
          value={formData.annualIncome}
          onChange={handleChange}
        />
      </div>

      <div className="form-field">
        <label htmlFor="personalAllowance">Personal Allowance:</label>
        <input
          type="number"
          id="personalAllowance"
          name="personalAllowance"
          placeholder="e.g. 12570 (optional)"
          value={formData.personalAllowance}
          onChange={handleChange}
        />
      </div>

      <div className="form-field">
        <label htmlFor="bonus">Bonus:</label>
        <input
          type="number"
          id="bonus"
          name="bonus"
          placeholder="e.g.10000 (optional)"
          value={formData.bonus}
          onChange={handleChange}
        />
      </div>

      <div className="form-field">
        <label htmlFor="pensionPercentage">Pension Contribution Percentage:</label>
        <input
          type="number"
          id="pensionPercentage"
          name="pensionPercentage"
          placeholder="e.g. 5 (optional)"
          value={formData.pensionPercentage}
          onChange={handleChange}
        />
      </div>

      <div className="form-field">
        <label htmlFor="planType">Student Loan Plan Type:</label>
        <select id="planType" name="planType" value={formData.planType} onChange={handleChange}>
          <option value="Plan 1">Plan 1</option>
          <option value="Plan 2">Plan 2</option>
          {/* Add other plan types as options */}
        </select>
      </div>

      <div className="form-field checkbox">
        <label>
          <input
            type="checkbox"
            name="isScottish"
            checked={formData.isScottish}
            onChange={handleChange}
          />
          Is Scottish?
        </label>
      </div>

      <div className="form-field checkbox">
        <label>
          <input
            type="checkbox"
            name="isMarried"
            checked={formData.isMarried}
            onChange={handleChange}
          />
          Is Married?
        </label>
      </div>

      <div className="form-field checkbox">
        <label>
          <input
            type="checkbox"
            name="isBlind"
            checked={formData.isBlind}
            onChange={handleChange}
          />
          Is Blind?
        </label>
      </div>
      
      <div className="form-field">
        <label htmlFor="startDate">Start Date:</label>
        <input
          type="date"
          id="startDate"
          name="startDate"
          value={formData.startDate}
          onChange={handleChange}
        />
      </div>

      {/* End Date field */}
      <div className="form-field">
        <label htmlFor="endDate">End Date:</label>
        <input
          type="date"
          id="endDate"
          name="endDate"
          value={formData.endDate}
          onChange={handleChange}
        />
      </div>

      <button type="submit" className="submit-btn">Add Income Stream</button>
    </form>
  );
}

export default IncomeStreamSalaryForm;
