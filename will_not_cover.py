import json
import os
import time
import re

import requests

here = os.path.abspath(os.path.dirname(__file__))
dist = os.path.join(here, 'dist')
data_dir = os.path.join(here, 'data')
if not os.path.exists(dist):
    os.makedirs(dist)
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


def main(cover=False):
    html = None
    for _ in range(2):
        try:
            rep = requests.get('https://gitter.im/IOTQQTalk/IOTQQ', timeout=10)
            rep.raise_for_status()
        except Exception:
            pass
        else:
            html = rep.text
            break
    if html is None:
        return

    file_urls = re.findall(r'<a href="(https://files\.gitter\.im/[A-Za-z0-9]+/[A-Za-z0-9]+/iotbot_.*?)"', html)
    if not file_urls:
        return
    files = []
    for file_url in file_urls:
        file_name = file_url.split('/')[-1]
        if cover:
            files.append((file_url, file_name))
        else:
            if file_name not in os.listdir(dist):
                files.append((file_url, file_name))

    for file in files:
        print(file)
        os.system(f'wget {file[0]} -O {dist}/{file[1]}')


if __name__ == "__main__":
    try:
        main(False)
    except Exception as e:
        print(f'[ERROR]{e}')
    finally:
        fileNames = os.listdir(dist)
        data = []
        for fileName in fileNames:
            if fileName.endswith('.tar.gz'):
                fileName_ok = fileName[:-7]
            elif fileName.endswith('.zip'):
                fileName_ok = fileName[:-4]
            else:
                continue
            _, version, system, arch = fileName_ok.split('_')
            data.append({
                'version': version,
                'os': system,
                'arch': arch,
                'fileName': fileName,
                'url': 'https://cdn.jsdelivr.net/gh/XiyaoWong/iotbot-mirror/dist/' + fileName
            })
            data.sort(key=lambda x: x['version'], reverse=True)
            details = {'last_sync': int(time.time()), 'data': data}
            with open(f'{data_dir}/data.json', 'w') as f:  # 存所有数据
                json.dump(details, f)

            latests = [i for i in data if i['version'] == data[0]['version']]
            # for linux
            linux = [i for i in latests if i['os'] == 'linux']
            for linux_i in linux:
                with open(f'{data_dir}/linux_{linux_i["arch"]}_latest.json', 'w') as f:
                    json.dump(linux_i, f)
            # for freebsd
            freebsd = [i for i in latests if i['os'] == 'freebsd']
            for freebsd_i in freebsd:
                with open(f'{data_dir}/freebsd_{freebsd_i["arch"]}_latest.json', 'w') as f:
                    json.dump(freebsd_i, f)
            # for darwin
            darwin = [i for i in latests if i['os'] == 'darwin']
            for darwin_i in darwin:
                with open(f'{data_dir}/darwin_{darwin_i["arch"]}_latest.json', 'w') as f:
                    json.dump(darwin_i, f)
            # for windows
            windows = [i for i in latests if i['os'] == 'windows']
            for windows_i in windows:
                with open(f'{data_dir}/windows_{windows_i["arch"]}_latest.json', 'w') as f:
                    json.dump(windows_i, f)
