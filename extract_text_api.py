# from fastapi import FastAPI, File, UploadFile
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.params import Form
# from fastapi.staticfiles import StaticFiles
# from pytesseract import image_to_string
# from PIL import Image
# from datetime import datetime
# import io, os, re, requests
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4

# # Initialize FastAPI
# app = FastAPI()
# current_userid = ""

# # Enable CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# # Serve PDF directory
# app.mount("/pdf_files", StaticFiles(directory="../edu_pilot/public/pdf_files"), name="pdfs")

# # Used to create Folder on each submission
# def create_submission_folder(submission_id: str):
#     folder_path = os.path.join("../edu_pilot/public/pdf_files", submission_id)
#     os.makedirs(folder_path, exist_ok=True)
#     return folder_path

# # 🔁 Use local Mistral model via Ollama
# def query_mistral(prompt: str):
#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={"model": "mistral", "prompt": prompt, "stream": False},
#     )
#     if response.status_code == 200:
#         return response.json().get("response", "").strip()
#     else:
#         return f"Error: {response.status_code} - {response.text}"

# # Clean and split text into topics
# def clean_and_split_text(text):
#     topics = re.split(r'[\n,;•-]+', text)
#     return [t.strip() for t in topics if t.strip()]

# # Generate explanation for one topic
# def generate_explanation(topic):
#     prompt = f"Explain this topic in detail: {topic}"
#     return query_mistral(prompt)

# # General prompt generator
# def generate_prompt_with_model(prompt):
#     return query_mistral(prompt)

# # Save a section to a separate PDF
# def save_section_to_pdf(filename, title, content):
#     c = canvas.Canvas(filename, pagesize=A4)
#     width, height = A4
#     textobject = c.beginText(40, height - 40)
#     textobject.setFont("Helvetica-Bold", 14)
#     textobject.textLine(title)
#     textobject.textLine("-" * 90)
#     textobject.setFont("Helvetica", 12)

#     for line in content.split('\n'):
#         if textobject.getY() <= 50:
#             c.drawText(textobject)
#             c.showPage()
#             textobject = c.beginText(40, height - 40)
#             textobject.setFont("Helvetica", 12)
#         textobject.textLine(line)

#     c.drawText(textobject)
#     c.save()

# # OCR + AI + PDF generation endpoint
# @app.post("/extract-text")
# async def extract_text(file: UploadFile = File(...),userid: str = Form(...),submissionId: str = Form(...)):
#     # Image File Reading from the request
#     contents = await file.read()
#     # Assigning user id after extraction 
#     current_userid = userid
#     # print(current_userid,"Submission_Id",submissionId)
    
#      # Step 1: Create folder named by submission_id
#     folder_path = create_submission_folder(submissionId)

#     # Step 2: Save image file
#     image_path = os.path.join(folder_path, file.filename)
#     # with open(image_path, "wb") as f: 
#     #     f.write(await file.read())
#     with open(image_path, "wb") as buffer:
#         buffer.write(await file.read())
#     print("Folder has been created and the image has been saved!")
        
#     image = Image.open(io.BytesIO(contents))
#     extracted_text = image_to_string(image)
#     topics = clean_and_split_text(extracted_text)
    
#     # 1. Topic Explanations
#     explained_topics = []
#     for topic in topics:
#         explanation = generate_explanation(topic)
#         explained_topics.append((topic, explanation))

#     explanations_text = "\n\n".join([f"{title}\n{'-'*50}\n{content}" for title, content in explained_topics])

#     # 2. Assignments
#     assignments_prompt = f"Generate assignment topics from this course content: {', '.join(topics)}"
#     assignments = generate_prompt_with_model(assignments_prompt)

#     # 3. Presentations
#     presentations_prompt = f"Suggest presentation topics for these contents: {', '.join(topics)}"
#     presentations = generate_prompt_with_model(presentations_prompt)

#     # 4. Quizzes
#     quiz_prompt = f"Create 1 quiz from this content \"{extracted_text}\" with easy level. Include MCQs, True/False, and Short Questions."
#     quiz = generate_prompt_with_model(quiz_prompt)

#     # 5. Mid & Final Term Papers
#     paper_prompt = f"Create Mid-Term and Final-Term papers with easy level from this content \"{extracted_text}\"."
#     papers = generate_prompt_with_model(paper_prompt)

#     # 6. Course Timeline
#     timeline_prompt = f"Create a timeline to cover the following topics in a 3-month course: {', '.join(topics)}"
#     timeline = generate_prompt_with_model(timeline_prompt)

#     # Create output directory
#     output_dir = folder_path+"/"+submissionId
#     os.makedirs(output_dir, exist_ok=True)
#     timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

#     # Save PDFs
#     explanation_file = os.path.join(output_dir, f"explanations_{timestamp}.pdf")
#     save_section_to_pdf(explanation_file, "Topic Explanations", explanations_text)

#     assignments_file = os.path.join(output_dir, f"assignments_{timestamp}.pdf")
#     save_section_to_pdf(assignments_file, "Assignment Topics", assignments)

#     presentations_file = os.path.join(output_dir, f"presentations_{timestamp}.pdf")
#     save_section_to_pdf(presentations_file, "Presentation Topics", presentations)

#     quiz_file = os.path.join(output_dir, f"quizzes_{timestamp}.pdf")
#     save_section_to_pdf(quiz_file, "Quiz", quiz)

#     papers_file = os.path.join(output_dir, f"papers_{timestamp}.pdf")
#     save_section_to_pdf(papers_file, "Mid & Final Term Papers", papers)

#     timeline_file = os.path.join(output_dir, f"timeline_{timestamp}.pdf")
#     save_section_to_pdf(timeline_file, "Course Timeline", timeline)

#     # Return text for testing or debugging
#     print(explained_topics,timeline,presentations,papers)
#     return {
#         "response": explanations_text
#         # You can also return PDF URLs here if frontend needs them
#     }





#####################################################################################################

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pytesseract import image_to_string
from PIL import Image
from datetime import datetime
import io, os, re, requests, textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

app = FastAPI()
current_userid = ""

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/pdf_files", StaticFiles(directory="../edu_pilot/public/pdf_files"), name="pdfs")

def create_submission_folder(submission_id: str):
    folder_path = os.path.join("../edu_pilot/public/pdf_files", submission_id)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def query_mistral(prompt: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "mistral", "prompt": prompt, "stream": False},
    )
    if response.status_code == 200:
        return response.json().get("response", "").strip()
    return f"Error: {response.status_code} - {response.text}"

def clean_and_split_text(text):
    topics = re.split(r'[\n,;•-]+', text)
    return [t.strip() for t in topics if t.strip()]

def generate_explanation(topic):
    prompt = f"Explain this topic in detail: {topic}"
    return query_mistral(prompt)

def generate_prompt_with_model(prompt):
    return query_mistral(prompt)

# ⬇️ PDF Writer with line wrapping
def save_section_to_pdf(filename, title, content, max_width=90):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    textobject = c.beginText(40, height - 40)
    textobject.setFont("Helvetica-Bold", 14)
    textobject.textLine(title)
    textobject.textLine("-" * 90)
    textobject.setFont("Helvetica", 12)

    for line in content.split('\n'):
        wrapped_lines = textwrap.wrap(line, width=max_width)
        for wline in wrapped_lines:
            if textobject.getY() <= 50:
                c.drawText(textobject)
                c.showPage()
                textobject = c.beginText(40, height - 40)
                textobject.setFont("Helvetica", 12)
            textobject.textLine(wline)

    c.drawText(textobject)
    c.save()

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...), userid: str = Form(...), submissionId: str = Form(...)):
    contents = await file.read()
    current_userid = userid
    folder_path = create_submission_folder(submissionId)
    image_path = os.path.join(folder_path, file.filename)

    with open(image_path, "wb") as buffer:
        buffer.write(contents)
    print("Folder created and image saved.")

    image = Image.open(io.BytesIO(contents))
    extracted_text = image_to_string(image)
    topics = clean_and_split_text(extracted_text)

    explained_topics = []
    for topic in topics:
        explanation = generate_explanation(topic)
        explained_topics.append((topic, explanation))
    explanations_text = "\n\n".join([f"{title}\n{'-'*50}\n{content}" for title, content in explained_topics])

    assignments = generate_prompt_with_model(f"Generate assignment topics from this course content: {', '.join(topics)}")
    presentations = generate_prompt_with_model(f"Suggest presentation topics for these contents: {', '.join(topics)}")
    quiz = generate_prompt_with_model(f"Create 1 quiz from this content \"{extracted_text}\" with easy level. Include MCQs, True/False, and Short Questions.")
    papers = generate_prompt_with_model(f"Create Mid-Term and Final-Term papers with easy level from this content \"{extracted_text}\".")
    timeline = generate_prompt_with_model(f"Create a timeline to cover the following topics in a 3-month course: {', '.join(topics)}")

    output_dir = folder_path + "/" + submissionId
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    save_section_to_pdf(os.path.join(output_dir, f"explanations_{timestamp}.pdf"), "Topic Explanations", explanations_text)
    save_section_to_pdf(os.path.join(output_dir, f"assignments_{timestamp}.pdf"), "Assignment Topics", assignments)
    save_section_to_pdf(os.path.join(output_dir, f"presentations_{timestamp}.pdf"), "Presentation Topics", presentations)
    save_section_to_pdf(os.path.join(output_dir, f"quizzes_{timestamp}.pdf"), "Quiz", quiz)
    save_section_to_pdf(os.path.join(output_dir, f"papers_{timestamp}.pdf"), "Mid & Final Term Papers", papers)
    save_section_to_pdf(os.path.join(output_dir, f"timeline_{timestamp}.pdf"), "Course Timeline", timeline)

    return {
        "response": explanations_text
    }



#########################################################################################################################

# from fastapi import FastAPI, File, UploadFile, Form
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from pytesseract import image_to_string
# from PIL import Image
# from datetime import datetime
# import io, os, re, requests
# from docx import Document

# app = FastAPI()
# current_userid = ""

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.mount("/pdf_files", StaticFiles(directory="../edu_pilot/public/pdf_files"), name="pdfs")

# def create_submission_folder(submission_id: str):
#     folder_path = os.path.join("../edu_pilot/public/pdf_files", submission_id)
#     os.makedirs(folder_path, exist_ok=True)
#     return folder_path

# def query_mistral(prompt: str):
#     response = requests.post(
#         "http://localhost:11434/api/generate",
#         json={"model": "mistral", "prompt": prompt, "stream": False},
#     )
#     if response.status_code == 200:
#         return response.json().get("response", "").strip()
#     return f"Error: {response.status_code} - {response.text}"

# def clean_and_split_text(text):
#     topics = re.split(r'[\n,;•-]+', text)
#     return [t.strip() for t in topics if t.strip()]

# def generate_explanation(topic):
#     prompt = f"Explain this topic in detail: {topic}"
#     return query_mistral(prompt)

# def generate_prompt_with_model(prompt):
#     return query_mistral(prompt)

# # ⬇️ DOCX Writer
# def save_section_to_docx(filename, title, content):
#     doc = Document()
#     doc.add_heading(title, level=1)
#     doc.add_paragraph("-" * 90)
#     for line in content.split('\n'):
#         doc.add_paragraph(line)
#     doc.save(filename)

# @app.post("/extract-text")
# async def extract_text(file: UploadFile = File(...), userid: str = Form(...), submissionId: str = Form(...)):
#     contents = await file.read()
#     current_userid = userid
#     folder_path = create_submission_folder(submissionId)
#     image_path = os.path.join(folder_path, file.filename)

#     with open(image_path, "wb") as buffer:
#         buffer.write(contents)
#     print("Folder created and image saved.")

#     image = Image.open(io.BytesIO(contents))
#     extracted_text = image_to_string(image)
#     topics = clean_and_split_text(extracted_text)

#     explained_topics = []
#     for topic in topics:
#         explanation = generate_explanation(topic)
#         explained_topics.append((topic, explanation))
#     explanations_text = "\n\n".join([f"{title}\n{'-'*50}\n{content}" for title, content in explained_topics])

#     assignments = generate_prompt_with_model(f"Generate assignment topics from this course content: {', '.join(topics)}")
#     presentations = generate_prompt_with_model(f"Suggest presentation topics for these contents: {', '.join(topics)}")
#     quiz = generate_prompt_with_model(f"Create 1 quiz from this content \"{extracted_text}\" with easy level. Include MCQs, True/False, and Short Questions.")
#     papers = generate_prompt_with_model(f"Create Mid-Term and Final-Term papers with easy level from this content \"{extracted_text}\".")
#     timeline = generate_prompt_with_model(f"Create a timeline to cover the following topics in a 3-month course: {', '.join(topics)}")

#     output_dir = folder_path + "/" + submissionId
#     os.makedirs(output_dir, exist_ok=True)
#     timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

#     save_section_to_docx(os.path.join(output_dir, f"explanations_{timestamp}.docx"), "Topic Explanations", explanations_text)
#     save_section_to_docx(os.path.join(output_dir, f"assignments_{timestamp}.docx"), "Assignment Topics", assignments)
#     save_section_to_docx(os.path.join(output_dir, f"presentations_{timestamp}.docx"), "Presentation Topics", presentations)
#     save_section_to_docx(os.path.join(output_dir, f"quizzes_{timestamp}.docx"), "Quiz", quiz)
#     save_section_to_docx(os.path.join(output_dir, f"papers_{timestamp}.docx"), "Mid & Final Term Papers", papers)
#     save_section_to_docx(os.path.join(output_dir, f"timeline_{timestamp}.docx"), "Course Timeline", timeline)

#     return {
#         "response": explanations_text
#     }
