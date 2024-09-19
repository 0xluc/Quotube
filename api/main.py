from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi as yttapi
import re
from unidecode import unidecode

app = Flask(__name__)

@app.route("/request",methods=['GET'])
def searchTextInVideo():
    try:
        data = request.get_json()
        video = data['video']
        text = data['text']
        language = data['language']
        match = re.search(r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})',video)
        youtubeUrl = match.groups()[0]
        subs = yttapi.get_transcript(youtubeUrl, languages=[language])
        filtered_dicts = filter_dicts(subs, text)
        print(filtered_dicts)
        texts, moments = [], []
        for d in filtered_dicts:
            texts.append(d['text'])
            moments.append(d['start'])
        result = {
                "texts":texts,
                "moments": moments
        }
        print(result)
 
        return jsonify(result), 200
    except Exception as e:
        print(e)
        return "Error, text not found", 404

def filter_dicts(dict_list, search_text):
    search_text = unidecode(search_text).lower()
    return [d for d in dict_list if search_text in unidecode(d['text']).lower()]
