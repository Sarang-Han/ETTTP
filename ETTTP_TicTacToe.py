
import re
import tkinter as tk
from socket import *
import _thread

SIZE=1024

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr, dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr
        self.recv_ip = src_addr
        
        self.total_cells = 9
        self.line_size = 3
        
        
        ############## updated ###########################
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-02-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': '#C3E7FA',
                     'win': 'Result: You Won!', 'text':'O','Name':"ME"}
            self.computer = {'value': 1, 'bg': '#FFDFDC',
                             'win': 'Result: You Lost!', 'text':'X','Name':"YOU"}   
        else:
            self.myID = 0 
            self.title('34743-02-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': '#FFDFDC',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': '#C3E7FA',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################

            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',25,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user=1):
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID:
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='#008000')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='#FF4500')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move):    
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='#FF4500')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


    def get_move(self):
        """
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        """
        ###################  Fill Out  #######################
        
        # Receive the message from the socket
        msg = self.socket.recv(SIZE).decode()
        msg_valid = check_msg(msg, self.recv_ip)

        # Check if the received message is valid
        if not msg_valid:
            self.socket.close()
            self.quit()
            return

        # Use regular expression to extract the row and column from the message
        match = re.search(r"New-Move:\((\d+),(\d+)\)", msg)
        if match:
            
            row, col = map(int, match.groups())
            
            # Construct the ACK message with the received move
            ack_msg = f"ACK ETTTP/1.0\r\nHost:{self.send_ip}\r\nNew-Move:({row},{col})\r\n\r\n"
            
            # Send the ACK message to the peer
            self.socket.send(str(ack_msg).encode())
            
            # Calculate the location on the board based on row and column
            loc = row * 3 + col
            
            ###################################################### 
            
            #vvvvvvvvvvvvvvvvvvv DO NOT CHANGE vvvvvvvvvvvvvvvvvvv
            # Update the board with the received move
            self.update_board(self.computer, loc, get=True)
            
            # Check if it's the current player's turn
            if self.state == self.active:
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status['text'] = ['Ready']
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                

    def send_debug(self):
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''

        # If it's not the current player's turn, clear the textbox and return
        if not self.my_turn:
            self.t_debug.delete(1.0,"end")
            return
        
        # Get the message from the input textbox
        d_msg = self.t_debug.get(1.0,"end")
        
        # Replace the newline characters with the correct format
        d_msg = d_msg.replace("\\r\\n","\r\n")  # msg is sanitized as \\r\\n is modified when it is given as input
        
        # Clear the textbox
        self.t_debug.delete(1.0,"end")
        
        ###################  Fill Out  #######################
        
        # Use regular expression to extract the row and column from the message
        match = re.search(r"New-Move:\((\d+),(\d+)\)", d_msg)
        if match:
            row, col = map(int, match.groups())
            user_move = row * 3 + col
            
            # Check if the selected cell on the board is empty
            if self.board[user_move] == 0:
                # Send the message to the peer
                self.socket.send(str(d_msg).encode())
                
                # Receive the ACK message from the peer
                ack_msg = self.socket.recv(SIZE).decode()
                
                # Check if the received ACK message is valid
                ack_valid = check_msg(ack_msg, self.recv_ip)
                
                if ack_valid:
                    loc = user_move
                else:
                    self.quit()
                    return
            else:
                return      

        ######################################################  
        
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        # Update the board with the user's move
        self.update_board(self.user, loc)
        
        # Check if it's the current player's turn
        if self.state == self.active:
            # It's the opponent's turn now
            self.my_turn = 0
            self.l_status_bullet.config(fg='#FF4500')
            self.l_status ['text'] = ['Hold']
            
            # Start a new thread to get the opponent's move
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        
    def send_move(self,selection):
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        # Calculate the row and column from the selection
        row,col = divmod(selection,3)
        
        ###################  Fill Out  #######################
        
        # Construct the send message with the selected row and column
        send_msg = f"SEND ETTTP/1.0\r\nHost:{self.send_ip}\r\nNew-Move:({row},{col})\r\n\r\n"
        
        # Send the message to the peer
        self.socket.send(str(send_msg).encode())
        
        # Receive the ACK message from the peer
        ack_msg = self.socket.recv(SIZE).decode()
        
        # Check if the received ACK message is valid and return the result
        return check_msg(ack_msg, self.recv_ip)
        
        ######################################################  

    
    def check_result(self,winner,get=False):
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        ###################  Fill Out  #######################
        
        # Construct the result message with the winner information
        own_result = f"RESULT ETTTP/1.0\r\nHost:{self.send_ip}\r\nWinner:{winner}\r\n\r\n"
        
        # Send the result message to the peer
        self.socket.send(str(own_result).encode())

        # Receive the result message from the peer
        peer_result = self.socket.recv(SIZE).decode()
        
        # Check if the received result message is valid
        result_valid = check_msg(peer_result, self.recv_ip)

        if get:
            # If the current user is getting the result (i.e., the peer is the winner)
            expected_winner = "ME" if winner == "YOU" else "YOU"
            
            # Check if the received result matches the expected winner and return the result
            return result_valid and peer_result.split('\r\n')[2].split(':')[1] == expected_winner
        else:
            # If the current user is reporting the result (i.e., the current user is the winner)
            expected_winner = "YOU" if winner == "ME" else "ME"
            
            # Check if the received result matches the expected winner and return the result
            return result_valid and peer_result.split('\r\n')[2].split(':')[1] == expected_winner

        ######################################################  

        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='#FF4500')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = '#90EE90'
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class
def check_msg(msg, recv_ip):
    """
    Checks if the received message is in ETTTP format.
    """
    ###################  Fill Out  #######################
    
    # Split the message into lines
    lines = msg.split('\r\n')
    
    # Check if the message has exactly 5 lines
    if len(lines) != 5:
        return False

    # Extract the message type and version
    type, version = lines[0].split()
    
    # Extract the host IP from the message
    host_ip = lines[1].split(':')[1].strip()

    # Check if the version is ETTTP/1.0 and if the host IP matches the expected IP
    if version != "ETTTP/1.0" or host_ip != recv_ip:
        return False

    # Check if the message type is SEND or ACK
    if type == "SEND" or type == "ACK":
        # Extract the first part of the third line
        first_part = lines[2].split(':')[0].strip()
        
        # Check if the first part is either "New-Move" or "First-Move"
        return first_part in ("New-Move", "First-Move")

    # If the message type is not SEND or ACK, check if it is RESULT
    return type == "RESULT"

    ######################################################