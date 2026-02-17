import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api/axios';
import './Common.css';

function Courses() {
  const [courses, setCourses] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [staff, setStaff] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    course_code: '',
    course_name: '',
    department: '',
    credits: '',
    semester: '',
    assigned_faculty: ''
  });
  const [editId, setEditId] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCourses();
    fetchDepartments();
    fetchStaff();
  }, []);

  const fetchCourses = async () => {
    try {
      const response = await API.get('/courses/');
      setCourses(response.data.results || response.data);
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

  const fetchStaff = async () => {
    try {
      const response = await API.get('/staff/');
      setStaff(response.data.results || response.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editId) {
        await API.put(`/courses/${editId}/`, formData);
        alert('Course updated successfully!');
      } else {
        await API.post('/courses/', formData);
        alert('Course created successfully!');
      }
      setShowForm(false);
      setFormData({ course_code: '', course_name: '', department: '', credits: '', semester: '', assigned_faculty: '' });
      setEditId(null);
      fetchCourses();
    } catch (err) {
      const errorMsg = err.response?.data?.errors 
        ? JSON.stringify(err.response.data.errors) 
        : err.response?.data?.message || 'Operation failed';
      alert('Error: ' + errorMsg);
      console.error('Full error:', err.response?.data);
    }
  };

  const handleEdit = (course) => {
    setFormData({
      course_code: course.course_code,
      course_name: course.course_name,
      department: course.department,
      credits: course.credits,
      semester: course.semester,
      assigned_faculty: course.assigned_faculty || ''
    });
    setEditId(course.id);
    setShowForm(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure?')) {
      try {
        await API.delete(`/courses/${id}/`);
        fetchCourses();
      } catch (err) {
        alert('Delete failed');
      }
    }
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div className="page-header-left">
          <button className="btn-back" onClick={() => navigate('/dashboard')}>← Back</button>
          <h1>Courses</h1>
        </div>
        <div className="page-header-right">
          <button onClick={() => {
            setShowForm(!showForm);
            if (!showForm) window.scrollTo({ top: 0, behavior: 'smooth' });
          }}>
            {showForm ? 'Cancel' : '+ Add Course'}
          </button>
        </div>
      </div>

      {showForm && (
        <div className="form-card">
          <form onSubmit={handleSubmit}>
            <input type="text" placeholder="Course Code" value={formData.course_code}
              onChange={(e) => setFormData({...formData, course_code: e.target.value})} required />
            <input type="text" placeholder="Course Name" value={formData.course_name}
              onChange={(e) => setFormData({...formData, course_name: e.target.value})} required />
            <select value={formData.department}
              onChange={(e) => setFormData({...formData, department: e.target.value})} required>
              <option value="">Select Department</option>
              {departments.map(dept => (
                <option key={dept.id} value={dept.id}>{dept.department_name}</option>
              ))}
            </select>
            <input type="number" placeholder="Credits" value={formData.credits}
              onChange={(e) => setFormData({...formData, credits: e.target.value})} required />
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
            <select value={formData.assigned_faculty}
              onChange={(e) => setFormData({...formData, assigned_faculty: e.target.value})}>
              <option value="">Select Faculty (Optional)</option>
              {staff.map(s => (
                <option key={s.id} value={s.id}>{s.name}</option>
              ))}
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
                <th>Course Code</th>
                <th>Course Name</th>
                <th>Department</th>
                <th>Credits</th>
                <th>Semester</th>
                <th>Faculty</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {courses.map((course) => (
                <tr key={course.id}>
                  <td>{course.course_code}</td>
                  <td>{course.course_name}</td>
                  <td>{course.department_name}</td>
                  <td>{course.credits}</td>
                  <td>{course.semester}</td>
                  <td>{course.faculty_name || '-'}</td>
                  <td>
                    <button onClick={() => handleEdit(course)} className="btn-edit">Edit</button>
                    <button onClick={() => handleDelete(course.id)} className="btn-delete">Delete</button>
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

export default Courses;
