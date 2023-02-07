import socket
from threading import Thread
import pickle
import random

sayi = 0
# server's IP address
SERVER_HOST = "192.168.1.39"
SERVER_PORT = 5555 # port we want to use

# initialize list/set of all connected client's sockets
client_sockets = set() # Boş bir set oluşturuldu. Liste de olabilirdi.
# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
try:
    s.bind((SERVER_HOST, SERVER_PORT))
except Exception as e:
    print(e)
# listen for upcoming connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

dic = {}
user_list = []


def generate_pos():
    rnd_x = random.randint(0,(30)-1)*20
    rnd_y = random.randint(0,(30)-1)*20
    return (rnd_x, rnd_y)

new_pos = generate_pos()
generate_food = False


def listen_for_client(cs):
    global new_pos
    global generate_food
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        dic["new_pos"] = new_pos
        try:
            # keep listening for a message from `cs` socket
            dic.update(pickle.loads(cs.recv(1024*2)))
            #msg = pickle.loads(cs.recv(1024))  #decode edince str formatına geliyor
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # if we received a message, replace the <SEP> 
            # token with ": " for nice printing
            pass
        # iterate over all connected sockets

        for i in dic:
            if  i != "new_pos":
                if dic[i][0][2] == True:
                    generate_food = True
                    break

        if generate_food:
            new_pos = generate_pos()
            dic["new_pos"] = new_pos
            generate_food = False
        

        for client_socket in client_sockets:
            # and send the message
                if len(dic) == sayi+1:
                    client_socket.send(pickle.dumps(dic))
        #print(dic)
        #user_list = list(dic)
        #print(user_list)
   
            
while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    sayi += 1
    print(sayi)
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()

# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()