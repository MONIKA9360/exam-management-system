import React, { useState, useEffect } from 'react';
import axios from '../api/axios';
import './Common.css';

const HallTickets = () => {
  const [hallTickets, setHallTickets] = useState([]);
  const [students, setStudents] = useState([]);
  const [exams, setExams] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [currentTicket, setCurrentTicket] = useState({
    student: '',
    exam: '',
    hall_ticket_number: ''
  });

  useEffect(() => {
    fetchHallTickets();
    fetchStudents();
    fetchExams();
  }, []);

  const fetchHallTickets = async () => {
    try {
      const response = await axios.get('/hall-tickets/');
      setHallTickets(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching hall tickets:', error);
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
      await axios.post('/hall-tickets/', currentTicket);
      alert('Hall Ticket generated successfully!');
      fetchHallTickets();
      handleCloseModal();
    } catch (error) {
      alert('Error: ' + (error.response?.data?.detail || 'Something went wrong'));
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setCurrentTicket({
      student: '',
      exam: '',
      hall_ticket_number: ''
    });
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div className="page-header-left">
          <button className="btn-back" onClick={() => window.history.back()}>← Back</button>
          <h1>Hall Tickets</h1>
        </div>
        <div className="page-header-right">
          <button className="btn-primary" onClick={() => {
            setShowModal(true);
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }}>
            + Generate Hall Ticket
          </button>
        </div>
      </div>

      {!showModal && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Hall Ticket No</th>
                <th>Student Name</th>
                <th>Register No</th>
                <th>Exam</th>
                <th>Date</th>
                <th>QR Code</th>
              </tr>
            </thead>
            <tbody>
              {hallTickets.map((ticket) => (
                <tr key={ticket.id}>
                  <td>{ticket.hall_ticket_number}</td>
                  <td>{ticket.student_name || ticket.student}</td>
                  <td>{ticket.register_no || '-'}</td>
                  <td>{ticket.exam_name || ticket.exam}</td>
                  <td>{ticket.issued_date}</td>
                  <td>
                    {ticket.qr_code && (
                      <img 
                        src={`http://127.0.0.1:8000${ticket.qr_code}`} 
                        alt="QR Code" 
                        style={{width: '50px', height: '50px'}}
                      />
                    )}
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
                value={currentTicket.student}
                onChange={(e) => setCurrentTicket({...currentTicket, student: e.target.value})}
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
                value={currentTicket.exam}
                onChange={(e) => setCurrentTicket({...currentTicket, exam: e.target.value})}
                required
              >
                <option value="">Select Exam</option>
                {exams.map((exam) => (
                  <option key={exam.id} value={exam.id}>{exam.exam_name}</option>
                ))}
              </select>
              <input
                type="text"
                placeholder="Hall Ticket Number (e.g., HT2024001)"
                value={currentTicket.hall_ticket_number}
                onChange={(e) => setCurrentTicket({...currentTicket, hall_ticket_number: e.target.value})}
                required
              />
              <div className="modal-actions">
                <button type="submit" className="btn-primary">Generate</button>
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

export default HallTickets;
