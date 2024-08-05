from flask import Flask, request, render_template_string
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext, Dispatcher
import threading

app = Flask(__name__)

# Telegram bot token
TOKEN = '7292593041:AAHWqRA7jn1oZu-dUmCNRjlsnvwAq1qD4BY'
bot = Bot(token=TOKEN)

# Create the Flask routes
@app.route('/')
def home():
    return 'Welcome to the Telegram WebApp Bot!'

@app.route('/connect')
def connect_wallet():
    return render_template_string('''
        <html>
        <head>
            <script src="https://cdn.jsdelivr.net/npm/@tonconnect/ui@0.0.0-0/dist/index.min.js"></script>
        </head>
        <body>
            <div id="ton-connect-ui"></div>
            <script>
                TonConnectUI.create({
                    manifestUrl: 'https://tonconnect.manifest.json'
                }).then(ui => {
                    ui.renderWalletSelector('#ton-connect-ui');
                });
            </script>
        </body>
        </html>
    ''')

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'OK'

# Telegram bot handlers
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! Use /connect to connect your wallet.')

def connect(update: Update, context: CallbackContext):
    update.message.reply_text('Connect your wallet here: http://web-production-2332.up.railway.app/connect')

# Set up the dispatcher
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('connect', connect))

# Set up a thread to run the Flask app
def run_app():
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    threading.Thread(target=run_app).start()
    bot.set_webhook(url='http://web-production-2332.up.railway.app/webhook')
