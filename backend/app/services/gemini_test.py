import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key='AIzaSyDmKaoRB4caVcFysxMlTvxofFtvVwV0fa4')  # 填入自己的api_key 
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("告诉我太阳系中最大行星的相关知识")
print(response.text)