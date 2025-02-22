"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import axios from "axios";
import Link from "next/link";


const registrationSchema = z.object({
  firstName: z.string().min(1, "First name is required"),
  lastName: z.string().min(1, "Last name is required"),
  username: z.string().min(3, "Username must be at least 3 characters"),
  email: z.string().email("Invalid email format"),
  password: z.string().min(6, "Password must be at least 6 characters"),
  role: z.enum(["teacher", "student"]),
});

type RegistrationData = z.infer<typeof registrationSchema>;

const Register = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegistrationData>({
    resolver: zodResolver(registrationSchema),
  });

  const [message, setMessage] = useState("");

  const onSubmit = async (data: RegistrationData) => {
    try {
      const response = await axios.post("https://your-api.com/register", data);
      setMessage("Registration successful!");
      console.log(response.data);
    } catch (error) {
      setMessage("Registration failed. Please try again.");
      console.error(error);
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
  
      <h2 className="text-2xl text-center font-bold mb-4">Sign Up</h2>
      {message && <p>{message}</p>}
      
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col space-y-4 text-black">
        <input {...register("firstName")} 
        placeholder=" First Name" 
        className = "w-full max-w-lg px-4 py-2 border rounded-lg text-gray-700 text-center bg-white shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
        />
        {errors.firstName && <p>{errors.firstName.message}</p>}
  

        <input {...register("lastName")} 
        placeholder="Last Name"
        className = "w-full max-w-lg px-4 py-2 border rounded-lg text-gray-700 text-center bg-white shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"        
        />

        {errors.lastName && <p>{errors.lastName.message}</p>}
  

        <input {...register("username")} 
        placeholder="Username" 
        className = "w-full max-w-lg px-4 py-2 border rounded-lg text-gray-700 text-center bg-white shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"
        />
        {errors.username && <p>{errors.username.message}</p>}
  

        <input {...register("email")} 
        placeholder="Email" 
        className = "w-full max-w-lg px-4 py-2 border rounded-lg text-gray-700 text-center bg-white shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"        
        />
        {errors.email && <p>{errors.email.message}</p>}
  

        <input type="password" {...register("password")} 
        placeholder=" Password" 
        className = "w-full max-w-lg px-4 py-2 border rounded-lg text-gray-700 text-center bg-white shadow-md focus:outline-none focus:ring-2 focus:ring-green-500"        
        />
        {errors.password && <p>{errors.password.message}</p>}
  

        <h2 className="text-1xl text-center font-bold mb-4 text-white">Select Role</h2>
  
        <select {...register("role")}
         className="w-full max-w-lg px-4 py-2 border rounded-lg text-center bg-white shadow-md text-gray-600 focus:outline-none focus:ring-2 focus:ring-green-500"
        >
          <option value="select one">Select One</option>
          <option value="teacher">Teacher</option>
          <option value="student">Student</option>
        </select>
        {errors.role && <p>{errors.role.message}</p>}
  
        <button 
            type="submit"
            className = "block mx-auto mb-4 px-11 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
            Register
        </button>
        <button 
            type= "reset"
            className = "block mx-auto mb-4 px-11 py-2 bg-red-500 text-white rounded hover:bg-red-600">
            Reset
        </button>
      </form>
    </div>
  );
};

export default Register;
  /*
  return (
    <div className="max-w-md mx-auto mt-10">
      <h2 className="text-2xl font-bold mb-4">Sign Up</h2>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col space-y-4">
        <input {...register("firstName")} placeholder=" First Name" />
        {errors.firstName && <p>{errors.firstName.message}</p>}

        <input {...register("lastName")} placeholder=" Last Name" />
        {errors.lastName && <p>{errors.lastName.message}</p>}

        <input {...register("username")} placeholder=" Username" />
        {errors.username && <p>{errors.username.message}</p>}

        <input {...register("email")} placeholder=" Email" />
        {errors.email && <p>{errors.email.message}</p>}

        <input type="password" {...register("password")} placeholder="  Password" />
        {errors.password && <p>{errors.password.message}</p>}

        <h2 className="text-1xl font-bold mb-4">Select Role</h2>

        <select {...register("role")} placeholder= " Select Role">
          <option value="teacher">Teacher</option>
          <option value="student">Student</option>
        </select>
        {errors.role && <p>{errors.role.message}</p>}

        <button type="submit">Register</button>
        <button type="reset">Reset</button>
      </form>

       Button to go to home Page 
      <Link href="/">
        <button className="block mx-auto mt-4 px-6 py-2 bg-green-600 text-white rounded hover:bg-gray-700">
          Back to Home
        </button>
      </Link>
    </div>

  );
};

export default Register;
*/