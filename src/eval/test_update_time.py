from src.lib.config import *
from src.lib.repo_operation import *
import logging
import argparse

base_dir = Path(__file__).parent

logging.basicConfig(
    filename=base_dir.parent.parent / 'evaluationlog' / 'test_update_time_log.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.getLogger('git').setLevel(logging.CRITICAL)


def test(REPO, commit_sha, i, test_num):
    repository_path = base_dir.parent.parent / 'dataset' / REPO

    # print(repository_path)

    cipher_path = base_dir.parent.parent / 'output' / 'test-update-comp' / REPO

    repo_cipher_path_line = cipher_path / 'linecipher' / str(i)
    repo_cipher_path_patch = cipher_path / 'patchcipher' / str(i)
    repo_cipher_path_file = cipher_path / 'filecipher' / str(i)
    repo_cipher_path_trivial = cipher_path / 'trivialcipher' / str(i)
    repo_plain_path_pre = cipher_path / 'plain_pre' / str(i)
    repo_plain_path_current = cipher_path / 'plain_current' / str(i)

    delete_all_files_in_directory(repo_cipher_path_line)
    delete_all_files_in_directory(repo_cipher_path_patch)
    delete_all_files_in_directory(repo_cipher_path_file)
    delete_all_files_in_directory(repo_plain_path_pre)
    delete_all_files_in_directory(repo_plain_path_current)
    delete_all_files_in_directory(repo_cipher_path_trivial)

    Repo.init(repo_cipher_path_line)
    Repo.init(repo_cipher_path_patch)
    Repo.init(repo_cipher_path_file)
    # Repo.init(repo_cipher_path_trivial)

    repo = Repo(repository_path)

    msg_upd = 'update'

    result = Get_git_diff(repo, commit_sha)
    # print(commit_sha)
    # print(result)

    # print(result)

    # make the parent version of commit_sha is shown in repository_path.

    repo.git.checkout(commit_sha + '~1')

    commit_init = repo.commit(commit_sha + '~1')

    msg_init = commit_init.message.strip()

    # Initialize the previous version

    # Plain
    Init_for_plain(result, repository_path, repo_plain_path_pre)

    # SGitLine
    Init_for_line_comp(result, repository_path, repo_cipher_path_line)

    # SGitChar
    Init_for_patch_comp(result, repository_path, repo_cipher_path_patch)

    # DE
    Init_for_DE_comp(result, repository_path, repo_cipher_path_file)

    # update

    repo.git.checkout(commit_sha)

    commit_upd = repo.commit(commit_sha)

    msg_upd = commit_upd.message.strip()

    # Plain
    Update_plain(result, repository_path, repo_plain_path_current)

    # Trivial

    delete_all_except_git(repo_cipher_path_trivial)

    trivial_upd_time = copy_repo_and_enc_files(repository_path, repo_cipher_path_trivial, test_num)

    # SGitChar
    patch_run_time, comp_patch, patch_enc, patch_delta_cipher = update_patch_diff(repository_path,
                                                                                  repo_cipher_path_patch, commit_sha,
                                                                                  msg_upd, NOSIGN, test_num)

    # print('update patch time:', patch_run_time)

    # SGitLine
    line_run_time, comp_diff, diff_enc, line_delta_cipher = update_line_diff(repository_path, repo_cipher_path_line,
                                                                             commit_sha, msg_upd, NOSIGN, test_num)

    print('compare line time:', comp_diff)

    # DE
    file_run_time, file_enc_time, file_delta_cipher = update_file_diff(repository_path, repo_cipher_path_file,
                                                                       commit_sha, msg_upd, NOSIGN, test_num)

    # print('update file time:', file_run_time)

    # result = Get_git_diff(repo, commit_sha)
    # #print(result)
    # result= Get_git_diff(repo_cipher, 'HEAD')
    # #print(result["inserted_content"])

    repo.git.checkout(Latest_commit[REPO])

    result = [line_run_time, comp_diff, diff_enc, line_delta_cipher,
              patch_run_time, comp_patch, patch_enc, patch_delta_cipher,
              file_run_time, file_enc_time, file_delta_cipher, trivial_upd_time]

    # print(result)

    repo.git.checkout(Latest_commit[REPO])

    return result


def main(REPO, commit_SHA, test_num):
    result = [0] * 12

    for i in range(len(commit_SHA)):
        result = [sum(x) for x in zip(result, test(REPO, commit_SHA[i], i, test_num))]

    result = [round(x / len(commit_SHA), 7) for x in result]

    return result


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Evaluate update computation cost for a given repo.')
    parser.add_argument('--repo', required=True,
                        help='Repository name to test, e.g., awesome, FPB, bootstrap, react, FCC')
    #parser.add_argument('--test-num', type=int, default=1, help='Number of times to repeat the test (default: 1)')
    args = parser.parse_args()

    repo_map = {
        'awesome': awesome,
        'FPB': FPB,
        'bootstrap': bootstrap,
        'react': react,
        'FCC': FCC,
    }

    if args.repo not in repo_map:
        raise ValueError(f"Unknown repo '{args.repo}'. Must be one of: {', '.join(repo_map)}")

    # result = [0] * 12

    test_num = 10

    # '''
    #     set the parameter REPO to `awesome/FPB/bootstrap/react/FCC`, respectively, to evaluate the performace on
    #     each repositories.
    # '''
    # REPO = awesome  # choose one repo
    REPO = repo_map[args.repo]
    commit_SHA = repo_commit_map[REPO]

    result = main(REPO, commit_SHA, test_num)

    result = [round(x, 5) for x in result]

    # result = [line_run_time, comp_diff, diff_enc, line_delta_cipher,
    #           patch_run_time, comp_patch, patch_enc, patch_delta_cipher,
    #           file_run_time, file_enc_time, file_delta_cipher]

    logging.info('The computation costs of update shown in Table 3 (s):')

    logging.info('Repo: %s', REPO)

    logging.info('SGitChar:')
    logging.info('Compare: %s', result[5])
    logging.info('Encrypt: %s', result[6])
    logging.info('Total: %.4f', result[5] + result[6])
    # print('\n')

    logging.info('SGitLine:')
    logging.info('Compare: %s', result[1])
    logging.info('Enc + update: %s', result[2])
    logging.info('Total: %s', result[1] + result[2])
    # print('\n')

    logging.info('Git-crypt: %s', result[9])
    # print('\n')

    logging.info('Trivial-enc-sign: %s', result[11])