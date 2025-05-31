from src.lib.config import *
from src.lib.repo_operation import *
from src.lib.file_operation import *
import logging

base_dir = Path(__file__).parent

logging.basicConfig(
    filename=base_dir.parent.parent / 'log'/ 'basic_test_log.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test(REPO):

    repository_path = base_dir.parent.parent / 'dataset' / REPO

    cipher_path = base_dir.parent.parent / 'output' / 'basic_test' / REPO

    url = basicurl()

    repo_cipher_path_line = cipher_path / 'linecipher'
    repo_cipher_path_patch = cipher_path / 'patchcipher'
    repo_cipher_path_file = cipher_path / 'filecipher'
    repo_cipher_path_trivial = cipher_path / 'trivial'
    repo_plain_path_pre = cipher_path / 'plain_pre'
    repo_plain_path_current = cipher_path / 'plain_current'

    repo_recover_path_line = cipher_path / 'recover' / 'line'
    repo_recover_path_patch = cipher_path / 'recover' / 'patch'
    repo_recover_path_file = cipher_path / 'recover' / 'file'
    repo_recover_path_trivial = cipher_path / 'recover' / 'trivial'


    delete_all_files_in_directory(repo_cipher_path_line)
    delete_all_files_in_directory(repo_cipher_path_patch)
    delete_all_files_in_directory(repo_cipher_path_file)
    delete_all_files_in_directory(repo_cipher_path_trivial)
    delete_all_files_in_directory(repo_plain_path_pre)
    delete_all_files_in_directory(repo_plain_path_current)


    Repo.init(repo_cipher_path_line)
    Repo.init(repo_cipher_path_patch)
    Repo.init(repo_cipher_path_file)
    Repo.init(repo_plain_path_pre)
    Repo.init(repo_cipher_path_trivial)

    repo = Repo(repository_path)
    repo_line = Repo(repo_cipher_path_line)
    repo_patch = Repo(repo_cipher_path_patch)
    repo_file = Repo(repo_cipher_path_file)
    repo_trivial = Repo(repo_cipher_path_trivial)

    all_commits = []


    for commit in repo.iter_commits():
        all_commits.append(commit.hexsha)
    if len(all_commits) < 2:
        raise Exception('error! not enough commits')

    commit_number = len(all_commits)

    repo.git.checkout(all_commits[commit_number - 1])  # checkout first version
    # print(all_commits[commit_number - 1])

    sum_line_time, sum_patch_time, sum_DE_time, sum_Trivial_time = 0, 0, 0, 0

    sum_push_time_line, sum_push_time_patch, sum_push_time_file, sum_push_time_trivial, sum_push_plain = 0, 0, 0, 0, 0

    commit_msg = 'init'

    # Line Init
    init_line_time = Init_for_line(repository_path, repo_cipher_path_line, commit_msg, GENSIGN)
    repo_line.git.branch('-M', 'line')
    repo_line.create_remote('origin', url)
    output_line, push_time_line = git_push_with_details(repo_cipher_path_line, 'line')
    comm_cost_line = get_pack_size(output_line)


    init_patch_time = Init_for_patch(repository_path, repo_cipher_path_patch, commit_msg, GENSIGN)
    repo_patch.git.branch('-M', 'patch')
    repo_patch.create_remote('origin', url)
    output_patch, push_time_patch = git_push_with_details(repo_cipher_path_patch, 'patch')
    comm_cost_patch = get_pack_size(output_patch)

    init_DE_time = Init_for_DE(repository_path, repo_cipher_path_file, commit_msg, NOSIGN)
    repo_file.git.branch('-M', 'file')
    repo_file.create_remote('origin', url)
    output_file, push_time_file = git_push_with_details(repo_cipher_path_file, 'file')
    comm_cost_file = get_pack_size(output_file)

    init_Trivial_time = Init_for_Trivial(repository_path, repo_cipher_path_trivial, commit_msg, GENSIGN)
    repo_trivial.git.branch('-M', 'trivial')
    repo_trivial.create_remote('origin', url)
    output_trivial, push_time_trivial = git_push_with_details(repo_cipher_path_trivial, 'trivial')
    comm_cost_trivial = get_pack_size(output_trivial)

    # plain init
    copy_repo_and_files(repository_path, repo_plain_path_pre)


    '''
        test for push
    '''

    i = 2

    commit_sha = all_commits[commit_number - i]
    # print(f'{i}-th update')
    # print(commit_sha)
    repo.git.checkout(commit_sha)

    commit_msg = f'{i}-th update'

    # line update
    line_comp_time, line_diff_time, line_update_time, line_ciphersize = update_line_diff(repository_path,
                                                                                         repo_cipher_path_line,
                                                                                         commit_sha, commit_msg, GENSIGN)
    # repo_line.git.gc()
    output_line, push_time_line = git_push_with_details(repo_cipher_path_line, 'line')
    comm_cost_line = get_pack_size(output_line)

    # patch update
    patch_comp_time, patch_diff_time, patch_enc_time, patch_ciphersize = update_patch_diff(repository_path,
                                                                                           repo_cipher_path_patch,
                                                                                           commit_sha, commit_msg, GENSIGN)
    # repo_patch.git.gc()
    output_patch, push_time_patch = git_push_with_details(repo_cipher_path_patch, 'patch')
    comm_cost_patch = get_pack_size(output_patch)

    # update DE
    DE_comp_time, DE_enc_time, DE_ciphersize = update_file_diff(repository_path, repo_cipher_path_file, commit_sha,
                                                                commit_msg, GENSIGN)
    # repo_file.git.gc()
    output_file, push_time_file = git_push_with_details(repo_cipher_path_file, 'file')
    comm_cost_file = get_pack_size(output_file)

    # update trivial
    delete_all_except_git(repo_cipher_path_trivial)
    Trival_comp_time = Init_for_Trivial(repository_path, repo_cipher_path_trivial, commit_msg, GENSIGN)
    # repo_trivial.git.gc()
    output_trivial, push_time_trivial = git_push_with_details(repo_cipher_path_trivial, 'trivial')
    comm_cost_trivial = get_pack_size(output_trivial)

    # update plain
    copy_repo_and_files(repository_path, repo_plain_path_current)


    logging.info('Repo: %s', REPO)

    logging.info('Communication cots of an update (KB):')

    logging.info('SGitChar: %s', comm_cost_patch)

    logging.info('SGitLine: %s', comm_cost_line)

    logging.info('Git-crypt: %s', comm_cost_file)

    logging.info('Trivial-enc-sign (MB): %s', comm_cost_trivial)


    repo.git.checkout(all_commits[0])

    '''
        test for recovery
    '''

    result = Get_git_diff(repo, commit_sha)

    Dec_line_time = Dec_line(result, repo_cipher_path_line, repo_plain_path_pre, repo_plain_path_current,
                             repo_recover_path_line)

    Dec_patch_time = Dec_patch(result, repo_cipher_path_patch, repo_plain_path_pre, repo_plain_path_current,
                               repo_recover_path_patch)

    Dec_DE_time = Dec_DE(result, repo_cipher_path_file, repo_plain_path_pre, repo_plain_path_current,
                         repo_recover_path_file)

    Dec_trivial_time = Dec_Trivial(repo_cipher_path_trivial, repo_recover_path_trivial)

    logging.info('Repo: %s', REPO)

    logging.info('Computation cots of recovering one version (KB):')

    logging.info('SGitChar: %s', Dec_patch_time)

    logging.info('SGitLine: %s', Dec_line_time)

    logging.info('Git-crypt: %s', Dec_DE_time)

    logging.info('Trivial-enc-sign: %s', Dec_trivial_time)




if __name__ == '__main__':
    REPO = awesome
    test(REPO)

