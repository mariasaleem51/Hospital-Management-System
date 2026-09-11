# CarePlus Hospital Management System

CarePlus is a modern **Hospital Management System** developed using **Flask and MongoDB**.  
The system provides a simple and professional platform for managing doctors, patients, appointments, and hospital staff.

## Features

- Secure Admin and Doctor Login
- Role-based access for Admin and Doctors
- Admin Dashboard
- Doctor Management
- Add and Manage Doctor Accounts
- Patient Registration
- Patient Consultation Records
- Appointment Management
- Electronic Health Record (EHR) View
- MongoDB Database Integration
- Password Hashing using Bcrypt
- Session-based Authentication
- Responsive and Modern User Interface
- Flash Messages for Success and Error Notifications

## User Roles

### Admin
- Access the hospital dashboard
- View registered doctors
- Add new doctor accounts
- View hospital statistics
- Monitor patient and appointment records

### Doctor
- Access personal doctor workspace
- Add new patient records
- View consultation queue
- Open patient EHR records
- View patient consultation details

## Technologies Used

- Python
- Flask
- MongoDB
- PyMongo
- HTML
- CSS
- JavaScript
- Tailwind CSS
- Font Awesome
- Bcrypt

## Project Structure

```text
Hospital Management System/
│
├── app.py
├── config.py
│
├── templates/
│   └── index.html
│
└── static/
    └── css/
        └── style.css
Database

The system uses MongoDB as its database.

Database Name:

hospital_db

Main Collections:

users
appointments
Users Collection

Stores hospital staff information such as:

Name
Email
Password
Role
Department
Appointments Collection

Stores patient consultation information such as:

Doctor ID
Patient Name
Consultation Time
Reason
Created Date
Application Workflow
Login
  ↓
Role Verification
  ↓
Admin / Doctor Dashboard
  ↓
Manage Doctors / Patients
  ↓
Store Data in MongoDB
  ↓
View Records
Security

The system includes:

Password hashing using Bcrypt
Session-based authentication
Role-based authorization
Protected Admin functions
Protected Doctor functions
Interface

CarePlus uses a clean medical-themed interface with:

Teal and slate color scheme
Responsive dashboard
Sidebar navigation
Professional cards and tables
Doctor and patient modals
EHR record interface
Login authentication screen
Project Purpose

The purpose of CarePlus is to demonstrate how a web-based Hospital Management System can be developed using Flask and MongoDB while providing role-based access, database management, patient records, and a modern user interface.

Developed With

Flask + MongoDB + HTML + CSS + JavaScript

CarePlus Hospital Management System © 2026