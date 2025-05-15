from flask import Flask, render_template, request, send_file, jsonify
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

def pad_key(key):
    # Ensure the key is exactly 8 bytes
    if len(key) > 8:
        return key[:8]
    return key.ljust(8, b'*')

def encrypt_file(input_file, key):
    # Pad the key to be exactly 8 bytes
    padded_key = pad_key(key.encode())
    
    # Create DES cipher
    cipher = DES.new(padded_key, DES.MODE_ECB)
    
    # Read and encrypt the file
    file_data = input_file.read()
    padded_data = pad(file_data, DES.block_size)
    encrypted_data = cipher.encrypt(padded_data)
    
    return encrypted_data

def decrypt_file(encrypted_data, key):
    # Pad the key to be exactly 8 bytes
    padded_key = pad_key(key.encode())
    
    # Create DES cipher
    cipher = DES.new(padded_key, DES.MODE_ECB)
    
    # Decrypt the data
    decrypted_data = cipher.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, DES.block_size)
    
    return unpadded_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    if 'file' not in request.files:
        return jsonify({'error': 'Vui lòng chọn file để mã hóa'}), 400
    
    file = request.files['file']
    key = request.form.get('key', '')
    
    if not file or not key:
        return jsonify({'error': 'Vui lòng chọn file và nhập khóa mã hóa'}), 400
    
    try:
        # Encrypt the file
        encrypted_data = encrypt_file(file, key)
        
        # Save encrypted data to temporary file
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'encrypted_' + file.filename)
        with open(temp_path, 'wb') as f:
            f.write(encrypted_data)
        
        return send_file(
            temp_path,
            as_attachment=True,
            download_name=f'encrypted_{file.filename}'
        )
    except Exception as e:
        return jsonify({'error': f'Lỗi khi mã hóa file: {str(e)}'}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if 'file' not in request.files:
        return jsonify({'error': 'Vui lòng chọn file để giải mã'}), 400
    
    file = request.files['file']
    key = request.form.get('key', '')
    
    if not file or not key:
        return jsonify({'error': 'Vui lòng chọn file và nhập khóa giải mã'}), 400
    
    try:
        # Read encrypted data
        encrypted_data = file.read()
        
        # Decrypt the file
        decrypted_data = decrypt_file(encrypted_data, key)
        
        # Save decrypted data to temporary file
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'decrypted_' + file.filename.replace('encrypted_', ''))
        with open(temp_path, 'wb') as f:
            f.write(decrypted_data)
        
        return send_file(
            temp_path,
            as_attachment=True,
            download_name=f'decrypted_{file.filename.replace("encrypted_", "")}'
        )
    except Exception as e:
        return jsonify({'error': f'Lỗi khi giải mã file: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True) 