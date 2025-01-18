import subprocess
import socket
import pandas as pd
import os
import re


class Model():
    def __init__(self, path, model, address, port_number, verbose, visible):
        # Initialize Model class with parameters
        self.path = path
        self.model = model
        self.address = address
        self.port_number = port_number
        self.verbose = verbose
        self.visible = visible
        
        self._launch_flexsim() # Call function to launch FlexSim
    
    
    # Function to launch FlexSim    
    def _launch_flexsim(self):
        if self.verbose:
            print("\nLaunching FlexSim...")
            print(f"Loading Model: {self.model}")

        # Launch FlexSim with subprocess to load the model
        args = [self.path, self.model, self.address, str(self.port_number), str(self.verbose), str(self.visible)]
        self.process = subprocess.Popen(args)

        # Call function to initialize socket connection
        self._socket_init(self.address, self.port_number)
    
    
    # Function to close FlexSim
    def _close_flexsim(self):
        if self.process:
            self.process.terminate()
            if self.verbose:
                print("FlexSim process terminated.")
        
    
    # Function to initialize socket connection (Server-side)
    def _socket_init(self, host, port):
        if self.verbose:
            print(f"Waiting for FlexSim to connect to socket on {self.address}:{self.port_number}")

        # Initialize socket connection once (outside the loop)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
        self.socket.bind((host, port))  # Bind socket to address and port
        self.socket.listen()  # Listen for connections

        # Loop to accept connections and handle data
        while True:
            self.connection, self.client_address = self.socket.accept()  # Accept connection
            if self.verbose:
                print(f"Opening socket connection...\n")

            try:
                self._data_handle()  # Call function to handle data
            except Exception as e:
                print(f"Error: {e}")
            finally:
                print("\nClosing socket connection...")
                self.connection.close()  # Close connection after handling data
     
    
    # Function to receive/send data to FlexSim
    def _data_handle(self):
        # Receive and send data from FlexSim
            with self.connection:
                print("Receiving data from FlexSim...")
                while True:
                    # Receive data from FlexSim
                    data = self.connection.recv(1024)
                    decoded_data = data.decode('utf-8')
                                        
                    if not data:
                        print("No data received from FlexSim...")
                        break

                    if self.verbose:
                        print(f"New entry from Flexsim \n {decoded_data}")
                    
                    # Handle the "PAUSE" message gracefully
                    if decoded_data == "PAUSE":
                        if self.verbose:
                            print("Simulation paused. Waiting for resumption...")
                        continue
                    
                    # Call the _data_store function to save the received data
                    self._data_store(decoded_data)
                    
                    # Send data to FlexSim
                    self.connection.sendall(b"ACK")  # The acknowledgment prevent freezing of FlexSim
                    
                    # # Handle the "READY" message gracefully
                    # if decoded_data == "READY":
                    #     if self.verbose:
                    #         print("Received 'READY' message, sending acknowledgment.")
                    #     self._send_data(b"ACK")  # Send acknowledgment to FlexSim
                    # else:
                    #     # Send back the same data as a default response
                    #     self._send_data(data)


    # Function to send data to FlexSim
    def _send_data(self, data):
        if self.connection:
            if self.verbose:
                print(f"Sending data: {data}")
            self.connection.sendall(data)
    

    # Function to store data in a CSV file
    def _data_store(self, data):
        # Use regular expressions to clean up the data
        cleaned_rows = []
        rows = data.strip().split("\n")  # Split data into rows

        # Loop through the rows and clean up the data
        for row in rows:
            # Remove specified labels using regex
            cleaned_row = re.sub(
                r"Rank: |Person: |ssn: "
                r"|Angle1: |Distance1: |Density1: |Angle2: |Distance2: |Density2: "
                r"|Angle3: |Distance3: |Density3: |Angle4: |Distance4: |Density4: "
                r"|Angle5: |Distance5: |Density5: |Angle6: |Distance6: |Density6: ",
                "",
                row,
            )
            cleaned_rows.append(cleaned_row.split(", "))  # Split fields by comma and space

        # Create a DataFrame from the cleaned data
        df = pd.DataFrame(cleaned_rows, columns=[
            "Rank", "Name & Surname", "SSN", 
            "Angle1", "Distance1", "Density1", "Angle2", "Distance2", "Density2",
            "Angle3", "Distance3", "Density3", "Angle4", "Distance4", "Density4",
            "Angle5", "Distance5", "Density5", "Angle6", "Distance6", "Density6"])

        # Define the CSV file path
        csv_file_path = os.path.join("output", "flexsim_data.csv")

        # Create the output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)

        # Check if the file already exists to determine whether to write the header
        file_exists = os.path.isfile(csv_file_path)

        # Append data to the CSV file
        df.to_csv(csv_file_path, mode='a', index=False, header=not file_exists)  # Append without header if file exists

        # Print a message to indicate that the entry was saved
        if self.verbose:
            print(f"Entry saved to filepath: {csv_file_path}\n")

        
    
def main():   
    flexsimPath = "C:/Program Files/FlexSim 2024 Update 2/program/flexsim.exe"  # Edit Local Path to FlexSim executable
    modelPath = "C:/Users/steal/Documents/GitHub/FlexSim_Processor/Model/Thesis_Model_v2.fsm" # Edit Local Path to FlexSim model
    host = '127.0.0.1' # This is the localhost
    port = 5005
    verbose = True
    visible = True
        
    Model(flexsimPath, modelPath, host, port, verbose, visible)
    
if __name__ == '__main__':
    main()