import sys
from Node import Node

name = "User"
host, port = '127.0.0.1', 3000
hosts, ports = [], []   #   connections

def parseArgs():
    global name
    global host
    global port
    global hosts
    global ports
    
    if len(sys.argv) < 4:
        print(f'Bad format arguments')
        return False
    else:
        try:
            name, host, port = str(sys.argv[1]), str(sys.argv[2]), int(sys.argv[3])
            
            for i in range(4, len(sys.argv)):
                # print(f"{i} == {sys.argv[i]}")
                cHost, cPort = str(sys.argv[i].split(':')[0]), int(sys.argv[i].split(':')[1])
                hosts.append(cHost)
                ports.append(cPort)
            
            return True

        except Exception as e:
            print(f'Bad formats arguments. {e}')
            return False       

def main():
    if parseArgs():
        try:
            Node(name, host, port, hosts, ports)
        except Exception as e:
            exit(0)

if __name__ == "__main__":
    main()