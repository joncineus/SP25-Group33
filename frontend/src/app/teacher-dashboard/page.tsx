"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import DashboardLayout from "@/app/components/DashboardLayout";
import QuizForm from "./QuizForm";

interface Quiz {
  id: number;
  title: string;
  due_date: string;
  is_published: boolean;
}

const TeacherDashboard = () => {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [token, setToken] = useState<string | null>(null);
  const router = useRouter();

  useEffect(() => {
    const storedToken = localStorage.getItem("access_token");
    setToken(storedToken);

    const fetchQuizzes = async () => {
      if (!storedToken) {
        console.error("No token found. Please log in.");
        return;
      }

      try {
        const response = await axios.get("http://127.0.0.1:8000/api/quizzes/", {
          headers: { Authorization: `Bearer ${storedToken}` },
        });
        setQuizzes(response.data);
      } catch (error) {
        console.error("Error fetching quizzes:", error);
      }
    };

    fetchQuizzes();
  }, []);

  const handleEdit = (quizId: number) => {
    if (typeof window !== "undefined") {
      router.push(`/teacher-dashboard/edit/${quizId}`);
    }
  };

  const handleDelete = async (quizId: number) => {
    if (!confirm("Are you sure you want to delete this quiz?")) return;

    if (!token) {
      alert("No token found, please log in.");
      return;
    }

    try {
      await axios.delete(`http://127.0.0.1:8000/api/quizzes/${quizId}/delete/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setQuizzes(quizzes.filter((quiz) => quiz.id !== quizId));
      alert("Quiz deleted successfully!");
    } catch (error) {
      console.error("Delete Error:", error);
      alert("Could not delete the quiz.");
    }
  };

  return (
    <DashboardLayout>
      <h1>Teacher Dashboard</h1>
      <QuizForm />

      <h2>Your Quizzes</h2>
      {quizzes.length === 0 ? (
        <p>No quizzes found.</p>
      ) : (
        <ul className="space-y-2">
          {quizzes.map((quiz) => (
            <li key={quiz.id} className="flex justify-between items-center border p-2 rounded">
              <span>
                {quiz.title} – Due: {quiz.due_date.substring(0, 10)} –{" "}
                {quiz.is_published ? "Published" : "Unpublished"}
              </span>
              <div>
                {/* Edit Button */}
                <button
                  onClick={() => handleEdit(quiz.id)}
                  className="bg-blue-500 text-white px-3 py-1 rounded mx-2"
                >
                  Edit
                </button>

                {/* Delete Button */}
                <button
                  onClick={() => handleDelete(quiz.id)}
                  className="bg-red-500 text-white px-3 py-1 rounded"
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </DashboardLayout>
  );
};

export default TeacherDashboard;
