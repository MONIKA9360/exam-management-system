import React, { useState, useEffect } from 'react';
import axios from '../api/axios';
import Toast from '../components/Toast';
import './Common.css';

const Results = () => {
  const [results, setResults] = useState([]);
  const [filteredResults, setFilteredResults] = useState([]);
  const [students, setStudents] = useState([]);
  const [exams, setExams] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [toast, setToast] = useState(null);
  const [filters, setFilters] = useState({
    semester: '',
    status: '',
    department: ''
  });
  const [currentResult, setCurrentResult] = useState({
    student: '',
    exam: '',
    total_marks: '',
    percentage: '',
    cgpa: '',
    result_status: 'Pass'
  });

  useEffect(() => {
    fetchResults();
    fetchStudents();
    fetchExams();
    fetchDepartments();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [results, filters]);

  const fetchDepartments = async () => {
    try {
      const response = await axios.get('/departments/');
      setDepartments(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching departments:', error);
    }
  };

  const applyFilters = () => {
    let filtered = [...results];

    if (filters.semester) {
      filtered = filtered.filter(r => {
        const exam = exams.find(e => e.id === r.exam || e.exam_name === r.exam_name);
        return exam && exam.semester === parseInt(filters.semester);
      });
    }

    if (filters.status) {
      filtered = filtered.filter(r => r.result_status === filters.status);
    }

    if (filters.department) {
      filtered = filtered.filter(r => {
        const student = students.find(s => s.id === r.student || s.full_name === r.student_name);
        return student && student.department === parseInt(filters.department);
      });
    }

    setFilteredResults(filtered);
  };

  const handleFilterChange = (key, value) => {
    setFilters({...filters, [key]: value});
  };

  const clearFilters = () => {
    setFilters({
      semester: '',
      status: '',
      department: ''
    });
  };

  const fetchResults = async () => {
    try {
      const response = await axios.get('/results/');
      setResults(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching results:', error);
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
      if (editMode) {
        await axios.put(`/results/${currentResult.id}/`, currentResult);
        setToast({ message: 'Result updated successfully!', type: 'success' });
      } else {
        await axios.post('/results/', currentResult);
        setToast({ message: 'Result added successfully!', type: 'success' });
      }
      fetchResults();
      handleCloseModal();
    } catch (error) {
      console.error('Error details:', error.response?.data);
      
      // Check for duplicate entry
      if (error.response?.status === 400) {
        const errorData = error.response?.data;
        if (errorData?.non_field_errors || 
            (typeof errorData === 'object' && JSON.stringify(errorData).includes('already exists'))) {
          setToast({ message: 'Result already exists for this student and exam!', type: 'warning' });
        } else {
          const errorMsg = errorData?.detail || 
                         errorData?.message ||
                         'Invalid data. Please check all fields.';
          setToast({ message: errorMsg, type: 'error' });
        }
      } else {
        setToast({ message: 'Something went wrong. Please try again.', type: 'error' });
      }
    }
  };

  const handleEdit = (result) => {
    setCurrentResult(result);
    setEditMode(true);
    setShowModal(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditMode(false);
    setCurrentResult({
      student: '',
      exam: '',
      total_marks: '',
      percentage: '',
      cgpa: '',
      result_status: 'Pass'
    });
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

      <div className="page-header">
        <div className="page-header-left">
          <button className="btn-back" onClick={() => window.history.back()}>
            ← Back
          </button>
          <h1>Results</h1>
        </div>
        <div className="page-header-right">
          <button className="btn-primary" onClick={() => {
            setShowModal(true);
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }}>
            + Add Result
          </button>
        </div>
      </div>

      {!showModal && (
        <>
          <div className="filter-section" style={{
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            padding: '20px',
            borderRadius: '15px',
            marginBottom: '20px',
            boxShadow: '0 4px 15px rgba(0,0,0,0.1)'
          }}>
            <h3 style={{margin: '0 0 15px 0', color: '#667eea'}}>Filter Results</h3>
            <div style={{display: 'flex', gap: '15px', flexWrap: 'wrap'}}>
              <select
                value={filters.semester}
                onChange={(e) => handleFilterChange('semester', e.target.value)}
                style={{
                  padding: '12px',
                  border: '2px solid #e0e0e0',
                  borderRadius: '8px',
                  fontSize: '15px',
                  minWidth: '150px'
                }}
              >
                <option value="">All Semesters</option>
                <option value="1">Semester 1</option>
                <option value="2">Semester 2</option>
                <option value="3">Semester 3</option>
                <option value="4">Semester 4</option>
                <option value="5">Semester 5</option>
                <option value="6">Semester 6</option>
                <option value="7">Semester 7</option>
                <option value="8">Semester 8</option>
              </select>

              <select
                value={filters.status}
                onChange={(e) => handleFilterChange('status', e.target.value)}
                style={{
                  padding: '12px',
                  border: '2px solid #e0e0e0',
                  borderRadius: '8px',
                  fontSize: '15px',
                  minWidth: '150px'
                }}
              >
                <option value="">All Status</option>
                <option value="Pass">Pass</option>
                <option value="Fail">Fail</option>
              </select>

              <select
                value={filters.department}
                onChange={(e) => handleFilterChange('department', e.target.value)}
                style={{
                  padding: '12px',
                  border: '2px solid #e0e0e0',
                  borderRadius: '8px',
                  fontSize: '15px',
                  minWidth: '200px'
                }}
              >
                <option value="">All Departments</option>
                {departments.map((dept) => (
                  <option key={dept.id} value={dept.id}>{dept.department_name}</option>
                ))}
              </select>

              <button
                onClick={clearFilters}
                style={{
                  padding: '12px 24px',
                  background: '#6c757d',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  cursor: 'pointer',
                  fontWeight: '600'
                }}
              >
                Clear Filters
              </button>
            </div>
            <p style={{marginTop: '15px', color: '#666', fontSize: '14px'}}>
              Showing {filteredResults.length} of {results.length} results
            </p>
          </div>

          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Exam</th>
                  <th>Total Marks</th>
                  <th>Percentage</th>
                  <th>CGPA</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredResults.map((result) => (
                  <tr key={result.id}>
                    <td>{result.student_name || result.student}</td>
                    <td>{result.exam_name || result.exam}</td>
                    <td>{result.total_marks}</td>
                    <td>{result.percentage}%</td>
                    <td>{result.cgpa}</td>
                    <td>
                      <span className={result.result_status === 'Pass' ? 'status-active' : 'status-inactive'}>
                        {result.result_status}
                      </span>
                    </td>
                    <td>
                      <button className="btn-edit" onClick={() => handleEdit(result)}>Edit</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {showModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <form onSubmit={handleSubmit}>
              <select
                value={currentResult.student}
                onChange={(e) => setCurrentResult({...currentResult, student: e.target.value})}
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
                value={currentResult.exam}
                onChange={(e) => setCurrentResult({...currentResult, exam: e.target.value})}
                required
              >
                <option value="">Select Exam</option>
                {exams.map((exam) => (
                  <option key={exam.id} value={exam.id}>{exam.exam_name}</option>
                ))}
              </select>
              <input
                type="number"
                placeholder="Total Marks"
                value={currentResult.total_marks}
                onChange={(e) => setCurrentResult({...currentResult, total_marks: e.target.value})}
                required
              />
              <input
                type="number"
                step="0.01"
                placeholder="Percentage"
                value={currentResult.percentage}
                onChange={(e) => setCurrentResult({...currentResult, percentage: e.target.value})}
                required
              />
              <input
                type="number"
                step="0.01"
                placeholder="CGPA"
                value={currentResult.cgpa}
                onChange={(e) => setCurrentResult({...currentResult, cgpa: e.target.value})}
                required
              />
              <select
                value={currentResult.result_status}
                onChange={(e) => setCurrentResult({...currentResult, result_status: e.target.value})}
                required
              >
                <option value="Pass">Pass</option>
                <option value="Fail">Fail</option>
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

export default Results;
