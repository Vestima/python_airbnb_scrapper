from flask import Flask, request, jsonify
from scrapper import get_data_from_url

app = Flask(__name__)

@app.route('/scrape', methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        data = request.get_json()
        url = data.get("url")
    else:
        url = request.args.get("url")

    if not url:
        return jsonify({"error": "Nenhum URL fornecido."}), 400

    try:
        result = get_data_from_url(url)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()