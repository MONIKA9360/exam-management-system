import React, { useState, useEffect } from 'react';
import axios from '../api/axios';
import './Common.css';

const ExamSchedules = () => {
  const [schedules, setSchedules] = useState([]);
  const [exams, setExams] = useState([]);
  const [courses, setCourses] = useState([]);
  const [staff, setStaff] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentSchedule, setCurrentSchedule] = useState({
    exam: '',
    subject: '',
    date: '',
    start_time: '',
    end_time: '',
    hall_number: '',
    invigilator: ''
  });

  useEffect(() => {
    fetchSchedules();
    fetchExams();
    fetchCourses();
    fetchStaff();
  }, []);

  const fetchSchedules = async () => {
    try {
      const response = await axios.get('/exam-schedules/');
      setSchedules(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching schedules:', error);
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

  const fetchCourses = async () => {
    try {
      const response = await axios.get('/courses/');
      setCourses(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching courses:', error);
    }
  };

  const fetchStaff = async () => {
    try {
      const response = await axios.get('/staff/');
      setStaff(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching staff:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editMode) {
        await axios.put(`/exam-schedules/${currentSchedule.id}/`, currentSchedule);
        alert('Schedule updated successfully!');
      } else {
        await axios.post('/exam-schedules/', currentSchedule);
        alert('Schedule created successfully!');
      }
      fetchSchedules();
      handleCloseModal();
    } catch (error) {
      alert('Error: ' + (error.response?.data?.detail || 'Something went wrong'));
    }
  };

  const handleEdit = (schedule) => {
    setCurrentSchedule(schedule);
    setEditMode(true);
    setShowModal(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this schedule?')) {
      try {
        await axios.delete(`/exam-schedules/${id}/`);
        alert('Schedule deleted successfully!');
        fetchSchedules();
      } catch (error) {
        alert('Error deleting schedule');
      }
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditMode(false);
    setCurrentSchedule({
      exam: '',
      subject: '',
      date: '',
      start_time: '',
      end_time: '',
      hall_number: '',
      invigilator: ''
    });
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div className="page-header-left">
          <button className="btn-back" onClick={() => window.history.back()}>← Back</button>
          <h1>Exam Schedules</h1>
        </div>
        <div className="page-header-right">
          <button className="btn-primary" onClick={() => {
            setShowModal(true);
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }}>
            + Add Schedule
          </button>
        </div>
      </div>

      {!showModal && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Exam</th>
                <th>Subject</th>
                <th>Date</th>
                <th>Start Time</th>
                <th>End Time</th>
                <th>Hall</th>
                <th>Invigilator</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {schedules.map((schedule) => (
                <tr key={schedule.id}>
                  <td>{schedule.exam_name || schedule.exam}</td>
                  <td>{schedule.subject_name || schedule.subject}</td>
                  <td>{schedule.date}</td>
                  <td>{schedule.start_time}</td>
                  <td>{schedule.end_time}</td>
                  <td>{schedule.hall_number}</td>
                  <td>{schedule.invigilator_name || schedule.invigilator}</td>
                  <td>
                    <button className="btn-edit" onClick={() => handleEdit(schedule)}>Edit</button>
                    <button className="btn-delete" onClick={() => handleDelete(schedule.id)}>Delete</button>
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
                value={currentSchedule.exam}
                onChange={(e) => setCurrentSchedule({...currentSchedule, exam: e.target.value})}
                required
              >
                <option value="">Select Exam</option>
                {exams.map((exam) => (
                  <option key={exam.id} value={exam.id}>{exam.exam_name}</option>
                ))}
              </select>
              <select
                value={currentSchedule.subject}
                onChange={(e) => setCurrentSchedule({...currentSchedule, subject: e.target.value})}
                required
              >
                <option value="">Select Subject</option>
                {courses.map((course) => (
                  <option key={course.id} value={course.id}>{course.course_name}</option>
                ))}
              </select>
              <input
                type="date"
                placeholder="Date"
                value={currentSchedule.date}
                onChange={(e) => setCurrentSchedule({...currentSchedule, date: e.target.value})}
                required
              />
              <input
                type="time"
                placeholder="Start Time"
                value={currentSchedule.start_time}
                onChange={(e) => setCurrentSchedule({...currentSchedule, start_time: e.target.value})}
                required
              />
              <input
                type="time"
                placeholder="End Time"
                value={currentSchedule.end_time}
                onChange={(e) => setCurrentSchedule({...currentSchedule, end_time: e.target.value})}
                required
              />
              <input
                type="text"
                placeholder="Hall Number"
                value={currentSchedule.hall_number}
                onChange={(e) => setCurrentSchedule({...currentSchedule, hall_number: e.target.value})}
                required
              />
              <select
                value={currentSchedule.invigilator}
                onChange={(e) => setCurrentSchedule({...currentSchedule, invigilator: e.target.value})}
                required
              >
                <option value="">Select Invigilator</option>
                {staff.map((s) => (
                  <option key={s.id} value={s.id}>{s.name}</option>
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

export default ExamSchedules;
