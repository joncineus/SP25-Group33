"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import axios from "axios";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { jwtDecode } from "jwt-decode";
import { storeTokens } from "../../utils/authService";



type LoginData = {
  username: string;
  password: string;
};

type AuthResponse = {
  refresh: string;
  access: string;
};

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
      const response = await axios.post<AuthResponse>("http://127.0.0.1:8000/token/", data);
  
      console.log("🔹 Full API Response:", response.data);
      console.log("🔹 Access Token:", response.data.access);
  
      // Decode JWT token
      const decodedToken = jwtDecode<{ role: string }>(response.data.access);
      console.log("🔹 Decoded Token:", decodedToken);
  
      // Ensure role exists before storing tokens
      if (decodedToken && "role" in decodedToken) {
        console.log("✅ User Role Found:", decodedToken.role);
        
        // Store access, refresh tokens & user role
        storeTokens(response.data.access, response.data.refresh, decodedToken.role);
        
        // Redirect based on role
        if (decodedToken.role === "teacher") {
          router.push("/teacher-dashboard");
        } else {
          router.push("/student-dashboard");
        }
      } else {
        console.error("❌ Role not found in token:", decodedToken);
        setMessage("Role not found in token. Please try again.");
      }
    } catch (error: any) {
      console.error("❌ Login Error:", error.response?.data || error.message);
      setMessage("Invalid credentials. Please try again.");
    }
  };


  return (
    <div className="max-w-md mx-auto mt-10">
      {/* Back to Home Button */}
      <Link href="/">
        <button className="block mx-auto mb-4 px-9 py-2 bg-green-600 text-white rounded hover:bg-green-700">
          Back to Home
        </button>
      </Link>

      <h2 className="text-2xl text-center font-bold mb-4">Login</h2>
      {message && <p className="text-red-500">{message}</p>}

      <form
        onSubmit={handleSubmit(onSubmit)}
        className="flex flex-col space-y-4 text-black"
      >
        <input
          {...register("username", { required: "Username is required" })}
          placeholder="Username"
          className="w-full max-w-lg px-4 py-2 border rounded-lg text-gray-700 text-center bg-white shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
        />
        {errors.username && <p className="text-red-500">{errors.username.message}</p>}

        <input
          type="password"
          {...register("password", { required: "Password is required" })}
          placeholder="Password"
          className="w-full max-w-lg px-4 py-2 border rounded-lg text-gray-700 text-center bg-white shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
        />
        {errors.password && <p className="text-red-500">{errors.password.message}</p>}

        <button
          type="submit"
          className="block mx-auto mb-4 px-11 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;

