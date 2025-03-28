'use client';
import { useEffect, useState } from 'react';
import axiosInstance from '@/utils/axiosInstance';

interface Quiz {
  id: number;
  title: string;
  due_date: string;
  published: boolean;
}

const QuizList = () => {
  const [quizzes, setQuizzes] = useState<Quiz[]>([]);
  const [search, setSearch] = useState('');

  useEffect(() => {
    const fetchQuizzes = async () => {
      try {
        const response = await axiosInstance.get('/teacher/quizzes/');
        setQuizzes(response.data);
      } catch (error) {
        console.error('Failed to fetch quizzes', error);
      }
    };

    fetchQuizzes();
  }, []);

  const filteredQuizzes = quizzes.filter((quiz) =>
    quiz.title.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-4">
      <input
        type="text"
        placeholder="Search quizzes..."
        className="mb-4 p-2 border rounded"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <table className="w-full table-auto border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-50">
            <th className="p-2 border text-black">Title</th>
            <th className="p-2 border text-black">Due Date</th>
            <th className="p-2 border text-black">Published</th>
          </tr>
        </thead>
        <tbody>
          {filteredQuizzes.map((quiz) => (
            <tr key={quiz.id} className="text-center">
              <td className="p-2 border">{quiz.title}</td>
              <td className="p-2 border">{quiz.due_date}</td>
              <td className="p-2 border">{quiz.published ? '✅' : '❌'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default QuizList;
