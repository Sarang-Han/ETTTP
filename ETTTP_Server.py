
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
        # Accept incoming connection from a client
        client_socket, client_addr = server_socket.accept()
        
        ###################################################################
       
        # Select a random player (0 or 1) to start the game
        start = random.randrange(0,2)
        
        # Determine the first player based on the random selection
        if start == 0:
            first_player = "ME"  # Server is first player
        else:
            first_player = "YOU"  # Client is first player
        
        # Construct the start message with the first player information
        start_msg = f"SEND ETTTP/1.0\r\nHost:{MY_IP}\r\nFirst-Move:{first_player}\r\n\r\n"
        print(start_msg)
        
        # Send the start message to the client
        client_socket.send(start_msg.encode())
        
        ######################### Fill Out ################################
        
        # Receive the ACK message from the client
        ack_msg = client_socket.recv(SIZE).decode()

        # Check if the received ACK message is valid
        ack_valid = check_msg(ack_msg, MY_IP)
        if not ack_valid:
            client_socket.close()
            TTT.quit()
        
        ###################################################################
        
        # Create a new instance of the TTT class for the game
        root = TTT(client=False, target_socket=client_socket, src_addr=MY_IP, dst_addr=client_addr[0])

        # Start the game with the randomly selected start_user
        root.play(start_user=start)
        root.mainloop()

        # Close the client socket after the game is finished
        client_socket.close()
        break  # Exit the loop after one game

    # Close the server socket
    server_socket.close()