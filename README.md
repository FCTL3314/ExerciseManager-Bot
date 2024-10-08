<div align="center">
  <img width="148" height="148" src="https://github.com/user-attachments/assets/b8b8f3ba-d6da-414e-b5f5-339578b498a8"/>
  <h1>Exercise Manager - Bot</h1>
  <p>Telegram bot for managing workout routines, tracking exercise progress, and sending reminders. Supports creating custom workout plans, adding exercises with durations and breaks, and tracking completion of sport activities.</p>

[![Python](https://img.shields.io/badge/Python-3.12-3777A7?style=flat-square)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.13.1-009CFB?style=flat-square)](https://aiogram.dev/)
[![Fastapi](https://img.shields.io/badge/FastAPI-0.115.0-009688?style=flat-square)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.9.2-E92063?style=flat-square)](https://docs.pydantic.dev)
[![Aiohttp](https://img.shields.io/badge/Aiohttp-3.10.5-2C5BB4?style=flat-square)](https://docs.aiohttp.org)
[![Black](https://img.shields.io/badge/Style-Black-black?style=flat-square)](https://black.readthedocs.io/en/stable/)
</div>

# 📃 Notes
* To ensure your application has access to the API endpoints, you need to run the backend server locally using this repository: [ExerciseManager-Backend](https://github.com/FCTL3314/ExerciseManager-Backend). Follow the setup and run instructions provided in the repository.
* All Docker volumes are stored in the `docker/local/volumes/` directory. If you need to reset your database or any other data, simply delete the corresponding folder.

# ⚒️ Development
1. Download dependencies: `pip install -r requirements.txt`
2. Create an `.env` file or rename `.env.dist` to `.env` and fill it with development environment variables.
   * For the `WEBHOOK_HOST` variable, you can use a ngrok HTTP tunnel by running: `ngrok http 8000`
   * For the `API_BASE_URL` variable, use the base URL of your locally installed server, for example: `http://127.0.0.1:8080/api/v1/`
3. Start Docker services: `make up_local_services`
4. Compile localization files: `make compile_locales`
   * If the locales directory has changed, you can specify it explicitly: `make compile_locales LOCALES_DIR=new/location/`
5. Run the application: `python main.py`
