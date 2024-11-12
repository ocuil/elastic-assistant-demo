from ui.streamlit_app import StreamlitApp
from utils.logging_config import setup_logging

def main():
    # Setup logging
    logger = setup_logging()
    
    try:
        # Run the Streamlit app
        app = StreamlitApp()
        app.run()
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise

if __name__ == "__main__":
    main()