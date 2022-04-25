import requests
import subprocess
import threading
import sys

subprocess.run('clear')

ip = input("enter server ip: ")
port = input("enter server port: ")
try:
    r = requests.get(f'http://{ip}:{port}/buddy/')
except:
    print("no chatserver running at this server/port")
    sys.exit()
combine = f'{ip}:{port}'
username = input("enter your username: ")
requests.put(f'http://{combine}/server', data={'content': f'{username} just joined the room!'})

print(f"type '!exit' to leave")

def listen():
    global localmsg
    localmsg = {}
    while True:
        r = requests.get(f'http://{combine}/buddy')
        if r.json() != localmsg:
            for i in r.json():
                try:
                    # print(f'DEBUG: {r.json[i]}, {localmsg[i]}')
                    if i != username and r.json()[i] != localmsg[i]:
                        print(f"{i}: {r.json().get(i)}")
                except KeyError:
                    continue
            localmsg = r.json()


listener = threading.Thread(target=listen, daemon=True)
listener.start()

while True:
    msg = input('')
    if msg == '!exit':
        requests.put(f'http://{combine}/server', data={'content': f'{username} has left the room.'})
        print(f'left server at {combine}')
        sys.exit()

    if msg == '!cmds':
        print('commands are: !exit, !servermsg')
    elif msg.startswith('!servermsg'):
        requests.put(f'http://{combine}/server', data={'content': msg.split('!servermsg ')[1]})
    else:
        requests.put(f'http://{combine}/{username}', data={'content': msg})
