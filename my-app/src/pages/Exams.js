import React, { useState, useEffect } from 'react';
import axios from '../api/axios';
import './Common.css';

const Exams = () => {
  const [exams, setExams] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentExam, setCurrentExam] = useState({
    exam_name: '',
    exam_type: 'Internal',
    start_date: '',
    end_date: '',
    duration: '',
    total_marks: '',
    semester: '',
    department: ''
  });

  useEffect(() => {
    fetchExams();
    fetchDepartments();
  }, []);

  const fetchExams = async () => {
    try {
      const response = await axios.get('/exams/');
      setExams(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching exams:', error);
    }
  };

  const fetchDepartments = async () => {
    try {
      const response = await axios.get('/departments/');
      setDepartments(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching departments:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editMode) {
        await axios.put(`/exams/${currentExam.id}/`, currentExam);
        alert('Exam updated successfully!');
      } else {
        await axios.post('/exams/', currentExam);
        alert('Exam created successfully!');
      }
      fetchExams();
      handleCloseModal();
    } catch (error) {
      alert('Error: ' + (error.response?.data?.detail || 'Something went wrong'));
    }
  };

  const handleEdit = (exam) => {
    setCurrentExam(exam);
    setEditMode(true);
    setShowModal(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this exam?')) {
      try {
        await axios.delete(`/exams/${id}/`);
        alert('Exam deleted successfully!');
        fetchExams();
      } catch (error) {
        alert('Error deleting exam');
      }
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditMode(false);
    setCurrentExam({
      exam_name: '',
      exam_type: 'Internal',
      start_date: '',
      end_date: '',
      duration: '',
      total_marks: '',
      semester: '',
      department: ''
    });
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <h1>Exams Management</h1>
        <button className="btn-primary" onClick={() => {
          setShowModal(true);
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }}>
          + Add Exam
        </button>
      </div>

      {!showModal && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Exam Name</th>
                <th>Type</th>
                <th>Start Date</th>
                <th>End Date</th>
                <th>Duration</th>
                <th>Total Marks</th>
                <th>Semester</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {exams.map((exam) => (
                <tr key={exam.id}>
                  <td>{exam.exam_name}</td>
                  <td>{exam.exam_type}</td>
                  <td>{exam.start_date}</td>
                  <td>{exam.end_date}</td>
                  <td>{exam.duration}</td>
                  <td>{exam.total_marks}</td>
                  <td>{exam.semester}</td>
                  <td>
                    <button className="btn-edit" onClick={() => handleEdit(exam)}>Edit</button>
                    <button className="btn-delete" onClick={() => handleDelete(exam.id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <form onSubmit={handleSubmit}>
              <input
                type="text"
                placeholder="Exam Name"
                value={currentExam.exam_name}
                onChange={(e) => setCurrentExam({...currentExam, exam_name: e.target.value})}
                required
              />
              <select
                value={currentExam.exam_type}
                onChange={(e) => setCurrentExam({...currentExam, exam_type: e.target.value})}
                required
              >
                <option value="Internal">Internal</option>
                <option value="Model">Model</option>
                <option value="Semester">Semester</option>
              </select>
              <input
                type="date"
                placeholder="Start Date"
                value={currentExam.start_date}
                onChange={(e) => setCurrentExam({...currentExam, start_date: e.target.value})}
                required
              />
              <input
                type="date"
                placeholder="End Date"
                value={currentExam.end_date}
                onChange={(e) => setCurrentExam({...currentExam, end_date: e.target.value})}
                required
              />
              <input
                type="number"
                placeholder="Duration (minutes)"
                value={currentExam.duration}
                onChange={(e) => setCurrentExam({...currentExam, duration: e.target.value})}
                required
              />
              <input
                type="number"
                placeholder="Total Marks"
                value={currentExam.total_marks}
                onChange={(e) => setCurrentExam({...currentExam, total_marks: e.target.value})}
                required
              />
              <select
                value={currentExam.semester}
                onChange={(e) => setCurrentExam({...currentExam, semester: e.target.value})}
                required
              >
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
              <select
                value={currentExam.department}
                onChange={(e) => setCurrentExam({...currentExam, department: e.target.value})}
                required
              >
                <option value="">Select Department</option>
                {departments.map((dept) => (
                  <option key={dept.id} value={dept.id}>{dept.department_name}</option>
                ))}
              </select>
              <div className="modal-actions">
                <button type="submit" className="btn-primary">
                  {editMode ? 'Update' : 'Create'}
                </button>
                <button type="button" className="btn-secondary" onClick={handleCloseModal}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Exams;
