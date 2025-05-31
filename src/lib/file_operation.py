import subprocess
import time
from src.lib.crypto_tool import *
from src.lib.config import ignore_list
from pathlib import Path
from src.lib.Char_diff_tool import *
import os
import stat
import shutil
from src.lib.crypto_tool import der_decrypt_file


def check_is_ignore(dir_path):
    for ignore in ignore_list:
        if ignore in dir_path or Path(dir_path).name == '.git':
            #print(dir_path)
            return True
    return False

def to_encryptor_dir_path(root_path, encrypt_path, file_path):
    source = Path(root_path)
    backup = Path(encrypt_path)
    if not backup.exists():
        backup.mkdir(parents=True, exist_ok=True)
    file_path = Path(file_path)

    # Calculate the relative path of the original path to the root directory
    relative_path = file_path.relative_to(source)

    # Calculate the backup path
    backup_path = backup / relative_path

    if not backup_path.parent.exists():
        backup_path.parent.mkdir(parents=True, exist_ok=True)
    return backup_path

# for Windows systems
# def get_folder_size(folder_path):
#     total_size = 0
#     for dirpath, dirnames, filenames in os.walk(folder_path):
#         for filename in filenames:
#             file_path = os.path.join(dirpath, filename)
#             if os.path.exists(file_path):  # ensure file_path exists
#                 total_size += os.path.getsize(file_path)
#     size_in_mb = total_size / (1024 * 1024)  # MB
#     return size_in_mb

def copy_repo_and_files(project_path, copy_path):
    for dir_path, dir_names, file_names in os.walk(project_path):
        if check_is_ignore(dir_path):
            continue
        for file_name in file_names:
            one_file_path = os.path.join(dir_path, file_name)
            target_file_path = to_encryptor_dir_path(project_path, copy_path, one_file_path)
            #print(copy_path)
            copy_one_whole_file(one_file_path, target_file_path)

def copy_repo_and_enc_files(project_path, encrypt_path, test_num=1):
    run_time = 0
    for dir_path, dir_names, file_names in os.walk(project_path):
        if check_is_ignore(dir_path):
            continue
        for file_name in file_names:
            one_file_path = os.path.join(dir_path, file_name)
            target_file_path = to_encryptor_dir_path(project_path, encrypt_path, one_file_path)
            ts1, ts2 = process_one_whole_file(one_file_path, target_file_path, test_num)
            run_time = run_time + ts1
    return run_time

def copy_repo_and_enc_lines(project_path, encrypt_path):
    run_time = 0
    for dir_path, dir_names, file_names in os.walk(project_path):
        if check_is_ignore(dir_path):
            continue
        for file_name in file_names:
            one_file_path = os.path.join(dir_path, file_name)
            target_file_path = to_encryptor_dir_path(project_path, encrypt_path, one_file_path)
            ts1, ts2 = process_file_by_line(one_file_path, target_file_path, test_num=1)
            run_time = run_time + ts1
    return run_time

def copy_repo_and_enc_DE(project_path, encrypt_path):
    run_time = 0
    for dir_path, dir_names, file_names in os.walk(project_path):
        if check_is_ignore(dir_path):
            continue
        for file_name in file_names:
            one_file_path = os.path.join(dir_path, file_name)
            target_file_path = to_encryptor_dir_path(project_path, encrypt_path, one_file_path)
            ts1, ts2 = process_one_whole_file_DE(one_file_path, target_file_path, test_num=1)
            run_time = run_time + ts1
    return run_time

def copy_one_whole_file(file_path, target_file_path):
    with open(file_path, 'rb') as f1:
        with open(target_file_path, 'wb') as f2:
            f2.write(f1.read())
    #print(f'[* copy_project_and_encrypt_files log] encrypt one file {file_path} to {target_file_path} by whole')
    return True

# used for Windows system
# def delete_all_files_in_directory(directory):
#     # Iterate over all files and subdirectories in the folder
#     for root, dirs, files in os.walk(directory, topdown=False):  # topdown=False Start with the subfolders
#         for name in files:
#             file_path = os.path.join(root, name)
#             try:
#                 os.chmod(file_path, stat.S_IWRITE)
#                 os.remove(file_path)  # delete file_path
#                 #print(f"Deleted: {file_path}")
#             except Exception as e:
#                 print(f"Error deleting {file_path}: {e}")
#
#         for name in dirs:
#             dir_path = os.path.join(root, name)
#             try:
#                 os.chmod(dir_path, stat.S_IWRITE)
#                 shutil.rmtree(dir_path)  # delete dir_path
#                 #print(f"Deleted directory: {dir_path}")
#             except Exception as e:
#                 print(f"Error deleting directory {dir_path}: {e}")

def move_and_rename_file(source_path, target_path, overwrite=False):
    """
    Move and rename the file (or create the destination directory if it doesn't exist).

    :param source_path: The full path to the source file
    :param target_path: The full path to the object file
    :param overwrite: Whether to overwrite the object file if it already exists (Default False)
    """
    source_path = Path(source_path)
    target_path = Path(target_path)

    if not source_path.exists():
        raise FileNotFoundError(f"source path does not exist: {source_path}")

    # Make sure the destination directory exists
    target_dir = target_path.parent
    target_dir.mkdir(parents=True, exist_ok=True)

    # if the file already exists
    if target_path.exists():
        if overwrite:
            target_path.unlink()  # delete
        else:
            raise FileExistsError(f"source path already exists: {target_path}")

    # Perform file movement (with filename changes supported)
    source_path.rename(target_path)
    #print(f"The file has been moved and renamed: {source_path} -> {target_path}")

def remove_empty_dirs(base_dir, reference_dir):
    """
    Removes the empty folder in base_dir or if the path does not exist in reference_dir.

    :param base_dir: Folders to clean up
    :param reference_dir: Reference folder
    """
    base_dir = Path(base_dir).resolve()
    reference_dir = Path(reference_dir).resolve()

    # Iterate over all subdirectories of base_dir
    for folder in sorted(base_dir.rglob("*"), key=lambda p: -len(p.parts)):
        if folder.is_dir() and not any(folder.iterdir()):  # Folder directory is empty
            relative_path = folder.relative_to(base_dir)  # Calculate relative paths
            reference_path = reference_dir / relative_path  # Compute the corresponding path in Reference folder

            if not reference_path.exists():
                try:
                    folder.rmdir()
                    #print(f"Deleted empty folder: {folder}")
                except Exception as e:
                    print(f"Failed to delete {folder}: {e}")

def process_file_by_line(file_path, target_file_path, test_num):
    # If the file can be Unicode decoded follow the line encryption otherwise encrypt the entire file
    total_enc_time = 0
    start = time.perf_counter()
    try:
        with open(file_path, 'r', encoding='utf-8') as f1:
            final_content = b''
            for _ in range(test_num):
                enc_time = 0
                for line in f1.readlines():
                    #print(line)
                    start_enc = time.perf_counter()
                    final_content += base64.b64encode(encrypt_aes(line.encode())) + b'\n'
                    end_enc = time.perf_counter()
                    enc_time = enc_time + end_enc - start_enc
                total_enc_time = total_enc_time + enc_time
            ts = total_enc_time/test_num
            # print(target_file_path)
            with open(target_file_path, 'wb') as f2:
                f2.write(final_content)
        #print(f'[* copy_project_and_encrypt_files log] encrypt one file {file_path} to {target_file_path} by lines')
    except UnicodeDecodeError:
        with open(file_path, 'rb') as f1:
            content = f1.read()
        cipher = b''
        for _ in range(test_num):
            start_enc = time.perf_counter()
            cipher = base64.b64encode(encrypt_aes(content))
            end_enc = time.perf_counter()
            total_enc_time = total_enc_time + (end_enc - start_enc)
        ts = total_enc_time / test_num
        with open(target_file_path, 'wb') as f2:
            f2.write(cipher)
        #print(f'[* copy_project_and_encrypt_files log] encrypt one file {file_path} to {target_file_path} by whole')
    end = time.perf_counter()
    return ts, end - start - total_enc_time

def process_one_whole_file(file_path, target_file_path, test_num=1):
    start = time.perf_counter()
    with open(file_path, 'rb') as f1:
        content = f1.read()
    total_enc_time = 0
    cipher = b''
    for _ in range(test_num):
        start_enc = time.perf_counter()
        cipher = base64.b64encode(encrypt_aes(content))
        end_enc = time.perf_counter()
        enc_time = end_enc - start_enc
        total_enc_time = total_enc_time + enc_time
    with open(target_file_path, 'wb') as f2:
        f2.write(cipher)
    # print(f'[* copy_project_and_encrypt_files log] encrypt one file {file_path} to {target_file_path} by whole')
    end = time.perf_counter()
    ts = total_enc_time/test_num
    return ts, end - start - total_enc_time
    # with open(file_path, 'rb') as f1:
    #     with open(target_file_path, 'wb') as f2:
    #         f2.write(base64.b64encode(encrypt_aes(f1.read())))
    # #print(f'[* copy_project_and_encrypt_files log] encrypt one file {file_path} to {target_file_path} by whole')
    # return True


def process_one_whole_file_DE(file_path, target_file_path, test_num = 1):
    start = time.perf_counter()
    total_enc_time = 0
    cipher = b''
    with open(file_path, 'rb') as f1:
        content = f1.read()
    for _ in range(test_num):
        start_enc = time.perf_counter()
        cipher = base64.b64encode(der_encrypt_file(content))
        end_enc = time.perf_counter()
        total_enc_time = total_enc_time + (end_enc - start_enc)
    ts = total_enc_time/test_num
    with open(target_file_path, 'wb') as f2:
        f2.write(cipher)
    #print(f'[* copy_project_and_encrypt_files log] encrypt one file {file_path} to {target_file_path} by whole')
    end = time.perf_counter()
    return ts, end - start - total_enc_time
    # with open(file_path, 'rb') as f1:
    #     with open(target_file_path, 'wb') as f2:
    #         f2.write(base64.b64encode(der_encrypt_file(f1.read())))
    # #print(f'[* copy_project_and_encrypt_files log] encrypt one file {file_path} to {target_file_path} by whole')
    # return True

def delete_all_except_git(directory):
    # Iterate over all files and subdirectories in the folder
    for root, dirs, files in os.walk(directory, topdown=False):
        if '.git' in root:
            continue
        # If the current folder is a.git folder, skip it
        if '.git' in dirs:
            dirs.remove('.git')  # Exclude the.git folder to prevent access and delete its contents

        for name in files:
            file_path = os.path.join(root, name)
            try:
                os.remove(file_path)  # delete
                #print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
        # Delete subdirectories (except.git folder)
        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                shutil.rmtree(dir_path)
                #print(f"Deleted directory: {dir_path}")
            except Exception as e:
                print(f"Error deleting directory {dir_path}: {e}")

def update_file_cipher_line(enc_byte, lines_to_delete, lines_to_insert, line_context):
    start_del = time.perf_counter()

    lines_to_delete_set = set(lines_to_delete)

    enc_byte = enc_byte.splitlines()

    lines = [line for i, line in enumerate(enc_byte, start=1) if i not in lines_to_delete_set]

    end_del = time.perf_counter()
    del_time = end_del - start_del

    start_ins = time.perf_counter()

    final_size = len(lines) + len(lines_to_insert)
    updated_lines = [None] * final_size

    plain_len = 0
    enc_time = 0
    current_insert_index = 0  # Index of the current insertion point
    current_updated_index = 0

    cipher_delta_len = 0

    for current_line_no, line in enumerate(lines):
        # insert new lines
        while (current_insert_index < len(lines_to_insert) and
               lines_to_insert[current_insert_index] == current_updated_index + 1):
            content = line_context[current_insert_index]
            plain_len = plain_len + len(content.encode())
            # if len(content.encode()) != 500:
            #     print(f"line index: {current_updated_index + 1}, line len: {len(content.encode())}")
            start_enc = time.perf_counter()
            one_line_enc_byte = base64.b64encode(encrypt_aes(content.encode() + b'\n'))
            cipher_delta_len = cipher_delta_len + len(one_line_enc_byte)
            end_enc = time.perf_counter()
            enc_time = enc_time + end_enc - start_enc
            #one_line_enc_byte = content.encode()
            updated_lines[current_updated_index] = one_line_enc_byte
            current_updated_index += 1
            current_insert_index += 1

        # insert the current line
        updated_lines[current_updated_index] = line
        current_updated_index += 1

        # Insert line numbers beyond the end of the file
    while current_insert_index < len(lines_to_insert):
        content = line_context[current_insert_index]
        start_enc1 = time.perf_counter()
        one_line_enc_byte = base64.b64encode(encrypt_aes(content.encode() + b'\n'))
        cipher_delta_len = cipher_delta_len + len(one_line_enc_byte)
        plain_len = plain_len + len(content.encode())
        end_enc1 = time.perf_counter()
        enc_time = enc_time + end_enc1 - start_enc1
        #one_line_enc_byte = content.encode()
        updated_lines[current_updated_index] = one_line_enc_byte
        current_updated_index += 1
        current_insert_index += 1

    end_ins = time.perf_counter()

    update_time = end_ins - start_ins - enc_time + del_time

    ins_time = end_ins - start_ins - enc_time

    #print(f'len: {plain_len}')

    return b'\n'.join(updated_lines) + b'\n', enc_time, update_time, del_time, ins_time, cipher_delta_len


def update_file_cipher_patch(enc_byte, parent_data_byte, current_data_byte):
    delta = time.perf_counter()
    cipher_delta_len = 0
    comp_patch_time = 0
    enc_time = 0
    try:
        parent_data_str = parent_data_byte.decode('utf-8')
        current_data_str = current_data_byte.decode('utf-8')
        start_patch = time.perf_counter()
        patch = create_patch(parent_data_str, current_data_str)
        serialized_patch = serialize_patch(patch)
        end_patch = time.perf_counter()
        comp_patch_time = end_patch - start_patch
        start_enc = time.perf_counter()
        enc_serialized_patch = base64.b64encode(encrypt_aes(serialized_patch.encode()))
        end_enc = time.perf_counter()
        enc_time = end_enc - start_enc
        cipher_delta_len = cipher_delta_len + len(enc_serialized_patch)
        final_byte = enc_byte + b'\n'
        final_byte += enc_serialized_patch
    except UnicodeDecodeError:
        #print('0')
        enc_byte = encrypt_aes(current_data_byte)
        final_byte = base64.b64encode(enc_byte)
    delta_end = time.perf_counter()
    #print(delta_end - delta)
    return final_byte, cipher_delta_len, comp_patch_time, enc_time

def decrypt_one_file_line(file_path):
    # If the file can be Unicode decoded follow the line decryption otherwise decrypt the entire file
    try:
        with open(file_path, 'r', encoding='utf-8') as f1:
            cipher_lines = f1.readlines()
        start = time.perf_counter()
        line_num = len(cipher_lines)
        final_content = [None] * line_num
        for x in range(line_num):
            final_content[x] = decrypt_aes(base64.b64decode(cipher_lines[x]))
        final_plain = b''.join(final_content)
        end = time.perf_counter()
        dec_time = end - start
    except UnicodeDecodeError:
        with open(file_path, 'rb') as f1:
            ciphertext = f1.read()
        start = time.perf_counter()
        final_plain = decrypt_aes(base64.b64decode(ciphertext))
        end = time.perf_counter()
        dec_time = end - start
        #print(f'[* copy_project_and_encrypt_files log] encrypt one file {file_path} to {target_file_path} by whole')
    return dec_time, final_plain

def is_binary_file_equal(file_path, target_bytes):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()

        content = content.replace(b'\r\n', b'\n')
        target_bytes = target_bytes.replace(b'\r\n', b'\n')
        if not content == target_bytes:
            print(content)
            #print("plain:")
            print(target_bytes)
        return content == target_bytes
    except Exception as e:
        print(f"read file fails: {e}")
        return False


def decrypt_one_file_line_rw(file_path, target_file_path):
    # If the file can be Unicode decoded follow the line decryption otherwise decrypt the entire file
    try:
        with open(file_path, 'rb') as f1:
            cipher_lines = f1.readlines()
        # print(file_path)
        lines = [line.rstrip(b'\n') for line in cipher_lines]
        #print(lines)
        start = time.perf_counter()
        line_num = len(cipher_lines)
        #print(line_num)
        final_content = [None] * line_num
        for x in range(line_num):
            # print(lines[x])
            final_content[x] = decrypt_aes(base64.b64decode(lines[x]))
            #print(final_content[x])
        plaintext = b''.join(final_content)
        #print(plaintext)
        end = time.perf_counter()
        dec_time = end - start
        #plaintext = plaintext.decode('utf-8')
        with open(target_file_path, 'wb') as f2:
            f2.write(plaintext)
        #print(f'[* copy_project_and_encrypt_files log] encrypt one file {file_path} to {target_file_path} by lines')
    except UnicodeDecodeError:
        print("coding error")
        with open(file_path, 'rb') as f1:
            ciphertext = f1.read()
        start = time.perf_counter()
        plaintext = decrypt_aes(base64.b64decode(ciphertext))
        end = time.perf_counter()
        dec_time = end - start
        with open(target_file_path, 'wb') as f2:
            f2.write(plaintext)
        #print(f'[* copy_project_and_encrypt_files log] encrypt one file {file_path} to {target_file_path} by whole')
    return dec_time, plaintext

def decrypt_one_file_patch_rw(pre_file, encrypted_file, decrypt_file):
    try:
        with open(encrypted_file, 'r') as file:
            lines = file.readlines()
        #encrypted_text = ''.join(lines[0]).rstrip()
        with open(pre_file, 'r') as f1:
            decrypted_text = f1.read()
        #decrypted_text = decrypt_aes(base64.b64decode(encrypted_text)).decode()
        start = time.perf_counter()
        for line in lines[1:]:
            start_enc = time.perf_counter()
            decrypted_patch = decrypt_aes(base64.b64decode(line)).decode()
            end_enc = time.perf_counter()
            #print(decrypted_patch)
            start_apply = time.perf_counter()
            patch = deserialize_patch(decrypted_patch)
            decrypted_text = apply_patch(decrypted_text, patch)
            end_apply = time.perf_counter()
            #print("dec patch time:", end_enc - start_enc)
            #print("apply patch time:", end_apply - start_apply)
            #print('applied patch')
        end = time.perf_counter()

        decrypted_text = decrypted_text.encode()

        with open(decrypt_file, 'wb') as f2:
            f2.write(decrypted_text)

    except UnicodeDecodeError:
        with open(encrypted_file, 'rb') as f1:
            cipher = f1.read()
        start = time.perf_counter()
        decrypted_text = decrypt_aes(base64.b64decode(cipher))
        end = time.perf_counter()
        with open(decrypt_file, 'wb') as f2:
            f2.write(decrypted_text)
    return end - start, decrypted_text

def decrypt_one_file_DE_rw(file_path, target_file_path):
    with open(file_path, 'rb') as f1:
        ciphertext = f1.read()
    start = time.perf_counter()
    plaintext = der_decrypt_file(base64.b64decode(ciphertext))
    end = time.perf_counter()
    with open(target_file_path, 'wb') as f2:
        f2.write(plaintext)
    #print(f'[* copy_project_and_encrypt_files log] encrypt one file {file_path} to {target_file_path} by whole')
    return end - start, plaintext

def decrypt_one_whole_file(file_path, target_file_path):
    with open(file_path, 'rb') as f1:
        ciphertext = f1.read()
    start = time.perf_counter()
    plaintext = decrypt_aes(base64.b64decode(ciphertext))
    end = time.perf_counter()
    with open(target_file_path, 'wb') as f2:
        f2.write(plaintext)
    #print(f'[* copy_project_and_encrypt_files log] encrypt one file {file_path} to {target_file_path} by whole')
    return end - start

def update_file_plain_line(pre_byte, lines_to_delete, lines_to_insert, line_context, recover_path):
    start = time.perf_counter()
    lines_to_delete_set = set(lines_to_delete)
    #pre_byte = pre_byte.splitlines()
    lines = [line for i, line in enumerate(pre_byte, start=1) if i not in lines_to_delete_set]
    final_size = len(lines) + len(lines_to_insert)
    #print(final_size)
    updated_lines = [None] * final_size


    current_insert_index = 0
    current_updated_index = 0

    cipher_delta_len = 0

    for current_line_no, line in enumerate(lines):
        # insert new lines
        while (current_insert_index < len(lines_to_insert) and
               lines_to_insert[current_insert_index] == current_updated_index + 1):
            content = line_context[current_insert_index]

            one_line_plain_byte = decrypt_aes(base64.b64decode(content))
            #print(one_line_plain_byte)

            updated_lines[current_updated_index] = one_line_plain_byte
            current_updated_index += 1
            current_insert_index += 1


        updated_lines[current_updated_index] = line
        current_updated_index += 1


    while current_insert_index < len(lines_to_insert):
        content = line_context[current_insert_index]

        one_line_plain_byte = decrypt_aes(base64.b64decode(content))

        updated_lines[current_updated_index] = one_line_plain_byte
        current_updated_index += 1
        current_insert_index += 1

    end = time.perf_counter()

    plaintext = b''.join(updated_lines)
    #print(updated_lines[0])

    with open(recover_path, 'wb') as f2:
        f2.write(plaintext)

    return end - start, plaintext

# used for linux system
def delete_all_files_in_directory(directory):
    # 遍历文件夹中的所有文件和子目录
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                os.chmod(file_path, stat.S_IRWXU)
                os.remove(file_path)
                #print(f"Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                os.chmod(dir_path, stat.S_IRWXU)
                shutil.rmtree(dir_path)
                #print(f"Deleted directory: {dir_path}")
            except Exception as e:
                print(f"Error deleting directory {dir_path}: {e}")

    # os.sync()