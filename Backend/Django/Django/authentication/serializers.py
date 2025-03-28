from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser 
from .models import Quiz
from .models import QuizResponse
from .models import Question
from django.utils import timezone



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)



class QuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'question_text', 'question_type', 'option_a', 'option_b',
            'option_c', 'option_d', 'correct_answer_mc', 'correct_answer_written'
        ]


class QuizCreateSerializer(serializers.ModelSerializer):
    questions = QuestionCreateSerializer(many=True, required=True)
    
    class Meta:
        model = Quiz
        fields = [
            'title', 'description', 'subject', 'difficulty_level',
            'time_limit', 'is_published', 'due_date', 'questions'
        ]
    
    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value
    
    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        validated_data['teacher'] = self.context['request'].user
        quiz = Quiz.objects.create(**validated_data)
        
        for question_data in questions_data:
            Question.objects.create(quiz=quiz, **question_data)
        
        return quiz



class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    question_type = serializers.CharField(source='get_question_type_display')

    class Meta:
        model = Question
        fields = [
            'id', 
            'question_text', 
            'question_type',
            'options', 
            'correct_answer_mc',
            'correct_answer_written'
        ]
        read_only_fields = ['correct_answer_mc', 'correct_answer_written']

    def get_options(self, obj):
        if obj.question_type == 'MC':
            return {
                'type': 'MC',
                'A': obj.option_a,
                'B': obj.option_b,
                'C': obj.option_c,
                'D': obj.option_d
            }
        return {
            'type': 'WR',
            'expected_length': len(obj.correct_answer_written) if obj.correct_answer_written else 0
        }






class QuizSerializer(serializers.ModelSerializer):
    # questions = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # teacher = serializers.PrimaryKeyRelatedField(read_only=True)

    questions = QuestionSerializer(many=True, read_only=True)  # Show full question details
    teacher = serializers.StringRelatedField()  # Show teacher name instead of ID

    class Meta:
        model = Quiz
        fields = [
            'id', 'title', 'description', 'created_at', 'teacher', 'subject',
            'difficulty_level', 'time_limit', 'is_published', 'questions', 'due_date'
        ]
        
    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value


class QuizResponseSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())
    
    class Meta:
        model = QuizResponse
        fields = ['quiz', 'answers']
        read_only_fields = ['student', 'score']

    def validate(self, data):
        quiz = data['quiz']
        answers = data['answers']
        
        for q_id, answer in answers.items():
            try:
                question = quiz.questions.get(id=int(q_id))
                
                if question.question_type == 'MC':
                    # Validate multiple choice answers
                    answer = answer.upper()
                    if answer not in ['A', 'B', 'C', 'D']:
                        raise serializers.ValidationError(
                            {f"answers.{q_id}": "Must be A, B, C, or D for multiple choice questions"}
                        )
                    # Update the answer to uppercase
                    answers[q_id] = answer
                
                # Written answers don't need format validation
                
            except Question.DoesNotExist:
                raise serializers.ValidationError(
                    {f"answers.{q_id}": "Invalid question ID"}
                )
        return data

    def create(self, validated_data):
        quiz = validated_data['quiz']
        answers = validated_data['answers']
        request = self.context.get('request')
        score = 0
        
        for q_id, answer in answers.items():
            question = quiz.questions.get(id=int(q_id))
            
            if question.question_type == 'MC':
                if answer.upper() == question.correct_answer_mc:
                    score += 1
            else:  # Written answer
                # Basic case-insensitive comparison
                if answer.lower().strip() == question.correct_answer_written.lower().strip():
                    score += 1
        
        return QuizResponse.objects.create(
            student=request.user,
            quiz=quiz,
            answers=answers,
            score=score
        )