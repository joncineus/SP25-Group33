"use client";

import DashboardLayout from '@/app/components/DashboardLayout';
import React from 'react';
import QuizList from './QuizList'; // Import the QuizList component

const TeacherDashboard: React.FC = () => {
  return (
    <DashboardLayout>
      <div>
        <h1>Teacher Dashboard</h1>
        <p>Welcome, Teacher!</p>

        <div className="mt-6">
          <h2 className="text-xl font-semibold mb-2">Your Quizzes</h2>
          <QuizList /> {/* Render the quiz list here */}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default TeacherDashboard;
