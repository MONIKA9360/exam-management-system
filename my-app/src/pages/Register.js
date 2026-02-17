import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api/axios';
import './Auth.css';

function Register() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    role: 'Admin'  // Always Admin
  });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await API.post('/auth/register/', formData);
      alert('Registration successful! Please login.');
      navigate('/login');
    } catch (err) {
      console.error('Registration error:', err.response?.data);
      const errorMsg = err.response?.data?.message || 
                       err.response?.data?.errors?.email?.[0] || 
                       err.response?.data?.errors?.username?.[0] ||
                       'Registration failed';
      setError(errorMsg);
    }
  };

  return (
    <div className="register-container">
      <h1 className="register-title">Exam Management System</h1>
      <div className="register-box">
        <h2>Register</h2>
        {error && <div className="error" style={{color: 'red', marginBottom: '15px'}}>{error}</div>}
        <form onSubmit={handleRegister}>
          <input
            type="text"
            placeholder="Username"
            value={formData.username}
            onChange={(e) => setFormData({...formData, username: e.target.value})}
            autoComplete="off"
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={formData.email}
            onChange={(e) => setFormData({...formData, email: e.target.value})}
            autoComplete="off"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={formData.password}
            onChange={(e) => setFormData({...formData, password: e.target.value})}
            autoComplete="new-password"
            required
          />
          <button type="submit">Register</button>
        </form>
        <p>
          Already have an account? <a href="/login">Login</a>
        </p>
      </div>
    </div>
  );
}

export default Register;
