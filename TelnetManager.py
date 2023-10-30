from dataclasses import dataclass
from telnetlib import Telnet
import time
import logging


@dataclass
class TelnetConfig:
    host: str = "localhost"
    port: int = 4444


class TelnetMgr:
    def __init__(self, config: TelnetConfig = TelnetConfig()) -> None:
        self.config = config
        self.response = ""

    def connect(self):
        logging.info(f"Connecting to telnet on port '{self.config.port}'... ")
        self.tn = Telnet(self.config.host, self.config.port)
        time.sleep(0.02)
        logging.info(f"Connected!")

    def send_command(self, cmd: str):
        self.tn.write(f"{cmd}\n".encode("ascii"))
        self.response = self.tn.read_some().decode("ascii")

    def get_response(self) -> str:
        # time.sleep(0.01)
        return self.response

    def close(self):
        logging.info("Closing connection ... ")
        self.tn.close()

    def test_read_var(self):
        for i in range(1000):
            self.send_command("mdw 0x20000028")
            res = self.get_response()
            # res = res.strip().split(" ")

            print(res)

    def run(self):
        self.connect()
        # self.send_command("help")
        res = self.get_response()
        logging.info(res)
        self.test_read_var()
        logging.info(res)
        self.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    cfg = TelnetConfig()
    tn = TelnetMgr(cfg)
    tn.run()

    # with Telnet("127.0.0.1", 4444) as tn:
    #     tn.write(b"help\n")
    #     tn.close()
