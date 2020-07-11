from src.app import app
from src.config import PORT
import controllers.user_endpoint
import controllers.chat_endpoint

app.run("0.0.0.0", PORT, debug=True)