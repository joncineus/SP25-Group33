"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import axios from "axios";
import Link from "next/link";
import { useRouter } from 'next/navigation';
import { jwtDecode } from 'jwt-decode'; 

type LoginData = {
  username: string;
  password: string;
};

type AuthResponse = {
  role: string;
  refresh: string;
  access: string;
}

const Login = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginData>();

  const [message, setMessage] = useState("");
  const router = useRouter();

  const onSubmit = async (data: LoginData) => {
    try {
        //i am not sure if im usign the correct backend  api
      const response = await axios.post<AuthResponse>("http://localhost:8000/auth/login/", data);
      setMessage("Login successful!");
      console.log("Response Data:", response.data);

      // Decode the access token to get the role
      const decodedToken = jwtDecode<{ role: string }>(response.data.access);
      console.log("Decoded Token:", decodedToken);

      // Store the role in local storage
      if (decodedToken.role) {
        localStorage.setItem('userRole', decodedToken.role);
        console.log("Stored Role:", decodedToken.role);

        // Redirect user based on their role
        if (decodedToken.role === "teacher") {
          router.push("/teacher-dashboard");
        } else if (decodedToken.role === "student") {
          router.push("/student-dashboard");
        }
        } else {
          setMessage("Role not found in token.");
        }
        } catch (error) {
        setMessage("Invalid credentials. Please try again.");
        console.error("Login Error:", error);
        }
        };


  return (
    <div className="max-w-md mx-auto mt-10">
      {/* Back to Home Button at the Top */}
      <Link href="/">
        <button className="block mx-auto mb-4 px-9 py-2 bg-green-600 text-white rounded hover:bg-green-700">
          Back to Home
        </button>
      </Link>
      
      <h2 className="text-2xl text-center font-bold mb-4">Login</h2>
      {message && <p>{message}</p>}

      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col space-y-4 text-black">
        <input {...register("username", { required: "Username is required" })}
        placeholder="Username" 
        className="w-full max-w-lg px-4 py-2 border rounded-lg text-gray-700 text-center bg-white shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
        />
        {errors.username && <p>{errors.username.message}</p>}

        <input type="password" {...register("password", { required: "Password is required" })}
        placeholder="Password" 
        className="w-full max-w-lg px-4 py-2 border rounded-lg text-gray-700 text-center bg-white shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
        />
        {errors.password && <p>{errors.password.message}</p>}

        <button type="submit" 
        className="block mx-auto mb-4 px-11 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
