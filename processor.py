import gymnasium as gym
import subprocess
import socket
import kagglehub
import os

class Model():
    def __init__(self, path, model, address, port, verbose, visible):
        # Initialize Processor
        self.path = path
        self.model = model
        self.address = address
        self.port = port
        self.verbose = verbose
        self.visible = visible
        
        # Call function to launch FlexSim
        self._launch_flexsim()
    
    
    # Function to launch FlexSim    
    def _launch_flexsim(self):
        if self.verbose:
            print("\nLaunching FlexSim...")
            print("Loading Model: " + self.model)

        # Launch FlexSim with subprocess to load the model
        args = [self.path, self.model, self.address, str(self.port), str(self.verbose), str(self.visible)]
        self.process = subprocess.Popen(args)

        # Call function to initialize socket connection
        self._socket_init(self.address, self.port)
    
    
    # Function to close FlexSim
    def _close_flexsim(self):
        self.process.terminate()
        
    
    # Function to initialize socket connection (Server-side)
    def _socket_init(self, host, port):
        if self.verbose:
            print("Waiting for FlexSim to connect to socket on " + self.address + ":" + str(self.port) + "\n")
            
        # Initialize socket connection
        while True:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a socket object
            self.socket.bind((host, port)) # Bind socket to address and port
            self.socket.listen() # Listen for connections
            self.connection, self.address = self.socket.accept() # Accept connection
            if self.verbose:
                print("Socket connected successfully!")
        
            # Receive and send data from FlexSim
            with self.connection:
                while True:
                    # Receive data from FlexSim
                    print("Receiving data...")
                    data = self.connection.recv(1024)
                    if self.verbose:
                        print("Received data: " + data.decode('utf-8'))
                    if not data:
                        break
                    if data == b"READY":
                        raise RuntimeError("Did not receive READY! message")
                
                    # Send data to FlexSim
                    # print("\nSending data...")
                    self.connection.sendall(data)
                    # if self.verbose:
                    #     print("Sent data: " + data.decode('utf-8') + "\n")
                
                # Close connection if no data is received
                print("\nClosing connection...\n")
                self.connection.close()
        
    
def main():
    dataset_path = "C:/Users/steal/Documents/GitHub/FlexSim_Processor/Datasets/people-10-m"
    
    # Check if the dataset path exists
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset path '{dataset_path}' does not exist.")
        return
    
    # Download latest version
    try:
        datasetPath = kagglehub.dataset_download(dataset_path)
        print("Path to dataset files:", datasetPath)
    except ValueError as e:
        print(f"Error downloading dataset: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return
    
    flexsimPath = "C:/Program Files/FlexSim 2024 Update 2/program/flexsim.exe"  # Edit Local Path to FlexSim executable
    modelPath = "C:/Users/steal/Documents/GitHub/FlexSim_Processor/Model/ChangeoverTimesRL.fsm"  # Edit Local Path to FlexSim model
    host = '127.0.0.1' # This is the localhost
    port = 5005
    verbose = True
    visible = True
        
    Model(flexsimPath, modelPath, host, port, verbose, visible)
    
if __name__ == '__main__':
    main()