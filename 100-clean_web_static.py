#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric.api import env
from fabric.api import local
from fabric.api import put
from fabric.api import run

env.hosts = ["54.90.28.121", "54.237.79.178"]


def do_clean(number=0):
    """Deletes out-of-date .tgz archives of web servers
    """

    number = int(number)

    if number >= 0:
        with lcd("versions"):
            _files = gets_out_of_date(number, 'local')

            for _file in _files:
                local("rm -f {file}".format(file=_file))

        with cd("/data/web_static/releases"):
            _folders = gets_out_of_date(number, 'remote')

            for _folder in _folders:
                run("rm -rf {folder}".format(folder=_folder))
