from django import forms
from django.core.exceptions import ValidationError
from .models import Course, Topic


class QuestSelectForm(forms.Form):
    course = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Enter a course name",
        "class": (
            "w-full appearance-none bg-white/[0.04] border border-white/[0.08] "
            "text-slate-200 rounded-2xl px-5 py-4 text-sm font-medium "
            "focus:outline-none focus:border-indigo-500/60 focus:ring-2 "
            "focus:ring-indigo-500/20 transition-all duration-200 "
            "hover:border-white/20"
        ),
    }))

    topic = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "Enter a topic name",
        "class": (
            "w-full appearance-none bg-white/[0.04] border border-white/[0.08] "
            "text-slate-200 rounded-2xl px-5 py-4 text-sm font-medium "
            "focus:outline-none focus:border-indigo-500/60 focus:ring-2 "
            "focus:ring-indigo-500/20 transition-all duration-200 "
            "hover:border-white/20"
        ),
    }))

    def clean(self):
        cleaned_data = super().clean()
        course_name = cleaned_data.get('course')
        topic_name = cleaned_data.get('topic')

        if not course_name or not topic_name:
            return cleaned_data

        course_name = course_name.strip()
        topic_name = topic_name.strip()

        course = Course.objects.filter(name__iexact=course_name).first()
        if not course:
            self.add_error('course', ValidationError(
                "Course not found. Please enter a valid course name."
            ))
            return cleaned_data

        topic = Topic.objects.filter(course=course, name__iexact=topic_name).first()
        if not topic:
            self.add_error('topic', ValidationError(
                "Topic not found for this course. Please enter the topic exactly as shown."
            ))
            return cleaned_data

        cleaned_data['course'] = course
        cleaned_data['topic'] = topic
        return cleaned_data

        