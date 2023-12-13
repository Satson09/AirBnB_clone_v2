#!/usr/bin/python3
"""web server distribution"""
from fabric.api import *
import os.path

env.user = 'ubuntu'
env.hosts = ["104.196.155.240", "34.74.146.120"]
env.key_filename = "~/id_rsa"

def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract archive to /data/web_static/releases/<archive filename without extension>
        filename = archive_path.split("/")[-1]
        foldername = "/data/web_static/releases/{}".format(filename.split(".")[0])
        run("mkdir -p {}".format(foldername))
        run("tar -xzf /tmp/{} -C {}".format(filename, foldername))

        # Remove the uploaded archive from the web server
        run("rm /tmp/{}".format(filename))

        # Move files from extracted folder to proper locations
        run("mv {}/web_static/* {}".format(foldername, foldername))
        run("rm -rf {}/web_static".format(foldername))

        # Remove the existing symbolic link
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link to the new version of the code
        run("ln -s {} /data/web_static/current".format(foldername))

        print("New version deployed!")
        return True

    except Exception as e:
        return False
