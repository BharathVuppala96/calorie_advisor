# Import required libraries
import streamlit as st  # for creating the web app
from dotenv import load_dotenv  # for loading API key from .env file
import os
from openai import OpenAI  
from PIL import Image  # for handling images
import base64

# # Load the API key from .env file
# load_dotenv()

# # Set up the Google Gemini AI with your API key
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

client = OpenAI()

def prepare_image(uploaded_file):
    """Convert uploaded image to base64 for GPT-4o"""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        return base64.b64encode(bytes_data).decode("utf-8")
    return None

def get_gpt_response(image_b64, prompt):
    """Send image to GPT-4o and get calorie info"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                    ]
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"
# Main web app
def main():
    # Set up the webpage
    st.set_page_config(page_title="Calorie Advisor", page_icon="🍽️")
    
    # Add title and description
    st.title("🍽️ Calorie Advisor")
    st.write("Upload a photo of your food to get calorie information!")

    # Create file uploader
    uploaded_file = st.file_uploader(
        "Upload your food image (jpg, jpeg, or png)",
        type=["jpg", "jpeg", "png"]
    )

    # Display uploaded image
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Food Image", use_column_width=True)

        # Create Analyze button
        if st.button("Calculate Calories"):
            with st.spinner("Analyzing your food..."):
                # Prepare the prompt for AI
                prompt = """
                Please analyze this food image and provide:
                1. List each food item and its calories
                2. Total calories
                3. Simple health advice

                Format like this:
                FOOD ITEMS:
                1. [Food Item] - [Calories]
                2. [Food Item] - [Calories]

                TOTAL CALORIES: [Number]

                HEALTH TIPS:
                • [Tip 1]
                • [Tip 2]
                """

                # Get and display AI response
                image_data = prepare_image(uploaded_file)
                if image_data is not None:
                    response = get_gpt_response(image_data, prompt)
                    st.success("Analysis Complete!")
                    st.write(response)
                else:
                    st.error("Please upload an image first!")

# Run the app
if __name__ == "__main__":
    main()
