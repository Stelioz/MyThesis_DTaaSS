import subprocess
import socket
import pandas as pd
import os
import re


class Model:
    def __init__(self, path, model, address, port_number, verbose, visible, output_prefix):
        self.path = path
        self.model = model
        self.address = address
        self.port_number = port_number
        self.verbose = verbose
        self.visible = visible
        self.output_prefix = output_prefix

        self._launch_flexsim()

    def _launch_flexsim(self):
        if self.verbose:
            print("\nLaunching FlexSim...")
            print(f"Loading Model: {self.model}")

        args = [self.path, self.model, self.address, str(self.port_number), str(self.verbose), str(self.visible)]
        self.process = subprocess.Popen(args)

        self._socket_init(self.address, self.port_number)

    def _close_flexsim(self):
        if self.process:
            self.process.terminate()
            if self.verbose:
                print("FlexSim process terminated.")

    def _socket_init(self, host, port):
        if self.verbose:
            print(f"Waiting for FlexSim to connect to socket on {self.address}:{self.port_number}")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen()

        while True:
            self.connection, self.client_address = self.socket.accept()
            if self.verbose:
                print(f"Opening socket connection...\n")

            try:
                self._data_handle()
            except Exception as e:
                print(f"Error: {e}")
            finally:
                print("\nClosing socket connection...")
                self.connection.close()

    def _data_handle(self):
        with self.connection:
            print("Receiving data from FlexSim...")
            while True:
                data = self.connection.recv(1024)
                decoded_data = data.decode('utf-8')

                if not data:
                    print("No data received from FlexSim...")
                    break

                if self.verbose:
                    print(f"New entry from FlexSim \n{decoded_data}")

                if decoded_data == "PAUSE":
                    if self.verbose:
                        print("Simulation paused. Waiting for resumption...")
                    continue

                self._data_store(decoded_data)

                self.connection.sendall(b"ACK")

    def _data_store(self, data):
        cleaned_rows = []
        rows = data.strip().split("\n")
        for row in rows:
            cleaned_row = re.sub(
                r"Rank:"
                r"|Angle1: |Distance1: |Density1: |Angle2: |Distance2: |Density2: "
                r"|Angle3: |Distance3: |Density3: |Angle4: |Distance4: |Density4: "
                r"|Angle5: |Distance5: |Density5: |Angle6: |Distance6: |Density6: "
                r"|Angle7: |Distance7: |Density7: |Angle8: |Distance8: |Density8: "
                r"|Angle9: |Distance9: |Density9: ",
                "",
                row,
            )
            cleaned_rows.append(cleaned_row.split(", "))

        df = pd.DataFrame(cleaned_rows, columns=[
            "Rank",
            "Angle1", "Distance1", "Density1", "Angle2", "Distance2", "Density2",
            "Angle3", "Distance3", "Density3", "Angle4", "Distance4", "Density4",
            "Angle5", "Distance5", "Density5", "Angle6", "Distance6", "Density6",
            "Angle7", "Distance7", "Density7", "Angle8", "Distance8", "Density8",
            "Angle9", "Distance9", "Density9"
        ])

        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        csv_file_path = os.path.join("output", f"{self.output_prefix}_flexsim_data.csv")
        os.makedirs("output", exist_ok=True)
        file_exists = os.path.isfile(csv_file_path)
        df.to_csv(csv_file_path, mode='a', index=False, header=not file_exists)

        self._process_and_save_performances(csv_file_path)

        if df["Rank"].astype(int).max() >= 1000:
            print("Rank 1000 reached. Terminating the simulation.")
            self._close_flexsim()
            os._exit(0)

    def _process_and_save_performances(self, file_path):
        data = pd.read_csv(file_path)

        W_DISTANCE = 0.4
        W_ANGLE = 0.4
        W_DENSITY = 0.2
        MAX_DENSITY = 20

        def calculate_performance(angle, distance, density):
            performance = (
                (W_DISTANCE * (distance / 10)) +
                (W_ANGLE * (angle / 10)) -
                (W_DENSITY * (density / MAX_DENSITY))
            )
            return max(0, min(1, performance)) * 100

        result_data = data[["Rank"]].copy()

        for i in range(1, 7):
            performance_column = f"Camera{i}_Performance"
            result_data[performance_column] = data.apply(
                lambda row: calculate_performance(row[f"Angle{i}"], row[f"Distance{i}"], row[f"Density{i}"]),
                axis=1
            )

        # Include 'Rank' as the first column
        grouped_result = result_data.groupby("Rank").agg(
            {
                "Rank": "first",  # Preserve the Rank column
                **{f"Camera{i}_Performance": "max" for i in range(1, 7)}
            }
        )

        # Reorder columns to ensure 'Rank' is the first column
        grouped_result = grouped_result[["Rank"] + [f"Camera{i}_Performance" for i in range(1, 7)]]

        output_file_path = os.path.join("output", f"{self.output_prefix}_camera_performances.csv")
        grouped_result.to_csv(output_file_path, index=False)

        print("\nCamera Performances:")
        print(grouped_result)

        if self.verbose:
            print(f"Camera performances saved to: {output_file_path}")


def main():
    flexsimPath = "C:/Program Files/FlexSim 2024 Update 2/program/flexsim.exe"
    models_dir = "C:/Users/steal/Documents/GitHub/FlexSim_Processor/models/"
    
    print("Please choose the time of the day you want to simulate:")
    print("1: Morning")
    print("2: Noon")
    print("3: Afternoon")
    
    choice = input("\nEnter your choice (1/2/3): ").strip()
    model_map = {
        "1": ("9C_Model_Morning.fsm", "9c_morning"),
        "2": ("9C_Model_Noon.fsm", "9c_noon"),
        "3": ("9C_Model_Afternoon.fsm", "9c_afternoon")
    }
    
    if choice not in model_map:
        print("\nInvalid choice. Exiting...")
        return
    
    model_file, output_prefix = model_map[choice]
    modelPath = os.path.join(models_dir, model_file)
    host = '127.0.0.1'
    port = 5005
    verbose = True
    visible = True

    Model(flexsimPath, modelPath, host, port, verbose, visible, output_prefix)


if __name__ == '__main__':
    main()
