import gymnasium as gym
import subprocess
import socket

class Processor():
    def __init__(self, path, model, address, port, verbose, visible):
        self.path = path
        self.model = model
        self.address = address
        self.port = port
        self.verbose = verbose
        self.visible = visible
        
        self._launch_flexsim()
    
    # Function to launch FlexSim    
    def _launch_flexsim(self):
        if self.verbose:
            print("\nLaunching FlexSim...")
            print("Loading Model: " + self.model + "\n")

        args = [self.path, self.model, self.address, str(self.port), str(self.verbose), str(self.visible)]
        self.process = subprocess.Popen(args)

        self._socket_init(self.address, self.port)
    
    # Function to close FlexSim
    def _close_flexsim(self):
        self.process.terminate()
        
    # Function to initialize socket connection (Client-side)
    def _socket_init(self, socket_address, socket_port):
        if self.verbose:
            print("Initializing Socket connection on " + self.address + ":" + str(self.port))
            
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((socket_address, socket_port))
        
        (self.serversocket, self.serveraddress) = self.clientsocket.accept()
        if self.verbose:
            print("Socket connected")
        
        if self.verbose:
            print("Waiting for READY message")
        message = self._socket_recv()
        if self.verbose:
            print(message.decode('utf-8'))
        if message != b"READY":
            raise RuntimeError("Did not receive READY! message")
    
def main():
    flexsimPath = "C:/Program Files/FlexSim 2024 Update 2/program/flexsim.exe"  # Edit Local Path to FlexSim executable
    modelPath = "C:/Users/steal/Documents/FlexSim/Test_Models/ChangeoverTimesRL.fsm"  # Edit Local Path to FlexSim model
    host = 'localhost'
    port = 5005
    verbose = True
    visible = True
        
    Processor(flexsimPath, modelPath, host, port, verbose, visible)
    
if __name__ == '__main__':
    main()