import string
import serial
import serial.tools.list_ports
import sys
import time
from datetime import datetime

class receiver():
    def __init__(
            self, 
            port: str, 
            baudrate: int = 115200, 
            timeout: float = 1
        ):
        
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        
        try:
            self.serial = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout,
                xonxoff=False,
                rtscts=False,
                write_timeout=timeout,
                dsrdtr=False,
                inter_byte_timeout=None
            )
        except serial.SerialException as e:
            print(f'WARNING: Serial Exeption')
            print(e)
            self.serial = None
            raise

    def read_response(self):
        return self.serial.readline().decode('utf-8').strip()

    def check_connection(self):
        return self.serial.is_open
    
    def send_command(self, command):
        self.serial.write(command)

    def close(self):
        self.serial.close()


def list_ports():
    if sys.platform.startswith('win'):  # For Windows
        return [port.device for port in serial.tools.list_ports.comports()]
    elif sys.platform.startswith(('linux', 'cygwin')):  # For Linux and Cygwin
        return [port.device for port in serial.tools.list_ports.comports() if port.device.startswith('/dev/ttyUSB') or port.device.startswith('/dev/ttyACM')]
    
    return []

def main(argv: string) -> int:
    
    ports = list_ports()
    
    print("Available COM ports:")
    for idx, port in enumerate(ports):
        print(f"{idx}: {port}")

    idx = int(input("Enter the number of the COM port to connect: "))
    port = ports[idx]

    com = receiver(port)
    
    datapoints = [] 
    samples_countdown = 10
    sample_count = 1

    while com.check_connection():
      if samples_countdown <= 0:
        break
      ping = 0
      start = datetime.now()
      response = com.read_response()
      print(f"Sample {sample_count}: {response}")
      # with open('Dados-Teste-Estatico/Calibrar_celula/Dados.txt', 'a') as file:
          # file.write(response + '\n')
      datapoints.append(response)
      stop = datetime.now()
      ping = (stop - start).total_seconds() * 1000
      time.sleep(ping / 1000 if ping > 0 else 0.5)
    else:
      print(f"Warning: broken connection, max amout of samples {sample_count}")

    com.close()
    
    return 0

if __name__ == "__main__":
    exit(main(sys.argv))