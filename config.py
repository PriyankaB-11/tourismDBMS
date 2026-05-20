import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "root123")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "tourism_db")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", "3306"))
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", os.path.join("static", "images", "uploads"))
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
