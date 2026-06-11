import  django.forms 
from .models import Courses,Topic,Question


class CourseMdoelForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = "__all__"

class TopicModelForm(forms.ModelForm):
    class Meta:
        model = Topic

class QuestionModelForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
    