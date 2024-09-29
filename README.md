<div align="center">
  <img width="148" height="148" src="https://github.com/user-attachments/assets/b8b8f3ba-d6da-414e-b5f5-339578b498a8"/>
  <h1>Exercise Manager - Bot</h1>
  <p>Python based telegram bot for workout reminders and tracking exercise completion, including fitness activities like calisthenics and so on.</p>

[![Python](https://img.shields.io/badge/Python-3.12-3777A7?style=flat-square)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.13.1-009CFB?style=flat-square)](hhttps://aiogram.dev/)
[![Fastapi](https://img.shields.io/badge/FastAPI-0.115.0-009688?style=flat-square)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/Pydantic-2.9.2-E92063?style=flat-square)](https://docs.pydantic.dev)
[![Aiohttp](https://img.shields.io/badge/Aiohttp-3.10.5-2C5BB4?style=flat-square)](https://docs.aiohttp.org)
[![Black](https://img.shields.io/badge/Style-Black-black?style=flat-square)](https://black.readthedocs.io/en/stable/)
</div>

# 📃 Notes
* All Docker volumes are stored in the `docker/local/volumes/` folder. If you want to clear your DB or any other data, you can simply delete the folder there.

# ⚒️ Development
1. Download dependencies: `pip install -r requirements.txt`
2. Create an `.env` file or rename `.env.dist` in `.env` and populate it with development variables.
   * For `WEBHOOK_HOST` variable you can use ngrok http tunnel: `ngrok http 8000`
3. Start docker services: `make up_local_services`
4. Compile localization files: `make compile_locales`
   * If the locales directory has changed, you can specify it explicitly: `make compile_locales LOCALES_DIR=new/location/`
5. Run application: `python main.py`
