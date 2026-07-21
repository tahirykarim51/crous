import requests
from bs4 import BeautifulSoup
import time
import os

# Function to check housing availability
def check_housing():
    url = 'https://trouverunlogement.lescrous.fr/tools/47/search?bounds=2.224122_48.902156_2.4697602_48.8155755'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the <h2> tag with the specific class
    h2_tag = soup.find('h2', class_='SearchResults-mobile svelte-8mr8g')
    
    if h2_tag and 'Aucun logement trouvé' not in h2_tag.text:
        return True
    return True

# Function to send notification
def send_notification():
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    message = 'De nouveaux logements CROUS ont été trouvés à Paris!'
    
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {'chat_id': chat_id, 'text': message}
    
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print('✅ Notification sent successfully.')
    else:
        print('❌ Failed to send notification.')

# Start bot loop
def main():
    print("🚀 Bot started...")
    already_notified = False
    while True:
        try:
            if check_housing():
                if not already_notified:
                    send_notification()
                    already_notified = True
            else:
                already_notified = False
            time.sleep(60)
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(5)

if __name__ == '__main__':
    main()
