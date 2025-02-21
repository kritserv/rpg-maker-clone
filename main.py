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
from glob import glob

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
    cell_table = []
    base64_images = {}
    inv_map = {}
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
                tile_id: encode_image_to_base64(os.path.join(project_folder, f"assets/img/tile/{image_name}.png"))
                for tile_id, image_name in tile_mappings.get(selected_map['tileset'], {}).items()
            }
            inv_map = {v: k for k, v in base64_images.items()}

            # Read CSV layers into tables
            table = [render_csv_layer(path, base64_images) for path in tile_map_layer_paths]

            if map_name == start_map_name:
                base64_images['player'] = crop_sprite_from_sheet(player_image_path, 16, 24)

                player_layer = []
                player_position = game_data.get("player_start_position", (0, 0))
                player_position = (player_position[1] // 16, player_position[0] // 16)
                player_layer.append(render_command_layer(tile_map_layer_paths[1], player_position, base64_images['player']))
                if player_layer:
                    table += player_layer

                if base64_images:
                    # remove player from tile_dict
                    base64_images.popitem()

            command_layer = []
            for i in range(len(table[0])):
                row = ['' for _ in range(len(table[0][i]))]
                command_layer.append(row)
            command_layer = [command_layer]

            try:
                command_list = json_loader(os.path.join(project_folder, f"game_data/data/commands/{map_name}.json"))
            except:
                command_list = []
            for command in command_list:
                command_data = command_list[command]
                if command_data['show']==True and command_data['img'] != False:
                    command_layer[0][(command_data['position'][1])//16][(command_data['position'][0])//16] = encode_image_to_base64(os.path.join(project_folder, f"assets/img/sprite/{command_data['img']}.png"))

            if command_layer:
                table += command_layer

        except Exception as e:
            return render_template('error.html', message=str(e))

    context = {
        "maps": maps,
        "selected_map": map_name,
        "table": [(index, layer) for index, layer in enumerate(table)],
        "tile_dict": base64_images,
        "inv_map": inv_map,
    }
    return render_template('index.html', context=context)

@app.route('/save_map', methods=['POST'])
def save_map():
    data = request.json
    map_name = data.get('map_name')
    layers = data.get('layers')

    if not map_name or not layers:
        return jsonify({"error": "Invalid data"}), 400

    # Get the project folder path
    config = json_loader(CONFIG_FILE)
    current_project = config.get("current_project", {})
    project_folder = current_project.get("project_folder", "")

    if not project_folder:
        return jsonify({"error": "Project folder not found"}), 400

    try:
        # Save each layer to its corresponding CSV file
        for index, layer in enumerate(layers):
            layer_file_path = os.path.join(
                project_folder, f"game_data/data/maps/{map_name}layer{index + 1}.csv"
            )
            with open(layer_file_path, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(layer)

        return jsonify({"message": "Map saved successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def render_csv_layer(csv_path, base64_images):
    """Render a CSV layer into a table of base64 images."""
    table = []
    if os.path.exists(csv_path):
        with open(csv_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                table.append([base64_images.get(cell, "") for cell in row])
    return table

def render_command_layer(csv_path, player_position, player_image):
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

@app.route('/export-to-desktop')
def export_to_desktop():
    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
    except FileNotFoundError:
        return redirect(url_for('index'))

    if current_project:
        return render_template('export/desktop.html')

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

def resize_csv(input_file, target_rows, target_cols):
    data = []

    try:
        with open(input_file, newline='') as csvfile:
            reader = csv.reader(csvfile)
            data = [row for row in reader]
    except FileNotFoundError:
        data = [[''] * target_cols for _ in range(target_rows)]

    # Resize rows
    data = data[:target_rows] + [[''] * len(data[0]) for _ in range(target_rows - len(data))]

    # Resize columns
    for i in range(len(data)):
        data[i] = data[i][:target_cols] + [''] * (target_cols - len(data[i]))

    # Write the resized CSV
    with open(input_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

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
    folder_path = False
    dbjson = {}
    skillsjson = {}
    itemsjson = {}

    if current_project and project_folder:
        folder_path = current_project['project_folder']
        game_data_folder_path = f"{folder_path}/game_data"
        dbjson = json_loader(f"{game_data_folder_path}/db.json")
        skillsjson = json_loader(f"{game_data_folder_path}/data/skills.json")
        itemsjson = json_loader(f"{game_data_folder_path}/data/items.json")

    if request.method == 'POST':
        data = request.form

        if 'add_skill' in data:
            # Add new empty skill
            new_skill_name = data['skill_name']
            skillsjson[new_skill_name] = {
                "img": "",
                "description": "",
                "attrs": {"atk": 0}
            }
        elif 'save_skills' in data:
            # Update existing skills
            new_skillsjson = {}
            skill_names = request.form.getlist('skill_name')
            skill_imgs = request.form.getlist('skill_img')
            skill_descs = request.form.getlist('skill_desc')
            skill_atks = request.form.getlist('skill_atk')

            for i in range(len(skill_names)):
                if skill_names[i]:  # Only save if name exists
                    new_skillsjson[skill_names[i]] = {
                        "img": skill_imgs[i],
                        "description": skill_descs[i],
                        "attrs": {"atk": int(skill_atks[i])}
                    }
            skillsjson = new_skillsjson

        elif 'add_item' in data:
            # Add new empty item
            new_item_name = data['item_name']
            itemsjson[new_item_name] = {
                "img": "",
                "description": "",
                "key_item": "",
                "equipable": "",
            }
        elif 'save_items' in data:
            # Update existing items
            new_itemsjson = {}
            item_names = request.form.getlist('item_name')
            item_imgs = request.form.getlist('item_img')
            item_descs = request.form.getlist('item_desc')
            item_key_items = request.form.getlist('item_key')
            item_equipables = request.form.getlist('item_equip')

            for i in range(len(item_names)):
                if item_names[i]:  # Only save if name exists
                    new_itemsjson[item_names[i]] = {
                        "img": item_imgs[i],
                        "description": item_descs[i],
                        "key_item": item_key_items[i]=='True',
                        "equipable": item_equipables[i]=='True'
                    }
            itemsjson = new_itemsjson

        elif 'add_map' in data:
            # Add new map
            new_map_name = data['map_name']
            dbjson['maps'].append({
                "name": new_map_name,
                "tileset": "",
                "size": [16, 16]
            })

            # Save DB to file
            json_saver(dbjson, f"{game_data_folder_path}/db.json")

        elif 'save_main' in request.form:
            new_main_title = request.form['main_title']
            dbjson['main']['main_title'] = new_main_title

            new_start_map = request.form['start_map']
            dbjson['start_map'] = new_start_map

            new_player_start_position_x = request.form['player_start_position_x']
            new_player_start_position_y = request.form['player_start_position_y']
            dbjson['player_start_position'] = [int(new_player_start_position_x), int(new_player_start_position_y)]

            new_maps = []
            map_names = request.form.getlist('map_name')
            map_tilesets = request.form.getlist('map_tileset')
            map_widths = request.form.getlist('map_width')
            map_heights = request.form.getlist('map_height')

            print(map_names)

            all_map_files = []
            for i in range(len(map_names)):
                new_maps.append({
                    "name": map_names[i],
                    "tileset": map_tilesets[i],
                    "size": [int(map_widths[i]), int(map_heights[i])],
                })

                for layer in range(1, 5):
                    input_file = f"{folder_path}/game_data/data/maps/{map_names[i]}layer{layer}.csv"
                    all_map_files.append(input_file)
                    resize_csv(input_file, int(map_heights[i]), int(map_widths[i]))

                command_path = f"{folder_path}/game_data/data/commands/{map_names[i]}.json"
                all_map_files.append(command_path)
                if not os.path.exists(command_path):
                    with open(command_path, 'w') as file:
                        file.write('{}')

            all_map_files.append(f"{folder_path}/game_data/data/maps/tilesets.json")
            all_map_files.append(f"{folder_path}/game_data/data/commands/all_map.json")

            for file in glob(f"{folder_path}/game_data/data/maps/*") + glob(f"{folder_path}/game_data/data/commands/*"):
                if file not in all_map_files:
                    os.remove(file)

            dbjson['maps'] = new_maps
            # Save DB to file
            json_saver(dbjson, f"{game_data_folder_path}/db.json")

        # Save Skill to file
        if 'add_skill' in request.form or 'save_skills' in request.form:
            json_saver(skillsjson, f"{game_data_folder_path}/data/skills.json")

        # Save Item to file
        if 'add_item' in request.form or 'save_items' in request.form:
            json_saver(itemsjson, f"{game_data_folder_path}/data/items.json")

        return redirect(url_for('database'))

    context = {
        "game_data_folder_path": game_data_folder_path,
        "dbjson": dbjson,
        "skillsjson": skillsjson,
        "itemsjson": itemsjson,
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

def git_init():
    """Initializes a new git repository in the current project folder."""
    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
        project_folder = current_project.get("project_folder") if current_project else None
        if not project_folder or not os.path.exists(project_folder):
            flash("Project folder not found!", "danger")
            return False
        command = "git init"
        result = subprocess.run(command, cwd=project_folder, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            flash("Git repository initialized successfully!", "success")
        else:
            flash(f"Error in git init: {result.stderr}", "danger")
        return result.returncode == 0
    except FileNotFoundError:
        flash("Config file not found!", "danger")
        return False

def git_revert(commit_hash):
    """Reverts the specified commit."""
    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
        project_folder = current_project.get("project_folder") if current_project else None
        if not project_folder or not os.path.exists(project_folder):
            flash("Project folder not found!", "danger")
            return False
        command = f"git revert {commit_hash}"
        result = subprocess.run(command, cwd=project_folder, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            flash("Commit reverted successfully!", "success")
        else:
            flash(f"Error in git revert: {result.stderr}", "danger")
        return result.returncode == 0
    except FileNotFoundError:
        flash("Config file not found!", "danger")
        return False

def git_stash():
    """Stashes current changes."""
    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
        project_folder = current_project.get("project_folder") if current_project else None
        if not project_folder or not os.path.exists(project_folder):
            flash("Project folder not found!", "danger")
            return False
        command = "git stash"
        result = subprocess.run(command, cwd=project_folder, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            flash("Changes stashed successfully!", "success")
        else:
            flash(f"Error in git stash: {result.stderr}", "danger")
        return result.returncode == 0
    except FileNotFoundError:
        flash("Config file not found!", "danger")
        return False

def git_stash_pop():
    """Applies and removes the latest stash."""
    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
        project_folder = current_project.get("project_folder") if current_project else None
        if not project_folder or not os.path.exists(project_folder):
            flash("Project folder not found!", "danger")
            return False
        command = "git stash pop"
        result = subprocess.run(command, cwd=project_folder, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            flash("Stash applied successfully!", "success")
        else:
            flash(f"Error in git stash pop: {result.stderr}", "danger")
        return result.returncode == 0
    except FileNotFoundError:
        flash("Config file not found!", "danger")
        return False

def git_reset(commit_hash, mode="--hard"):
    """Resets to specified commit."""
    try:
        config = json_loader(CONFIG_FILE)
        current_project = config.get("current_project")
        project_folder = current_project.get("project_folder") if current_project else None
        if not project_folder or not os.path.exists(project_folder):
            flash("Project folder not found!", "danger")
            return False
        command = f"git reset {mode} {commit_hash}"
        result = subprocess.run(command, cwd=project_folder, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            flash(f"Reset to {commit_hash} successful!", "success")
        else:
            flash(f"Error in git reset: {result.stderr}", "danger")
        return result.returncode == 0
    except FileNotFoundError:
        flash("Config file not found!", "danger")
        return False

@app.route('/git-init', methods=['POST'])
def handle_git_init():
    """Handles the git init operation."""
    success = git_init()
    return redirect(url_for('git'))

@app.route('/git-revert', methods=['POST'])
def handle_git_revert():
    """Handles the git revert operation."""
    commit_hash = request.form.get("commit_hash")
    if not commit_hash:
        flash("Commit hash is required!", "danger")
        return redirect(url_for('git'))
    success = git_revert(commit_hash)
    return redirect(url_for('git'))

@app.route('/git-stash', methods=['POST'])
def handle_git_stash():
    """Handles the git stash operation."""
    success = git_stash()
    return redirect(url_for('git'))

@app.route('/git-stash-pop', methods=['POST'])
def handle_git_stash_pop():
    """Handles the git stash pop operation."""
    success = git_stash_pop()
    return redirect(url_for('git'))

@app.route('/git-reset', methods=['POST'])
def handle_git_reset():
    """Handles the git reset operation."""
    commit_hash = request.form.get("commit_hash")
    reset_mode = request.form.get("reset_mode", "--hard")
    if not commit_hash:
        flash("Commit hash is required!", "danger")
        return redirect(url_for('git'))
    success = git_reset(commit_hash, reset_mode)
    return redirect(url_for('git'))

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
    app.run(debug=False)
