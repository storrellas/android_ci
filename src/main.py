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

def run_container_gradle():
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


if __name__ == "__main__":
  client = docker.DockerClient(base_url='unix://var/run/docker.sock')
  #print(client.containers.run("android_ci", "gradle"))
#   container = client.containers.create(
#     image='android_ci',
#     stdin_open=True,
#     tty=True,
#     command='ls -la',
#     volumes=['/home/storrellas/workspace/we_are_nutrition-android'],
#     host_config=client.create_host_config(binds={
#         '/home/storrellas/workspace/we_are_nutrition-android': {
#             'bind': '/home/gradle/project/',
#             'mode': 'rw',
#         }
#     })
# )
# print(client.start(container))
  # print("Running container")
  # container = client.containers.run(image="android_ci", command="echo hello world", detach=True)
  # print("Grab logs")
  # logs = container.logs()
  # print(logs)

  #run_container_volume()
  run_container_gradle()

  