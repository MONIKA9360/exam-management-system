import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api/axios';
import './Common.css';

function Staff() {
  const [staff, setStaff] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    staff_id: '',
    name: '',
    email: '',
    phone: '',
    department: '',
    designation: '',
    qualification: ''
  });
  const [editId, setEditId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchStaff();
    fetchDepartments();
  }, []);

  const fetchStaff = async () => {
    try {
      const response = await API.get('/staff/');
      setStaff(response.data.results || response.data);
    } catch (err) {
      console.error(err);
    }
  };

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
        await API.put(`/staff/${editId}/`, formData);
      } else {
        await API.post('/staff/', formData);
      }
      setShowForm(false);
      setFormData({ staff_id: '', name: '', email: '', phone: '', department: '', designation: '', qualification: '' });
      setEditId(null);
      fetchStaff();
    } catch (err) {
      alert(err.response?.data?.message || 'Operation failed');
    }
  };

  const handleEdit = (staffMember) => {
    setFormData({
      staff_id: staffMember.staff_id,
      name: staffMember.name,
      email: staffMember.email,
      phone: staffMember.phone,
      department: staffMember.department,
      designation: staffMember.designation,
      qualification: staffMember.qualification
    });
    setEditId(staffMember.id);
    setShowForm(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure?')) {
      try {
        await API.delete(`/staff/${id}/`);
        fetchStaff();
      } catch (err) {
        alert('Delete failed');
      }
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <button onClick={() => navigate('/dashboard')}>← Back</button>
        <h1>Staff</h1>
        <button onClick={() => {
          setShowForm(!showForm);
          if (!showForm) window.scrollTo({ top: 0, behavior: 'smooth' });
        }}>
          {showForm ? 'Cancel' : '+ Add Staff'}
        </button>
      </div>

      {showForm && (
        <div className="form-card">
          <form onSubmit={handleSubmit}>
            <input type="text" placeholder="Staff ID" value={formData.staff_id}
              onChange={(e) => setFormData({...formData, staff_id: e.target.value})} required />
            <input type="text" placeholder="Name" value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})} required />
            <input type="email" placeholder="Email" value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})} required />
            <input type="tel" placeholder="Phone" value={formData.phone}
              onChange={(e) => setFormData({...formData, phone: e.target.value})} required />
            <select value={formData.department}
              onChange={(e) => setFormData({...formData, department: e.target.value})} required>
              <option value="">Select Department</option>
              {departments.map(dept => (
                <option key={dept.id} value={dept.id}>{dept.department_name}</option>
              ))}
            </select>
            <input type="text" placeholder="Designation" value={formData.designation}
              onChange={(e) => setFormData({...formData, designation: e.target.value})} required />
            <input type="text" placeholder="Qualification" value={formData.qualification}
              onChange={(e) => setFormData({...formData, qualification: e.target.value})} required />
            <button type="submit">{editId ? 'Update' : 'Create'}</button>
          </form>
        </div>
      )}

      {!showForm && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Staff ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Department</th>
                <th>Designation</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {staff.map((staffMember) => (
                <tr key={staffMember.id}>
                  <td>{staffMember.staff_id}</td>
                  <td>{staffMember.name}</td>
                  <td>{staffMember.email}</td>
                  <td>{staffMember.department_name}</td>
                  <td>{staffMember.designation}</td>
                  <td>
                    <button onClick={() => handleEdit(staffMember)} className="btn-edit">Edit</button>
                    <button onClick={() => handleDelete(staffMember.id)} className="btn-delete">Delete</button>
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

export default Staff;
