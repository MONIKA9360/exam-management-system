import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Departments from './pages/Departments';
import Students from './pages/Students';
import Staff from './pages/Staff';
import Courses from './pages/Courses';
import Exams from './pages/Exams';
import ExamSchedules from './pages/ExamSchedules';
import HallTickets from './pages/HallTickets';
import Marks from './pages/Marks';
import Results from './pages/Results';
import Notifications from './pages/Notifications';

function App() {
  const isAuthenticated = () => {
    return localStorage.getItem('token') !== null;
  };

  // Clear auth on page load/refresh
  React.useEffect(() => {
    // Check if this is a page refresh or direct URL access
    const navigationEntries = performance.getEntriesByType('navigation');
    const isReload = navigationEntries.length > 0 && 
                     (navigationEntries[0].type === 'reload' || 
                      navigationEntries[0].type === 'navigate');
    
    // Clear localStorage on any page load except login/register
    const currentPath = window.location.pathname;
    if (currentPath !== '/login' && currentPath !== '/register' && currentPath !== '/') {
      localStorage.clear();
      window.location.href = '/login';
    }
  }, []);

  const PrivateRoute = ({ children }) => {
    return isAuthenticated() ? children : <Navigate to="/login" replace />;
  };

  const PublicRoute = ({ children }) => {
    return isAuthenticated() ? <Navigate to="/dashboard" replace /> : children;
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={
          <PublicRoute>
            <Login />
          </PublicRoute>
        } />
        <Route path="/register" element={
          <PublicRoute>
            <Register />
          </PublicRoute>
        } />
        <Route path="/dashboard" element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        } />
        <Route path="/departments" element={
          <PrivateRoute>
            <Departments />
          </PrivateRoute>
        } />
        <Route path="/students" element={
          <PrivateRoute>
            <Students />
          </PrivateRoute>
        } />
        <Route path="/staff" element={
          <PrivateRoute>
            <Staff />
          </PrivateRoute>
        } />
        <Route path="/courses" element={
          <PrivateRoute>
            <Courses />
          </PrivateRoute>
        } />
        <Route path="/exams" element={
          <PrivateRoute>
            <Exams />
          </PrivateRoute>
        } />
        <Route path="/exam-schedules" element={
          <PrivateRoute>
            <ExamSchedules />
          </PrivateRoute>
        } />
        <Route path="/hall-tickets" element={
          <PrivateRoute>
            <HallTickets />
          </PrivateRoute>
        } />
        <Route path="/marks" element={
          <PrivateRoute>
            <Marks />
          </PrivateRoute>
        } />
        <Route path="/results" element={
          <PrivateRoute>
            <Results />
          </PrivateRoute>
        } />
        <Route path="/notifications" element={
          <PrivateRoute>
            <Notifications />
          </PrivateRoute>
        } />
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
