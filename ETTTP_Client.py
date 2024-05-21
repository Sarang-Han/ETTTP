
from socket import *
from ETTTP_TicTacToe import TTT, check_msg
    

if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)  
        print("TCP connection setup!")
        
        ###################################################################
        
        # Receive who will start first from the server
        start_msg = client_socket.recv(SIZE).decode()
        
        msg_valid = check_msg(start_msg, MY_IP)
        if not msg_valid:
            client_socket.close()
            TTT.quit()

        split_msg = start_msg.split("\r\n")
        first_player = split_msg[2].split(":")[1].strip()
        
        if first_player == "ME":
            start = 0
            first_player = "YOU"
        else:
            start = 1
            first_player = "ME"

        ######################### Fill Out ################################
        
        # Send ACK 
        ack_msg = f"ACK ETTTP/1.0\r\nHost:{MY_IP}\r\nFirst-Move:{first_player}\r\n\r\n"
        print(ack_msg)
        
        client_socket.send(ack_msg.encode())
        
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        