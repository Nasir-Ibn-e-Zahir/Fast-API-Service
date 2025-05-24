# # extract_text_api.py
# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# from pytesseract import image_to_string
# from PIL import Image
# import io
# import requests 

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.post("/extract-text")
# async def extract_text(file: UploadFile = File(...)):
#     contents = await file.read()
#     image = Image.open(io.BytesIO(contents))
    # text = image_to_string(image)
    # check = "NLP,SVM,Regression,Classification,Supervised Learning, Unsupervised Learning"
    # return {"response": text}
    # prompt = (
    #     f"Prepare exam paper from the contents. Include:\n"
    #     f"- 4 short questions\n"
    #     f"- 3 long questions\n"
    #     f"- 6 MCQs with options\n"
    #     f"- 6 True/False\n\n"
    #     f"Content:\n{text}"
    # )\"{text}\"
    # prompt = (f"Give m")
    # print(prompt)
    # response = requests.post(
    #     "http://localhost:11434/api/generate",
    #     json={
    #         "model": "mistral",
    #         "prompt": prompt,
    #         "stream": False
    #     }
    # )

    # result = response.json()
    # print(result)
    # return {"response":result}




#######################################################################################

# # main.py
# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# from PIL import Image
# import io
# import pytesseract

# from langchain.llms import Ollama
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# app = FastAPI()

# # CORS setup (optional if you're testing locally)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load local LLM via Ollama
# llm = Ollama(model="mistral")

# # Prompt template to generate a 30-day schedule
# schedule_prompt = PromptTemplate(
#     input_variables=["text"],
#     template="""
# You are an educational assistant. Create a 30-day course schedule based on the following contents:

# {text}

# Make sure the schedule includes key topics per day, and is logically organized.
# """
# )

# # Chain for scheduling
# schedule_chain = LLMChain(llm=llm, prompt=schedule_prompt)

# @app.post("/generate-schedule/")
# async def generate_schedule(file: UploadFile = File(...)):
#     try:
#         # Step 1: Read and convert uploaded image
#         contents = await file.read()
#         image = Image.open(io.BytesIO(contents))

#         # Step 2: Extract text using Tesseract OCR
#         extracted_text = pytesseract.image_to_string(image)

#         # Step 3: Use LangChain to generate the schedule
#         result = schedule_chain.run(text=extracted_text)

#         return {"response": result}

#     except Exception as e:
#         return {"error": str(e)}  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


# from fastapi import FastAPI, File, UploadFile, Form
# from fastapi.middleware.cors import CORSMiddleware
# from pytesseract import image_to_string
# from PIL import Image
# import io, requests, re
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from datetime import datetime
# import os

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def clean_and_split_text(text):
#     topics = re.split(r'[\n,;•-]+', text)
#     topics = [t.strip() for t in topics if t.strip()]
#     return topics

# def generate_explanation(topic):
#     prompt = f"Explain this topic in simple terms for beginners: {topic}"
#     response = requests.post("http://localhost:11434/api/generate", json={
#         "model": "mistral",
#         "prompt": prompt,
#         "stream": False
#     })
#     return response.json().get("response", "")

# def generate_prompt_with_model(prompt):
#     response = requests.post("http://localhost:11434/api/generate", json={
#         "model": "mistral",
#         "prompt": prompt,
#         "stream": False
#     })
#     return response.json().get("response", "")

# def save_to_pdf(filename, sections):
#     c = canvas.Canvas(filename, pagesize=A4)
#     width, height = A4
#     textobject = c.beginText(40, height - 40)
#     textobject.setFont("Helvetica", 12)

#     for title, content in sections:
#         textobject.textLine(f"\n{title}")
#         textobject.textLine("-" * 90)
#         for line in content.split('\n'):
#             textobject.textLine(line)
#         textobject.textLine("\n")

#     c.drawText(textobject)
#     c.save()

# @app.post("/extract-text")
# async def extract_text(
#     file: UploadFile = File(...),
#     # quiz_count: int = Form(...),
#     # difficulty: str = Form(...)
# ):
#     contents = await file.read()
#     image = Image.open(io.BytesIO(contents))
#     extracted_text = image_to_string(image)

#     topics = clean_and_split_text(extracted_text)

#     # Explain each topic individually
#     explained_topics = []
#     for topic in topics:
#         explanation = generate_explanation(topic)
#         explained_topics.append((topic, explanation))

#     # Assignments & Presentations
#     assignments_prompt = f"Generate assignment topics from this course content: {', '.join(topics)}"
#     assignments = generate_prompt_with_model(assignments_prompt)

#     presentations_prompt = f"Suggest presentation topics for these contents: {', '.join(topics)}"
#     presentations = generate_prompt_with_model(presentations_prompt)

#     # Quiz, Mid, Final
#     quiz_prompt = f"Create {1} quizzes from this content with easy level. Each quiz should include MCQs, True/False, and Short Questions."
#     quiz = generate_prompt_with_model(quiz_prompt)

#     paper_prompt = f"Create Mid-Term and Final-Term papers with easy level from this content."
#     papers = generate_prompt_with_model(paper_prompt)

#     # Timeline generation
#     timeline_prompt = f"Create a timeline to cover the following topics in a 3-month course: {', '.join(topics)}"
#     timeline = generate_prompt_with_model(timeline_prompt)

#     # PDF generation
#     sections = explained_topics + [
#         ("Assignment Topics", assignments),
#         ("Presentation Topics", presentations),
#         ("Quizzes", quiz),
#         ("Mid-Term and Final-Term Papers", papers),
#         ("Course Timeline", timeline)
#     ]

#     filename = f"/mnt/data/course_output_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
#     save_to_pdf(filename, sections)

#     return {"download_url": filename}

# from fastapi import FastAPI, File, UploadFile, Form
# from fastapi.middleware.cors import CORSMiddleware
# from pytesseract import image_to_string
# from PIL import Image
# import io, requests, re
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from datetime import datetime
# import os

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ⛔ Replace this with your actual OpenRouter API Key
# API_KEY = "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"

# def query_llama3(prompt):
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "HTTP-Referer": "http://localhost",  # Required by OpenRouter
#         "Content-Type": "application/json"
#     }

#     body = {
#         "model": "meta-llama/llama-3-70b-instruct",  # or "llama-3-8b-instruct"
#         "messages": [
#             {"role": "user", "content": prompt}
#         ]
#     }

#     response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

#     if response.status_code == 200:
#         return response.json()['choices'][0]['message']['content']
#     else:
#         return f"Error: {response.status_code} - {response.text}"

# def clean_and_split_text(text):
#     topics = re.split(r'[\n,;•-]+', text)
#     topics = [t.strip() for t in topics if t.strip()]
#     return topics

# def generate_explanation(topic):
#     prompt = f"Explain this topic in simple terms for beginners: {topic}"
#     return query_llama3(prompt)

# def generate_prompt_with_model(prompt):
#     return query_llama3(prompt)

# def save_to_pdf(filename, sections):
#     c = canvas.Canvas(filename, pagesize=A4)
#     width, height = A4
#     textobject = c.beginText(40, height - 40)
#     textobject.setFont("Helvetica", 12)

#     for title, content in sections:
#         textobject.textLine(f"\n{title}")
#         textobject.textLine("-" * 90)
#         for line in content.split('\n'):
#             textobject.textLine(line)
#         textobject.textLine("\n")

#     c.drawText(textobject)
#     c.save()

# @app.post("/extract-text")
# async def extract_text(
#     file: UploadFile = File(...),
#     # quiz_count: int = Form(...),
#     # difficulty: str = Form(...)
# ):
#     contents = await file.read()
#     image = Image.open(io.BytesIO(contents))
#     extracted_text = image_to_string(image)

#     topics = clean_and_split_text(extracted_text)
#     print(topics)
#     # Explain each topic individually
#     explained_topics = []
#     for topic in topics:
#         explanation = generate_explanation(topic)
#         explained_topics.append((topic, explanation))
#     print(explained_topics)
#     # Assignments & Presentations
#     assignments_prompt = f"Generate assignment topics from this course content: {', '.join(topics)}"
#     assignments = generate_prompt_with_model(assignments_prompt)
#     print(assignments)
#     presentations_prompt = f"Suggest presentation topics for these contents: {', '.join(topics)}"
#     presentations = generate_prompt_with_model(presentations_prompt)
#     print(presentations)
#     # Quiz, Mid, Final
#     quiz_prompt = f"Create {1} quizzes from this content \"{extracted_text}\" with easy level. Each quiz should include MCQs, True/False, and Short Questions."
#     quiz = generate_prompt_with_model(quiz_prompt)
#     print(quiz)
#     paper_prompt = f"Create Mid-Term and Final-Term papers with easy level from this content \"{extracted_text}\"."
#     papers = generate_prompt_with_model(paper_prompt)
#     print(papers)
#     # Timeline generation
#     timeline_prompt = f"Create a timeline to cover the following topics in a 3-month course: {', '.join(topics)}"
#     timeline = generate_prompt_with_model(timeline_prompt)
#     print(timeline)
#     # PDF generation
#     sections = explained_topics + [
#         ("Assignment Topics", assignments),
#         ("Presentation Topics", presentations),
#         ("Quizzes", quiz),
#         ("Mid-Term and Final-Term Papers", papers),
#         ("Course Timeline", timeline)
#     ]

#     output_dir = "pdf_files"
#     os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
#     filename = os.path.join(output_dir, f"course_output_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
#     save_to_pdf(filename, sections)

#     return {"download_url": filename}


from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pytesseract import image_to_string
from PIL import Image
from datetime import datetime
import io, os, re, requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory to serve PDFs
app.mount("/pdf_files", StaticFiles(directory="pdf_files"), name="pdfs")

# ⛔ Replace this with your real OpenRouter API key
API_KEY = "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"

# Query LLaMA 3 using OpenRouter
def query_llama3(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost",
        "Content-Type": "application/json"
    }

    body = {
        "model": "meta-llama/llama-3-70b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body)

    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

# Clean and split text into topics
def clean_and_split_text(text):
    topics = re.split(r'[\n,;•-]+', text)
    return [t.strip() for t in topics if t.strip()]

# Generate explanation for one topic
def generate_explanation(topic):
    prompt = f"Explain this topic in simple terms for beginners: {topic}"
    return query_llama3(prompt)

# General prompt generator
def generate_prompt_with_model(prompt):
    return query_llama3(prompt)

# Save a section to a separate PDF
def save_section_to_pdf(filename, title, content):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    textobject = c.beginText(40, height - 40)
    textobject.setFont("Helvetica-Bold", 14)
    textobject.textLine(title)
    textobject.textLine("-" * 90)
    textobject.setFont("Helvetica", 12)

    for line in content.split('\n'):
        if textobject.getY() <= 50:
            c.drawText(textobject)
            c.showPage()
            textobject = c.beginText(40, height - 40)
            textobject.setFont("Helvetica", 12)
        textobject.textLine(line)

    c.drawText(textobject)
    c.save()

# OCR + AI + PDF generation endpoint
@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    extracted_text = image_to_string(image)

    topics = clean_and_split_text(extracted_text)

    # 1. Topic Explanations
    explained_topics = []
    for topic in topics:
        explanation = generate_explanation(topic)
        explained_topics.append((topic, explanation))

    explanations_text = "\n\n".join([f"{title}\n{'-'*50}\n{content}" for title, content in explained_topics])

    # 2. Assignments
    assignments_prompt = f"Generate assignment topics from this course content: {', '.join(topics)}"
    assignments = generate_prompt_with_model(assignments_prompt)

    # 3. Presentations
    presentations_prompt = f"Suggest presentation topics for these contents: {', '.join(topics)}"
    presentations = generate_prompt_with_model(presentations_prompt)

    # 4. Quizzes
    quiz_prompt = f"Create 1 quiz from this content \"{extracted_text}\" with easy level. Include MCQs, True/False, and Short Questions."
    quiz = generate_prompt_with_model(quiz_prompt)

    # 5. Mid & Final Term Papers
    paper_prompt = f"Create Mid-Term and Final-Term papers with easy level from this content \"{extracted_text}\"."
    papers = generate_prompt_with_model(paper_prompt)

    # 6. Course Timeline
    timeline_prompt = f"Create a timeline to cover the following topics in a 3-month course: {', '.join(topics)}"
    timeline = generate_prompt_with_model(timeline_prompt)

    # Create output directory
    output_dir = "pdf_files"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Save each section to its own PDF
    explanation_file = os.path.join(output_dir, f"explanations_{timestamp}.pdf")
    save_section_to_pdf(explanation_file, "Topic Explanations", explanations_text)

    assignments_file = os.path.join(output_dir, f"assignments_{timestamp}.pdf")
    save_section_to_pdf(assignments_file, "Assignment Topics", assignments)

    presentations_file = os.path.join(output_dir, f"presentations_{timestamp}.pdf")
    save_section_to_pdf(presentations_file, "Presentation Topics", presentations)

    quiz_file = os.path.join(output_dir, f"quizzes_{timestamp}.pdf")
    save_section_to_pdf(quiz_file, "Quiz", quiz)

    papers_file = os.path.join(output_dir, f"papers_{timestamp}.pdf")
    save_section_to_pdf(papers_file, "Mid & Final Term Papers", papers)

    timeline_file = os.path.join(output_dir, f"timeline_{timestamp}.pdf")
    save_section_to_pdf(timeline_file, "Course Timeline", timeline)

    # Return URLs for frontend
    return { "response":explanations_text
        # "explanations_pdf": f"/pdf_files/{os.path.basename(explanation_file)}",
        # "assignments_pdf": f"/pdf_files/{os.path.basename(assignments_file)}",
        # "presentations_pdf": f"/pdf_files/{os.path.basename(presentations_file)}",
        # "quizzes_pdf": f"/pdf_files/{os.path.basename(quiz_file)}",
        # "papers_pdf": f"/pdf_files/{os.path.basename(papers_file)}",
        # "timeline_pdf": f"/pdf_files/{os.path.basename(timeline_file)}"
    }
