import cv2
import telebot
import numpy as np
class Detector():
    def is_cloud_exist(self, input_video):
        _, frame = input_video.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_blue = np.array([60, 50, 50])
        upper_blue = np.array([240, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        kernel = np.ones((5, 5), np.uint8)
        closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(frame, contours, -1, (255, 0, 255), 2)
        cv2.imshow('Cloud Detection', frame)
        cv2.waitKey(1)
        return len(contours)

class Sender():
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id
    def send_message(self, message):
        self.bot.send_message(chat_id=self.chat_id, text=message)

class Application():
    def __init__(self, input_video, bot_token, chat_id):
        self.input_video = input_video
        self.bot = telebot.TeleBot(bot_token)
        self.sender = Sender(self.bot, chat_id)
        self.detector = Detector()
    def run(self):
        threshold = 6
        while True:
            if self.detector.is_cloud_exist(self.input_video) > threshold:
                message = "Cloudy"
            else:
                message = "Not cloudy"
            self.sender.send_message(message)

if __name__ == "__main__":
    bot_token = "Token"
    chat_id = "Chat_id"
    input_video = cv2.VideoCapture(0)
    myapp = Application(input_video,bot_token,chat_id)
    myapp.run()