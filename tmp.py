import subprocess

d = subprocess.check_output("sensors", shell=True)

print([d[:-2]])