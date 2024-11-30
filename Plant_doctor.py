import os
import streamlit as st
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from datetime import datetime
from PIL import Image

# Configure the generative AI model
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Streamlit app
st.title("Plant Doctor")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    # Get the current date
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Define the prompt template with placeholders
    prompt = """You are Plant Doctor. 
    You are tasked with diagnosing the health of the plant in the image. 
    The plant is unhealthy. What is the diagnosis and what is the treatment? 
    Today's date is {date}.
    Mention on which dates what has to be done from today like a prescription.
    Also Mention when should be the next checkup."""

    # Create a PromptTemplate object
    prompt_template = PromptTemplate(template=prompt)

    # Format the prompt with the current date
    formatted_prompt = prompt_template.format(date=current_date)

    # Initialize the generative model
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")

    # Generate content using the formatted prompt
    response = model.generate_content([image, formatted_prompt])

    # Print the response
    st.write(response.text)