import encoder as en
import decoder as de
import compressor as com
import flask
from noise import add_noise
from base64 import b64decode, b64encode
from hashlib import sha256
import json
from entropy import calculate_entropy

app = flask.Flask(__name__)

generator_polynomial = [1, 1, 0, 0, 0, 0, 1]
gen_copy = generator_polynomial.copy()

json_message = ""

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/receive-file', methods=['GET', 'POST'])
def receive_file():
    message = json.loads(json_message)
    enc_file = b64decode(message['encoded_message'][1:])
    encoding = message['encoding']
    sent_errors = message['errors']
    gen_poly = message['parameters'][0]
    n = message['parameters'][1]
    num_bytes = message['parameters'][2]
    comp_code = message['parameters'][3]

    sha_hash = message['SHA256']
    sent_entropy = message['entropy']

    msg_list = de.convert_to_binary_str(enc_file, num_bytes, n)
    decoded_msg, caught_errors = de.decode(msg_list, gen_poly, encoding)

    decompressed_file = com.decompress(decoded_msg, comp_code)

    return flask.render_template('decode.html', 
                                 sent_errors=sent_errors, caught_errors=caught_errors,
                                 sha_hash=sha_hash, received_hash=sha256(decompressed_file).digest().hex(), 
                                 sent_entropy=sent_entropy, received_entropy=calculate_entropy(decompressed_file))

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if flask.request.method == 'POST':
        f = flask.request.files['file']
        X = float(flask.request.form['noise'])

        file = f.stream.read()

        comp_code = com.get_compression_code(file)
        pure_enc_file = en.encode_file(file, comp_code, generator_polynomial)

        enc_file, errors = add_noise(pure_enc_file, en.n, X)
        enc_file_bytes, num_bytes = en.convert_to_bytes(enc_file)
        b64_file = b64encode(enc_file_bytes)
        
        message = {
            "encoded_message": str(b64_file),
            "compression_algorithm": "fano-shannon",
            "encoding": "cyclic",
            "parameters": [gen_copy, en.n, num_bytes, comp_code],
            "errors": errors,
            "SHA256": sha256(file).digest().hex(),
            "entropy": calculate_entropy(file)
        }

        global json_message
        json_message = json.dumps(message)

        return flask.redirect(flask.url_for('receive_file'))
    
if __name__ == '__main__':
    app.run()