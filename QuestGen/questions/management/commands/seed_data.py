from django.core.management.base import BaseCommand
from questions.models import Courses, Topic, Question

class Command(BaseCommand):
    help = 'Seeds initial courses, topics, and questions into the database'

    def handle(self, *args, **kwargs):
        self.stdout.write("Clearing existing data...")
        Question.objects.all().delete()
        Topic.objects.all().delete()
        Courses.objects.all().delete()

        self.stdout.write("Creating courses, topics, and questions...")

        # Course 1: Python Programming
        python_course = Courses.objects.create(name="Python Programming")
        
        # Topic 1.1: Syntax & Basics
        py_basics = Topic.objects.create(course=python_course, name="Syntax & Basics")
        Question.objects.create(
            topic=py_basics,
            question="Who is the creator of Python?",
            option_a="Dennis Ritchie",
            option_b="Guido van Rossum",
            option_c="Bjarne Stroustrup",
            option_d="James Gosling",
            correct_answer="Guido van Rossum"
        )
        Question.objects.create(
            topic=py_basics,
            question="Which of the following is an immutable data type in Python?",
            option_a="List",
            option_b="Dictionary",
            option_c="Tuple",
            option_d="Set",
            correct_answer="Tuple"
        )
        Question.objects.create(
            topic=py_basics,
            question="Which character is used to comment out a line of code in Python?",
            option_a="//",
            option_b="/*",
            option_c="#",
            option_d="--",
            correct_answer="#"
        )
        Question.objects.create(
            topic=py_basics,
            question="What is the output of len(['apple', 'banana', 'cherry']) in Python?",
            option_a="3",
            option_b="18",
            option_c="2",
            option_d="Error",
            correct_answer="3"
        )
        Question.objects.create(
            topic=py_basics,
            question="Which keyword is used to define a function in Python?",
            option_a="function",
            option_b="def",
            option_c="func",
            option_d="define",
            correct_answer="def"
        )

        # Topic 1.2: Advanced Concepts
        py_adv = Topic.objects.create(course=python_course, name="Advanced Concepts")
        Question.objects.create(
            topic=py_adv,
            question="Which of the following defines a generator in Python?",
            option_a="A function that returns a list",
            option_b="A class with a __call__ method",
            option_c="A function containing a yield expression",
            option_d="A decorator that logs calls",
            correct_answer="A function containing a yield expression"
        )
        Question.objects.create(
            topic=py_adv,
            question="Which decorator is used to define a method that belongs to the class itself rather than instances?",
            option_a="@staticmethod",
            option_b="@classmethod",
            option_c="@property",
            option_d="@instancemethod",
            correct_answer="@classmethod"
        )
        Question.objects.create(
            topic=py_adv,
            question="How do you correctly handle multiple exceptions (ValueError and TypeError) in a single except block?",
            option_a="except ValueError, TypeError:",
            option_b="except (ValueError, TypeError):",
            option_c="except ValueError or TypeError:",
            option_d="except [ValueError, TypeError]:",
            correct_answer="except (ValueError, TypeError):"
        )

        # Course 2: Web Development
        web_course = Courses.objects.create(name="Web Development")

        # Topic 2.1: HTML & CSS
        html_css = Topic.objects.create(course=web_course, name="HTML & CSS")
        Question.objects.create(
            topic=html_css,
            question="What does HTML stand for?",
            option_a="HyperText Markup Language",
            option_b="HighText Machine Language",
            option_c="HyperTabular Markup Link",
            option_d="HyperText Main Link",
            correct_answer="HyperText Markup Language"
        )
        Question.objects.create(
            topic=html_css,
            question="Which HTML tag is used to reference an external CSS file?",
            option_a="<style>",
            option_b="<script>",
            option_c="<link>",
            option_d="<href>",
            correct_answer="<link>"
        )
        Question.objects.create(
            topic=html_css,
            question="What CSS property changes the text color of an element?",
            option_a="text-color",
            option_b="font-color",
            option_c="color",
            option_d="background-color",
            correct_answer="color"
        )
        Question.objects.create(
            topic=html_css,
            question="Which display value makes an element inline-level but allows setting width and height?",
            option_a="block",
            option_b="inline",
            option_c="inline-block",
            option_d="flex",
            correct_answer="inline-block"
        )

        # Topic 2.2: JavaScript
        javascript = Topic.objects.create(course=web_course, name="JavaScript")
        Question.objects.create(
            topic=javascript,
            question="Which keyword is used to declare a block-scoped local variable in JavaScript?",
            option_a="var",
            option_b="let",
            option_c="const",
            option_d="both let and const",
            correct_answer="both let and const"
        )
        Question.objects.create(
            topic=javascript,
            question="What is the purpose of the '===' operator in JavaScript?",
            option_a="Assigns a value to a variable",
            option_b="Compares values for equality, performing type conversion if necessary",
            option_c="Compares values and types for strict equality, without type conversion",
            option_d="Checks if a value is undefined",
            correct_answer="Compares values and types for strict equality, without type conversion"
        )
        Question.objects.create(
            topic=javascript,
            question="How do you write 'Hello World' in an alert box in JavaScript?",
            option_a="msgBox('Hello World');",
            option_b="alertBox('Hello World');",
            option_c="alert('Hello World');",
            option_d="console.log('Hello World');",
            correct_answer="alert('Hello World');"
        )
        Question.objects.create(
            topic=javascript,
            question="Which array method adds an element to the end of an array and returns its new length?",
            option_a="pop()",
            option_b="shift()",
            option_c="push()",
            option_d="unshift()",
            correct_answer="push()"
        )

        # Course 3: Science & Space
        science_course = Courses.objects.create(name="Science & Space")

        # Topic 3.1: Astronomy
        astronomy = Topic.objects.create(course=science_course, name="Astronomy")
        Question.objects.create(
            topic=astronomy,
            question="Which planet is commonly referred to as the Red Planet?",
            option_a="Venus",
            option_b="Mars",
            option_c="Jupiter",
            option_d="Mercury",
            correct_answer="Mars"
        )
        Question.objects.create(
            topic=astronomy,
            question="What is the largest planet in our solar system?",
            option_a="Saturn",
            option_b="Uranus",
            option_c="Neptune",
            option_d="Jupiter",
            correct_answer="Jupiter"
        )
        Question.objects.create(
            topic=astronomy,
            question="What is the hottest planet in our solar system?",
            option_a="Mercury",
            option_b="Venus",
            option_c="Mars",
            option_d="Jupiter",
            correct_answer="Venus"
        )
        Question.objects.create(
            topic=astronomy,
            question="How many stars are in our solar system?",
            option_a="1",
            option_b="Millions",
            option_c="About 100",
            option_d="0",
            correct_answer="1"
        )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
