import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/quizzes/";  // ✅ Django API endpoint

export const fetchQuizzes = async () => {
    try {
        const response = await axios.get(API_URL, {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("access_token")}` // ✅ Send JWT token
            }
        });
        return response.data;  // ✅ Returns quiz data
    } catch (error) {
        console.error("Error fetching quizzes:", error);
        return []; // Return empty array on error
    }
};
