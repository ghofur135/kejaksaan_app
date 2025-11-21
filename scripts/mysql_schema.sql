-- MySQL Schema for Kejaksaan Application
-- Created for migration from SQLite to MySQL

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS db_kejaksaan_app 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Use the database
USE db_kejaksaan_app;

-- Drop tables if they exist (for clean re-creation)
DROP TABLE IF EXISTS pidum_data;
DROP TABLE IF EXISTS pidsus_data;
DROP TABLE IF EXISTS users;

-- Create PIDUM table
CREATE TABLE pidum_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    no VARCHAR(50) NOT NULL,
    periode VARCHAR(50) NOT NULL,
    tanggal DATE NOT NULL,
    jenis_perkara VARCHAR(100) NOT NULL,
    tahapan_penanganan VARCHAR(50) NOT NULL DEFAULT 'PRA PENUNTUTAN',
    keterangan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tanggal (tanggal),
    INDEX idx_jenis_perkara (jenis_perkara),
    INDEX idx_tahapan (tahapan_penanganan),
    INDEX idx_periode (periode)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create PIDSUS table
CREATE TABLE pidsus_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    no VARCHAR(50) NOT NULL,
    periode VARCHAR(50) NOT NULL,
    tanggal DATE NOT NULL,
    jenis_perkara VARCHAR(100) NOT NULL,
    penyidikan VARCHAR(10) NOT NULL DEFAULT '0',
    penuntutan VARCHAR(10) NOT NULL DEFAULT '0',
    keterangan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_tanggal (tanggal),
    INDEX idx_jenis_perkara (jenis_perkara),
    INDEX idx_penyidikan (penyidikan),
    INDEX idx_penuntutan (penuntutan),
    INDEX idx_periode (periode)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create users table for authentication
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default admin user (password: P@ssw0rd25#!)
INSERT INTO users (username, password) VALUES 
('admin', 'a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e1')
ON DUPLICATE KEY UPDATE username = username;