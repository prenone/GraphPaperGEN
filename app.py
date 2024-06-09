import os
import logging
from flask import Flask, request, jsonify, render_template, send_from_directory
import json
import random
import string
from datetime import datetime
from gp_gen import gp_gen, gp_state, gp_sanitycheck, sanitize_filename

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/graphpapergen'

RESULTS_FOLDER = 'results'
MAX_DIR_SIZE = 10 * 1024 * 1024

if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)


def get_dir_size(path='.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def remove_oldest_files(path, target_size):
    files = sorted(
        (os.path.join(dirpath, f) for dirpath, _, filenames in os.walk(path) for f in filenames),
        key=lambda p: os.path.getmtime(p)
    )
    size = get_dir_size(path)
    while size > target_size and files:
        os.remove(files.pop(0))
        size = get_dir_size(path)

@app.route(app.config['APPLICATION_ROOT'] + '/')
def index():
    return render_template('index.html')

@app.route(app.config['APPLICATION_ROOT'] + '/api/gp_gen', methods=['GET'])
def generate_plot():
    try:
        state_json = request.args.get('state')
        if state_json is None:
            return jsonify({"error": "No state provided"}), 400
        
        state_dict = json.loads(state_json)
        
        state = gp_state()
        state.height = state_dict.get('height', state.height)
        state.width = state_dict.get('width', state.width)
        state.margin_left = state_dict.get('margin_left', state.margin_left)
        state.margin_right = state_dict.get('margin_right', state.margin_right)
        state.margin_top = state_dict.get('margin_top', state.margin_top)
        state.margin_bottom = state_dict.get('margin_bottom', state.margin_bottom)
        state.xscale = state_dict.get('xscale', state.xscale)
        state.yscale = state_dict.get('yscale', state.yscale)
        state.grid = state_dict.get('grid', state.grid)
        state.grid_major_thicker_x = state_dict.get('grid_major_thicker_x', state.grid_major_thicker_x)
        state.grid_major_thicker_y = state_dict.get('grid_major_thicker_y', state.grid_major_thicker_y)
        state.x_max = state_dict.get('x_max', state.x_max)
        state.x_min = state_dict.get('x_min', state.x_min)
        state.y_max = state_dict.get('y_max', state.y_max)
        state.y_min = state_dict.get('y_min', state.y_min)
        state.title = state_dict.get('title', state.title)
        state.x_label = state_dict.get('x_label', state.x_label)
        state.y_label = state_dict.get('y_label', state.y_label)
        state.x_tiks_numbers = state_dict.get('x_tiks_numbers', state.x_tiks_numbers)
        state.y_tiks_numbers = state_dict.get('y_tiks_numbers', state.y_tiks_numbers)
        state.img_format = state_dict.get('img_format', state.img_format)

        if not gp_sanitycheck(state):
            return jsonify({"error": "Invalid state provided"}), 400

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        filename = f"{timestamp}_{random_str}.{state.img_format}"
        sanitized_filename = sanitize_filename(filename)
        output_path = os.path.join(RESULTS_FOLDER, sanitized_filename)
        
        # Generate the plot
        gp_gen(state, output_path)

        # Check and manage the results directory size
        if get_dir_size(RESULTS_FOLDER) > MAX_DIR_SIZE:
            remove_oldest_files(RESULTS_FOLDER, MAX_DIR_SIZE)

        return jsonify({"filename": sanitized_filename}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route(app.config['APPLICATION_ROOT'] + '/results/<filename>')
def get_result(filename):
    sanitized_filename = sanitize_filename(filename)
    return send_from_directory(RESULTS_FOLDER, sanitized_filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
