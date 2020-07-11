from src.app import app
from src.config import PORT
import src.controllers.user_endpoint
import src.controllers.chat_endpoint

app.run("0.0.0.0", PORT, debug=True)