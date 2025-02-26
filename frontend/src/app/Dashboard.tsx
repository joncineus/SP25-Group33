"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import TeacherDashboard from '@/app/teacher-dashboard/page'; 
import StudentDashboard from '@/app/student-dashboard/page';

const Dashboard = () => {
  const [userRole, setUserRole] = useState<string | null>(null); // Type the state
  const router = useRouter();

  useEffect(() => {
    const storedRole = localStorage.getItem('userRole');
    if (storedRole) {
      setUserRole(storedRole); // Now TypeScript knows this is okay
    } else {
      router.push('/login');
    }
  }, [router]); // Correct dependency array

  if (!userRole) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      {userRole === 'teacher' ? <TeacherDashboard /> : <StudentDashboard />}
    </div>
  );
};

export default Dashboard;