#!/usr/bin/python3
# Fabfile for distributing an archive to a web server.
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["", ""]


def do_deploy(archive_path):
    """Distribute an archive to a web server.

    Args:
        archive_path (str): The path of the archive to be distributed.

    Returns:
        bool: True if the distribution is successful, False otherwise.
    """
    # Check if the file exists at the specified archive_path.
    if os.path.isfile(archive_path) is False:
        return False

    # Extract relevant information from the archive file path.
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    # Perform the deployment steps.
    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False

    # Return True to indicate successful deployment.
    return True
