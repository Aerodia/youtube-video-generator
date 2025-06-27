# backend/app.py
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file automatically

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai # New import for Gemini API

app = Flask(__name__)
CORS(app)

# --- Configuration for Google Gemini ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
# Updated to a model that is available and supports generateContent
GOOGLE_GEMINI_MODEL = os.environ.get("GOOGLE_GEMINI_MODEL", "models/gemini-1.5-flash-latest")

# Configure the Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# --- Define the Generative Model ---
# This line will initialize the model only once when the app starts
try:
    gemini_model = genai.GenerativeModel(GOOGLE_GEMINI_MODEL)
except Exception as e:
    print(f"Error configuring Gemini model: {e}")
    # Handle the error, maybe exit if the API key is truly missing or invalid
    gemini_model = None # Set to None to indicate configuration failure

# --- Temporary Debugging Function to List Available Models ---
# This function is kept for reference but will not be called in __main__ anymore
def list_available_gemini_models():
    print("\n--- LISTING AVAILABLE GEMINI MODELS ---")
    if not GOOGLE_API_KEY:
        print("GOOGLE_API_KEY not set. Cannot list models.")
        return

    try:
        # Fetch all available models
        all_models = list(genai.list_models())
        
        # Filter for models that support text generation (generateContent)
        text_gen_models = [
            m for m in all_models if 'generateContent' in m.supported_generation_methods
        ]

        if not text_gen_models:
            print("No text generation models found that support 'generateContent' for this API key.")
        else:
            print("Available text generation models (supporting 'generateContent'):")
            for m in text_gen_models:
                print(f"  Name: {m.name}, Display Name: {m.display_name}")
        print("--- END MODEL LIST ---")
    except Exception as e:
        print(f"Error listing models: {e}")
# --- END Temporary Debugging Function ---


# --- Renamed and adapted function for Gemini API ---
def generate_youtube_content_gemini(script_or_summary):
    if not GOOGLE_API_KEY:
        return {"error": "GOOGLE_API_KEY environment variable not set."}
    if gemini_model is None:
        return {"error": "Gemini model could not be configured. Check API key and network."}

    prompt = f"""
    You are an expert YouTube content strategist. Based on the following video script or summary,
    generate 3 catchy, clickbait-style but informative YouTube video titles and a detailed,
    SEO-optimized YouTube video description.

    Focus on:
    - Keywords relevant to the content.
    - Engaging language for titles.
    - A clear summary, timestamps (if applicable, suggest placeholders), calls to action,
      and relevant hashtags for the description.

    ---
    Video Script/Summary:
    {script_or_summary}
    ---

    Format your response as follows:

    TITLES:
    1. [Title 1]
    2. [Title 2]
    3. [Title 3]

    DESCRIPTION:
    [Start with an engaging hook related to the video content.]

    In this video, we'll cover:
    - [Main point 1]
    - [Main point 2]
    - [Main point 3]
    [Add more points as relevant]

    Timestamps:
    0:00 Intro
    [Suggest other key timestamps based on likely video structure, e.g., 1:30 Topic A, 3:45 Topic B]

    🔔 Don't forget to like, comment, and subscribe for more valuable content!
    🔗 Connect with me: [Your Social Media Link] | [Your Website Link]

    #RelevantHashtag1 #RelevantHashtag2 #RelevantHashtag3 #YouTubeTips
    """

    try:
        # Use the generate_content method for the model
        # You can add generation_config for more control, similar to watsonx.ai parameters
        response = gemini_model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=500,
                # top_p is not directly equivalent to repetition_penalty, but affects output diversity.
                # Repetition penalty is not a direct parameter in Gemini's generate_content via SDK.
                # top_p=1.0,
                stop_sequences=["---"], # Gemini uses simpler stop sequences, list of strings
            )
        )
        
        # Access the generated text
        generated_text = ""
        if response.parts:
            for part in response.parts:
                if hasattr(part, 'text'):
                    generated_text += part.text
        # Fallback for direct text access if 'parts' is not the primary way
        elif hasattr(response, 'text') and response.text:
            generated_text = response.text

        if not generated_text:
            # Check if there were any safety ratings that blocked content
            if response.prompt_feedback and response.prompt_feedback.safety_ratings:
                blocked_reasons = [
                    f"Category: {s.category.name}, Probability: {s.probability.name}"
                    for s in response.prompt_feedback.safety_ratings if s.blocked
                ]
                if blocked_reasons:
                    return {"error": f"Content blocked by safety filters: {'; '.join(blocked_reasons)}"}
            return {"error": "No content generated from Gemini. It might be an empty response or another issue."}


        # Parse the content into titles and description (same logic as before)
        try:
            titles_section = generated_text.split("DESCRIPTION:")[0].replace("TITLES:", "").strip()
            description_section = generated_text.split("DESCRIPTION:")[1].strip()

            titles = [line.strip().split('. ', 1)[1] for line in titles_section.split('\n') if line.strip().startswith(tuple(str(i) + "." for i in range(1, 4)))]
            while len(titles) < 3:
                titles.append(f"Generated Title {len(titles) + 1}")

        except IndexError:
            print(f"Warning: Could not parse Gemini response structure. Full response: {generated_text}")
            titles = ["Could not generate specific titles.", "Try rephrasing your summary.", "Default Title"]
            description_section = generated_text # Return raw generated text as description
            
        return {"titles": titles, "description": description_section}

    except Exception as e:
        # Catch specific API errors if needed, but a general exception catch is fine for now
        print(f"Gemini API Error: {e}")
        return {"error": f"Failed to generate content from Gemini: {e}"}

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    script_or_summary = data.get('script_or_summary', '').strip()

    if not script_or_summary:
        return jsonify({"error": "Please provide a video script or summary."}), 400

    # Call the new Gemini generation function
    generated_content = generate_youtube_content_gemini(script_or_summary)

    if "error" in generated_content:
        # Return specific HTTP status codes for different errors
        if "API key" in generated_content["error"] or "Gemini model could not be configured" in generated_content["error"]:
            return jsonify(generated_content), 500
        else:
            return jsonify(generated_content), 500
    else:
        return jsonify(generated_content)

if __name__ == '__main__':
    # Call the model listing function when the app starts (kept for initial diagnostics)
    # You can remove or comment this line out once you've confirmed a working model
    # list_available_gemini_models() # Removed this call as it's for initial debugging
    app.run(debug=True, port=5000)

