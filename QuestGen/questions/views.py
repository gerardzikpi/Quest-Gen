import random
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from .models import Courses, Topic, Question

class HomeView(ListView):
    model = Courses
    template_name = 'questions/home.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        # Prefetch topics and their corresponding questions to reduce database queries
        return Courses.objects.prefetch_related('topic_set__question_set').all()

class TopicDetailView(DetailView):
    model = Topic
    template_name = 'questions/topic_detail.html'
    context_object_name = 'topic'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add question count to context
        context['question_count'] = self.object.question_set.count()
        return context

class QuizStartView(View):
    def get(self, request, topic_id):
        return self.start_quiz(request, topic_id)

    def post(self, request, topic_id):
        return self.start_quiz(request, topic_id)

    def start_quiz(self, request, topic_id):
        topic = get_object_or_404(Topic, id=topic_id)
        questions = list(Question.objects.filter(topic=topic).values_list('id', flat=True))
        
        if not questions:
            messages.warning(request, f"The topic '{topic.name}' does not have any questions yet.")
            return redirect('topic_detail', pk=topic.id)
            
        # Shuffle the question IDs to randomize order
        random.shuffle(questions)
        
        # Initialize session variables for the quiz
        request.session['quiz_topic_id'] = topic.id
        request.session['quiz_questions'] = questions
        request.session['quiz_current_index'] = 0
        request.session['quiz_answers'] = {}
        request.session['quiz_score'] = 0
        request.session.modified = True
        
        return redirect('quiz_question')

class QuizQuestionView(View):
    def get(self, request):
        if 'quiz_questions' not in request.session or 'quiz_current_index' not in request.session:
            return redirect('home')
            
        index = request.session['quiz_current_index']
        question_ids = request.session['quiz_questions']
        
        if index < 0 or index >= len(question_ids):
            return redirect('quiz_results')
            
        question_id = question_ids[index]
        question = get_object_or_404(Question, id=question_id)
        
        # Check if the user has already answered this question in this session
        answers = request.session.get('quiz_answers', {})
        has_answered = str(question_id) in answers
        
        context = {
            'question': question,
            'current_number': index + 1,
            'total_questions': len(question_ids),
            'progress_percentage': int((index / len(question_ids)) * 100),
            'show_feedback': False,
        }
        
        if has_answered:
            selected_option = answers[str(question_id)]
            selected_value = getattr(question, selected_option, "")
            is_correct = selected_value.strip() == question.correct_answer.strip()
            
            # Find the correct option key
            correct_option_key = None
            for opt in ['option_a', 'option_b', 'option_c', 'option_d']:
                if getattr(question, opt, "").strip() == question.correct_answer.strip():
                    correct_option_key = opt
                    break
                    
            context.update({
                'show_feedback': True,
                'selected_option': selected_option,
                'correct_option_key': correct_option_key,
                'is_correct': is_correct,
            })
            
        return render(request, 'questions/quiz_question.html', context)

    def post(self, request):
        if 'quiz_questions' not in request.session or 'quiz_current_index' not in request.session:
            return redirect('home')
            
        index = request.session['quiz_current_index']
        question_ids = request.session['quiz_questions']
        action = request.POST.get('action')
        
        if index < 0 or index >= len(question_ids):
            return redirect('quiz_results')
            
        question_id = question_ids[index]
        question = get_object_or_404(Question, id=question_id)
        
        if action == 'submit':
            selected_option = request.POST.get('option')
            if not selected_option:
                # If no option is selected, re-render the page with an error message
                context = {
                    'question': question,
                    'current_number': index + 1,
                    'total_questions': len(question_ids),
                    'progress_percentage': int((index / len(question_ids)) * 100),
                    'error_message': "Please select an option to submit your answer.",
                    'show_feedback': False,
                }
                return render(request, 'questions/quiz_question.html', context)
                
            # Check if correct
            selected_value = getattr(question, selected_option, "")
            is_correct = selected_value.strip() == question.correct_answer.strip()
            
            # Save the answer
            answers = request.session.get('quiz_answers', {})
            answers[str(question_id)] = selected_option
            request.session['quiz_answers'] = answers
            
            if is_correct:
                request.session['quiz_score'] = request.session.get('quiz_score', 0) + 1
                
            request.session.modified = True
            
            # Find the correct option key
            correct_option_key = None
            for opt in ['option_a', 'option_b', 'option_c', 'option_d']:
                if getattr(question, opt, "").strip() == question.correct_answer.strip():
                    correct_option_key = opt
                    break
                    
            context = {
                'question': question,
                'current_number': index + 1,
                'total_questions': len(question_ids),
                'progress_percentage': int((index / len(question_ids)) * 100),
                'show_feedback': True,
                'selected_option': selected_option,
                'correct_option_key': correct_option_key,
                'is_correct': is_correct,
            }
            return render(request, 'questions/quiz_question.html', context)
            
        elif action == 'next':
            # Advance to the next question
            request.session['quiz_current_index'] = index + 1
            request.session.modified = True
            
            if index + 1 >= len(question_ids):
                return redirect('quiz_results')
            else:
                return redirect('quiz_question')
                
        return redirect('quiz_question')

class QuizResultsView(TemplateView):
    template_name = 'questions/quiz_results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        session = self.request.session
        if 'quiz_questions' not in session:
            return context
            
        topic_id = session.get('quiz_topic_id')
        question_ids = session.get('quiz_questions', [])
        answers = session.get('quiz_answers', {})
        score = session.get('quiz_score', 0)
        
        topic = get_object_or_404(Topic, id=topic_id)
        
        # Build question breakdown
        breakdown = []
        for index, q_id in enumerate(question_ids):
            question = get_object_or_404(Question, id=q_id)
            selected_option = answers.get(str(q_id))
            
            selected_value = getattr(question, selected_option, "No answer selected") if selected_option else "No answer selected"
            is_correct = selected_value.strip() == question.correct_answer.strip() if selected_option else False
            
            # Find the correct option key
            correct_option_key = None
            for opt in ['option_a', 'option_b', 'option_c', 'option_d']:
                if getattr(question, opt, "").strip() == question.correct_answer.strip():
                    correct_option_key = opt
                    break
            
            breakdown.append({
                'number': index + 1,
                'question': question,
                'selected_option': selected_option,
                'selected_value': selected_value,
                'correct_option_key': correct_option_key,
                'is_correct': is_correct,
            })
            
        total = len(question_ids)
        percentage = int((score / total) * 100) if total > 0 else 0
        
        # Determine status message and color based on score
        if percentage >= 80:
            status_message = "Outstanding! You've mastered this topic."
            status_color = "text-emerald-400"
            ring_color = "stroke-emerald-500"
        elif percentage >= 50:
            status_message = "Good job! With a bit more practice, you'll be an expert."
            status_color = "text-amber-400"
            ring_color = "stroke-amber-500"
        else:
            status_message = "Keep learning! Review the questions below and try again."
            status_color = "text-rose-400"
            ring_color = "stroke-rose-500"
            
        dash_offset = 251.2 * (1 - (percentage / 100))

        context.update({
            'topic': topic,
            'score': score,
            'total': total,
            'percentage': percentage,
            'status_message': status_message,
            'status_color': status_color,
            'ring_color': ring_color,
            'dash_offset': dash_offset,
            'breakdown': breakdown,
        })
        
        return context
