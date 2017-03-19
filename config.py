import os

project_dir = os.path.dirname(os.path.abspath(__file__))

db_url = os.path.join(project_dir, "tools", "db.sqlite")

jwt_secret = 'jwt_secret_for_playlist_server'

