import google.generativeai as genai
import os

genai.configure(api_key=os.environ["AIzaSyCMlwNbVEoIuhqxm63jeTf4a44ckVc2_kI"])

model = genai.GenerativeModel('gemini-1.5-flash')

response = model.generate_content("Are you alive?")
print(response.text)