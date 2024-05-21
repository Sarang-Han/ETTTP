
import random
from socket import *
from ETTTP_TicTacToe import TTT, check_msg

    
if __name__ == '__main__':
    
    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'
    
    while True:
        print("Wait for incoming...")
        client_socket, client_addr = server_socket.accept()
        
        ###################################################################
       
        start = random.randrange(0,2)   # select random to start
        
        # Send start move information to peer
        if start == 0:
            first_player = "ME"  # server is first
        else:
            first_player = "YOU"  # client is first
        
        # 게임 시작 메시지 전송
        start_msg = f"SEND ETTTP/1.0\r\nHost:{MY_IP}\r\nFirst-Move:{first_player}\r\n\r\n"
        print(start_msg)
        
        client_socket.send(start_msg.encode())
        
        ######################### Fill Out ################################
        
        # Receive ack - if ack is correct, start game
        ack_msg = client_socket.recv(SIZE).decode()

        ack_valid = check_msg(ack_msg, MY_IP)
        if not ack_valid:
            client_socket.close()
            TTT.quit()
        
        ###################################################################
        
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        
        client_socket.close()
        
        break
    server_socket.close()