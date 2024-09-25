from flask import Flask, request, jsonify
from youtube_transcript_api import NoTranscriptFound, YouTubeTranscriptApi as yttapi
import re
from unidecode import unidecode
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/api", methods=["POST"])
def searchTextInVideo():
    try:
        data = request.get_json()
        video = data['video']
        text = data['text']
        language = data['language']
        match = re.search(r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})',video)
        youtubeUrl = match.groups()[0]
        res = yttapi.list_transcripts(youtubeUrl)
        #print(res)
        subs = yttapi.get_transcript(youtubeUrl, languages=[language])
        filtered_dicts = filter_dicts(subs, text)
        print(filtered_dicts)
        print(request.remote_addr)
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            print(jsonify({'ip': request.environ['REMOTE_ADDR']}))
        else:
            print(jsonify({'ip': request.environ['HTTP_X_FORWARDED_FOR']}))
        
        return jsonify(filtered_dicts), 200
    except NoTranscriptFound as e:
        res = yttapi.list_transcripts(youtubeUrl)
        return str(res), 404
    except Exception as e:
        print(e)
        print(e.__class__.__name__)
        return "Error, text not found or url invalid", 404

def filter_dicts(dict_list, search_text):
    search_text = unidecode(search_text).lower()
    return [d for d in dict_list if search_text in unidecode(d['text']).lower()]
