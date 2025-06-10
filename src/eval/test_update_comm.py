from src.lib.config import *
from src.lib.repo_operation import *
from src.lib.file_operation import *
import logging

base_dir = Path(__file__).parent

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)


logging.basicConfig(
    filename=base_dir.parent.parent / 'log' / 'test_update_comm_log.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.getLogger('git').setLevel(logging.CRITICAL)

def test(REPO, commit_sha, i):
    url = remoteurl(REPO)
    base_dir = Path(__file__).parent

    repository_path = base_dir.parent.parent / 'dataset' / REPO

    # print(repository_path)

    cipher_path = base_dir.parent.parent / 'output' / 'test-update-comm' / REPO

    repo_cipher_path_line = cipher_path / 'linecipher' / str(i)
    repo_cipher_path_patch = cipher_path / 'patchcipher' / str(i)
    repo_cipher_path_file = cipher_path / 'filecipher' / str(i)
    repo_cipher_path_trivial = cipher_path / 'trivialcipher' / str(i)
    repo_plain_path = cipher_path / 'plain' / str(i)

    delete_all_files_in_directory(repo_cipher_path_line)
    delete_all_files_in_directory(repo_cipher_path_patch)
    delete_all_files_in_directory(repo_cipher_path_file)
    delete_all_files_in_directory(repo_plain_path)
    delete_all_files_in_directory(repo_cipher_path_trivial)

    Repo.init(repo_cipher_path_line)
    Repo.init(repo_cipher_path_patch)
    Repo.init(repo_cipher_path_file)
    Repo.init(repo_cipher_path_trivial)
    Repo.init(repo_plain_path)

    repo = Repo(repository_path)
    repo_line = Repo(repo_cipher_path_line)
    repo_patch = Repo(repo_cipher_path_patch)
    repo_file = Repo(repo_cipher_path_file)
    repo_plain = Repo(repo_plain_path)
    repo_trivial = Repo(repo_cipher_path_trivial)

    set_Git_Config(repo_line)
    set_Git_Config(repo_patch)
    set_Git_Config(repo_file)
    set_Git_Config(repo_plain)
    set_Git_Config(repo_trivial)


    sum_plain, sum_line, sum_patch, sum_DE, sum_trivial = 0, 0, 0, 0, 0

    # make the parent version of commit_sha is shown in repository_path.

    result = Get_git_diff(repo, commit_sha)
    print(commit_sha)
    print(result)

    repo.git.checkout(commit_sha + '~1')

    commit_init = repo.commit(commit_sha + '~1')

    msg_init = commit_init.message.strip()

    # Initialize the previous version

    # Plain
    Init_for_plain(result, repository_path, repo_plain_path)
    repo_plain.git.add('--all')
    repo_plain.index.commit(msg_init)
    repo_plain.git.branch('-M', 'plain')
    repo_plain.create_remote('origin', url)
    git_push_with_details(repo_plain_path, 'plain')

    # SGitLine
    Init_for_line_comp(result, repository_path, repo_cipher_path_line)
    repo_line.git.add('--all')
    repo_line.index.commit(msg_init)
    commit_line = repo_line.commit('HEAD')
    signature = generate_Signature(commit_line, sign_key)
    repo_line.git.commit('--amend', '-m', signature)
    repo_line.git.branch('-M', 'line')
    repo_line.create_remote('origin', url)
    git_push_with_details(repo_cipher_path_line, 'line')

    # SGitChar
    Init_for_patch_comp(result, repository_path, repo_cipher_path_patch)
    repo_patch.git.add('--all')
    repo_patch.index.commit(msg_init)
    commit_patch = repo_patch.commit('HEAD')
    signature = generate_Signature(commit_patch, sign_key)
    repo_patch.git.commit('--amend', '-m', signature)
    repo_patch.git.branch('-M', 'patch')
    repo_patch.create_remote('origin', url)
    git_push_with_details(repo_cipher_path_patch, 'patch')

    # DE
    Init_for_DE_comp(result, repository_path, repo_cipher_path_file)
    repo_file.git.add('--all')
    repo_file.index.commit(msg_init)
    # commit_file = repo_file.commit('HEAD')
    # signature = generate_Signature(commit_file, sign_key)
    # repo_file.git.commit('--amend', '-m', signature)
    repo_file.git.branch('-M', 'file')
    repo_file.create_remote('origin', url)
    git_push_with_details(repo_cipher_path_file, 'file')


    # update
    repo.git.checkout(commit_sha)

    commit_upd = repo.commit(commit_sha)

    msg_upd = commit_upd.message.strip()



    Update_plain_comm(result, repository_path, repo_plain_path)
    repo_plain.git.add('--all')
    repo_plain.index.commit(msg_upd)
    output_plain, push_time_plain = git_push_with_details(repo_plain_path, 'plain')
    comm_cost_plain = get_pack_size(output_plain)
    sum_plain = sum_plain + comm_cost_plain

    # print("init finished")

    comm_cost_trivial = 0

    # Trivial
    trivial_upd_time = Init_for_Trivial(repository_path, repo_cipher_path_trivial, msg_upd, NOSIGN)
    repo_trivial.git.branch('-M', 'trivial')
    repo_trivial.create_remote('origin', url)
    output_trivial, push_time_trivial = git_push_with_details(repo_cipher_path_trivial, 'trivial')
    print(output_trivial)
    comm_cost_trivial = get_pack_size(output_trivial)
    print(comm_cost_trivial)
    sum_trivial = sum_trivial + comm_cost_trivial


    # patch diff
    patch_run_time, comp_patch, patch_enc, patch_delta_cipher = update_patch_diff(repository_path, repo_cipher_path_patch, commit_sha, msg_upd, NOSIGN)
    output_patch, push_time_patch = git_push_with_details(repo_cipher_path_patch, 'patch')
    comm_cost_patch = get_pack_size(output_patch)
    print(comm_cost_patch)
    sum_patch = sum_patch + comm_cost_patch


    #line diff
    line_run_time, comp_diff, diff_enc, line_delta_cipher = update_line_diff(repository_path, repo_cipher_path_line, commit_sha, msg_upd, NOSIGN)
    output_line, push_time_line = git_push_with_details(repo_cipher_path_line, 'line')
    comm_cost_line = get_pack_size(output_line)
    print(comm_cost_line)
    sum_line = sum_line + comm_cost_line


    #file diff
    file_run_time, file_enc_time, file_delta_cipher = update_file_diff(repository_path, repo_cipher_path_file, commit_sha, msg_upd, NOSIGN)
    output_file, push_time_file = git_push_with_details(repo_cipher_path_file, 'file')
    comm_cost_DE = get_pack_size(output_file)
    print(comm_cost_DE)
    sum_DE = sum_DE + comm_cost_DE

    # logging.info('Costs of Git, SGitLine, SGitChar, Git-crypt, Trivial-enc-sign:')

    # logging.info('comm. cost: %s, %s, %s, %s, %s', comm_cost_plain, comm_cost_line, comm_cost_patch, comm_cost_DE, comm_cost_trivial)


    # result = Get_git_diff(repo, commit_sha)
    # #print(result)
    # result= Get_git_diff(repo_cipher, 'HEAD')
    # #print(result['inserted_content'])

    repo.git.checkout(Latest_commit[REPO])

    # result = [sum_plain, sum_line, sum_patch, sum_DE, sum_trivial]

    result = [comm_cost_plain, comm_cost_line, comm_cost_patch, comm_cost_DE, comm_cost_trivial]

    #print(result)

    return result

def main(REPO, commit_SHA):
    result = [0] * 5

    for i in range(len(commit_SHA)):
        result = [sum(x) for x in zip(result, test(REPO, commit_SHA[i], i))]

    result = [round(x / len(commit_SHA), 7) for x in result]

    # result = [sum(x) for x in zip(result, test(REPO, commit_SHA[0], 0))]



    return result


if __name__ == '__main__':

    result = [0] * 5

    test_num = 1

    REPO = awesome  # choose one repo
    commit_SHA = repo_commit_map[REPO]

    for _ in range(test_num):
        result = [sum(x) for x in zip(result, main(REPO, commit_SHA))]


    result = [round(x / test_num, 4) for x in result]

    logging.info('The communication costs of update shown in Table 2 (KB):')

    logging.info('Repo: %s', REPO)

    logging.info('Git: %s', result[0])

    logging.info('SGitChar: %s', result[2])

    logging.info('SGitLine: %s', result[1])

    logging.info('Git-crypt: %s', result[3])

    logging.info('Trivial-enc-sign (MB): %s', round(result[4] / 1024, 4))
