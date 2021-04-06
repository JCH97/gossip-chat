import random, json, threading, uuid
import socket as sock
from typing import List, Dict

class Node:
    connectedHost: List[str] = []
    connectedPort: List[int] = []

    infectedNodes: List[str] =  []
    susceptibleNodes: List[str] = []

    def __init__(self, nodeName: str, host: str, port: int, connectedHost: List[str], connectedPort: List[int]):
        self.port = port if port != None else 0
        self.host = host if host != None else '127.0.0.1'
        
        self.socket: sock.socket = sock.socket(sock.AF_INET, sock.SOCK_DGRAM) 
        self.socket.bind((self.host, self.port))
        self.nodeName = nodeName
        self.replayMsg: Dict[str, str] = {} 
        self.tempId: str = 0
        self.conncNodes: List[str] = []

        for i in range(len(connectedHost)):
            connectedHost.append(connectedHost[i])
            connectedPort.append(connectedPort[i])
            Node.susceptibleNodes.append(f'{connectedHost[i]}:{connectedPort[i]}')
            self.conncNodes.append(Node.susceptibleNodes[i])
        
        self.threads()

    
    def recvAll(self):
        while True:
            nMsg, addr = self.socket.recvfrom(1024)
            inJson = json.loads(nMsg.decode('ascii'))

            tempId = inJson['id']
            msg = inJson['msg']
            name = inJson['name']

            if tempId in self.replayMsg:
                continue

            self.replayMsg[tempId] = msg
            print(f'\033[31m{name}\033[39m : {msg}')

            self.spreadMessage(msg, tempId,f'{addr[0]}:{addr[1]}', name)
        
    def waitMessage(self):
        while True:
            msg: str = input()
            self.spreadMessage(msg)        

    def spreadMessage(self, msg: str, _id: str = None, addr: str = None, nameOther: str = None):
        while Node.susceptibleNodes:
            addrRnd: str = random.choice(Node.susceptibleNodes)

            if _id == None:
                _id: uuid.UUID = uuid.uuid4()
                self.replayMsg[_id] = msg

            inJson = json.dumps({
                'id': f'{_id}',
                'msg': msg,
                'name': nameOther if nameOther != None else self.nodeName
            })

            if addr != None and addr == addrRnd: # message not formed here
                Node.susceptibleNodes.remove(addrRnd)
                self.infectedNodes.append(addrRnd)
                continue
            
            # print(addrRnd)
            self.socket.sendto(inJson.encode('ascii'), (addrRnd.split(':')[0], int(addrRnd.split(':')[1])))
            # print(Node.susceptibleNodes)
            Node.susceptibleNodes.remove(addrRnd)
            self.infectedNodes.append(addrRnd)

        self.infectedNodes = []
        for n in self.conncNodes:
            Node.susceptibleNodes.append(n)

        self.tempId = f'{uuid.uuid4()}'
            

    def threads(self):
        threading.Thread(target = self.recvAll).start()
        threading.Thread(target = self.waitMessage).start()
    