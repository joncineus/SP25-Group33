"use client";

import { useParams, useRouter } from "next/navigation";
import DashboardLayout from "@/app/components/DashboardLayout";
import QuizForm from "../../QuizForm"; // ✅ Ensure correct import

const EditQuizPage = () => {
  const params = useParams();
  const router = useRouter(); // ✅ Use router to go back

  const quizId = Number(params.id); // ✅ Get quiz ID from URL

  return (
    <DashboardLayout>
      <h1>Edit Quiz</h1>
      <QuizForm quizId={quizId} />

      {/* ✅ Add a "Go Back" button */}
      <button
        onClick={() => router.push("/teacher-dashboard")}
        className="bg-gray-500 text-white px-4 py-2 rounded mt-4"
      >
        Go Back
      </button>
    </DashboardLayout>
  );
};

export default EditQuizPage;
