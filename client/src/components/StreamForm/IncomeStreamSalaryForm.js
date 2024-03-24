import React, { useState } from 'react';
import './IncomeStreamSalaryForm.css'; // Import the CSS styles

function IncomeStreamSalaryForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    annualIncome: '',
    personalAllowance: '',
    bonus: '',
    pensionPercentage: '',
    planType: 'Plan 1',
    isScottish: false,
    isMarried: false,
    isBlind: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    // Update form data state based on input type
    setFormData(prevData => ({
      ...prevData,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
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

      <button type="submit" className="submit-btn">Add Income Stream</button>
    </form>
  );
}

export default IncomeStreamSalaryForm;
