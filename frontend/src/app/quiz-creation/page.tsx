import React from 'react';
import DashboardLayout from '../components/DashboardLayout';

const QuizCreationPage = () => {
    return (
        <div>
            <DashboardLayout>
            <h1>Quiz Creation</h1>
            <form>
                <div>
                    <label htmlFor="quizTitle">Quiz Title:</label>
                    <input type="text" id="quizTitle" name="quizTitle" />
                </div>
                <div>
                    <label htmlFor="description">Description:</label>
                    <input type="text" id="description" name="description" />
                </div>
                <div>
                    <label htmlFor="due-date">Due Date:</label>
                    <input type="date" id="due-date" name="due-date" />
                </div>
                <div>
                    <label htmlFor="published">Published:</label>
                    <input type="radio" id="published" name="published" />Yes
                    <input type="radio" id="published" name="published" />No
                </div>
                <button type="submit">Create Quiz</button>
            </form>
            </DashboardLayout>
        </div>
    );
};

export default QuizCreationPage;