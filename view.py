import subprocess

def run():
    subprocess.Popen(['cd visualisation/; ./web_server.sh'], shell=True)
