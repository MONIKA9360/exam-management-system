import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import API from '../api/axios';
import './Dashboard.css';

function Dashboard() {
  const [data, setData] = useState(null);
  const [user, setUser] = useState(null);
  const [showSearch, setShowSearch] = useState(false);
  const [searchType, setSearchType] = useState('students');
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('user'));
    setUser(userData);
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    try {
      const response = await API.get('/dashboard/');
      setData(response.data.data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setSearchResults([]);
      return;
    }

    try {
      const response = await API.get(`/${searchType}/`);
      const allData = response.data.results || response.data;
      
      // Filter based on search query
      const filtered = allData.filter(item => {
        const searchLower = searchQuery.toLowerCase();
        if (searchType === 'students') {
          return item.student_id?.toLowerCase().includes(searchLower) ||
                 item.full_name?.toLowerCase().includes(searchLower) ||
                 item.register_no?.toLowerCase().includes(searchLower);
        } else if (searchType === 'staff') {
          return item.staff_id?.toLowerCase().includes(searchLower) ||
                 item.name?.toLowerCase().includes(searchLower);
        } else if (searchType === 'departments') {
          return item.department_code?.toLowerCase().includes(searchLower) ||
                 item.department_name?.toLowerCase().includes(searchLower);
        }
        return false;
      });
      
      setSearchResults(filtered);
    } catch (err) {
      console.error('Search error:', err);
      setSearchResults([]);
    }
  };

  const handleSearchTypeChange = (type) => {
    setSearchType(type);
    setSearchQuery('');
    setSearchResults([]);
  };

  return (
    <div className="dashboard-container">
      <nav className="navbar">
        <h2>Exam Management System</h2>
        <div className="nav-right">
          <button className="search-btn" onClick={() => setShowSearch(!showSearch)}>
            🔍 Search
          </button>
          <span>Welcome, {user?.username}</span>
          <button onClick={handleLogout}>Logout</button>
        </div>
      </nav>

      {showSearch && (
        <div className="search-container">
          <div className="search-box">
            <select 
              value={searchType} 
              onChange={(e) => handleSearchTypeChange(e.target.value)}
              className="search-dropdown"
            >
              <option value="students">Students</option>
              <option value="staff">Staff</option>
              <option value="departments">Departments</option>
            </select>
            <input
              type="text"
              placeholder={`Search by ${searchType === 'students' ? 'Student ID, Name, or Register No' : searchType === 'staff' ? 'Staff ID or Name' : 'Department Code or Name'}`}
              value={searchQuery}
              onChange={(e) => {
                setSearchQuery(e.target.value);
                if (e.target.value.trim()) handleSearch();
                else setSearchResults([]);
              }}
              className="search-input"
            />
            <button onClick={() => setShowSearch(false)} className="close-search">✕</button>
          </div>
          
          {searchResults.length > 0 && (
            <div className="search-results">
              {searchResults.map((item) => (
                <div key={item.id} className="search-result-item">
                  {searchType === 'students' && (
                    <>
                      <strong>{item.student_id}</strong> - {item.full_name} ({item.register_no})
                    </>
                  )}
                  {searchType === 'staff' && (
                    <>
                      <strong>{item.staff_id}</strong> - {item.name}
                    </>
                  )}
                  {searchType === 'departments' && (
                    <>
                      <strong>{item.department_code}</strong> - {item.department_name}
                    </>
                  )}
                </div>
              ))}
            </div>
          )}
          
          {searchQuery && searchResults.length === 0 && (
            <div className="search-results">
              <div className="no-results">No results found</div>
            </div>
          )}
        </div>
      )}

      <div className="dashboard-content">
        <h1>Dashboard</h1>
        
        <div className="stats-grid">
          <div className="stat-card">
            <h3>{data?.total_students || 0}</h3>
            <p>Total Students</p>
          </div>
          <div className="stat-card">
            <h3>{data?.total_staff || 0}</h3>
            <p>Total Staff</p>
          </div>
          <div className="stat-card">
            <h3>{data?.total_departments || 0}</h3>
            <p>Departments</p>
          </div>
          <div className="stat-card">
            <h3>{data?.total_courses || 0}</h3>
            <p>Courses</p>
          </div>
          <div className="stat-card">
            <h3>{data?.upcoming_exams || 0}</h3>
            <p>Upcoming Exams</p>
          </div>
        </div>

        <div className="modules-grid">
          <div className="module-card" onClick={() => navigate('/departments')}>
            <h3>🏢 Departments</h3>
            <p>Manage departments</p>
          </div>
          <div className="module-card" onClick={() => navigate('/staff')}>
            <h3>👨‍🏫 Staff</h3>
            <p>Manage staff members</p>
          </div>
          <div className="module-card" onClick={() => navigate('/students')}>
            <h3>👨‍🎓 Students</h3>
            <p>Manage students</p>
          </div>
          <div className="module-card" onClick={() => navigate('/courses')}>
            <h3>📚 Courses</h3>
            <p>Manage courses</p>
          </div>
          <div className="module-card" onClick={() => navigate('/exams')}>
            <h3>📝 Exams</h3>
            <p>Manage exams</p>
          </div>
          <div className="module-card" onClick={() => navigate('/exam-schedules')}>
            <h3>📅 Schedules</h3>
            <p>Exam schedules</p>
          </div>
          <div className="module-card" onClick={() => navigate('/hall-tickets')}>
            <h3>🎫 Hall Tickets</h3>
            <p>Manage hall tickets</p>
          </div>
          <div className="module-card" onClick={() => navigate('/marks')}>
            <h3>📊 Marks</h3>
            <p>Enter marks</p>
          </div>
          <div className="module-card" onClick={() => navigate('/results')}>
            <h3>🏆 Results</h3>
            <p>View results</p>
          </div>
          <div className="module-card" onClick={() => navigate('/notifications')}>
            <h3>🔔 Notifications</h3>
            <p>Send notifications</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
