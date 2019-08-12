import docker
from docker.types import LogConfig

def run_container():
  print(client.containers.run(image="android_ci", command="echo hello world"))

def run_container_detach():
  print("Running container")
  container = client.containers.run(image="android_ci", command="echo hello world", detach=True)
  print("Grab logs")
  logs = container.logs()
  print(logs)


def run_container_volume():
  
  command="./gradlew build"
  logs = client.containers.run(image="android_ci", 
                                command="ls -la ./project/", 
                                working_dir="/home/gradle/",
                                volumes={'/home/vagrant/workspace/we_are_nutrition-android': {'bind': '/home/gradle/project/', 'mode': 'rw'}},
                                extra_hosts={"nexus.nespresso.com":"192.168.216.107"})
  # It comes as bytes -> Silly thing
  print(logs.decode())



def run_container_gradle_syslog():
  command="./gradlew build"
  container = client.containers.run(image="android_ci", 
                                command=command, 
                                log_config=LogConfig(type=LogConfig.types.SYSLOG, config={}),
                                working_dir="/home/gradle/project/",
                                volumes={'/home/vagrant/workspace/we_are_nutrition-android': {'bind': '/home/gradle/project/', 'mode': 'rw'}},
                                extra_hosts={"nexus.nespresso.com":"192.168.216.107"}, detach=True)
  # It comes as bytes -> Silly thing
  # logs = container.logs()
  # print(logs.decode())

def run_container_gradle():
  command="./gradlew " \
            "-Dhttp.proxyHost=barc.proxy.corp.sopra -Dhttp.proxyPort=8080 " \
            "-Dhttps.proxyHost=barc.proxy.corp.sopra -Dhttps.proxyPort=8080 " \
            "-Dhttp.nonProxyHosts=nexus.nespresso.com " \
            "-Dhttps.nonProxyHosts=nexus.nespresso.com build --debug"
  container = client.containers.run(image="android_ci", 
                                command=command, 
                                #log_config=LogConfig(type=LogConfig.types.SYSLOG, config={}),
                                working_dir="/home/gradle/project/",
                                volumes={'/home/vagrant/workspace/we_are_nutrition-android': {'bind': '/home/gradle/project/', 'mode': 'rw'}},
                                extra_hosts={"nexus.nespresso.com":"192.168.216.107"}, detach=True)
  for line in container.logs(stream=True):
    print(line.strip())

def run_container_gradle_noproxy():
  command="./gradlew build --debug"
  container = client.containers.run(image="android_ci", 
                                command=command, 
                                #log_config=LogConfig(type=LogConfig.types.SYSLOG, config={}),
                                working_dir="/home/gradle/project/",
                                volumes={'/home/vagrant/workspace/we_are_nutrition-android': {'bind': '/home/gradle/project/', 'mode': 'rw'}},
                                extra_hosts={"nexus.nespresso.com":"192.168.216.107"}, detach=True)
  for line in container.logs(stream=True):
    print(line.strip())


if __name__ == "__main__":
  client = docker.DockerClient(base_url='unix://var/run/docker.sock')

  #run_container_volume()
  #run_container_gradle()
  run_container_gradle_noproxy()

  