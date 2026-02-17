import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api/axios';
import './Common.css';

function Students() {
  const [students, setStudents] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    student_id: '',
    full_name: '',
    register_no: '',
    department: '',
    year: '',
    semester: '',
    email: '',
    phone: '',
    address: '',
    status: 'active'
  });
  const [editId, setEditId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchStudents();
    fetchDepartments();
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await API.get('/students/');
      setStudents(response.data.results || response.data);
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
        await API.put(`/students/${editId}/`, formData);
      } else {
        await API.post('/students/', formData);
      }
      setShowForm(false);
      setFormData({
        student_id: '', full_name: '', register_no: '', department: '',
        year: '', semester: '', email: '', phone: '', address: '', status: 'active'
      });
      setEditId(null);
      fetchStudents();
    } catch (err) {
      alert(err.response?.data?.message || 'Operation failed');
    }
  };

  const handleEdit = (student) => {
    setFormData({
      student_id: student.student_id,
      full_name: student.full_name,
      register_no: student.register_no,
      department: student.department,
      year: student.year,
      semester: student.semester,
      email: student.email,
      phone: student.phone,
      address: student.address,
      status: student.status
    });
    setEditId(student.id);
    setShowForm(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure?')) {
      try {
        await API.delete(`/students/${id}/`);
        fetchStudents();
      } catch (err) {
        alert('Delete failed');
      }
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <button onClick={() => navigate('/dashboard')}>← Back</button>
        <h1>Students</h1>
        <button onClick={() => {
          setShowForm(!showForm);
          if (!showForm) window.scrollTo({ top: 0, behavior: 'smooth' });
        }}>
          {showForm ? 'Cancel' : '+ Add Student'}
        </button>
      </div>

      {showForm && (
        <div className="form-card">
          <form onSubmit={handleSubmit}>
            <input type="text" placeholder="Student ID" value={formData.student_id}
              onChange={(e) => setFormData({...formData, student_id: e.target.value})} required />
            <input type="text" placeholder="Full Name" value={formData.full_name}
              onChange={(e) => setFormData({...formData, full_name: e.target.value})} required />
            <input type="text" placeholder="Register No" value={formData.register_no}
              onChange={(e) => setFormData({...formData, register_no: e.target.value})} required />
            <select value={formData.department}
              onChange={(e) => setFormData({...formData, department: e.target.value})} required>
              <option value="">Select Department</option>
              {departments.map(dept => (
                <option key={dept.id} value={dept.id}>{dept.department_name}</option>
              ))}
            </select>
            <select value={formData.year}
              onChange={(e) => setFormData({...formData, year: e.target.value})} required>
              <option value="">Select Year</option>
              <option value="1">I</option>
              <option value="2">II</option>
              <option value="3">III</option>
              <option value="4">IV</option>
            </select>
            <select value={formData.semester}
              onChange={(e) => setFormData({...formData, semester: e.target.value})} required>
              <option value="">Select Semester</option>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
              <option value="6">6</option>
              <option value="7">7</option>
              <option value="8">8</option>
            </select>
            <input type="email" placeholder="Email" value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})} required />
            <input type="tel" placeholder="Phone" value={formData.phone}
              onChange={(e) => setFormData({...formData, phone: e.target.value})} required />
            <textarea placeholder="Address" value={formData.address}
              onChange={(e) => setFormData({...formData, address: e.target.value})} required />
            <select value={formData.status}
              onChange={(e) => setFormData({...formData, status: e.target.value})}>
              <option value="active">Active</option>
              <option value="inactive">Inactive</option>
            </select>
            <button type="submit">{editId ? 'Update' : 'Create'}</button>
          </form>
        </div>
      )}

      {!showForm && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Student ID</th>
                <th>Name</th>
                <th>Register No</th>
                <th>Department</th>
                <th>Semester</th>
                <th>Email</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {students.map((student) => (
                <tr key={student.id}>
                  <td>{student.student_id}</td>
                  <td>{student.full_name}</td>
                  <td>{student.register_no}</td>
                  <td>{student.department_name}</td>
                  <td>{student.semester}</td>
                  <td>{student.email}</td>
                  <td>
                    <button onClick={() => handleEdit(student)} className="btn-edit">Edit</button>
                    <button onClick={() => handleDelete(student.id)} className="btn-delete">Delete</button>
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

export default Students;
