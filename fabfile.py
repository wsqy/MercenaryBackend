from datetime import datetime

from fabric.api import *
from fabric.contrib.project import rsync_project
from fabric.contrib.files import exists

test_env = 'ubuntu@119.29.253.195'
qcloud40 = 'ubuntu@118.24.157.119'

env.hosts = [
    test_env,
    qcloud40
]

ROOT_DIR = r'/www'
PROJECT_NAME = r'MercenaryBackend'
PROJECT_PATH = '{}/{}'.format(ROOT_DIR, PROJECT_NAME)
TAG = datetime.now().strftime('%y.%m.%d')
TAG_PATH = '{}/{}'.format(ROOT_DIR, TAG)


def test_fabric():
    with cd('/home'):
        run('pwd')
        run('whoami')


# @hosts(test_env)
def deploy(remote_dir):
    if exists(remote_dir):
        rsync_project(
            remote_dir=remote_dir,
            exclude=['fabfile.py', '.git', '.idea', '.gitignore', 'MercenaryBackend/settings_local.py'],
        )
    else:
        print("远程目录不存在，请先创建")


def restart_project():
    with cd(PROJECT_PATH):
        run('pipenv shell')
        run('pipenv install')
        run('python manage.py migrate')


@hosts(test_env)
def backup():
    if exists(PROJECT_PATH):
        run('cp -R {} {}'.format(PROJECT_PATH, TAG_PATH))
        deploy(ROOT_DIR)


# @hosts(qcloud40)
def recover():
    if exists(TAG_PATH):
        if exists(PROJECT_PATH):
            run('rm -rf {}'.format(PROJECT_PATH))
        run('mv {} {}'.format(TAG_PATH, PROJECT_PATH))
