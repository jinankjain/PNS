import os
from invoke import *

os.environ['FLASK_APP'] = "maintainer.py"


@task
def build(ctx):
    ctx.run("python3 -m flask run")
