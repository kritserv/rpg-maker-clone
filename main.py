from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
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
app.secret_key = 'your_secret_key'

CONFIG_FILE = 'config.json'

if not os.path.exists(CONFIG_FILE):
    initial_config = {
        "current_project": None,
        "other_settings": {},
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
    if 'theme' not in session:
        session['theme'] = 'light'

    map_name = request.args.get('map_name') or session.get('map_name')

    config = json_loader(CONFIG_FILE)
    current_project = config.get("current_project", dict())
    project_folder = ''
    if current_project:
        project_folder = current_project.get("project_folder")

    # Default to the starting map if not set
    if not map_name:

        current_project = config.get("current_project", dict())
        if current_project:
            if current_project.get("project_folder"):
                game_data_path = os.path.join((current_project).get("project_folder"), "game_data/db.json")
                try:
                    game_data = json_loader(game_data_path)
                    map_name = game_data.get('start_map', 'default_map')
                except FileNotFoundError:
                    return render_template('index.html', context={})

    # Store the selected map in the session
    session['map_name'] = map_name
    table = []
    base64_images = {}
    start_map = {}
    maps = []

    if project_folder:
        try:
            game_data_path = os.path.join(project_folder, "game_data/db.json")
            tile_map_setting_path = os.path.join(project_folder, "game_data/data/maps/tilesets.json")
            player_image_path = os.path.join(project_folder, "assets/img/sprite/player.png")

            game_data = json_loader(game_data_path)
            tile_mappings = json_loader(tile_map_setting_path)
            maps_dict = game_data.get("maps", {})
            maps.extend(maps_dict)

            start_map_name = game_data.get("start_map")
            if not map_name:
                map_name = start_map_name

            selected_map = next((m for m in maps_dict if m["name"] == map_name), None)
            if not selected_map:
                return render_template('error.html', message='Map not found')

            tile_map_path = f"game_data/data/maps/{map_name}"
            tile_map_layer_paths = [
                os.path.join(project_folder, f"{tile_map_path}layer1.csv"),
                os.path.join(project_folder, f"{tile_map_path}layer2.csv"),
                os.path.join(project_folder, f"{tile_map_path}layer3.csv"),
                os.path.join(project_folder, f"{tile_map_path}layer4.csv"),
            ]

            # Prepare base64 images for tiles
            base64_images = {
                tile_id: encode_image_to_base64(os.path.join(project_folder, f"assets/img/tile/{image_name}"))
                for tile_id, image_name in tile_mappings.get(selected_map['tileset'], {}).items()
            }

            # Load player sprite
            base64_images['player'] = crop_sprite_from_sheet(player_image_path, 16, 24)

            # Read CSV layers into tables
            table = [render_csv_layer(path, base64_images) for path in tile_map_layer_paths]

            # Add player position layer
            player_position = game_data.get("player_start_position", (0, 0))
            player_position = (player_position[1] // 16, player_position[0] // 16)
            object_layer = render_player_layer(tile_map_layer_paths[1], player_position, base64_images['player'])
            if map_name == start_map_name:
                table.append(object_layer)

        except Exception as e:
            return render_template('error.html', message=str(e))

    if base64_images:
        # remove player from tile_dict
        base64_images.popitem()
    context = {
        "maps": maps,
        "selected_map": map_name,
        "table": [(index, layer) for index, layer in enumerate(table)],
        "tile_dict": base64_images,
    }
    return render_template('index.html', context=context)

def render_csv_layer(csv_path, base64_images):
    """Render a CSV layer into a table of base64 images."""
    table = []
    if os.path.exists(csv_path):
        with open(csv_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                table.append([base64_images.get(cell, "") for cell in row])
    return table


def render_player_layer(csv_path, player_position, player_image):
    """Render a layer showing the player's position."""
    table = []
    if os.path.exists(csv_path):
        with open(csv_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row_index, row in enumerate(csv_reader):
                table.append([
                    player_image if (row_index, col_index) == player_position else ""
                    for col_index, _ in enumerate(row)
                ])
    return table


@app.route('/toggle-theme')
def toggle_theme():
    # Toggle between light and dark mode
    current_theme = session.get('theme', 'light')
    session['theme'] = 'dark' if current_theme == 'light' else 'light'
    return redirect(url_for('index'))

@app.route('/new-project', methods=['GET', 'POST'])
def new_project():
    current_map_name = request.args.get('map_name')
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

@app.route('/export-to-browser')
def export_to_browser():
    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
    except FileNotFoundError:
        return redirect(url_for('index'))

    if current_project:
        return render_template('export/browser.html')

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
            command = f'python3 main.py'
            if platform == "win32":
                command = f'python main.py'

            subprocess.Popen(command, cwd=folder_path, shell=True)

@app.route('/database', methods=['GET', 'POST'])
def database():
    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
        project_folder = False
        if config["current_project"]:
            project_folder = config["current_project"]["project_folder"]
    except FileNotFoundError:
        return None

    game_data_folder_path = False
    dbjson = {}

    if current_project and project_folder:
        folder_path = current_project['project_folder']
        game_data_folder_path = f"{folder_path}/game_data"
        dbjson = json_loader(f"{game_data_folder_path}/db.json")

    if request.method == 'POST':
        data = request.json
        new_main_title = data.get('main_title')
        if new_main_title:
            dbjson['main']['main_title'] = new_main_title
            json_saver(dbjson, f"{game_data_folder_path}/db.json")
            return jsonify({'message': 'Saved successfully!'}), 200
        return jsonify({'message': 'Invalid data'}), 400

    context = {
        "game_data_folder_path": game_data_folder_path,
        "dbjson": dbjson,
    }

    return render_template('database/database.html', context=context)

def _git_add_dot():
    """Adds all changes in the current project's folder."""
    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
        project_folder = current_project.get("project_folder") if current_project else None

        if not project_folder or not os.path.exists(project_folder):
            flash("Project folder not found!", "danger")
            return False

        command = "git add ."
        result = subprocess.run(command, cwd=project_folder, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            flash("Files added successfully!", "success")
        else:
            flash(f"Error in git add: {result.stderr}", "danger")
        return result.returncode == 0
    except FileNotFoundError:
        flash("Config file not found!", "danger")
        return False

def _git_pull():
    """Pull change from current project"""
    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
        project_folder = current_project.get("project_folder") if current_project else None

        if not project_folder or not os.path.exists(project_folder):
            flash("Project folder not found!", "danger")
            return False

        command = "git pull"
        result = subprocess.run(command, cwd=project_folder, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            flash("Files added successfully!", "success")
        else:
            flash(f"Error in git pull: {result.stderr}", "danger")
        return result.returncode == 0
    except FileNotFoundError:
        flash("Config file not found!", "danger")
        return False


def _git_commit_and_push(message, description):
    """Commits and pushes changes in the current project's folder."""
    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
        project_folder = current_project.get("project_folder") if current_project else None

        if not project_folder or not os.path.exists(project_folder):
            flash("Project folder not found!", "danger")
            return False

        commit_message = f"{message}\n\n{description}"
        command = f'git commit -m "{commit_message}" && git push'
        result = subprocess.run(command, cwd=project_folder, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            flash("Commit and push successful!", "success")
        else:
            flash(f"Error in git commit/push: {result.stderr}", "danger")
        return result.returncode == 0
    except FileNotFoundError:
        flash("Config file not found!", "danger")
        return False


@app.route('/git-add', methods=['POST'])
def git_add():
    """Handles the git add . operation."""
    success = _git_add_dot()
    return redirect(url_for('git'))


@app.route('/git-pull', methods=['POST'])
def git_pull():
    """Handles the git pull operation."""

    success = _git_pull()
    return redirect(url_for('git'))


@app.route('/git-push', methods=['POST'])
def git_push():
    """Handles the git commit and push operation."""
    message = request.form.get("message")
    description = request.form.get("description")
    if not message:
        flash("Commit message is required!", "danger")
        return redirect(url_for('git'))

    success = _git_commit_and_push(message, description)
    return redirect(url_for('git'))


@app.route('/git', methods=['GET', 'POST'])
def git():
    """Renders the Git page."""
    return render_template('git/git.html')

@app.route('/start-game')
def start_game():
    result = run_pygame()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
