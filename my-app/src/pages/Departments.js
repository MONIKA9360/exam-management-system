import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api/axios';
import Breadcrumb from '../components/Breadcrumb';
import Toast from '../components/Toast';
import './Common.css';

function Departments() {
  const [departments, setDepartments] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [toast, setToast] = useState(null);
  const [formData, setFormData] = useState({
    department_name: '',
    department_code: '',
    hod: '',
    description: ''
  });
  const [editId, setEditId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDepartments();
  }, []);

  const fetchDepartments = async () => {
    try {
      const response = await API.get('/departments/');
      setDepartments(response.data.results || response.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editId) {
        await API.put(`/departments/${editId}/`, formData);
        setToast({ message: 'Department updated successfully!', type: 'success' });
      } else {
        await API.post('/departments/', formData);
        setToast({ message: 'Department added successfully!', type: 'success' });
      }
      setShowForm(false);
      setFormData({ department_name: '', department_code: '', hod: '', description: '' });
      setEditId(null);
      fetchDepartments();
    } catch (err) {
      if (err.response?.status === 400) {
        setToast({ message: 'Department already exists or invalid data!', type: 'warning' });
      } else {
        setToast({ message: err.response?.data?.message || 'Operation failed', type: 'error' });
      }
    }
  };

  const handleEdit = (dept) => {
    setFormData({
      department_name: dept.department_name,
      department_code: dept.department_code,
      hod: dept.hod || '',
      description: dept.description || ''
    });
    setEditId(dept.id);
    setShowForm(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure?')) {
      try {
        await API.delete(`/departments/${id}/`);
        setToast({ message: 'Department deleted successfully!', type: 'success' });
        fetchDepartments();
      } catch (err) {
        setToast({ message: 'Delete failed', type: 'error' });
      }
    }
  };

  return (
    <div className="page-container">
      {toast && (
        <Toast 
          message={toast.message} 
          type={toast.type} 
          onClose={() => setToast(null)} 
        />
      )}

      <Breadcrumb items={[
        { label: 'Dashboard', path: '/dashboard' },
        { label: 'Departments' }
      ]} />

      <div className="page-header">
        <button onClick={() => navigate('/dashboard')}>← Back</button>
        <h1>Departments</h1>
        <button onClick={() => {
          setShowForm(!showForm);
          if (!showForm) window.scrollTo({ top: 0, behavior: 'smooth' });
        }}>
          {showForm ? 'Cancel' : '+ Add Department'}
        </button>
      </div>

      {showForm && (
        <div className="form-card">
          <form onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Department Name"
              value={formData.department_name}
              onChange={(e) => setFormData({...formData, department_name: e.target.value})}
              required
            />
            <input
              type="text"
              placeholder="Department Code"
              value={formData.department_code}
              onChange={(e) => setFormData({...formData, department_code: e.target.value})}
              required
            />
            <input
              type="text"
              placeholder="HOD Name"
              value={formData.hod}
              onChange={(e) => setFormData({...formData, hod: e.target.value})}
            />
            <textarea
              placeholder="Description"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
            />
            <button type="submit">{editId ? 'Update' : 'Create'}</button>
          </form>
        </div>
      )}

      {!showForm && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Department Code</th>
                <th>Department Name</th>
                <th>HOD</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {departments.map((dept) => (
                <tr key={dept.id}>
                  <td>{dept.department_code}</td>
                  <td>{dept.department_name}</td>
                  <td>{dept.hod || '-'}</td>
                  <td>
                    <button onClick={() => handleEdit(dept)} className="btn-edit">Edit</button>
                    <button onClick={() => handleDelete(dept.id)} className="btn-delete">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Departments;
