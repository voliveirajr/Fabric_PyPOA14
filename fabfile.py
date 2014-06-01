from fabric.api import *
from fabric.colors import green

WORKSPACE_HOME = "~/workspace"
GIT_URL = "https://github.com/voliveirajr/Fabric_PyPOA14.git"

def create_vm():
    print(green("Creating VM"))
    with cd("%s/Fabric_PyPOA14"%(WORKSPACE_HOME)):
        local('vagrant up')

def vagrant():
    create_vm()
    env.user = 'vagrant'
    env.hosts = ['127.0.0.1:2222']    
    # use vagrant ssh key
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]

def reqs():
    sudo('apt-get -q -y update')
    sudo('apt-get -q -y install python')
    sudo('apt-get -q -y install python-dev')
    sudo('apt-get -q -y install git')
    
    sudo('apt-get install -y python-pip')
    sudo('yes | pip install virtualenv')

def deploy():
    reqs()
    run("git clone %s"%(GIT_URL))
    create_venv()
    django_run()

def django_run():
    print(green("Running Django"))
    with cd("./Fabric_PyPOA14"):
        run('python manage.py syncdb')
        run('source ./bin/activate;python manage.py runserver 0.0.0.0:8000')
    
def create_venv():
    print(green("Loading virtualenv"))
    with cd("./Fabric_PyPOA14"):
        run('virtualenv .;source ./bin/activate;pip install -r requirements.txt')

def uname():
    run('uname -a')
