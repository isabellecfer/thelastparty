from flask import Flask, make_response, request, Response
import json
import playlistmaker

app = Flask(__name__)


@app.route('/<usuarios>')
def lista_musicas(usuarios):
	response = playlistmaker.makeplaylist(str(usuarios))
	response = make_response(response)
	response.headers['Access-Control-Allow-Origin'] = "*"
	return response


if __name__ == '__main__':
	app.debug = True
	app.run(host='0.0.0.0', port=5002)