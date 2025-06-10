from src.lib.config import *
from src.lib.repo_operation import *
from src.lib.file_operation import *
from pathlib import Path
import logging

base_dir = Path(__file__).parent

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    filename=base_dir.parent.parent / 'log'/ 'test_init_log.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.getLogger('git').setLevel(logging.CRITICAL)

def test_comp(REPO):

    repository_path = base_dir.parent.parent / 'dataset' / REPO

    # print(repository_path)

    cipher_path = base_dir.parent.parent / 'output' / 'test-init' / REPO

    repo_cipher_path_line = cipher_path / 'linecipher'
    repo_cipher_path_patch = cipher_path / 'patchcipher'
    repo_cipher_path_file = cipher_path / 'filecipher'
    repo_cipher_path_trivial = cipher_path / 'trivialcipher'


    delete_all_files_in_directory(repo_cipher_path_line)
    delete_all_files_in_directory(repo_cipher_path_patch)
    delete_all_files_in_directory(repo_cipher_path_file)
    delete_all_files_in_directory(repo_cipher_path_trivial)

    Repo.init(repo_cipher_path_line)
    Repo.init(repo_cipher_path_patch)
    Repo.init(repo_cipher_path_file)
    Repo.init(repo_cipher_path_trivial)

    repo = Repo(repository_path)

    repo.git.checkout(First_commit[REPO])

    commit_init = repo.commit(First_commit[REPO])

    msg = commit_init.message.strip()

    Init_line_time = Init_for_line(repository_path, repo_cipher_path_line, msg, NOSIGN)
    Init_DE_time = Init_for_DE(repository_path, repo_cipher_path_file, msg, NOSIGN)
    Init_tri_time = Init_for_Trivial(repository_path, repo_cipher_path_trivial, msg, NOSIGN)
    Init_patch_time = Init_for_patch(repository_path, repo_cipher_path_patch, msg, NOSIGN)

    repo.git.checkout(Latest_commit[REPO])

    return [Init_line_time, Init_DE_time, Init_tri_time, Init_patch_time]

    # print(Init_line_time, Init_DE_time, Init_tri_time, Init_patch_time)

def test_comm(REPO):
    url = remoteurl_init(REPO)


    repository_path = base_dir.parent.parent / 'dataset' / REPO

    # print(repository_path)

    cipher_path = base_dir.parent.parent / 'output' / 'test-init' / REPO

    repo_cipher_path_line = cipher_path / 'linecipher'
    repo_cipher_path_patch = cipher_path / 'patchcipher'
    repo_cipher_path_file = cipher_path / 'filecipher'
    repo_cipher_path_trivial = cipher_path / 'trivialcipher'

    repo_plain_path = cipher_path / 'plain'

    delete_all_files_in_directory(repo_plain_path)
    delete_all_files_in_directory(repo_cipher_path_line)
    delete_all_files_in_directory(repo_cipher_path_patch)
    delete_all_files_in_directory(repo_cipher_path_file)
    delete_all_files_in_directory(repo_cipher_path_trivial)

    Repo.init(repo_plain_path)
    Repo.init(repo_cipher_path_line)
    Repo.init(repo_cipher_path_patch)
    Repo.init(repo_cipher_path_file)
    Repo.init(repo_cipher_path_trivial)

    repo = Repo(repository_path)
    repo.git.checkout(First_commit[REPO])
    repo_line = Repo(repo_cipher_path_line)
    repo_patch = Repo(repo_cipher_path_patch)
    repo_file = Repo(repo_cipher_path_file)
    repo_trivial = Repo(repo_cipher_path_trivial)


    set_Git_Config(repo_line)
    set_Git_Config(repo_patch)
    set_Git_Config(repo_file)
    set_Git_Config(repo_trivial)

    commit_init = repo.commit(First_commit[REPO])

    msg = commit_init.message.strip()

    Init_line_time = Init_for_line(repository_path, repo_cipher_path_line, msg, NOSIGN)
    Init_DE_time = Init_for_DE(repository_path, repo_cipher_path_file, msg, NOSIGN)
    Init_tri_time = Init_for_Trivial(repository_path, repo_cipher_path_trivial, msg, NOSIGN)
    Init_patch_time = Init_for_patch(repository_path, repo_cipher_path_patch, msg, NOSIGN)

    # Plain
    repo.git.checkout(First_commit[REPO])
    Repo.init(repo_plain_path)
    repo_plain = Repo(repo_plain_path)
    set_Git_Config(repo_plain)
    copy_repo_and_files(repository_path, repo_plain_path)
    repo_plain.git.add('--all')
    repo_plain.index.commit(msg)
    repo_plain.git.branch('-M', 'plaininit')
    repo_plain.create_remote('origin', url)
    output_plain, t1 = git_push_with_details(repo_plain_path, 'plaininit')
    comm_cost_plain = get_pack_size(output_plain)
    repo.git.checkout(Latest_commit[REPO])
    # print(output_plain)
    #print('Git init comm costs (KB):', comm_cost_plain)

    # trivial
    repo_trivial.git.branch('-M', 'trivialinit')
    repo_trivial.create_remote('origin', url)
    output_trivial, t2 = git_push_with_details(repo_cipher_path_trivial, 'trivialinit')
    #print(output_trivial)
    comm_cost_trivial = get_pack_size(output_trivial)
    #print('Trivial init comm costs (KB):', comm_cost_trivial)
    print(output_trivial)

    # patch
    repo_patch.git.branch('-M', 'patchinit')
    repo_patch.create_remote('origin', url)
    output_patch, t3 = git_push_with_details(repo_cipher_path_patch, 'patchinit')
    comm_cost_patch = get_pack_size(output_patch)
    #print('patch init comm costs (KB):', comm_cost_patch)
    print(output_patch)

    # line
    repo_line.git.branch('-M', 'lineinit')
    repo_line.create_remote('origin', url)
    output_line, t4 = git_push_with_details(repo_cipher_path_line, 'lineinit')
    comm_cost_line = get_pack_size(output_line)
    #print('line init comm costs (KB):', comm_cost_line)
    print(output_line)

    # file
    repo_file.git.branch('-M', 'fileinit')
    repo_file.create_remote('origin', url)
    output_file, t5 = git_push_with_details(repo_cipher_path_file, 'fileinit')
    comm_cost_file = get_pack_size(output_file)
    #print('file init comm costs (KB):', comm_cost_file)
    # print(output_file)

    return [comm_cost_plain, comm_cost_trivial, comm_cost_patch, comm_cost_line, comm_cost_file]



if __name__ == '__main__':
    result = [0] * 4

    '''
        set the parameter REPO to `awesome/FPB/bootstrap/react/FCC`, respectively
    '''
    REPO = awesome

    test_num = 10  # set the number of tests

    for _ in range(test_num):
        result = [sum(x) for x in zip(result, test_comp(REPO))]

    result = [round(x / test_num, 4) for x in result]

    logging.info('The computation costs of Initialization shown in Table 4 (s):')
    logging.info('Repo: %s', REPO)
    logging.info('SGitChar: %s', result[3])
    logging.info('SGitLine: %s', result[0])
    logging.info('Git-crypt: %s', result[1])
    logging.info('Trivial-enc-sign: %s', result[2])


    result_comm = test_comm(REPO)

    result_comm = [round(x, 4) for x in result_comm]

    logging.info('The communication costs of Initialization shown in Table 2 (KB):')
    logging.info('Repo: %s', REPO)
    logging.info('Git: %s', result_comm[0])
    logging.info('SGitChar: %s', result_comm[2])
    logging.info('SGitLine: %s', result_comm[3])
    logging.info('Git-crypt: %s', result_comm[4])
    logging.info('Trivial-enc-sign: %s', result_comm[1])





