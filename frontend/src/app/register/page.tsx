"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import axios from "axios";

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
      <h2 className="text-2xl font-bold mb-4">Sign Up</h2>
      {message && <p>{message}</p>}
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col space-y-4">
        <input {...register("firstName")} placeholder="First Name" />
        {errors.firstName && <p>{errors.firstName.message}</p>}

        <input {...register("lastName")} placeholder="Last Name" />
        {errors.lastName && <p>{errors.lastName.message}</p>}

        <input {...register("username")} placeholder="Username" />
        {errors.username && <p>{errors.username.message}</p>}

        <input {...register("email")} placeholder="Email" />
        {errors.email && <p>{errors.email.message}</p>}

        <input type="password" {...register("password")} placeholder="Password" />
        {errors.password && <p>{errors.password.message}</p>}

        <select {...register("role")}>
          <option value="teacher">Teacher</option>
          <option value="student">Student</option>
        </select>
        {errors.role && <p>{errors.role.message}</p>}

        <button type="submit">Register</button>
        <button type="reset">Reset</button>
      </form>
    </div>
  );
};

export default Register;
