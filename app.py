from flask import Flask, jsonify
from openaiTest import make_plan
import asyncio

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/get_tasks', methods=['GET'])
async def get_tasks():
    tasks = await make_plan()
    return jsonify(tasks)

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)