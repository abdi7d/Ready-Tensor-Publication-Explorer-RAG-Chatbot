# app.py
from dotenv import load_dotenv
load_dotenv()  # loads .env
from src.ui.gradio_app import build_and_launch

if __name__ == "__main__":
    build_and_launch()
