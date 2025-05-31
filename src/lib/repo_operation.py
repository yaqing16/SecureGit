import subprocess
import re
from git import Repo
from src.lib.Git_command import *
from src.lib.file_operation import *

import logging

base_dir = Path(__file__).parent
#
# logging.basicConfig(
#     filename=base_dir.parent / 'log'/ 'test_update_time_log.log',
#     filemode='a',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s'
# )
#
# logging.getLogger('git').setLevel(logging.CRITICAL)

key_file = base_dir / 'private_key.der'

with open(key_file, 'rb') as private_file:
    sign_key = ECC.import_key(private_file.read())


def Init_for_line(project_path, encrypt_path, msg, flag):
    run_time = copy_repo_and_enc_lines(project_path, encrypt_path)
    repo_cipher = Repo(encrypt_path)
    repo_cipher.git.add('--all')
    repo_cipher.index.commit(msg)
    sign_time = 0
    if flag:
        commit_cipher = repo_cipher.commit('HEAD')
        start_sign = time.perf_counter()
        signature = generate_Signature(commit_cipher, sign_key)
        end_sign = time.perf_counter()
        sign_time = end_sign - start_sign
        # print(signature)
        repo_cipher.git.commit('--amend', '-m', signature)
    return run_time + sign_time

# return {
#         "added_files": added_files,
#         "added_files_content": added_files_content,
#         "deleted_files": deleted_files,
#         "renamed_files": renamed_files,
#         "modified_files": modified_files,
#         "deleted_lines": deleted_lines,
#         "inserted_lines": inserted_lines,
#         "inserted_content": inserted_content,
#     }

def copy_repo_and_files(result, project_path, copy_path):
    for dir_path, dir_names, file_names in os.walk(project_path):
        if check_is_ignore(dir_path):
            continue
        for file_name in file_names:
            one_file_path = os.path.join(dir_path, file_name)
            target_file_path = to_encryptor_dir_path(project_path, copy_path, one_file_path)
            #print(copy_path)
            copy_one_whole_file(one_file_path, target_file_path)

def Init_for_plain(result, project_path, copy_path):
    for one_file in result['modified_files']:
        target_file = copy_path / one_file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        copy_one_whole_file(project_path / one_file, target_file)
    for one_file in result['deleted_files']:
        target_file = copy_path / one_file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        copy_one_whole_file(project_path / one_file, target_file)
    for old_name, new_name in result['renamed_files']:
        target_file = copy_path / old_name
        target_file.parent.mkdir(parents=True, exist_ok=True)
        copy_one_whole_file(project_path / one_file, target_file)

def Update_plain(result, project_path, copy_path):
    for one_file in result['modified_files']:
        target_file = copy_path / one_file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        copy_one_whole_file(project_path / one_file, target_file)

def Update_plain_comm(result, project_path, copy_path):
    for one_file in result['modified_files']:
        target_file = copy_path / one_file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        copy_one_whole_file(project_path / one_file, target_file)
    for one_file in result['deleted_files']:
        file_name = copy_path / one_file
        if os.path.exists(file_name):
            os.remove(file_name)
    for old_name, new_name in result['renamed_files']:
        move_and_rename_file(copy_path / old_name, copy_path / new_name)



def Init_for_line_comp(result, project_path, encrypt_path):
    for one_file in result['modified_files']:
        target_file = encrypt_path / one_file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        process_file_by_line(project_path / one_file, target_file, 1)
    for one_file in result['deleted_files']:
        target_file = encrypt_path / one_file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        process_file_by_line(project_path / one_file, target_file, 1)
    for old_name, new_name in result['renamed_files']:
        target_file = encrypt_path / old_name
        target_file.parent.mkdir(parents=True, exist_ok=True)
        process_file_by_line(project_path / one_file, target_file, 1)

def Init_for_patch_comp(result, project_path, encrypt_path):
    for one_file in result['modified_files']:
        target_file = encrypt_path / one_file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        process_one_whole_file(project_path / one_file, target_file)
    for one_file in result['deleted_files']:
        target_file = encrypt_path / one_file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        process_one_whole_file(project_path / one_file, target_file)
    for old_name, new_name in result['renamed_files']:
        target_file = encrypt_path / old_name
        target_file.parent.mkdir(parents=True, exist_ok=True)
        process_one_whole_file(project_path / old_name, target_file)

def Init_for_DE_comp(result, project_path, encrypt_path):
    for one_file in result['modified_files']:
        target_file = encrypt_path / one_file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        process_one_whole_file_DE(project_path / one_file, target_file)
    for one_file in result['deleted_files']:
        target_file = encrypt_path / one_file
        target_file.parent.mkdir(parents=True, exist_ok=True)
        process_one_whole_file_DE(project_path / one_file, target_file)
    for old_name, new_name in result['renamed_files']:
        target_file = encrypt_path / old_name
        target_file.parent.mkdir(parents=True, exist_ok=True)
        process_one_whole_file_DE(project_path / old_name, target_file)


def Init_for_patch(project_path, encrypt_path, msg, flag):
    run_time = copy_repo_and_enc_files(project_path, encrypt_path)
    repo_cipher = Repo(encrypt_path)
    repo_cipher.git.add('--all')
    repo_cipher.index.commit(msg)
    sign_time = 0
    if flag:
        commit_cipher = repo_cipher.commit('HEAD')
        start_sign = time.perf_counter()
        signature = generate_Signature(commit_cipher, sign_key)
        end_sign = time.perf_counter()
        sign_time = end_sign - start_sign
        # print(signature)
        repo_cipher.git.commit('--amend', '-m', signature)
    return run_time + sign_time


def Init_for_Trivial(project_path, encrypt_path, msg, flag):
    run_time = copy_repo_and_enc_files(project_path, encrypt_path)
    # print("enc finish")
    repo_cipher = Repo(encrypt_path)
    repo_cipher.git.add('--all')
    repo_cipher.index.commit(msg)
    sign_time = 0
    if flag:
        commit_cipher = repo_cipher.commit('HEAD')
        start_sign = time.perf_counter()
        signature = generate_Signature(commit_cipher, sign_key)
        end_sign = time.perf_counter()
        # print(signature)
        sign_time = end_sign - start_sign
        repo_cipher.git.commit('--amend', '-m', signature)
    # all_files = []
    # batch_size = 1000
    # for root, dirs, files in os.walk(encrypt_path):
    #     for file in files:
    #         full_path = os.path.join(root, file)
    #         rel_path = os.path.relpath(full_path, encrypt_path)
    #         all_files.append(rel_path)
    #
    # # 分批添加
    # for i in range(0, len(all_files), batch_size):
    #     batch = all_files[i:i + batch_size]
    #     safe_remove_git_lock(repo_cipher.working_tree_dir)
    #     repo_cipher.index.add(batch)
    #     print(f"Added batch {i // batch_size + 1} with {len(batch)} files")
    # # repo_cipher.index.add(['.'])
    # print("trivial all")
    # repo_cipher.index.commit(msg)
    # print("trivial commit")
    return run_time + sign_time

def Init_for_DE(project_path, encrypt_path, msg, flag):
    run_time = copy_repo_and_enc_DE(project_path, encrypt_path)
    repo_cipher = Repo(encrypt_path)
    repo_cipher.git.add('--all')
    repo_cipher.index.commit(msg)
    sign_time = 0
    if flag:
        commit_cipher = repo_cipher.commit('HEAD')
        start_sign = time.perf_counter()
        signature = generate_Signature(commit_cipher, sign_key)
        end_sign = time.perf_counter()
        # print(signature)
        sign_time = end_sign - start_sign
        repo_cipher.git.commit('--amend', '-m', signature)
    return run_time + sign_time


def update_line_diff(repo_path, cipher_path, choice_commit, msg, flag, test_num=1):
    repo = Repo(repo_path)
    diff_run_time = 0
    for _ in range(test_num):
        start_diff = time.perf_counter()
        result = Get_git_diff(repo, choice_commit)
        end_diff = time.perf_counter()
        diff_run_time = diff_run_time + (end_diff - start_diff)
    diff_run_time = diff_run_time/test_num
    result = Get_git_diff(repo, choice_commit)
    # logging.info('git diff result: %s', result)
    # print("compute delta by line (s): ", diff_run_time)

    # Git diff return return {
    #     "added_files": added_files,
    #     "added_files_content": added_files_content,
    #     "deleted_files": deleted_files,
    #     "renamed_files": renamed_files,
    #     "modified_files": modified_files,
    #     "deleted_lines": deleted_lines,
    #     "inserted_lines": inserted_lines,
    #     "inserted_content": inserted_content,
    # }
    repo_cipher = Repo(cipher_path)

    sign_time = 0

    if result == '':
        repo_cipher.git.commit('--allow-empty', '-m', msg)
        commit_cipher = repo_cipher.commit('HEAD')
        start_sign = time.perf_counter()
        signature = generate_Signature(commit_cipher, sign_key)
        end_sign = time.perf_counter()
        sign_time = end_sign - start_sign
        # print(signature)
        repo_cipher.git.commit('--amend', '--allow-empty', '-m', f"{signature}")
        return diff_run_time + sign_time, diff_run_time, 0, 0

    repo_cipher = Path(cipher_path)
    repo_plain = Path(repo_path)

    rw_time = 0
    add_rw_time = 0
    cipher_delta_len = 0
    sum_enc_time = 0
    sum_update_ct_time = 0

    repo.git.checkout(choice_commit)

    for old_name, new_name in result['renamed_files']:
        move_and_rename_file(repo_cipher / old_name, repo_cipher / new_name)

    for del_name in result['deleted_files']:
        file_name = repo_cipher / del_name
        if os.path.exists(file_name):
            os.remove(file_name)

    start = time.perf_counter()

    # note: The version of choice_commit should be displayed in the repo folder.

    for add_name in result['added_files']:
        os.makedirs(os.path.dirname(repo_cipher / add_name), exist_ok=True)
        enc_time, time_rw = process_file_by_line(repo_plain / add_name, repo_cipher / add_name, test_num)
        sum_enc_time = sum_enc_time + enc_time
        add_rw_time = add_rw_time + time_rw

    for one_file, one_del, one_add, one_add_lines in zip(result['modified_files'], result['deleted_lines']
                                                                ,result['inserted_lines'], result['inserted_content']):
        if one_add == [] and one_del == [] and one_add_lines == []:
            enc_time, time_rw = process_file_by_line(repo_plain / one_file, repo_cipher / one_file, test_num)
            sum_enc_time = sum_enc_time + enc_time
            rw_time = rw_time + time_rw
            continue

        start_read = time.perf_counter()
        with open(repo_cipher / one_file, 'rb') as f1:
            lines = f1.readlines()
            enc_bytes = b''.join(lines)
        end_read = time.perf_counter()

        cipher_lines = b''
        enc_time, upd_time, cipher_delta = 0, 0, 0
        for _ in range(test_num):
            cipher_lines, enc_time_ite, upd_time_ite, del_time_ite, ins_time_ite, cipher_delta_ite = update_file_cipher_line(enc_bytes, one_del, one_add, one_add_lines)
            enc_time = enc_time + enc_time_ite
            upd_time = upd_time + upd_time_ite
            cipher_delta = cipher_delta + cipher_delta_ite

        sum_enc_time = sum_enc_time + enc_time/test_num
        sum_update_ct_time = sum_update_ct_time + upd_time/test_num
        cipher_delta_len = cipher_delta_len + cipher_delta/test_num
        start_write = time.perf_counter()
        with open(repo_cipher / one_file, 'wb') as file:
            file.write(cipher_lines)
        end_write = time.perf_counter()
        rw_time = rw_time + end_write - start_write + end_read - start_read
    end = time.perf_counter()
    remove_empty_dirs(cipher_path, repo_path)

    repo_cipher = Repo(cipher_path)
    repo_cipher.git.add('--all')
    repo_cipher.index.commit(msg)

    if flag:
        commit_cipher = repo_cipher.commit('HEAD')
        start_sign = time.perf_counter()
        signature = generate_Signature(commit_cipher, sign_key)
        end_sign = time.perf_counter()
        sign_time = end_sign - start_sign
    # print(signature)
        repo_cipher.git.commit('--amend', '--allow-empty', '-m', f"{signature}")
    return end - start - rw_time - add_rw_time + diff_run_time + sign_time, diff_run_time, sum_enc_time + sum_update_ct_time, cipher_delta_len


def update_patch_diff(repo_path, cipher_path, choice_commit, msg, flag, test_num = 1):
    repo = Repo(repo_path)
    current_commit = repo.commit(choice_commit)
    previous_commit = current_commit.parents[0] if current_commit.parents else None

    result = Get_git_diff(repo, choice_commit)
    #print("compute delta by line (s): ", diff_run_time)

    repo_cipher = Path(cipher_path)
    repo_plain = Path(repo_path)


    sign_time = 0



    if result == '':
        repo_cipher = Repo(cipher_path)
        repo_cipher.git.commit('--allow-empty', '-m', msg)
        commit_cipher = repo_cipher.commit('HEAD')
        start_sign = time.perf_counter()
        signature = generate_Signature(commit_cipher, sign_key)
        end_sign = time.perf_counter()
        sign_time = end_sign - start_sign
        # print(signature)
        repo_cipher.git.commit('--amend', '--allow-empty', '-m', f"{signature}")
        return sign_time, 0, 0, 0

    start = time.perf_counter()
    rw_time = 0
    add_rw_time = 0
    cipher_delta_len = 0
    comp_patch_time = 0
    sum_enc_time = 0

    repo.git.checkout(choice_commit)

    for old_name, new_name in result['renamed_files']:
        move_and_rename_file(repo_cipher / old_name, repo_cipher / new_name)

    for del_name in result['deleted_files']:
        file_name = repo_cipher / del_name
        if os.path.exists(file_name):
            os.remove(file_name)

    start = time.perf_counter()

    for add_name in result['added_files']:
        os.makedirs(os.path.dirname(repo_cipher / add_name), exist_ok=True)
        enc_time, time_rw = process_one_whole_file(repo_plain / add_name, repo_cipher / add_name, test_num)
        sum_enc_time = sum_enc_time + enc_time
        add_rw_time = add_rw_time + time_rw

    for one_file in result['modified_files']:
        start_read = time.perf_counter()
        modified_text = ''
        if choice_commit:
            current_content = current_commit.tree / one_file
            modified_text = current_content.data_stream.read()

        original_text = ''
        if previous_commit:
            try:
                parent_content = previous_commit.tree / one_file
                original_text = parent_content.data_stream.read()
            except KeyError:
                for old_name, new_name in result['renamed_files']:
                    if new_name == one_file:
                        parent_content = previous_commit.tree / old_name
                        original_text = parent_content.data_stream.read()

        with open(repo_cipher / one_file, 'rb') as f:
            original_cipher_bytes = f.read()

        end_read = time.perf_counter()

        final_bytes = b''

        cipher_delta, ts1, ts2 = 0, 0, 0
        for _ in range(test_num):
            final_bytes, cipher_delta_ite, ts1_ite, ts2_ite = update_file_cipher_patch(original_cipher_bytes, original_text, modified_text)
            # print('ts1_ite', ts1_ite)
            # print('ts2_ite', ts2_ite)
            ts1 = ts1 + ts1_ite
            ts2 = ts2 + ts2_ite
            cipher_delta = cipher_delta_ite + cipher_delta

        comp_patch_time = comp_patch_time + ts1 / test_num
        sum_enc_time = sum_enc_time + ts2 / test_num
        cipher_delta_len = cipher_delta_len + cipher_delta / test_num

        #print('re time:', end1 - start1)
        start_write = time.perf_counter()
        with open(repo_cipher / one_file, 'wb') as f:
            f.write(final_bytes)
        end_write = time.perf_counter()

        rw_time = rw_time + (end_write - start_write) + (end_read - start_read)

    end = time.perf_counter()
    remove_empty_dirs(cipher_path, repo_path)
    repo_cipher = Repo(cipher_path)
    repo_cipher.git.add('--all')
    repo_cipher.index.commit(msg)

    if flag:
        commit_cipher = repo_cipher.commit('HEAD')
        start_sign = time.perf_counter()
        signature = generate_Signature(commit_cipher, sign_key)
        end_sign = time.perf_counter()
        sign_time = end_sign - start_sign
        # print(signature)
        repo_cipher.git.commit('--amend', '--allow-empty', '-m', f"{signature}")
    return end - start - rw_time - add_rw_time + sign_time, comp_patch_time, sum_enc_time, cipher_delta_len


def update_file_diff(repo_path, cipher_path, choice_commit, msg, flag, test_num=1):
    repo = Repo(repo_path)
    start_diff = time.perf_counter()
    result = Get_git_diff(repo, choice_commit)
    end_diff = time.perf_counter()
    diff_run_time = end_diff - start_diff
    #print('compute delta by file (s):', diff_run_time)


    repo_cipher = Path(cipher_path)
    repo_plain = Path(repo_path)

    sign_time = 0

    if result == '':
        repo_cipher = Repo(cipher_path)
        repo_cipher.git.commit('--allow-empty', '-m', msg)
        return 0, 0, 0

    # start_init = time.perf_counter()
    current_commit = repo.commit(choice_commit)
    # for one_file in result["modified_files"]:
    #     directory = os.path.dirname(repo_cipher / one_file)
    #     if not os.path.exists(directory):
    #         os.makedirs(directory)
    #     process_one_whole_file_DE(repo_plain / one_file, repo_cipher / one_file)
    # end_init = time.perf_counter()
    rw_time = 0
    cipher_delta_len = 0
    sum_enc_time = 0
    add_rw_time = 0

    repo.git.checkout(choice_commit)

    for old_name, new_name in result['renamed_files']:
        move_and_rename_file(repo_cipher / old_name, repo_cipher / new_name)

    for del_name in result['deleted_files']:
        file_name = repo_cipher / del_name
        if os.path.exists(file_name):
            os.remove(file_name)

    start = time.perf_counter()
    for add_name in result['added_files']:
        os.makedirs(os.path.dirname(repo_cipher / add_name), exist_ok=True)
        enc_time, time_rw = process_one_whole_file_DE(repo_plain / add_name, repo_cipher / add_name, test_num)
        sum_enc_time = sum_enc_time + enc_time
        add_rw_time = add_rw_time + time_rw

    for one_file in result['modified_files']:
        start_read = time.perf_counter()
        modified_text = ''
        if choice_commit:
            current_content = current_commit.tree / one_file
            modified_text = current_content.data_stream.read()
        end_read = time.perf_counter()

        total_enc_time = 0
        for _ in range(test_num):
            start_enc = time.perf_counter()
            final_bytes = base64.b64encode(der_encrypt_file(modified_text))
            end_enc = time.perf_counter()
            total_enc_time = total_enc_time + (end_enc - start_enc)

        sum_enc_time = sum_enc_time + total_enc_time/test_num

        cipher_delta_len = cipher_delta_len + len(final_bytes)
        start_write = time.perf_counter()
        with open(repo_cipher / one_file, 'wb') as f:
            f.write(final_bytes)
        end_write = time.perf_counter()
        rw_time = rw_time + end_write - start_write + end_read - start_read
    end = time.perf_counter()
    remove_empty_dirs(cipher_path, repo_path)
    repo_cipher = Repo(cipher_path)
    repo_cipher.git.add('--all')
    repo_cipher.index.commit(msg)
    if flag:
        commit_cipher = repo_cipher.commit('HEAD')
        signature = generate_Signature(commit_cipher, sign_key)
        # print(signature)
        repo_cipher.git.commit('--amend', '--allow-empty', '-m', f"{signature}")
    return end - start - rw_time - add_rw_time, sum_enc_time, cipher_delta_len


def Dec_line(diff, repo_cipher_path_line, repo_plain_path_pre, repo_plain_path_current, repo_recover_path_line):
    cipher_path = Path(repo_cipher_path_line)
    plain_path_pre = Path(repo_plain_path_pre)
    plain_path_current = Path(repo_plain_path_current)
    recover_path = Path(repo_recover_path_line)

    dec_time = 0
    for one_file in diff['added_files']:
        os.makedirs(os.path.dirname(recover_path / one_file), exist_ok=True)
        ts, plain = decrypt_one_file_line_rw(cipher_path / one_file, recover_path / one_file)
        dec_time = dec_time + ts
        if not is_binary_file_equal(plain_path_current / one_file, plain):
            print("line Inconsistency!")
            print(one_file)

    for old_name, new_name in diff['renamed_files']:
        move_and_rename_file(plain_path_pre / old_name, plain_path_pre / new_name)

    for one_file in diff['modified_files']:
        os.makedirs(os.path.dirname(recover_path / one_file), exist_ok=True)
        ts, plain = decrypt_one_file_line_rw(cipher_path / one_file, recover_path / one_file)
        dec_time = dec_time + ts
        if not is_binary_file_equal(plain_path_current / one_file, plain):
            print("line Inconsistency!")
            print(one_file)
    return dec_time

def Dec_patch(diff, repo_cipher_path_patch, repo_plain_path_pre, repo_plain_path_current, repo_recover_path_patch):
    cipher_path = Path(repo_cipher_path_patch)
    plain_path_pre = Path(repo_plain_path_pre)
    plain_path_current = Path(repo_plain_path_current)
    recover_path = Path(repo_recover_path_patch)

    dec_time = 0
    for one_file in diff['added_files']:
        os.makedirs(os.path.dirname(recover_path / one_file), exist_ok=True)
        ts, plain = decrypt_one_file_line_rw(cipher_path / one_file, recover_path / one_file)
        dec_time = dec_time + ts
        if not is_binary_file_equal(plain_path_current / one_file, plain):
            print("Inconsistency!")
            print(one_file)

    for old_name, new_name in diff['renamed_files']:
        move_and_rename_file(plain_path_pre / old_name, plain_path_pre / new_name)

    for one_file in diff['modified_files']:
        os.makedirs(os.path.dirname(recover_path / one_file), exist_ok=True)
        ts, plain = decrypt_one_file_patch_rw(plain_path_pre / one_file, cipher_path / one_file, recover_path / one_file)
        dec_time = dec_time + ts
        if not is_binary_file_equal(plain_path_current / one_file, plain):
            print("Inconsistency!")
            print(one_file)
    return dec_time



def Dec_DE(diff, repo_cipher_path_DE, repo_plain_path_pre, repo_plain_path_current, repo_recover_path_DE):
    cipher_path = Path(repo_cipher_path_DE)
    plain_path_pre = Path(repo_plain_path_pre)
    plain_path_current = Path(repo_plain_path_current)
    recover_path = Path(repo_recover_path_DE)

    dec_time = 0
    for one_file in diff['added_files']:
        os.makedirs(os.path.dirname(recover_path / one_file), exist_ok=True)
        ts, plain = decrypt_one_file_DE_rw(cipher_path / one_file, recover_path / one_file)
        dec_time = dec_time + ts
        if not is_binary_file_equal(plain_path_current / one_file, plain):
            print("Inconsistency!")
            print(one_file)

    for old_name, new_name in diff['renamed_files']:
        move_and_rename_file(plain_path_pre / old_name, plain_path_pre / new_name)

    for one_file in diff['modified_files']:
        os.makedirs(os.path.dirname(recover_path / one_file), exist_ok=True)
        ts, plain = decrypt_one_file_DE_rw(cipher_path / one_file, recover_path / one_file)
        dec_time = dec_time + ts
        if not is_binary_file_equal(plain_path_current / one_file, plain):
            print("Inconsistency!")
            print(one_file)
    return dec_time

def Dec_Trivial(cipher_path, plain_path):
    # 枚举处理每个文件
    dec_time = 0
    for dir_path, dir_names, file_names in os.walk(cipher_path):
        if check_is_ignore(dir_path):
            continue
        for file_name in file_names:
            one_file_path = os.path.join(dir_path, file_name)
            target_file_path = to_encryptor_dir_path(cipher_path, plain_path, one_file_path)

            ts = decrypt_one_whole_file(one_file_path, target_file_path)
            dec_time = dec_time + ts
    return dec_time


def Dec_line_eff(repo_cipher_path_line, repo_plain_path_pre, repo_plain_path_current, repo_recover_path_line):
    repo_cipher = Repo(repo_cipher_path_line)
    cipher_path = Path(repo_cipher_path_line)
    plain_path_pre = Path(repo_plain_path_pre)
    plain_path_current = Path(repo_plain_path_current)
    recover_path = Path(repo_recover_path_line)

    start_diff = time.perf_counter()
    diff = Get_git_diff(repo_cipher, 'HEAD')
    end_diff = time.perf_counter()

    dec_time = 0
    for one_file in diff['added_files']:
        os.makedirs(os.path.dirname(recover_path / one_file), exist_ok=True)
        ts, plain = decrypt_one_file_line_rw(cipher_path / one_file, recover_path / one_file)
        dec_time = dec_time + ts
        if not is_binary_file_equal(plain_path_current / one_file, plain):
            print("Inconsistency!")
            print(one_file)

    for old_name, new_name in diff['renamed_files']:
        move_and_rename_file(plain_path_pre / old_name, plain_path_pre / new_name)

    for one_file, one_del, one_add, one_add_lines in zip(diff['modified_files'], diff['deleted_lines']
                , diff['inserted_lines'], diff['inserted_content']):
        os.makedirs(os.path.dirname(recover_path / one_file), exist_ok=True)

        if one_add == [] and one_del == [] and one_add_lines == []:
            ts, plain = decrypt_one_file_line_rw(cipher_path / one_file, recover_path / one_file)
            dec_time = dec_time + ts
            if not is_binary_file_equal(plain_path_current / one_file, plain):
                print("Inconsistency!")
                print(one_file)
            continue


        with open(plain_path_pre / one_file, 'rb') as f1:
            lines = f1.readlines()
            #print(lines)
            #pre_bytes = b''.join(lines)
        #print(pre_bytes)
        ts, plain = update_file_plain_line(lines, one_del, one_add, one_add_lines, recover_path / one_file)
        dec_time = dec_time + ts
        if not is_binary_file_equal(plain_path_current / one_file, plain):
            print("Inconsistency!")
            print(one_file)
    return dec_time + end_diff - start_diff


def git_push_with_details(repo_path, refspec):
    #command = f"git -C {repo_path} push --porcelain --force --progress origin {refspec}"
    command = ["git", "-C", repo_path, "push", "--porcelain", "--force", "--progress", "origin", refspec]
    start = time.perf_counter()
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    end = time.perf_counter()
    # 处理输出
    output_lines = result.stdout.splitlines() + result.stderr.splitlines()

    return output_lines, end - start


def get_pack_size(ol):
    pattern = re.compile(r"Writing objects: 100%.*?, (\d+(\.\d+)?) (bytes|KiB|MiB|GiB) \|")

    unit_map = {"bytes": 1 / 1024, "KiB": 1, "MiB": 1024, "GiB": 1024 * 1024}

    for line in ol:
        match = pattern.search(line)
        if match:
            #print(match)
            size = match.group(1)
            #print(size)
            unit = match.group(3)  # (bytes, KiB, MiB, GiB)
            #print(unit)
            size_kb = float(size) * unit_map.get(unit, 1)  # KB
            #print(type(size_kb))
            return float(size_kb)

    return None


def get_folder_size(folder_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            if os.path.exists(file_path):  # 确保文件存在
                total_size += os.path.getsize(file_path)
    size_in_mb = total_size / (1024 * 1024)
    return size_in_mb

    # result = subprocess.run(['du', '-sb', folder_path], stdout=subprocess.PIPE, text=True)
    # size_in_bytes = int(result.stdout.split()[0])
    # return size_in_bytes / (1024 * 1024)  # KB

def git_gc(repo_path):
    try:
        # run git gc --aggressive --prune=now
        result = subprocess.run(
            ['git', 'gc', '--aggressive', '--prune=now'],
            cwd=repo_path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        print("Git garbage collection (aggressive) successful!")
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        print("Error during git gc:")
        print(e.stderr.decode())