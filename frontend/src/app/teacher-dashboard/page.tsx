"use client";

import DashboardLayout from '@/app/components/DashboardLayout';
import React from 'react';

const TeacherDashboard: React.FC = () => {
  return (
    <DashboardLayout>
      <div>
        <h1>Teacher Dashboard</h1>
        <p>Welcome, Teacher!</p>
      </div>
    </DashboardLayout>
  );
};

export default TeacherDashboard;