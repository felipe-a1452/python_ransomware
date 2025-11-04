from cryptography.fernet import Fernet
import os
import sys

#constant
DEFAULT_DIR='arquivos'
IGN_ARQ=[os.path.basename(__file__), 'key.key','discovery.py','decrypt.py']
KEY_PATH='key.key'

def read_key(key_path):
    if not os.path.isfile(key_path):
        print(f'cryptography key not found!{key_path}')
    with open (key_path,'rb') as key_file:
        key=key_file.read()
    return key

def decrypt_file(key,all_files):
    decoded_file=[]
    for file in all_files:
        try:
            with open(file,'rb') as enc_file:
                content=enc_file.read()
            raw_content=Fernet(key).decrypt(content)
            with open(file,'wb') as dec_file:
                dec_file.write(raw_content)
            decoded_file.append(raw_content)
        except Exception as e:
            print(f'{e} encryption error')
    
    return decoded_file

def list_files(base_dir):
    all_files=[]
    
    for entry in os.listdir(base_dir):
        full_path=os.path.abspath(os.path.join(base_dir, entry))
        if os.path.isdir(full_path):
            all_files+=list_files(full_path)
        elif os.path.isfile(full_path) and entry is not IGN_ARQ:
            all_files.append(full_path)
    return all_files

def main():
    dir=sys.argv[1] if len(sys.argv)>1 else DEFAULT_DIR
    all_files=list_files(dir)
    key=read_key('key.key')
    decoded_files=decrypt_file(key,all_files)
    print(decoded_files)
    

if __name__ == '__main__':
    main()