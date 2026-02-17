import React, { useState, useEffect } from 'react';
import axios from '../api/axios';
import './Common.css';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [currentNotification, setCurrentNotification] = useState({
    title: '',
    message: '',
    target_role: 'All'
  });

  useEffect(() => {
    fetchNotifications();
  }, []);

  const fetchNotifications = async () => {
    try {
      const response = await axios.get('/notifications/');
      setNotifications(response.data.results || response.data);
    } catch (error) {
      console.error('Error fetching notifications:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editMode) {
        await axios.put(`/notifications/${currentNotification.id}/`, currentNotification);
        alert('Notification updated successfully!');
      } else {
        await axios.post('/notifications/', currentNotification);
        alert('Notification created successfully!');
      }
      fetchNotifications();
      handleCloseModal();
    } catch (error) {
      alert('Error: ' + (error.response?.data?.detail || 'Something went wrong'));
    }
  };

  const handleEdit = (notification) => {
    setCurrentNotification(notification);
    setEditMode(true);
    setShowModal(true);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this notification?')) {
      try {
        await axios.delete(`/notifications/${id}/`);
        alert('Notification deleted successfully!');
        fetchNotifications();
      } catch (error) {
        alert('Error deleting notification');
      }
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditMode(false);
    setCurrentNotification({
      title: '',
      message: '',
      target_role: 'All'
    });
  };

  return (
    <div className="page-container">
      <div className="page-header">
        <div className="page-header-left">
          <button className="btn-back" onClick={() => window.history.back()}>← Back</button>
          <h1>Notifications</h1>
        </div>
        <div className="page-header-right">
          <button className="btn-primary" onClick={() => {
            setShowModal(true);
            window.scrollTo({ top: 0, behavior: 'smooth' });
          }}>
            + Create Notification
          </button>
        </div>
      </div>

      {!showModal && (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Title</th>
                <th>Message</th>
                <th>Target Role</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {notifications.map((notification) => (
                <tr key={notification.id}>
                  <td>{notification.title}</td>
                  <td>{notification.message}</td>
                  <td>{notification.target_role}</td>
                  <td>{new Date(notification.created_at).toLocaleDateString()}</td>
                  <td>
                    <button className="btn-edit" onClick={() => handleEdit(notification)}>Edit</button>
                    <button className="btn-delete" onClick={() => handleDelete(notification.id)}>Delete</button>
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
                placeholder="Title"
                value={currentNotification.title}
                onChange={(e) => setCurrentNotification({...currentNotification, title: e.target.value})}
                required
              />
              <textarea
                placeholder="Message"
                value={currentNotification.message}
                onChange={(e) => setCurrentNotification({...currentNotification, message: e.target.value})}
                rows="4"
                required
              />
              <select
                value={currentNotification.target_role}
                onChange={(e) => setCurrentNotification({...currentNotification, target_role: e.target.value})}
                required
              >
                <option value="All">All</option>
                <option value="Admin">Admin</option>
                <option value="Staff">Staff</option>
                <option value="Student">Student</option>
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

export default Notifications;
