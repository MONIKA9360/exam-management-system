-- ============================================
-- EXAM MANAGEMENT SYSTEM - DATABASE SETUP
-- ============================================

-- Step 1: Create Database
CREATE DATABASE IF NOT EXISTS examination 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Step 2: Use Database
USE examination;

-- Step 3: Verify Database
SHOW DATABASES;

-- Step 4: Check if database is selected
SELECT DATABASE();

-- ============================================
-- OPTIONAL: Create MySQL User (if needed)
-- ============================================

-- Create user (uncomment if needed)
-- CREATE USER 'exam_user'@'localhost' IDENTIFIED BY 'your_password';

-- Grant privileges (uncomment if needed)
-- GRANT ALL PRIVILEGES ON examination.* TO 'exam_user'@'localhost';

-- Flush privileges (uncomment if needed)
-- FLUSH PRIVILEGES;

-- ============================================
-- VERIFY SETUP
-- ============================================

-- Show all tables (run after Django migrations)
SHOW TABLES;

-- Check table structure (run after migrations)
-- DESCRIBE users;
-- DESCRIBE students;
-- DESCRIBE staff;
-- DESCRIBE departments;
-- DESCRIBE courses;
-- DESCRIBE exams;
-- DESCRIBE exam_schedules;
-- DESCRIBE hall_tickets;
-- DESCRIBE marks_entries;
-- DESCRIBE results;
-- DESCRIBE notifications;
-- DESCRIBE audit_logs;

-- ============================================
-- USEFUL QUERIES FOR TESTING
-- ============================================

-- Count records in each table
-- SELECT 'users' as table_name, COUNT(*) as count FROM users
-- UNION ALL
-- SELECT 'students', COUNT(*) FROM students
-- UNION ALL
-- SELECT 'staff', COUNT(*) FROM staff
-- UNION ALL
-- SELECT 'departments', COUNT(*) FROM departments
-- UNION ALL
-- SELECT 'courses', COUNT(*) FROM courses
-- UNION ALL
-- SELECT 'exams', COUNT(*) FROM exams
-- UNION ALL
-- SELECT 'exam_schedules', COUNT(*) FROM exam_schedules
-- UNION ALL
-- SELECT 'hall_tickets', COUNT(*) FROM hall_tickets
-- UNION ALL
-- SELECT 'marks_entries', COUNT(*) FROM marks_entries
-- UNION ALL
-- SELECT 'results', COUNT(*) FROM results
-- UNION ALL
-- SELECT 'notifications', COUNT(*) FROM notifications
-- UNION ALL
-- SELECT 'audit_logs', COUNT(*) FROM audit_logs;

-- ============================================
-- BACKUP COMMANDS (for production)
-- ============================================

-- Backup database
-- mysqldump -u root -p examination > examination_backup.sql

-- Restore database
-- mysql -u root -p examination < examination_backup.sql

-- ============================================
-- CLEANUP (use with caution!)
-- ============================================

-- Drop database (WARNING: This will delete all data!)
-- DROP DATABASE IF EXISTS examination;

-- ============================================
-- NOTES
-- ============================================

-- 1. Make sure MySQL server is running before executing
-- 2. Update credentials in Django settings.py:
--    - NAME: 'examination'
--    - USER: 'root'
--    - PASSWORD: 'Monika@2004'
--    - HOST: 'localhost'
--    - PORT: '3306'
-- 3. Run Django migrations after database creation:
--    python manage.py makemigrations
--    python manage.py migrate
-- 4. Create superuser:
--    python manage.py createsuperuser

-- ============================================
-- TROUBLESHOOTING
-- ============================================

-- Check MySQL version
-- SELECT VERSION();

-- Check current user
-- SELECT USER();

-- Show all users
-- SELECT User, Host FROM mysql.user;

-- Check database charset
-- SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
-- FROM information_schema.SCHEMATA
-- WHERE SCHEMA_NAME = 'examination';

-- ============================================
-- END OF SETUP SCRIPT
-- ============================================
