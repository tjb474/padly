// client/src/IncomeForm.js
import React, { useState } from 'react';

function IncomeForm({ onSubmit }) {
    const [formData, setFormData] = useState({
      annualIncome: '',
      bonus: '',
      pensionPercentage: '',
      planType: 'Plan 1', // Default value
    });
  
    const handleChange = (e) => {
      const { name, value } = e.target;
      setFormData(prevFormData => ({
        ...prevFormData,
        [name]: value
      }));
    };
  
    // This async function handles the form submission event.
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
        const response = await fetch('/calculate', { // Assuming your Flask backend and React frontend are running on the same server during development.
            method: 'POST',
            headers: {
            'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData),
        });
        const data = await response.json();
        // Do something with the response data, like storing it in a state or displaying it on the page.
        console.log(data); // For now, we just log it to the console.
        } catch (error) {
        console.error('Error:', error);
        }
    };
  
    return (
      <form onSubmit={handleSubmit}>
        <label>
          Annual Income:
          <input type="number" name="annualIncome" value={formData.annualIncome} onChange={handleChange} required />
        </label><br />
        <label>
          Bonus:
          <input type="number" name="bonus" value={formData.bonus} onChange={handleChange} />
        </label><br />
        <label>
          Pension Contributions (%):
          <input type="number" name="pensionPercentage" value={formData.pensionPercentage} onChange={handleChange} />
        </label><br />
        <label>
          Plan Type:
          <select name="planType" value={formData.planType} onChange={handleChange}>
            <option value="Plan 1">Plan 1</option>
            <option value="Plan 2">Plan 2</option>
            <option value="Plan 4">Plan 4</option>
          </select>
        </label><br />
        <button type="submit">Calculate</button>
      </form>
    );
  }
  
  export default IncomeForm;
