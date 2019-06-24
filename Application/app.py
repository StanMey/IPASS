from flask import Flask, send_from_directory, jsonify, redirect
import formations_recommender as fr

app = Flask(__name__)


@app.route('/')
def home():
    return redirect("/index.html", code=302)


@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory('static', filename, as_attachment=False)


@app.route('/formationpage')
def get_competitions_options():
    return jsonify(fr.get_competitions_choice())


@app.route('/getformationsoptions/<string:league>')
def get_formations_choice(league):
    return jsonify(fr.get_formations_options(league))


@app.route('/recomformation/<string:opp_formation>/<string:league>')
def get_recom_formation(opp_formation, league):
    return jsonify(fr.get_recommended_formations(opp_formation, league, 2))


if __name__ == '__main__':
    app.run()
