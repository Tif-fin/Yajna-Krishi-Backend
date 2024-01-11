from firebase_admin import messaging
import logging

def send_notification_to_token():
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler('log/app.log')  
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger.info("Started sending notification")

    message = messaging.Message(
        notification=messaging.Notification(title="सूचना", body="तपाईंको क्षेत्रमा लेट ब्लाइटको अपडेट छ। तिनीहरूलाई जाँच गर्न यहाँ क्लिक गर्नुहोस्"), topic="lateblight"
    )
    response = messaging.send(message)
    print('Notification sent:', response)
    return response

    



