<div align="center">
  <img width="148" height="148" src="https://github.com/user-attachments/assets/b8b8f3ba-d6da-414e-b5f5-339578b498a8"/>
  <h1>Exercise Manager - Bot</h1>
  <p>Python based telegram bot for workout reminders and tracking exercise completion, including fitness activities like calisthenics and so on.</p>

[![Go](https://img.shields.io/badge/Go-1.23.1-45a3ec?style=flat-square)](https://go.dev/)
[![Gin](https://img.shields.io/badge/Gin-1.10.0-458cec?style=flat-square)](https://github.com/gin-gonic/gin)
[![Gorm](https://img.shields.io/badge/Gorm-1.25.12-38B6FF?style=flat-square)](https://github.com/go-gorm/gorm)
[![Gorm](https://img.shields.io/badge/Viper-1.19.0-66BC67?style=flat-square)](https://github.com/spf13/viper)

</div>

# 📃 Notes
* All Docker volumes are stored in the `docker/local/volumes/` folder. If you want to clear your DB or any other data, you can simply delete the folder there.

# ⚒️ Development
1. Download dependencies: `pip install -r requirements.txt`
2. Start docker services: `make up_local_services`
