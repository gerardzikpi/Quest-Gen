from django.test import TestCase
from django.urls import reverse
from .models import Courses, Topic, Question

class QuizAppTestCase(TestCase):
    def setUp(self):
        # Create seed data for testing
        self.course = Courses.objects.create(name="Test Course")
        self.topic = Topic.objects.create(course=self.course, name="Test Topic")
        
        self.q1 = Question.objects.create(
            topic=self.topic,
            question="What is 2 + 2?",
            option_a="3",
            option_b="4",
            option_c="5",
            option_d="6",
            correct_answer="4"
        )
        self.q2 = Question.objects.create(
            topic=self.topic,
            question="What is the capital of France?",
            option_a="London",
            option_b="Berlin",
            option_c="Paris",
            option_d="Rome",
            correct_answer="Paris"
        )

    def test_model_str_methods(self):
        self.assertEqual(str(self.course), "Test Course")
        self.assertEqual(str(self.topic), "Test Course - Test Topic")
        self.assertEqual(str(self.q1), "Test Topic: What is 2 + 2?")

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Course")
        self.assertContains(response, "Test Topic")

    def test_topic_detail_view(self):
        response = self.client.get(reverse('topic_detail', args=[self.topic.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Topic")
        self.assertContains(response, "Total Questions")
        # Should show 2 questions count
        self.assertEqual(response.context['question_count'], 2)

    def test_quiz_lifecycle(self):
        # 1. Start the quiz
        response = self.client.post(reverse('quiz_start', args=[self.topic.id]))
        self.assertRedirects(response, reverse('quiz_question'))
        
        # Verify session is initialized
        session = self.client.session
        self.assertEqual(session['quiz_topic_id'], self.topic.id)
        self.assertEqual(len(session['quiz_questions']), 2)
        self.assertEqual(session['quiz_current_index'], 0)
        self.assertEqual(session['quiz_score'], 0)
        
        # 2. Get the first question page
        response = self.client.get(reverse('quiz_question'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Question 1 of 2")
        
        # Determine which question ID is first (shuffled)
        first_q_id = session['quiz_questions'][0]
        first_q = Question.objects.get(id=first_q_id)
        
        # 3. Submit correct answer for first question
        # Determine the option key corresponding to correct answer
        correct_option_key = None
        for opt in ['option_a', 'option_b', 'option_c', 'option_d']:
            if getattr(first_q, opt) == first_q.correct_answer:
                correct_option_key = opt
                break
                
        response = self.client.post(reverse('quiz_question'), {
            'action': 'submit',
            'option': correct_option_key
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['show_feedback'])
        self.assertTrue(response.context['is_correct'])
        
        # Verify score is incremented
        self.assertEqual(self.client.session['quiz_score'], 1)
        self.assertEqual(self.client.session['quiz_answers'][str(first_q_id)], correct_option_key)
        
        # 4. Continue to second question
        response = self.client.post(reverse('quiz_question'), {
            'action': 'next'
        })
        self.assertRedirects(response, reverse('quiz_question'))
        self.assertEqual(self.client.session['quiz_current_index'], 1)
        
        # 5. Get second question
        response = self.client.get(reverse('quiz_question'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Question 2 of 2")
        
        second_q_id = self.client.session['quiz_questions'][1]
        second_q = Question.objects.get(id=second_q_id)
        
        # Determine an incorrect option key
        incorrect_option_key = None
        for opt in ['option_a', 'option_b', 'option_c', 'option_d']:
            if getattr(second_q, opt) != second_q.correct_answer:
                incorrect_option_key = opt
                break
                
        # Submit incorrect answer
        response = self.client.post(reverse('quiz_question'), {
            'action': 'submit',
            'option': incorrect_option_key
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['show_feedback'])
        self.assertFalse(response.context['is_correct'])
        
        # Score should remain 1
        self.assertEqual(self.client.session['quiz_score'], 1)
        
        # 6. Continue to results
        response = self.client.post(reverse('quiz_question'), {
            'action': 'next'
        })
        self.assertRedirects(response, reverse('quiz_results'))
        
        # 7. View results page
        response = self.client.get(reverse('quiz_results'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['score'], 1)
        self.assertEqual(response.context['total'], 2)
        self.assertEqual(response.context['percentage'], 50)
        self.assertContains(response, "50%")
        self.assertContains(response, "Good job!")

