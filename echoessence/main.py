from flask import Flask, render_template, request
import os
import openai

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None 
    if request.method == 'POST':
        language = request.form['language']
        customLanguage = request.form['customLanguage']
        audio_file = request.files['audiofile']
        audio_file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
        audio_file.save(audio_file_path)
        client = openai.OpenAI(api_key=os.environ.get('secret_key'))
        with open(audio_file_path, 'rb') as audio_file:
            transcript = client.audio.translations.create(
                model="whisper-1", 
                file=audio_file
            )
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            temperature=0,
            max_tokens=256,
            messages=[
                {"role": "system", "content": f"You will be provided with a sentence, and your task is to Translate it to {customLanguage} and also return the english transliteration of that translation."},
                {"role": "user", "content": transcript.text}
            ]
        )
        result = response.choices[0].message.content

    return render_template('index.html', result=result)

