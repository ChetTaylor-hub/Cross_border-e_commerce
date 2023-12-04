import time
from ozon_Api import OzonApi




class Control():
    def __init__(self) -> None:
        self.goods_delivered_interval = None
        self.goods_delivered_message = None
        self.passport_registration_interval = None
        self.passport_registration_message = None
        self.start = False

        headers = {
            "Client-Id": "1499102",
            "Api-Key": "d8c89da0-9caa-4d70-b034-54a2f21c94a2",
        }

        self.ozonapi = OzonApi(headers)

    def save_auto_reply_settings(self, 
                                 goods_delivered_interval, 
                                 goods_delivered_message, 
                                 passport_registration_interval, 
                                 passport_registration_message):
        
        self.goods_delivered_interval = goods_delivered_interval
        self.goods_delivered_message = goods_delivered_message
        self.passport_registration_interval = passport_registration_interval
        self.passport_registration_message = passport_registration_message
        
    def get_auto_reply_settings(self):
        return (self.goods_delivered_interval, 
                self.goods_delivered_message, 
                self.passport_registration_interval, 
                self.passport_registration_message)
    
    def start_auto_reply(self):
        self.start = True

    def stop_auto_reply(self):
        self.start = False

    def ReminderRegisterPassportRun(self, start):

        while self.start:
            self.ozonapi.ReminderRegisterPassport(self.passport_registration_message)
            time.sleep(self.passport_registration_interval * 60)

    def ReminderDelivered(self, start):
        

        while start:
            self.ozonapi.ReminderDelivered(self.goods_delivered_message)
            time.sleep(self.goods_delivered_interval * 60)



if __name__ == "__main__":

    ozonapi = OzonApi(headers)

    

        
    
    while True:

        ozonapi.ReminderRegisterPassport()
        time.sleep(10)

