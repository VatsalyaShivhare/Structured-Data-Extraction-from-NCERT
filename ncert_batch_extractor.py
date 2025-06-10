import os
import re
import json
import subprocess
import time
from pathlib import Path
import pandas as pd

SCIENCE_DIR = "science"
MATH_DIR = "math"
CHUNK_SIZE_WORDS = 300
OLLAMA_MODEL = "mistral"
OLLAMA_TIMEOUT = 180  # seconds

# Output filenames
SCIENCE_OUTPUT = "Science Sample.xlsx"
MATH_OUTPUT = "Math Sample.xlsx"

def chunk_text(text, max_words=CHUNK_SIZE_WORDS):
    words = text.split()
    for i in range(0, len(words), max_words):
        yield " ".join(words[i:i+max_words])

def call_ollama(prompt):
    command = ["ollama", "run", OLLAMA_MODEL]
    try:
        result = subprocess.run(
            command,
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=OLLAMA_TIMEOUT,
        )
        output = result.stdout.decode("utf-8").strip()
        if result.returncode != 0:
            print(f"❌ Ollama error: {result.stderr.decode('utf-8').strip()}")
            return None
        return output
    except subprocess.TimeoutExpired:
        print("❌ Ollama call timed out.")
        return None

def extract_text_from_pdf(pdf_path):
    import fitz
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_json_from_text(text):
    try:
        # First try direct JSON parsing
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
            
        # Try to find JSON with more flexible pattern
        json_pattern = r'(\{(?:[^{}]|(?:\{[^{}]*\}))*\})'
        matches = re.finditer(json_pattern, text, re.DOTALL)
        
        for match in matches:
            try:
                json_data = json.loads(match.group(1))
                if "Chapter" in json_data and "Topics" in json_data:
                    return json_data
            except json.JSONDecodeError:
                continue
                
        return None
    except Exception as e:
        print(f"⚠️ JSON extraction error: {e}")
        return None

def process_pdf(pdf_path):
    print(f"📘 Processing {pdf_path.name}")
    text = extract_text_from_pdf(pdf_path)

    chunks = list(chunk_text(text))
    chunks_responses = []
    
    for i, chunk_text_piece in enumerate(chunks):
        prompt = f"""Extract structured data from this NCERT chapter text into JSON format.
ONLY return valid JSON, no other text. Format:

{{
  "Chapter": "Exact Chapter Title",
  "Topics": [
    {{
      "Topic": "Main Topic Name",
      "Subtopics": [
        {{
          "Sub-topic": "Subtopic Name",
          "Figures": ["Figure 1: Description", "Figure 2: Description"],
          "Tables": ["Table 1: Description", "Table 2: Description"],
          "Examples": ["Example 1: Description", "Example 2: Description"],
          "Exercises": ["Exercise 1", "Exercise 2"],
          "Activities": ["Activity 1: Description", "Activity 2: Description"]
        }}
      ]
    }}
  ]
}}

Text to analyze:
{chunk_text_piece}"""
        # ... rest of the function remains the same ...
def merge_json_chunks(chunks_json):
    merged = None
    for chunk in chunks_json:
        if chunk is None:
            continue
            
        json_data = extract_json_from_text(chunk)
        if not json_data:
            print("⚠️ Failed to extract JSON from chunk")
            continue
            
        if not isinstance(json_data, dict):
            print("⚠️ Extracted data is not a dictionary")
            continue
            
        if merged is None:
            merged = json_data
        else:
            # Merge topics arrays
            if isinstance(json_data.get("Topics"), list):
                merged["Topics"].extend(json_data.get("Topics", []))
    
    return merged

def flatten_json(chapter_json):
    if not chapter_json or not isinstance(chapter_json, dict):
        print("⚠️ Invalid chapter JSON format")
        return []
        
    rows = []
    chapter_name = chapter_json.get("Chapter", "Unknown Chapter")
    topics = chapter_json.get("Topics", [])
    
    if not isinstance(topics, list):
        print("⚠️ Topics is not a list")
        return []
        
    for topic in topics:
        if not isinstance(topic, dict):
            print(f"⚠️ Invalid topic format: {topic}")
            continue
            
        topic_name = topic.get("Topic", "")
        subtopics = topic.get("Subtopics", [])
        
        if not isinstance(subtopics, list):
            print("⚠️ Subtopics is not a list")
            continue
            
        for sub in subtopics:
            if not isinstance(sub, dict):
                print(f"⚠️ Invalid subtopic format: {sub}")
                continue
                
            row = {
                "Chapter": chapter_name,
                "Topic": topic_name,
                "Sub-topic": sub.get("Sub-topic", ""),
                "Figures": ", ".join(str(f) for f in sub.get("Figures", [])),
                "Tables": ", ".join(str(t) for t in sub.get("Tables", [])),
                "Examples": ", ".join(str(e) for e in sub.get("Examples", [])),
                "Exercises": ", ".join(str(ex) for ex in sub.get("Exercises", [])),
                "Activities": ", ".join(str(a) for a in sub.get("Activities", [])),
            }
            rows.append(row)
    return rows

def process_pdf(pdf_path):
    print(f"📘 Processing {pdf_path.name}")
    text = extract_text_from_pdf(pdf_path)

    chunks = list(chunk_text(text))
    chunks_responses = []
    
    for i, chunk_text_piece in enumerate(chunks):
        prompt = f"""Analyze this NCERT chapter text and return ONLY a JSON object with the following structure. Do not include any other text or explanations.

{{
  "Chapter": "Exact Chapter Title",
  "Topics": [
    {{
      "Topic": "Main Topic Name",
      "Subtopics": [
        {{
          "Sub-topic": "Subtopic Name",
          "Figures": ["Figure 1.1: ...", "Figure 1.2: ..."],
          "Tables": ["Table 1: ...", "Table 2: ..."],
          "Examples": ["Example 1: ...", "Example 2: ..."],
          "Exercises": ["Q1. ...", "Q2. ..."],
          "Activities": ["Activity 1: ...", "Activity 2: ..."]
        }}
      ]
    }}
  ]
}}

Text:
{chunk_text_piece}"""

        print(f" → Processing chunk {i+1}/{len(chunks)}")
        response = call_ollama(prompt)
        if response is None:
            print(f"⚠️ Skipping chunk {i+1} due to no response.")
            continue
            
        # Print response preview for debugging
        print(f"📝 Response preview: {response[:100]}...")
        
        chunks_responses.append(response)
        time.sleep(1)  # Increased delay between chunks

    if not chunks_responses:
        print(f"❌ No data extracted from {pdf_path.name}")
        return None

    merged = merge_json_chunks(chunks_responses)
    if merged:
        print(f"✅ Successfully extracted data from {pdf_path.name}")
    return merged
    
def process_folder(folder_name):
    folder_path = Path(folder_name)
    if not folder_path.exists():
        print(f"❌ Folder not found: {folder_name}")
        return []
        
    all_rows = []
    pdf_files = sorted(folder_path.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {folder_name}")
        return []
        
    for pdf_file in pdf_files:
        chapter_json = process_pdf(pdf_file)
        if chapter_json is None:
            continue
        rows = flatten_json(chapter_json)
        all_rows.extend(rows)
    return all_rows

def save_to_excel(data_rows, filename):
    if not data_rows:
        print(f"⚠️ No data to save to {filename}")
        return
        
    df = pd.DataFrame(data_rows, columns=[
        "Chapter", "Topic", "Sub-topic", "Figures", 
        "Tables", "Examples", "Exercises", "Activities"
    ])
    df.to_excel(filename, index=False)
    print(f"✅ Saved {len(data_rows)} rows to {filename}")

def main():
    print("🔄 Starting extraction process...")
    
    science_data = process_folder(SCIENCE_DIR)
    math_data = process_folder(MATH_DIR)

    if science_data:
        save_to_excel(science_data, SCIENCE_OUTPUT)
    else:
        print("⚠️ No Science data to save.")

    if math_data:
        save_to_excel(math_data, MATH_OUTPUT)
    else:
        print("⚠️ No Math data to save.")
        
    print("✨ Process completed!")

if __name__ == "__main__":
    main()