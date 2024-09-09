import openai
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  

root = tk.Tk()
root.title("AI Audio Analyzer")
root.geometry("800x600")
root.config(bg="#f4f4f4")

openai_key = ''

def transcriber(audio_file_path):
    try:
        client = openai.OpenAI(api_key=openai_key)
        with open(audio_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                response_format="verbose_json"
            )
        return transcription.text
    except Exception as e:
        messagebox.showerror("Error", f"Error in transcription: {e}")
        return None

def analyze_discussion(transcript):
    try:
        client = openai.OpenAI(api_key=openai_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an assistant skilled in summarizing academic discussions and identifying areas to focus on for improvement."},
                {"role": "user", "content": f"""
                    Here is a discussion transcript: "{transcript}". 
                    Please analyze this discussion and provide the following details in a structured format:
                    
                    Summary: A brief summary of the discussion.
                    Key Topics: Three key topics related to the discussion (1-2 words each).
                    Sentiments: Three individual words to describe the sentiments in the discussion.
                    Study Recommendations: Three specific study recommendations as bullet points.
                """}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        messagebox.showerror("Error", f"Error in AI analysis: {e}")
        return None

def selectFile():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3 *.wav")])
    if file_path:
        file_label.config(text=f"Selected File: {os.path.basename(file_path)}", fg="green")
        return file_path
    return None

def processAudio():
    audio_file_path = selectFile()
    if audio_file_path:
        transcript = transcriber(audio_file_path)
        
        if transcript:
            summary = analyze_discussion(transcript)

            if summary:
                try:
                    summary_text = summary.split('Key Topics:')[0].split('Summary:')[1].strip()
                    topics_text = summary.split('Key Topics:')[1].split('Sentiments:')[0].strip()
                    sentiments_text = summary.split('Sentiments:')[1].split('Study Recommendations:')[0].strip()
                    recommendations_text = summary.split('Study Recommendations:')[1].strip()
                    
                    summary_label.config(text=f"Summary:\n{summary_text}")
                    
                    for i, topic in enumerate(topics_text.split("\n")[:3]):
                        topic_boxes[i].config(text=f"{topic.strip()}")
                    
                    for i, sentiment in enumerate(sentiments_text.split("\n")[:3]):
                        sentiment_boxes[i].config(text=f"{sentiment.strip()}")
                    
                    recommendations = recommendations_text.split('\n')[:3]
                    for i, recommendation in enumerate(recommendations):
                        recommendation_labels[i].config(text=f"• {recommendation.strip()}")

                except Exception as e:
                    messagebox.showerror("Error", f"Failed to parse the AI response: {e}")

style_font = ("Arial", 14, "bold")
label_font = ("Arial", 12)
button_font = ("Arial", 12)

logo_image = Image.open("logo.png")
logo_image = logo_image.resize((400, 225), Image.LANCZOS)  
logo_photo = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(root, image=logo_photo, bg="#f4f4f4")
logo_label.pack(pady=20)

file_label = tk.Label(root, text="No file selected", font=label_font, bg="#f4f4f4", wraplength=600, fg="black")
file_label.pack(pady=10)

select_button = tk.Button(root, text="Select Audio File", font=button_font, bg="#000000", fg="black", padx=20, pady=10, command=processAudio)
select_button.pack(pady=10)

summary_label = tk.Label(root, text="Summary: \n[Waiting for output]", font=label_font, bg="#f4f4f4", wraplength=600, fg="black")
summary_label.pack(pady=10)

topics_label = tk.Label(root, text="Topics", font=label_font, bg="#f4f4f4", wraplength=600, fg="black")
topics_label.pack(pady=10)

topics_frame = tk.Frame(root, bg="#f4f4f4")
topics_frame.pack(pady=10)

topic_boxes = []
for _ in range(3):
    topic_box = tk.Label(topics_frame, text="", font=label_font, width=20, height=2, bg="#e0e0e0", fg="black", relief=tk.RAISED)
    topic_box.pack(side=tk.LEFT, padx=10, pady=5)
    topic_boxes.append(topic_box)

sentiments_label = tk.Label(root, text="Sentiments", font=label_font, bg="#f4f4f4", wraplength=600, fg="black")
sentiments_label.pack(pady=10)

sentiments_frame = tk.Frame(root, bg="#f4f4f4")
sentiments_frame.pack(pady=10)

sentiment_boxes = []
for _ in range(3):
    sentiment_box = tk.Label(sentiments_frame, text="", font=label_font, width=20, height=2, bg="#e0e0e0", fg="black", relief=tk.RAISED)
    sentiment_box.pack(side=tk.LEFT, padx=10, pady=5)
    sentiment_boxes.append(sentiment_box)

recommendations_label = tk.Label(root, text="Recommendations", font=label_font, bg="#f4f4f4", wraplength=600, fg="black")
recommendations_label.pack(pady=10)

recommendation_labels = []
for _ in range(3):
    rec_label = tk.Label(root, text="", font=label_font, bg="#f4f4f4", fg="black", wraplength=600)
    rec_label.pack(pady=5)
    recommendation_labels.append(rec_label)

root.mainloop()
