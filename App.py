from flask_classful import FlaskView, route
from flask import Flask, jsonify, request, render_template
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import rsa
import rsa

node = None


class App(FlaskView):

    def __init__(self):
        self.app = Flask(__name__)

    def start(self, port):
        App.register(self.app, route_base='/')
        self.app.run(host='0.0.0.0', port=port)

    def injectNode(self, injectedNode):
        global node
        node = injectedNode

    @route('/', methods=['GET'])
    def home(self):
        return render_template('index.html')

    @route('/generate', methods=['GET'])
    def generate(self):
        key = RSA.generate(2048)

        with open('keys/publicKey.pem', 'wb') as f:
            f.write(key.publickey().exportKey('PEM'))
            f.close()

        f = open('keys/privateKey.pem', 'wb')
        f.write(key.export_key('PEM'))
        f.close()

        return key.export_key('PEM')

    @route('/getPublic', methods=['GET'])
    def getPublic(self):
        f = open('keys/publicKey.pem', 'rb')
        return f.read()

    @route('/encode', methods=['GET'])
    def encodePage(self):
        f = open('keys/publicKey.pem', 'rb')
        pubKey = f.read()
        f.close()
        return render_template('encode.html', pubKey=pubKey)

    @route('/encode-message', methods=['GET'])
    def encodedMessage(self):
        message = request.args.get('message')

        key = RSA.import_key(open('keys/publicKey.pem').read())
        cipher = PKCS1_OAEP.new(key)
        encrypted = cipher.encrypt(message.encode('utf-8'))

        f = open('encoded.txt', 'wb')
        f.write(encrypted)
        f.close()

        f = open('encoded.txt', 'rb')
        text = f.read()
        f.close()

        return text

    @route('/decode', methods=['GET'])
    def decodePage(self):
        f = open('encoded.txt', 'rb')
        message = f.read()
        f.close

        f = open('keys/privateKey.pem', 'rb')
        privateKey = f.read()
        f.close()

        return render_template('decode.html', message=message, privateKey=privateKey)

    @route('/decode-message', methods=['GET'])
    def decodedMessage(self):

        key = RSA.import_key(open('keys/privateKey.pem').read())
        cipher = PKCS1_OAEP.new(key)

        f = open('encoded.txt', 'rb')

        decrypted = cipher.decrypt(f.read())
        return decrypted.decode("utf-8")

