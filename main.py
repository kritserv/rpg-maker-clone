from flask import Flask, render_template, request, redirect, url_for
from sys import platform
import os
import shutil
from json import load, dump
import subprocess
import base64
import csv
from PIL import Image
import io

def json_loader(path) -> dict:
    with open(path) as f:
        return load(f)

def json_saver(data, path):
    with open(path, 'w') as f:
        dump(data, f, indent=4)

app = Flask(__name__)

CONFIG_FILE = 'config.json'

if not os.path.exists(CONFIG_FILE):
    initial_config = {
        "current_project": None,
        "other_settings": {}
    }
    json_saver(initial_config, CONFIG_FILE)


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def crop_sprite_from_sheet(image_path, sprite_width, sprite_height):
    """
    Crop the top-left sprite from the spritesheet.
    """
    with Image.open(image_path) as img:
        # Crop the top-left sprite (0, 0) to (sprite_width, sprite_height)
        cropped_sprite = img.crop((0, 0, sprite_width, sprite_height))
        # Convert the cropped image to base64
        buffered = io.BytesIO()
        cropped_sprite.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

@app.route('/')
def index():
    config = json_loader(CONFIG_FILE)
    project_folder = False
    table = []
    player_position = None

    if config["current_project"]:
        project_folder = config["current_project"]["project_folder"]

    if project_folder:
        # Paths
        tile_map_path = os.path.join(project_folder, "game_data/data/maps/map001.csv")
        tile_map_setting_path = os.path.join(project_folder, "game_data/data/maps/tilesets.json")

        # Load tile mappings
        tile_mappings = json_loader(tile_map_setting_path)

        # Prepare base64 image map
        base64_images = {}
        for tile_id, image_name in tile_mappings["forests"].items():
            image_path = os.path.join(project_folder, f"assets/img/tile/{image_name}")
            base64_images[tile_id] = encode_image_to_base64(image_path)

        player_image_path = os.path.join(project_folder, f"assets/img/sprite/player.png")
        base64_images['player'] = crop_sprite_from_sheet(player_image_path, 16, 24)  # Encode player image

        game_data_path = os.path.join(project_folder, "game_data/db.json")
        game_data = json_loader(game_data_path)
        player_start_position = game_data["player_start_position"]
        player_position = tuple(player_start_position)  # Convert to tuple for easy comparison

        # Read the CSV file and construct the table
        with open(tile_map_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row_index, row in enumerate(csv_reader):
                table_row = []
                for col_index, cell in enumerate(row):
                    if (row_index, col_index) == player_position:
                        # Insert player sprite at player's position
                        table_row.append(base64_images['player'])
                    else:
                        table_row.append(base64_images.get(cell, ""))
                table.append(table_row)

    # Populate context
    context = {
        "project_folder": project_folder,
        "table": table,
    }
    return render_template('index.html', context=context)

@app.route('/new-project', methods=['GET', 'POST'])
def new_project():
    if request.method == 'POST':
        project_name = request.form['name']
        if project_name:
            src = 'start_project'
            dest = os.path.join('your_projects', project_name)

            shutil.copytree(src, dest)

            config = json_loader(CONFIG_FILE)
            config["current_project"] = {"project_folder": dest}
            json_saver(config, CONFIG_FILE)

            return redirect(url_for('index'))

    return render_template('file/new_project_form.html')


@app.route('/open-project', methods=['GET', 'POST'])
def open_project():
    projects_dir = 'your_projects'

    try:
        project_folders = os.listdir(projects_dir)
    except FileNotFoundError:
        return redirect(url_for('index'))

    if request.method == 'POST':
        selected_project = request.form['project_folder']

        if selected_project:
            project_folder = os.path.join(projects_dir, selected_project)

            config = json_loader(CONFIG_FILE)
            config["current_project"] = {"project_folder": project_folder}
            json_saver(config, CONFIG_FILE)

            return redirect(url_for('index'))

    return render_template('file/open_project.html', project_folders=project_folders)


@app.route('/close-project')
def close_project():
    projects_dir = 'your_projects'

    config = json_loader(CONFIG_FILE)
    config["current_project"] = {"project_folder": False}
    json_saver(config, CONFIG_FILE)

    return redirect(url_for('index'))

@app.route('/open-folder')
def open_folder():
    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
        project_folder = config["current_project"]["project_folder"]
    except FileNotFoundError:
        return redirect(url_for('index'))

    if current_project and project_folder:
        folder_path = current_project['project_folder']
        if platform == "win32":
            os.startfile(folder_path)
        elif platform == "linux" or platform == "linux2":
            open_folder_with = 'thunar' #xdg-open

            os.system(f'{open_folder_with} "{folder_path}"')

    return redirect(url_for('index'))

def change_web_line(main_file_path, boolean):
    with open(main_file_path, "r") as file:
        lines = file.readlines()
    lines[0] = f"web = {boolean}\n"
    with open(main_file_path, "w") as file:
        file.writelines(lines)


@app.route('/export-to-browser')
def export_to_browser():
    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
    except FileNotFoundError:
        return redirect(url_for('index'))

    if current_project:
        folder_path = current_project['project_folder']

        main_file_path = os.path.join(folder_path, "main.py")
        change_web_line(main_file_path, True)

        command = 'pygbag --archive .'
        subprocess.Popen(command, cwd=folder_path, shell=True)

        change_web_line(main_file_path, False)

        return redirect(url_for('index'))

    return redirect(url_for('index'))


@app.route('/export-to-android')
def export_to_android():
    if platform == "linux" or platform == "linux2":
        pass
    else:
        return render_template('error.html', message='Export to android only work for Linux.')

    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
    except FileNotFoundError:
        return redirect(url_for('index'))

    if current_project:
        return render_template('export/android.html')

    return redirect(url_for('index'))


def run_pygame():
    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
        project_folder = False
        if config["current_project"]:
            project_folder = config["current_project"]["project_folder"]
    except FileNotFoundError:
        return None

    if current_project and project_folder:
        folder_path = current_project['project_folder']
        if os.path.exists(folder_path):

            if platform == "win32":
                command = f'python main.py'
            elif platform == "linux" or platform == "linux2":
                command = f'python3 main.py'

            subprocess.Popen(command, cwd=folder_path, shell=True)


@app.route('/start-game')
def start_game():
    result = run_pygame()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
