import React, { useState, useEffect } from 'react';
import axios from '../api/axios';
import './Common.css';

const Marks = () => {
  const [marks, setMarks] = useState([]);
  const [students, setStudents] = useState([]);
  const [courses, setCourses] = useState([]);
  const [exams, setExams] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentMark, setCurrentMark] = useState({
    student: '',
    subject: '',
    exam: '',
    internal_marks: '',
    external_marks: '',
    remarks: ''
  });

  useEffect(() => {
    fetchMarks();
    fetchStudents();
    fetchCourses();
    fetchExams();
  }, []);

  const fetchMarks = async () => {
    try {
      const response = await axios.get('/marks/');
      setMarks(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching marks:', error);
    }
  };

  const fetchStudents = async () => {
    try {
      const response = await axios.get('/students/');
      setStudents(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching students:', error);
    }
  };

  const fetchCourses = async () => {
    try {
      const response = await axios.get('/courses/');
      setCourses(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  };

  const fetchExams = async () => {
    try {
      const response = await axios.get('/exams/');
      setExams(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching exams:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editMode) {
        await axios.put(`/marks/${currentMark.id}/`, currentMark);
        alert('Marks updated successfully!');
      } else {
        await axios.post('/marks/', currentMark);
        alert('Marks entered successfully!');
      }
      fetchMarks();
      handleCloseModal();
    } catch (error) {
      alert('Error: ' + (error.response?.data?.detail || 'Something went wrong'));
    }
  };

  const handleEdit = (mark) => {
    setCurrentMark(mark);
    setEditMode(true);
    setShowModal(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this mark entry?')) {
      try {
        await axios.delete(`/marks/${id}/`);
        alert('Mark entry deleted successfully!');
        fetchMarks();
      } catch (error) {
        alert('Error deleting mark entry');
      }
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditMode(false);
    setCurrentMark({
      student: '',
      subject: '',
      exam: '',
      internal_marks: '',
      external_marks: '',
      remarks: ''
    });
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div className="page-header-left">
          <button className="btn-back" onClick={() => window.history.back()}>← Back</button>
          <h1>Marks Entry</h1>
        </div>
        <div className="page-header-right">
          <button className="btn-primary" onClick={() => {
            setShowModal(true);
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }}>
            + Add Marks
          </button>
        </div>
      </div>

      {!showModal && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Student</th>
                <th>Subject</th>
                <th>Exam</th>
                <th>Internal</th>
                <th>External</th>
                <th>Total</th>
                <th>Grade</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {marks.map((mark) => (
                <tr key={mark.id}>
                  <td>{mark.student_name || mark.student}</td>
                  <td>{mark.subject_name || mark.subject}</td>
                  <td>{mark.exam_name || mark.exam}</td>
                  <td>{mark.internal_marks}</td>
                  <td>{mark.external_marks}</td>
                  <td>{mark.total_marks}</td>
                  <td>{mark.grade}</td>
                  <td>
                    <button className="btn-edit" onClick={() => handleEdit(mark)}>Edit</button>
                    <button className="btn-delete" onClick={() => handleDelete(mark.id)}>Delete</button>
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
              <select
                value={currentMark.student}
                onChange={(e) => setCurrentMark({...currentMark, student: e.target.value})}
                required
              >
                <option value="">Select Student</option>
                {students.map((student) => (
                  <option key={student.id} value={student.id}>
                    {student.full_name} ({student.register_no})
                  </option>
                ))}
              </select>
              <select
                value={currentMark.subject}
                onChange={(e) => setCurrentMark({...currentMark, subject: e.target.value})}
                required
              >
                <option value="">Select Subject</option>
                {courses.map((course) => (
                  <option key={course.id} value={course.id}>{course.course_name}</option>
                ))}
              </select>
              <select
                value={currentMark.exam}
                onChange={(e) => setCurrentMark({...currentMark, exam: e.target.value})}
                required
              >
                <option value="">Select Exam</option>
                {exams.map((exam) => (
                  <option key={exam.id} value={exam.id}>{exam.exam_name}</option>
                ))}
              </select>
              <input
                type="number"
                placeholder="Internal Marks"
                value={currentMark.internal_marks}
                onChange={(e) => setCurrentMark({...currentMark, internal_marks: e.target.value})}
                min="0"
                required
              />
              <input
                type="number"
                placeholder="External Marks"
                value={currentMark.external_marks}
                onChange={(e) => setCurrentMark({...currentMark, external_marks: e.target.value})}
                min="0"
                required
              />
              <textarea
                placeholder="Remarks (optional)"
                value={currentMark.remarks}
                onChange={(e) => setCurrentMark({...currentMark, remarks: e.target.value})}
                rows="3"
              />
              <div className="modal-actions">
                <button type="submit" className="btn-primary">
                  {editMode ? 'Update' : 'Submit'}
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

export default Marks;
