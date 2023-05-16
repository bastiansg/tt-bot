import requests


class DSP:
    def __init__(self, base_url: str = "http://0.0.0.0:8000/"):
        self.base_url = base_url

    def dsp_post(self, endpoint: str, json_data: dict = {}):
        url = f"{self.base_url}{endpoint}/"
        _ = requests.post(
            url,
            json=json_data,
        )

    def start_rand_inv(self):
        self.dsp_post("start_rand_inv")

    def stop_rand_inv(self):
        self.dsp_post("stop_rand_inv")

    def start_intermittent(self):
        self.dsp_post("start_intermittent")

    def stop_intermittent(self):
        self.dsp_post("stop_intermittent")

    def start_arrows(self):
        self.dsp_post("start_arrows")

    def stop_arrows(self):
        self.dsp_post("stop_arrows")

    def start_message(self, text: str, wait_time: float = 0.05):
        self.dsp_post(
            "start_message",
            json_data={
                "text": text,
                "wait_time": wait_time,
            },
        )

    def stop_message(self):
        self.dsp_post("stop_message")

    def clear(self):
        self.dsp_post("clear")
