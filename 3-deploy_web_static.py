#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["52.87.153.171", "18.234.107.142"]


def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file = "versions/web_static_{}{}{}{}{}{}.tgz".format(dt.year,
                                                         dt.month,
                                                         dt.day,
                                                         dt.hour,
                                                         dt.minute,
                                                         dt.second)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -cvzf {} web_static".format(file)).failed is True:
        return None
    return file


def do_deploy(archive_path):
    """Distributes an archive to a web server.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        If the file doesn't exist at archive_path or an error occurs - False.
        Otherwise - True.
    """
    if not os.path.isfile(archive_path):
        return False
    try:
        filename = archive_path.split('/')[-1]
        no_ext = filename.split('.')[0]
        path_no_ext = '/data/web_static/releases/{}/'.format(no_ext)
        symlink = '/data/web_static/current'
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(path_no_ext))
        run('tar -xzf /tmp/{} -C {}'.format(filename, path_no_ext))
        run('rm /tmp/{}'.format(filename))
        run('mv {}web_static/* {}'.format(path_no_ext, path_no_ext))
        run('rm -rf {}web_static'.format(path_no_ext))
        run('rm -rf {}'.format(symlink))
        run('ln -s {} {}'.format(path_no_ext, symlink))
        return True
    except Exception:
        return False


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
