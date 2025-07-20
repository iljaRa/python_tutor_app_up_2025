import os
import gradio as gr
from dotenv import load_dotenv
from langchain_together import ChatTogether
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Load username and password from environment variables
USERNAME = os.getenv("PYTUTOR_USERNAME")
PASSWORD = os.getenv("PYTUTOR_PASSWORD")

# Authentication function
def auth_func(username, password):
    return username == USERNAME and password == PASSWORD

# QuestionGenerator class handles the generation of Python programming questions
# using the Together API. It takes difficulty level and topic as inputs and
# returns a formatted question with problem statement, example input, and
# requirements using the Mistral language model.

class QuestionGenerator:    
    def __init__(self):
        self.api_key = os.getenv("TOGETHER_API_KEY")
        self.prompt = PromptTemplate(
            input_variables=["difficulty", "topic"],
            template="""Generate a Python programming question for a student.
            Difficulty level: {difficulty}
            Topic: {topic}

            The students are allowed to avoid the following techniques: {excluded_techniques}
            
            The question should be clear, concise, and include:
            1. The problem statement
            2. Example input

            Do NOT provide any further suggestions for the solutions.
            
            Question:"""
        )
        self.llm = ChatTogether(
            # model="mistralai/Mistral-7B-Instruct-v0.3",
            # model="mistralai/Mistral-Small-24B-Instruct-2501",
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            temperature=0.7,
            max_tokens=1000
        )
        self.question_generator = self.prompt | self.llm | StrOutputParser()

    def invoke(self, difficulty, topic, excluded_techniques):
        return self.question_generator.invoke({
            "difficulty": difficulty, 
            "topic": topic,
            "excluded_techniques": excluded_techniques
        })

# Evaluator class handles the evaluation of student's Python code submissions
# using the Together API. It takes a question and student's answer as inputs and
# returns a formatted evaluation with score, feedback, and suggestions using the
# Mistral language model.
class Evaluator:    
    def __init__(self):
        self.api_key = os.getenv("TOGETHER_API_KEY")
        self.prompt = PromptTemplate(
            input_variables=["question", "student_answer"],
            template="""Evaluate the following Python code submission for the given question.
            
            Question: {question}
            
            Student's Answer:
            {student_answer}
            
            The students are allowed to avoid the following techniques: {excluded_techniques}
            
            Please provide:
            1. A score out of 10 in the format: x/10 , where x is the score
            2. Detailed feedback on the code
            3. Suggestions for improvement
            4. A possible ideal solution to the question
            
            Evaluation:"""
        )
        self.llm = ChatTogether(
            # model="mistralai/Mistral-7B-Instruct-v0.3",
            # model="mistralai/Mistral-Small-24B-Instruct-2501",
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            temperature=0.3,
            max_tokens=2000
        )
        self.evaluator = self.prompt | self.llm | StrOutputParser()

    def invoke(self, question, student_answer, excluded_techniques):
        return self.evaluator.invoke({
            "question": question, 
            "student_answer": student_answer,
            "excluded_techniques": excluded_techniques
        })

# Initialize the classes
question_generator = QuestionGenerator()
evaluator = Evaluator()

# Generate a new Python programming question
def generate_question(difficulty, topic, excluded_techniques):
    """Generate a new Python programming question."""
    response = question_generator.invoke(difficulty, topic, excluded_techniques)
    return response

# Evaluate the student's answer
def evaluate_answer(question, student_answer, excluded_techniques):
    """Evaluate the student's answer."""
    if not student_answer:
        return "Please submit your answer first."
    response = evaluator.invoke(question, student_answer, excluded_techniques)
    return response

# Create the Gradio interface
with gr.Blocks(title="Python Tutor") as demo:
    gr.Markdown("# Python Programming Tutor")
    gr.Markdown("Learn Python programming with AI-powered feedback!")
    
    with gr.Tabs() as tabs:
        with gr.TabItem("Practice Session 1"):
            with gr.Row():
                with gr.Column():
                    difficulty1 = gr.Dropdown(
                        choices=["Beginner", "Intermediate", "Advanced"],
                        value="Beginner",
                        label="Difficulty Level"
                    )
                    topic1 = gr.Textbox(
                        label="Topic (e.g., 'Lists', 'Functions', 'Classes')",
                        value="variables, data types, code comments, operators, basic expressions"
                    )
                    excluded_techniques1 = gr.Textbox(
                        label="Excluded Techniques (e.g., 'Recursion', 'Dynamic Programming')",
                        value="control flow, loops, functions, classes, objects, inheritance, polymorphism, encapsulation, abstraction, exception handling",
                        visible=False
                    )
                    generate_btn1 = gr.Button("Generate New Question")
                
                with gr.Column():
                    question_display1 = gr.Textbox(
                        label="Question",
                        lines=5,
                        interactive=False,
                        show_copy_button=True
                    )
            
            with gr.Row():
                student_answer1 = gr.Textbox(
                    label="Your Answer",
                    lines=5,
                    placeholder="Write your Python code here...",
                    show_copy_button=True
                )
                submit_btn1 = gr.Button("Submit Answer")
            
            evaluation_display1 = gr.Textbox(
                label="Evaluation",
                lines=8,
                interactive=False
            )
            
            # Connect the components for first tab
            generate_btn1.click(
                fn=generate_question,
                inputs=[difficulty1, topic1, excluded_techniques1],
                outputs=question_display1
            )
            
            submit_btn1.click(
                fn=evaluate_answer,
                inputs=[question_display1, student_answer1, excluded_techniques1],
                outputs=evaluation_display1
            )

        with gr.TabItem("Practice Session 2"):
            with gr.Row():
                with gr.Column():
                    difficulty2 = gr.Dropdown(
                        choices=["Beginner", "Intermediate", "Advanced"],
                        value="Beginner",
                        label="Difficulty Level"
                    )
                    topic2 = gr.Textbox(
                        label="Topic (e.g., 'Lists', 'Functions', 'Classes')",
                        value="control flow, loops, functions, classes, objects, inheritance, polymorphism"
                    )
                    excluded_techniques2 = gr.Textbox(
                        label="Excluded Techniques (e.g., 'Recursion', 'Dynamic Programming')",
                        value="encapsulation, abstraction, exception handling, recursion, dynamic programming",
                        visible=False
                    )
                    generate_btn2 = gr.Button("Generate New Question")
                
                with gr.Column():
                    question_display2 = gr.Textbox(
                        label="Question",
                        lines=5,
                        interactive=False,
                        show_copy_button=True
                    )
            
            with gr.Row():
                student_answer2 = gr.Textbox(
                    label="Your Answer",
                    lines=5,
                    placeholder="Write your Python code here...",
                    show_copy_button=True
                )
                submit_btn2 = gr.Button("Submit Answer")
            
            evaluation_display2 = gr.Textbox(
                label="Evaluation",
                lines=8,
                interactive=False
            )
            
            # Connect the components for second tab
            generate_btn2.click(
                fn=generate_question,
                inputs=[difficulty2, topic2, excluded_techniques2],
                outputs=question_display2
            )
            
            submit_btn2.click(
                fn=evaluate_answer,
                inputs=[question_display2, student_answer2, excluded_techniques2],
                outputs=evaluation_display2
            )

if __name__ == "__main__":
    demo.launch(
        share=False, 
        server_port=7860, 
        server_name="0.0.0.0",
        max_threads=40,
        auth=auth_func
    ) 