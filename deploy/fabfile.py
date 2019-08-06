import sys, json, os

# Necessary for logger
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

# Fabric imports
from fabric import task
import utils

# Configure hosts
aws = {}
aws['host'] = 'storrellas@10.99.21.72'
aws['connect_kwargs'] = {"key_filename": "/home/vagrant/.ssh/id_rsa"}
my_hosts = [aws]


# Create logger
logger = utils.get_logger()
docker_folder = './docker'

def print_init_banner(message):
    logger.info("++++++++++++++++++++++++++++++")
    logger.info(message)

def print_end_banner(message = 'DONE!'):
    logger.info(message)
    logger.info("++++++++++++++++++++++++++++++")

def get_repo_folder(repo):
    # Get repo folder from URL
    repo_folder = repo.split('/')[-1]
    if repo_folder.endswith('.git'):
        repo_folder = repo_folder[:-len('.git')]
    return repo_folder

# Configuration parameters
config = {}
try:
    with open('config.json') as json_file:
        config = json.load(json_file)
except FileNotFoundError:
    logger.error("Config file not found")
    sys.exit(0)

print_init_banner("Configuration")
print(json.dumps(config, indent=2))
print_end_banner(" ")

@task(hosts=my_hosts)
def test(c):
    """
    Testing task
    """
    print_init_banner('Testing task')
    print_end_banner()

    # Update System
    c.run('ls -la', echo=True)


@task(hosts=my_hosts)
def provision(c):
    """
    Installs Dependencies
    See: https://docs.docker.com/install/linux/docker-ce/ubuntu/
    """
    print_init_banner('provision: Installs dependencies')
    print_end_banner()

    # Update System
    print_init_banner("Installing Dependencies ... ")
    c.run('sudo apt update', echo=True)

    # Install former
    c.run('sudo apt-get remove docker docker-engine docker.io containerd runc', echo=True)


    # Install dependencies
    c.run('sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common', echo=True)

    # Add GPG key
    c.run('sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -', echo=True)


    # Verify
    output = c.run('sudo apt-key fingerprint 0EBFCD88', echo=True)
    if len(output.stdout) <= 0:
        raise Exception("Verification failed")
    
    # Add repository
    c.run('sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"', echo=True)

    # Install docker
    c.run('sudo apt update', echo=True)
    c.run('sudo apt-get -y install docker-ce docker-ce-cli containerd.io', echo=True)
    c.run('docker --version', echo=True)

    # Install docker-compose
    c.run('sudo curl -L \
            \"https://github.com/docker/compose/releases/download/1.24.1/docker-compose-$(uname -s)-$(uname -m)\" \
            -o /usr/local/bin/docker-compose', echo=True)
    c.run('sudo chmod +x /usr/local/bin/docker-compose', echo=True)
    c.run('docker-compose --version', echo=True)

    print_end_banner()

@task(hosts=my_hosts)
def gitSSH(c):
    """
    Uploads GIT key to perform clone
    """
    print_init_banner('gitSSH: Uploads keys to download repo')
    print_end_banner()

    # # Generate RSA keys
    # keypath = '~/.ssh/stem'
    # created_rsa_key=False
    # if c.run('test -f {}'.format(keypath), warn=True).failed:
    #     c.run('echo y |ssh-keygen -q -t rsa -N "" -f ~/.ssh/stem', hide=True)
    #     created_rsa_key=True
    # else:
    #     logger.info("Key already exists")
    #
    # # Print public key value
    # output = c.run('cat ~/.ssh/stem.pub', hide=True)
    # logger.info("++++++++++++++++++++++++++++++")
    # logger.info("++ Generated RSA public key ++")
    # logger.info("++++++++++++++++++++++++++++++")
    # print(output.stdout)

    # Upload keys
    print_init_banner("Upload RSA keys ...")
    # c.put('./deploy/rsa/stem_bitbucket', remote='./.ssh/id_rsa')
    # c.put('./deploy/rsa/stem_bitbucket.pub', remote='./.ssh/id_rsa.pub')
    c.put(config['git_key_public'], remote='./.ssh/id_rsa.pub')
    c.put(config['git_key_private'], remote='./.ssh/id_rsa')



    # Change permissions
    c.run('sudo chmod 600 ./.ssh/id_rsa')
    c.run('sudo chmod 600 ./.ssh/id_rsa.pub')
    print_end_banner()


@task(hosts=my_hosts)
def docker_proxy(c):
    """
    Pull and build gradle
    See: https://docs.docker.com/config/daemon/systemd/
    """
    # Configure SystemD
    c.run('sudo mkdir -p /etc/systemd/system/docker.service.d', echo=True)
    c.put('./http-proxy.conf')
    c.run('sudo mv http-proxy.conf /etc/systemd/system/docker.service.d', echo=True)

    # Restart
    c.run('sudo systemctl daemon-reload', echo=True)
    c.run('sudo systemctl restart docker', echo=True)
    c.run('sudo systemctl show --property=Environment docker', echo=True)

    # Pull image
    #c.run('sudo docker pull gradle:latest', echo=True)

@task(hosts=my_hosts)
def gradleBuild(c):
    """
    Builds gradle image
    """

    repo_ci_folder = get_repo_folder(config['repository_android_ci'])
    with c.cd(config['remote_workspace']):

        # Get latest changes
        print_init_banner('Git pull ... ')          
        with c.cd(repo_ci_folder):
            # Get specific branch
            if  config['branch'] is not None:
                c.run('git fetch --all ', echo=True, pty=True)
                c.run('git checkout ' + config['branch'], echo=True, pty=True)
                c.run('git pull origin ' +  config['branch'], echo=True, pty=True)
            else:
                c.run('git pull origin master', echo=True, pty=True)
            if c.run('test -f {}'.format(docker_folder + '/.env'), warn=True).failed:
                c.run('cp -rv ' + docker_folder + '/.env.template ' + docker_folder + '/.env', echo=True)
        print_end_banner()
    
        # Generate docker image
        print_init_banner('Docker image ... ')
        with c.cd(repo_ci_folder + '/' + docker_folder):
            c.run('sudo docker-compose stop', echo=True)
            c.run('sudo docker-compose build', echo=True)
        print_end_banner()


@task(hosts=my_hosts)
def gradleRun(c):
    """
    Run gradle image
    """

    #command="./project/gradlew -Dhttp.proxyHost=barc.proxy.corp.sopra -Dhttp.proxyPort=8080 -Dhttps.proxyHost=barc.proxy.corp.sopra -Dhttps.proxyPort=8080 -Dhttp.nonProxyHosts=nexus.nespresso.com -Dhttps.nonProxyHosts=nexus.nespresso.com  assemble"
    command="./project/gradlew tasks"

    repo_ci_folder = get_repo_folder(config['repository_android_ci'])
    with c.cd(config['remote_workspace']):
   
        # Generate docker image
        print_init_banner('Docker image ... ')
        with c.cd(repo_ci_folder + '/' + docker_folder):
            c.run('sudo docker-compose run android_ci ' + command, echo=True)
        print_end_banner()




@task(hosts=my_hosts)
def deploy(c):
    """
    Clones, Pull and Gradle
    """
    print_init_banner('Deploy: Clones, Pull and launches docker-compose build')
    print_end_banner()

    # Get repo folder from URL
    repo_folder = get_repo_folder(config['repository'])

    # Print public key value
    print_init_banner('Using public RSA key')
    output = c.run('cat ~/.ssh/id_rsa.pub', hide=True)
    print(output.stdout)
    print_end_banner()

    # proceeding to deployment
    print_init_banner('Deploying to folder ' + config['remote_workspace'])
    if c.run('test -d {}'.format(config['remote_workspace']), warn=True).failed:
        logger.info("Creating folder")
        c.run('mkdir ' + config['remote_workspace'])
    print_end_banner()

    # Remote tasks
    with c.cd(config['remote_workspace']):

        # Cloning repository
        print_init_banner('Cloning project repository ... ')
        if c.run('test -d {}'.format(repo_folder), warn=True).failed:
            c.run('git clone ' + config['repository'], echo=True, pty=True)
        else:
            logger.info('Repository exists skipping')
        print_end_banner()


    with c.cd(config['remote_workspace']):

        # Get latest changes
        print_init_banner('Git pull ... ')
        with c.cd(repo_folder):
            # Get specific branch
            if  config['branch'] is not None:
                c.run('git fetch --all ', echo=True, pty=True)
                c.run('git checkout ' + config['branch'], echo=True, pty=True)
                c.run('git pull origin ' +  config['branch'], echo=True, pty=True)
            else:
                c.run('git pull origin master', echo=True, pty=True)





@task(hosts=my_hosts)
def build(c):
    """
    Builds and puts compiled modules
    """

    # Get repo folder from URL
    repo_folder = get_repo_folder(config['repository'])

    # Generating build
    c.local('cd .. && ./node_modules/.bin/webpack --mode production --config webpack.config.prod.js', echo=True)


@task(hosts=my_hosts)
def launch(c):
    """
    Relaunches docker
    """
    print_init_banner('Relaunches docker')
    print_end_banner()

    # Get repo folder from URL
    repo_folder = get_repo_folder(config['repository'])

    print_init_banner('Docker image ... ')
    with c.cd(config['remote_workspace'] + '/' + repo_folder + '/docker'):
        c.run('sudo docker-compose stop', echo=True)
        c.run('sudo docker-compose up -d', echo=True)

    print_end_banner()

@task(hosts=my_hosts)
def halt(c):
    """
    halt docker
    """
    print_init_banner('Stop docker')
    print_end_banner()

    # Get repo folder from URL
    repo_folder = get_repo_folder(config['repository'])

    with c.cd(config['remote_workspace'] + '/' + repo_folder + '/docker'):
        c.run('sudo docker-compose stop', echo=True)

    print_end_banner()

@task(hosts=my_hosts)
def ddns(c):
    """
    Update DNS A record
    """
    print_init_banner('Update DNS record in Godaddy')
    print_end_banner()

    c.put('./godaddy_ddns.py')
    c.run('python3 godaddy_ddns.py --key ' + config['godaddy_key'] + \
            ' --secret ' + config['godaddy_secret'] + ' ' + config['godaddy_domain'], echo=True)

    # More complex version
    # repo_folder = get_repo_folder(config['repository'])
    # with c.cd(config['remote_workspace'] + '/' + repo_folder + '/deploy/'):
    #     c.run('python3 godaddy_ddns.py --key ' + config['godaddy_key'] + \
    #             ' --secret ' + config['godaddy_secret'] + ' ' + config['godaddy_domain'], echo=True)


@task(hosts=my_hosts)
def log(c):
    """
    Configure logging
    """

    # Rsyslog
    c.put('./rsyslog/60-stem.conf')
    c.run('sudo mv 60-stem.conf /etc/rsyslog.d/', echo=True)
    c.run('sudo /etc/init.d/rsyslog restart', echo=True)

    # Logrotate
    c.put('./rsyslog/stem-logrotate')
    c.run('sudo mv stem-logrotate /etc/logrotate.d/', echo=True)



# from fabric import Connection
# if __name__ == "__main__":
#     c = Connection(host='ec2-35-178-81-90.eu-west-2.compute.amazonaws.com', user="ubuntu", connect_kwargs={"key_filename": "/home/vagrant/.ssh/stem.pem"})
#     c.run('ls -la')
