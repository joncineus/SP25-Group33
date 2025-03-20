/*import Link from "next/link";

const Navbar = () => {
  return (
    <nav className="flex justify-between items-center p-4 bg-gray-800 text-white">
      <h1 className="text-lg font-bold">My App</h1>
      <div className="flex space-x-4">
        <Link href="/" className="hover:underline">
          Home
        </Link>
        <Link href="/register" className="hover:underline">
          Sign Up
        </Link>
      </div>
    </nav>
  );
};

export default Navbar;
*/
"use client"; // Ensure it runs on the client side

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

const Navbar = () => {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if accessToken exists in localStorage
    const token = localStorage.getItem("accessToken");
    setIsAuthenticated(!!token);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    setIsAuthenticated(false);
    router.push("/login"); // Redirect to login page
  };

  return (
    <nav className="flex justify-between items-center p-4 bg-gray-800 text-white">
      <h1 className="text-lg font-bold">Quiz++</h1>
      <div className="flex space-x-4">
        <Link href="/" className="hover:underline">Home</Link>
        {!isAuthenticated ? (
          <>
            <Link href="/register" className="hover:underline">Sign Up</Link>
            <Link href="/login" className="hover:underline">Login</Link>
          </>
        ) : (
          <button onClick={handleLogout} className="hover:underline">Logout</button>
        )}
        <Link href="/teacher-dashboard" className="hover:underline">Teacher Dashboard</Link>
        <Link href="/student-dashboard" className="hover:underline">Student Dashboard</Link>
      </div>
    </nav>
  );
};

export default Navbar;




