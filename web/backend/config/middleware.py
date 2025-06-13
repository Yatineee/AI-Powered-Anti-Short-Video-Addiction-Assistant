# config/middleware.py
from fastapi.middleware.cors import CORSMiddleware

def setup_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # ⚠️ 生产环境替换为前端域名
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
