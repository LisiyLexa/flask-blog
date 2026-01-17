from app import create_app
from app.logger import setup_logger

logger = setup_logger(__name__)

logger.info("Creating app.")
app = create_app()


if __name__ == "__main__":
    logger.info("Running app.")
    app.run(debug=True)
