"use client";

import { useState, useEffect } from "react";
import axios from "axios";

interface QuizFormProps {
  quizId?: number;
}

const QuizForm = ({ quizId }: QuizFormProps) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [isPublished, setIsPublished] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (quizId) {
      const fetchQuiz = async () => {
        const token = localStorage.getItem("access_token");
        const res = await axios.get(`http://127.0.0.1:8000/api/quizzes/${quizId}/edit/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        const quiz = res.data;
        setTitle(quiz.title);
        setDescription(quiz.description);
        setDueDate(quiz.due_date.substring(0, 10));
        setIsPublished(quiz.is_published);
      };
      fetchQuiz();
    }
  }, [quizId]);
  

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!title || !dueDate) {
      setError("Title and due date are required!");
      return;
    }

    const token = localStorage.getItem("access_token");
console.log("Using Token:", token);

    const data = { title, description, due_date: dueDate, is_published: isPublished };

    try {
      if (quizId) {
        await axios.put(`http://127.0.0.1:8000/api/quizzes/${quizId}/edit/`, data, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert("Quiz updated successfully!");
      } else {
        await axios.post("http://127.0.0.1:8000/api/quizzes/create/", data, {
          headers: { Authorization: `Bearer ${token}` },
        });
        alert("Quiz created successfully!");
      }

      window.location.reload();
    } catch (error: any) {
      console.error("Error:", error);
      setError(error.response?.data.detail || "An error occurred!");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-lg">
      <h2 className="text-xl font-semibold">{quizId ? "Edit Quiz" : "Create Quiz"}</h2>

      {error && <p className="text-red-500">{error}</p>}

      <div>
        <label>Title *</label>
        <input
          type="text"
          className="border p-2 w-full rounded"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
        />
      </div>

      <div>
        <label>Description</label>
        <textarea
          className="border p-2 w-full rounded"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        ></textarea>
      </div>

      <div>
        <label>Due Date *</label>
        <input
          type="date"
          className="border p-2 w-full rounded"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
        />
      </div>

      <div className="flex items-center gap-2">
        <label>Publish Quiz:</label>
        <input
          type="checkbox"
          checked={isPublished}
          onChange={(e) => setIsPublished(e.target.checked)}
        />
      </div>

      <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded">
        {quizId ? "Update Quiz" : "Create Quiz"}
      </button>
    </form>
  );
};

export default QuizForm;
