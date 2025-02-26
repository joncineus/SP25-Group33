"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Navbar from '@/app/Navbar';  // Correct import path
import { getAccessToken } from "../../utils/authService";

interface Props {
  children: React.ReactNode;
}

const DashboardLayout = ({ children }: Props) => {
  const [userRole, setUserRole] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const token = getAccessToken();
    const storedRole = localStorage.getItem('userRole');
    if (token && storedRole) {
      setUserRole(storedRole);
    } else {
      router.push("/login"); // Redirect to login if no token or role
    }
  }, [router]); // Add router to the dependency array

  if (!userRole) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <Navbar />
      {children}
    </div>
  );
};

export default DashboardLayout;