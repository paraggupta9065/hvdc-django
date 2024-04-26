import os
from dotenv import load_dotenv
load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DEBUG = os.getenv('DEBUG')
SECRET_KEY = "django-insecure-ij8d=@k^)6j@$f%sjd4)#xj9nbw&mtf6+^p_4@s)(77(0v_go5"