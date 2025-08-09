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

# from fastapi import FastAPI, File, UploadFile, Form
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from pytesseract import image_to_string
# from PIL import Image
# from datetime import datetime
# import io, os, re, requests, textwrap
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4

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

# # ⬇️ PDF Writer with line wrapping
# def save_section_to_pdf(filename, title, content, max_width=90):
#     c = canvas.Canvas(filename, pagesize=A4)
#     width, height = A4
#     textobject = c.beginText(40, height - 40)
#     textobject.setFont("Helvetica-Bold", 14)
#     textobject.textLine(title)
#     textobject.textLine("-" * 90)
#     textobject.setFont("Helvetica", 12)

#     for line in content.split('\n'):
#         wrapped_lines = textwrap.wrap(line, width=max_width)
#         for wline in wrapped_lines:
#             if textobject.getY() <= 50:
#                 c.drawText(textobject)
#                 c.showPage()
#                 textobject = c.beginText(40, height - 40)
#                 textobject.setFont("Helvetica", 12)
#             textobject.textLine(wline)

#     c.drawText(textobject)
#     c.save()

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

#     save_section_to_pdf(os.path.join(output_dir, f"explanations_{timestamp}.pdf"), "Topic Explanations", explanations_text)
#     save_section_to_pdf(os.path.join(output_dir, f"assignments_{timestamp}.pdf"), "Assignment Topics", assignments)
#     save_section_to_pdf(os.path.join(output_dir, f"presentations_{timestamp}.pdf"), "Presentation Topics", presentations)
#     save_section_to_pdf(os.path.join(output_dir, f"quizzes_{timestamp}.pdf"), "Quiz", quiz)
#     save_section_to_pdf(os.path.join(output_dir, f"papers_{timestamp}.pdf"), "Mid & Final Term Papers", papers)
#     save_section_to_pdf(os.path.join(output_dir, f"timeline_{timestamp}.pdf"), "Course Timeline", timeline)

#     return {
#         "response": explanations_text
#     }



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




# ******************************************************************************************

# from fastapi import FastAPI, File, UploadFile, Form
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from pytesseract import image_to_string
# from PIL import Image
# from datetime import datetime
# import io, os, re, requests, textwrap
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from typing import List, Optional

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

# # Modular generators
# def generate_assignments(topics,assignmentCount):
#     return generate_prompt_with_model(f"Generate  {assignmentCount} assignment topics from this course content: {', '.join(topics)}")

# def generate_presentations(topics,presentationCount):
#     return generate_prompt_with_model(f"Suggest {presentationCount} presentation topics for these contents: {', '.join(topics)}")

# def generate_quiz(text,quizDifficulty,mcqsCount,trueFalseCount,shortQCount,LongQCount):
#     return generate_prompt_with_model(f"Create 1 quiz from this content \"{text}\" with {quizDifficulty} level. Include {mcqsCount} MCQ's with four options (a,b,c,d), {trueFalseCount} True/False,{shortQCount} Short Questions and {LongQCount} Long Questions?")

# def summarize_text(text: str):
#         prompt = f"Summarize the following content in a short phrase (max 10 words): {text[:1000]}"
#         return generate_prompt_with_model(prompt)

# def generate_mid_papers(text,midMcqsCount,midTrueFalseCount,midShortQCount,midLongQCount):
#     return generate_prompt_with_model(f"Create a Final-Term paper including {midMcqsCount} mcqs with options, {midTrueFalseCount} true/false, {midShortQCount} short questions and {midLongQCount} long questions  from this content \"{text}\".")

# def generate_final_papers(text,finalMcqsCount,finalTrueFalseCount,finalShortQCount,finalLongQCount):
#     return generate_prompt_with_model(f"Create a Final-Term paper including {finalMcqsCount} mcqs with options, {finalTrueFalseCount} true/false, {finalShortQCount} short questions and {finalLongQCount} long questions  from this content \"{text}\".")

# def generate_timeline(topics):
#     return generate_prompt_with_model(f"Create a timeline to cover the following topics in a 3-month course: {', '.join(topics)}")

# # ⬇️ PDF Writer with line wrapping
# def save_section_to_pdf(filename, title, content, max_width=90):
#     c = canvas.Canvas(filename, pagesize=A4)
#     width, height = A4
#     textobject = c.beginText(40, height - 40)
#     textobject.setFont("Helvetica-Bold", 14)
#     textobject.textLine(title)
#     textobject.textLine("-" * 90)
#     textobject.setFont("Helvetica", 12)

#     for line in content.split('\n'):
#         wrapped_lines = textwrap.wrap(line, width=max_width)
#         for wline in wrapped_lines:
#             if textobject.getY() <= 50:
#                 c.drawText(textobject)
#                 c.showPage()
#                 textobject = c.beginText(40, height - 40)
#                 textobject.setFont("Helvetica", 12)
#             textobject.textLine(wline)

#     c.drawText(textobject)
#     c.save()

# @app.post("/extract-text")
# async def extract_text(
#     file: UploadFile = File(...),
#     userid: str = Form(...),
#     submissionId: str = Form(...),
#     features: List[str] = Form(...),
#         # Quiz counts
#     mcqsCount: Optional[int] = Form(None),
#     trueFalseCount: Optional[int] = Form(None),
#     shortQCount: Optional[int] = Form(None),
#     longQCount: Optional[int] = Form(None),
#     quizDifficulty: Optional[str] = Form(None),

#     # Midterm counts
#     midMcqsCount: Optional[int] = Form(None),
#     midTrueFalseCount: Optional[int] = Form(None),
#     midShortQCount: Optional[int] = Form(None),
#     midLongQCount: Optional[int] = Form(None),

#     # Finalterm counts
#     finalMcqsCount: Optional[int] = Form(None),
#     finalTrueFalseCount: Optional[int] = Form(None),
#     finalShortQCount: Optional[int] = Form(None),
#     finalLongQCount: Optional[int] = Form(None),

#     # Assignment and Presentation counts
#     assignmentCount: Optional[int] = Form(None),
#     presentationCount: Optional[int] = Form(None),
    
# ):  
#     print(f"📥 Incoming Upload: UserID={userid}, SubmissionID={submissionId}, File={file.filename}, Features={features}, "
#       f"📝 Quiz: MCQs={mcqsCount}, TF={trueFalseCount}, ShortQ={shortQCount}, LongQ={longQCount}, "
#       f"🧪 Mid: MCQs={midMcqsCount}, TF={midTrueFalseCount}, ShortQ={midShortQCount}, LongQ={midLongQCount}, "
#       f"🧾 Final: MCQs={finalMcqsCount}, TF={finalTrueFalseCount}, ShortQ={finalShortQCount}, LongQ={finalLongQCount}, "
#       f"📚 Other: Assignments={assignmentCount}, Presentations={presentationCount}")
#     print(f"Features------------------------------->  {features}")
#     contents = await file.read()
#     folder_path = create_submission_folder(submissionId)
#     image_path = os.path.join(folder_path, file.filename)

#     with open(image_path, "wb") as buffer:
#         buffer.write(contents)
#     print("Folder created and image saved.")

#     image = Image.open(io.BytesIO(contents))
#     extracted_text = image_to_string(image)
#     topics = clean_and_split_text(extracted_text)
    
#     # ⬇️ Generate summarized name for DB (not for folder)
#     summary = summarize_text(extracted_text)
#     clean_summary = re.sub(r'[^a-zA-Z0-9_\- ]', '', summary).strip()
#     request_name = clean_summary  # store in DB

#     explained_topics = []
#     output_dir = folder_path + "/" 
#     os.makedirs(output_dir, exist_ok=True)
#     timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

#     response_data = {}
    
   

#     if "Notes" in features:
#         for topic in topics:
#             explanation = generate_explanation(topic)
#             explained_topics.append((topic, explanation))
#         explanations_text = "\n\n".join([f"{title}\n{'-'*50}\n{content}" for title, content in explained_topics])
#         save_section_to_pdf(os.path.join(output_dir, f"explanations_{timestamp}.pdf"), "Topic Explanations", explanations_text)
#         response_data["explanations"] = explanations_text

#     if "Assignments" in features:
#         assignments = generate_assignments(topics,assignmentCount)
#         save_section_to_pdf(os.path.join(output_dir, f"assignments_{timestamp}.pdf"), "Assignment Topics", assignments)
#         response_data["assignments"] = assignments

#     if "Presentations" in features:
#         presentations = generate_presentations(topics,presentationCount)
#         save_section_to_pdf(os.path.join(output_dir, f"presentations_{timestamp}.pdf"), "Presentation Topics", presentations)
#         response_data["presentations"] = presentations

#     if "Quiz" in features:
#         quiz = generate_quiz(extracted_text,quizDifficulty,mcqsCount,trueFalseCount,shortQCount,longQCount)
#         save_section_to_pdf(os.path.join(output_dir, f"quizzes_{timestamp}.pdf"), "Quiz", quiz)
#         response_data["quiz"] = quiz

#     if "Midterm" in features:
#         papers = generate_mid_papers(extracted_text,midMcqsCount,midTrueFalseCount,midShortQCount,midLongQCount)
#         save_section_to_pdf(os.path.join(output_dir, f"papers_{timestamp}.pdf"), "Mid Term Papers", papers)
#         response_data["papers"] = papers
        
#     if "Finalterm" in features:
#         papers = generate_final_papers(extracted_text,finalMcqsCount,finalTrueFalseCount,finalShortQCount,finalLongQCount)
#         save_section_to_pdf(os.path.join(output_dir, f"papers_{timestamp}.pdf"), "Final Term Papers", papers)
#         response_data["papers"] = papers

#     if "timeline" in features:
#         timeline = generate_timeline(topics)
#         save_section_to_pdf(os.path.join(output_dir, f"timeline_{timestamp}.pdf"), "Course Timeline", timeline)
#         response_data["timeline"] = timeline
        
#     print(request_name)
#     return {
#         "response": request_name
#     }


# import shutil
# from fastapi import FastAPI, File, HTTPException, UploadFile, Form, BackgroundTasks, WebSocket
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from pytesseract import image_to_string
# from PIL import Image
# from datetime import datetime
# import io, os, re, requests, textwrap
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from typing import List, Optional
# import json

# app = FastAPI()
# current_userid = ""
# websocket_connections = {}  # Store WebSocket connections by user_id

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

# def generate_assignments(topics, assignmentCount):
#     return generate_prompt_with_model(f"Generate {assignmentCount} assignment topics from this course content: {', '.join(topics)}")

# def generate_presentations(topics, presentationCount):
#     return generate_prompt_with_model(f"Suggest {presentationCount} presentation topics for these contents: {', '.join(topics)}")

# def generate_quiz(text, quizDifficulty, mcqsCount, trueFalseCount, shortQCount, longQCount):
#     return generate_prompt_with_model(f"Create 1 quiz from this content \"{text}\" with {quizDifficulty} level. Include {mcqsCount} MCQ's with four options (a,b,c,d), {trueFalseCount} True/False,{shortQCount} Short Questions and {longQCount} Long Questions?")

# def summarize_text(text: str):
#     prompt = f"Summarize the following content in a short phrase (max 10 words): {text[:1000]}"
#     return generate_prompt_with_model(prompt)

# def generate_mid_papers(text, midMcqsCount, midTrueFalseCount, midShortQCount, midLongQCount):
#     return generate_prompt_with_model(f"Create a Final-Term paper including {midMcqsCount} mcqs with options, {midTrueFalseCount} true/false, {midShortQCount} short questions and {midLongQCount} long questions  from this content \"{text}\".")

# def generate_final_papers(text, finalMcqsCount, finalTrueFalseCount, finalShortQCount, finalLongQCount):
#     return generate_prompt_with_model(f"Create a Final-Term paper including {finalMcqsCount} mcqs with options, {finalTrueFalseCount} true/false, {finalShortQCount} short questions and {finalLongQCount} long questions  from this content \"{text}\".")

# def generate_timeline(topics):
#     return generate_prompt_with_model(f"Create a timeline to cover the following topics in a 3-month course: {', '.join(topics)}")

# def save_section_to_pdf(filename, title, content, max_width=90):
#     c = canvas.Canvas(filename, pagesize=A4)
#     width, height = A4
#     textobject = c.beginText(40, height - 40)
#     textobject.setFont("Helvetica-Bold", 14)
#     textobject.textLine(title)
#     textobject.textLine("-" * 90)
#     textobject.setFont("Helvetica", 12)

#     for line in content.split('\n'):
#         wrapped_lines = textwrap.wrap(line, width=max_width)
#         for wline in wrapped_lines:
#             if textobject.getY() <= 50:
#                 c.drawText(textobject)
#                 c.showPage()
#                 textobject = c.beginText(40, height - 40)
#                 textobject.setFont("Helvetica", 12)
#             textobject.textLine(wline)

#     c.drawText(textobject)
#     c.save()

# async def process_file_generation(
#     contents: bytes,
#     file_name: Optional[str],
#     prompt:Optional[str],
#     userid: str,
#     submissionId: str,
#     features: List[str],
#     mcqsCount: Optional[int],
#     trueFalseCount: Optional[int],
#     shortQCount: Optional[int],
#     longQCount: Optional[int],
#     quizDifficulty: Optional[str],
#     midMcqsCount: Optional[int],
#     midTrueFalseCount: Optional[int],
#     midShortQCount: Optional[int],
#     midLongQCount: Optional[int],
#     finalMcqsCount: Optional[int],
#     finalTrueFalseCount: Optional[int],
#     finalShortQCount: Optional[int],
#     finalLongQCount: Optional[int],
#     assignmentCount: Optional[int],
#     presentationCount: Optional[int],
# ):
#     print(f"📥 Background Task Started: UserID={userid}, SubmissionID={submissionId}, File={file_name}, Features={features}")
#     folder_path = create_submission_folder(submissionId)
#     image_path = os.path.join(folder_path, file_name)

#     with open(image_path, "wb") as buffer:
#         buffer.write(contents)
#     print("Folder created and image saved.")

#     image = Image.open(io.BytesIO(contents))
#     extracted_text = image_to_string(image)
#     topics = clean_and_split_text(extracted_text)
#     output_dir = folder_path + "/"
#     os.makedirs(output_dir, exist_ok=True)
#     timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

#     response_data = {}

#     if "Notes" in features:
#         explained_topics = [(topic, generate_explanation(topic)) for topic in topics]
#         explanations_text = "\n\n".join([f"{title}\n{'-'*50}\n{content}" for title, content in explained_topics])
#         save_section_to_pdf(os.path.join(output_dir, f"explanations_{timestamp}.pdf"), "Topic Explanations", explanations_text)
#         response_data["explanations"] = explanations_text

#     if "Assignments" in features:
#         assignments = generate_assignments(topics, assignmentCount)
#         save_section_to_pdf(os.path.join(output_dir, f"assignments_{timestamp}.pdf"), "Assignment Topics", assignments)
#         response_data["assignments"] = assignments

#     if "Presentations" in features:
#         presentations = generate_presentations(topics, presentationCount)
#         save_section_to_pdf(os.path.join(output_dir, f"presentations_{timestamp}.pdf"), "Presentation Topics", presentations)
#         response_data["presentations"] = presentations

#     if "Quiz" in features:
#         quiz = generate_quiz(extracted_text, quizDifficulty, mcqsCount, trueFalseCount, shortQCount, longQCount)
#         save_section_to_pdf(os.path.join(output_dir, f"quizzes_{timestamp}.pdf"), "Quiz", quiz)
#         response_data["quiz"] = quiz

#     if "Midterm" in features:
#         papers = generate_mid_papers(extracted_text, midMcqsCount, midTrueFalseCount, midShortQCount, midLongQCount)
#         save_section_to_pdf(os.path.join(output_dir, f"papers_mid_{timestamp}.pdf"), "Mid Term Papers", papers)
#         response_data["mid_papers"] = papers

#     if "Finalterm" in features:
#         papers = generate_final_papers(extracted_text, finalMcqsCount, finalTrueFalseCount, finalShortQCount, finalLongQCount)
#         save_section_to_pdf(os.path.join(output_dir, f"papers_final_{timestamp}.pdf"), "Final Term Papers", papers)
#         response_data["final_papers"] = papers

#     if "timeline" in features:
#         timeline = generate_timeline(topics)
#         save_section_to_pdf(os.path.join(output_dir, f"timeline_{timestamp}.pdf"), "Course Timeline", timeline)
#         response_data["timeline"] = timeline

#     # Notify user via WebSocket
#     if userid in websocket_connections:
#         ws = websocket_connections[userid]
#         await ws.send_text(json.dumps({
#             "status": "completed",
#             "submissionId": submissionId,
#             "message": "File generation completed.",
#             "files": [f"/pdf_files/{submissionId}/{f}" for f in os.listdir(output_dir) if f.endswith('.pdf')]
#         }))
#     print(f"✅ Background Task Completed: UserID={userid}, SubmissionID={submissionId}")

# @app.websocket("/ws/{user_id}")
# async def websocket_endpoint(websocket: WebSocket, user_id: str):
#     await websocket.accept()
#     websocket_connections[user_id] = websocket
#     try:
#         while True:
#             data = await websocket.receive_text()
#             print(f"WebSocket received: {data} from UserID={user_id}")
#     except Exception as e:
#         print(f"WebSocket closed for UserID={user_id}: {e}")
#     finally:
#         websocket_connections.pop(user_id, None)
        
        
# SUBMISSIONS_DIR = "../edu_pilot/public/pdf_files"
# # --- DELETE Endpoint ---
# @app.delete("/api/submissions/{submission_id}")
# def delete_submission(submission_id):
#     try:
      

#         # --- Step 2: Delete Folder ---
#         folder_path = os.path.join(SUBMISSIONS_DIR, str(submission_id))
#         if os.path.exists(folder_path):
#             shutil.rmtree(folder_path)  # deletes folder and all its contents

#         return {"message": "Submission and files deleted successfully."}

#     except Exception as e:
#         print("Error:", e)
#         raise HTTPException(status_code=500, detail="Failed to delete submission")





# @app.post("/extract-text")
# async def extract_text(
#     background_tasks: BackgroundTasks,
#     file: Optional[UploadFile] = File(...),
#     prompt: Optional[str] = Form(...),
#     userid: str = Form(...),
#     submissionId: str = Form(...),
#     features: List[str] = Form(...),
#     mcqsCount: Optional[int] = Form(None),
#     trueFalseCount: Optional[int] = Form(None),
#     shortQCount: Optional[int] = Form(None),
#     longQCount: Optional[int] = Form(None),
#     quizDifficulty: Optional[str] = Form(None),
#     midMcqsCount: Optional[int] = Form(None),
#     midTrueFalseCount: Optional[int] = Form(None),
#     midShortQCount: Optional[int] = Form(None),
#     midLongQCount: Optional[int] = Form(None),
#     finalMcqsCount: Optional[int] = Form(None),
#     finalTrueFalseCount: Optional[int] = Form(None),
#     finalShortQCount: Optional[int] = Form(None),
#     finalLongQCount: Optional[int] = Form(None),
#     assignmentCount: Optional[int] = Form(None),
#     presentationCount: Optional[int] = Form(None),
# ):
#     print(f"📥 Incoming Upload: UserID={userid}, SubmissionID={submissionId}, File={file.filename},Prompt = {prompt}")
#     contents = await file.read()
#     image = Image.open(io.BytesIO(contents))
#     extracted_text = image_to_string(image)

#     # Generate summarized name for DB
#     summary = summarize_text(extracted_text)
#     clean_summary = re.sub(r'[^a-zA-Z0-9_\- ]', '', summary).strip()
#     request_name = clean_summary

#     # Schedule file generation in background
#     background_tasks.add_task(
#         process_file_generation,
#         contents,
#         file.filename,
#         userid,
#         submissionId,
#         features,
#         mcqsCount,
#         trueFalseCount,
#         shortQCount,
#         longQCount,
#         quizDifficulty,
#         midMcqsCount,
#         midTrueFalseCount,
#         midShortQCount,
#         midLongQCount,
#         finalMcqsCount,
#         finalTrueFalseCount,
#         finalShortQCount,
#         finalLongQCount,
#         assignmentCount,
#         presentationCount,
#     )

#     return {
#         "response": request_name,
#         "submissionId": submissionId,
#         "status": "processing"
#     }

import shutil
from fastapi import FastAPI, File, HTTPException, UploadFile, Form, BackgroundTasks, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pytesseract import image_to_string
from PIL import Image
from datetime import datetime
import io, os, re, requests, textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from typing import List, Optional
import json

app = FastAPI()
current_userid = ""
websocket_connections = {}  # Store WebSocket connections by user_id

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

def generate_assignments(topics, assignmentCount):
    return generate_prompt_with_model(f"Generate {assignmentCount} assignment topics from this course content: {', '.join(topics)}")

def generate_presentations(topics, presentationCount):
    return generate_prompt_with_model(f"Suggest {presentationCount} presentation topics for these contents: {', '.join(topics)}")

def generate_quiz(text, quizDifficulty, mcqsCount, trueFalseCount, shortQCount, longQCount):
    return generate_prompt_with_model(f"Create 1 quiz from this content \"{text}\" with {quizDifficulty} level. Include {mcqsCount} MCQ's with four options (a,b,c,d), {trueFalseCount} True/False,{shortQCount} Short Questions and {longQCount} Long Questions?")

def summarize_text(text: str):
    prompt = f"Summarize the following content in a short phrase (max 10 words): {text[:1000]}"
    return generate_prompt_with_model(prompt)

def generate_mid_papers(text, midMcqsCount, midTrueFalseCount, midShortQCount, midLongQCount):
    return generate_prompt_with_model(f"Create a Mid-Term paper including {midMcqsCount} mcqs with options, {midTrueFalseCount} true/false, {midShortQCount} short questions and {midLongQCount} long questions from this content \"{text}\".")

def generate_final_papers(text, finalMcqsCount, finalTrueFalseCount, finalShortQCount, finalLongQCount):
    return generate_prompt_with_model(f"Create a Final-Term paper including {finalMcqsCount} mcqs with options, {finalTrueFalseCount} true/false, {finalShortQCount} short questions and {finalLongQCount} long questions from this content \"{text}\".")

def generate_timeline(topics):
    return generate_prompt_with_model(f"Create a timeline to cover the following topics in a 3-month course: {', '.join(topics)}")

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

async def process_file_generation(
    extracted_text: str,
    file_name: Optional[str],
    userid: str,
    submissionId: str,
    features: List[str],
    mcqsCount: Optional[int],
    trueFalseCount: Optional[int],
    shortQCount: Optional[int],
    longQCount: Optional[int],
    quizDifficulty: Optional[str],
    midMcqsCount: Optional[int],
    midTrueFalseCount: Optional[int],
    midShortQCount: Optional[int],
    midLongQCount: Optional[int],
    finalMcqsCount: Optional[int],
    finalTrueFalseCount: Optional[int],
    finalShortQCount: Optional[int],
    finalLongQCount: Optional[int],
    assignmentCount: Optional[int],
    presentationCount: Optional[int],
):
    print(f"📥 Background Task Started: UserID={userid}, SubmissionID={submissionId}, File={file_name}, Features={features}")
    folder_path = create_submission_folder(submissionId)
    output_dir = folder_path + "/"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    topics = clean_and_split_text(extracted_text)
    response_data = {}

    if "Notes" in features:
        explained_topics = [(topic, generate_explanation(topic)) for topic in topics]
        explanations_text = "\n\n".join([f"{title}\n{'-'*50}\n{content}" for title, content in explained_topics])
        save_section_to_pdf(os.path.join(output_dir, f"explanations_{timestamp}.pdf"), "Topic Explanations", explanations_text)
        response_data["explanations"] = explanations_text

    if "Assignments" in features:
        assignments = generate_assignments(topics, assignmentCount)
        save_section_to_pdf(os.path.join(output_dir, f"assignments_{timestamp}.pdf"), "Assignment Topics", assignments)
        response_data["assignments"] = assignments

    if "Presentations" in features:
        presentations = generate_presentations(topics, presentationCount)
        save_section_to_pdf(os.path.join(output_dir, f"presentations_{timestamp}.pdf"), "Presentation Topics", presentations)
        response_data["presentations"] = presentations

    if "Quiz" in features:
        quiz = generate_quiz(extracted_text, quizDifficulty, mcqsCount, trueFalseCount, shortQCount, longQCount)
        save_section_to_pdf(os.path.join(output_dir, f"quizzes_{timestamp}.pdf"), "Quiz", quiz)
        response_data["quiz"] = quiz

    if "Midterm" in features:
        papers = generate_mid_papers(extracted_text, midMcqsCount, midTrueFalseCount, midShortQCount, midLongQCount)
        save_section_to_pdf(os.path.join(output_dir, f"papers_mid_{timestamp}.pdf"), "Mid Term Papers", papers)
        response_data["mid_papers"] = papers

    if "Finalterm" in features:
        papers = generate_final_papers(extracted_text, finalMcqsCount, finalTrueFalseCount, finalShortQCount, finalLongQCount)
        save_section_to_pdf(os.path.join(output_dir, f"papers_final_{timestamp}.pdf"), "Final Term Papers", papers)
        response_data["final_papers"] = papers

    if "timeline" in features:
        timeline = generate_timeline(topics)
        save_section_to_pdf(os.path.join(output_dir, f"timeline_{timestamp}.pdf"), "Course Timeline", timeline)
        response_data["timeline"] = timeline

    if userid in websocket_connections:
        ws = websocket_connections[userid]
        await ws.send_text(json.dumps({
            "status": "completed",
            "submissionId": submissionId,
            "message": "File generation completed.",
            "files": [f"/pdf_files/{submissionId}/{f}" for f in os.listdir(output_dir) if f.endswith('.pdf')]
        }))
    print(f"✅ Background Task Completed: UserID={userid}, SubmissionID={submissionId}")

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    websocket_connections[user_id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            print(f"WebSocket received: {data} from UserID={user_id}")
    except Exception as e:
        print(f"WebSocket closed for UserID={user_id}: {e}")
    finally:
        websocket_connections.pop(user_id, None)

SUBMISSIONS_DIR = "../edu_pilot/public/pdf_files"

@app.delete("/api/submissions/{submission_id}")
def delete_submission(submission_id):
    try:
        folder_path = os.path.join(SUBMISSIONS_DIR, str(submission_id))
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        return {"message": "Submission and files deleted successfully."}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Failed to delete submission")

@app.post("/extract-text")
async def extract_text(
    background_tasks: BackgroundTasks,
    file: Optional[UploadFile] = File(None),
    prompt: Optional[str] = Form(None),
    userid: str = Form(...),
    submissionId: str = Form(...),
    features: List[str] = Form(...),
    mcqsCount: Optional[int] = Form(None),
    trueFalseCount: Optional[int] = Form(None),
    shortQCount: Optional[int] = Form(None),
    longQCount: Optional[int] = Form(None),
    quizDifficulty: Optional[str] = Form(None),
    midMcqsCount: Optional[int] = Form(None),
    midTrueFalseCount: Optional[int] = Form(None),
    midShortQCount: Optional[int] = Form(None),
    midLongQCount: Optional[int] = Form(None),
    finalMcqsCount: Optional[int] = Form(None),
    finalTrueFalseCount: Optional[int] = Form(None),
    finalShortQCount: Optional[int] = Form(None),
    finalLongQCount: Optional[int] = Form(None),
    assignmentCount: Optional[int] = Form(None),
    presentationCount: Optional[int] = Form(None),
):
    extracted_text = None
    file_name = None

    if prompt:
        extracted_text = prompt
        file_name = "prompt_input.txt"
    elif file:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        extracted_text = image_to_string(image)
        file_name = file.filename
    else:
        raise HTTPException(status_code=400, detail="Either 'prompt' or 'file' must be provided.")

    summary = summarize_text(extracted_text)
    clean_summary = re.sub(r'[^a-zA-Z0-9_\- ]', '', summary).strip()
    request_name = clean_summary

    background_tasks.add_task(
        process_file_generation,
        extracted_text,
        file_name,
        userid,
        submissionId,
        features,
        mcqsCount,
        trueFalseCount,
        shortQCount,
        longQCount,
        quizDifficulty,
        midMcqsCount,
        midTrueFalseCount,
        midShortQCount,
        midLongQCount,
        finalMcqsCount,
        finalTrueFalseCount,
        finalShortQCount,
        finalLongQCount,
        assignmentCount,
        presentationCount,
    )

    return {
        "response": request_name,
        "submissionId": submissionId,
        "status": "processing"
    }
