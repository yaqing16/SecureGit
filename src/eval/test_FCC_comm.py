from src.lib.config import *
from src.lib.repo_operation import *
from src.lib.file_operation import *
import logging
import argparse

base_dir = Path(__file__).parent

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)


logging.basicConfig(
    filename=base_dir.parent.parent / 'evaluationlog' / 'test_FCC_comm_log.log',
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

    repo_cipher_path_trivial = cipher_path / 'trivialcipher' / str(i)

    delete_all_files_in_directory(repo_cipher_path_trivial)


    Repo.init(repo_cipher_path_trivial)

    repo = Repo(repository_path)


    repo_trivial = Repo(repo_cipher_path_trivial)

    set_Git_Config(repo_trivial)

    msg_upd = 'update'

    sum_plain, sum_line, sum_patch, sum_DE, sum_trivial = 0, 0, 0, 0, 0

    # make the parent version of commit_sha is shown in repository_path.

    result = Get_git_diff(repo, commit_sha)
    print(commit_sha)
    print(result)

    repo.git.checkout(commit_sha)


    # Trivial

    #run_time = copy_repo_and_enc_files(repository_path, repo_cipher_path_trivial)

    # Trivial
    trivial_enc_time, trivial_sign_time = Init_for_Trivial(repository_path, repo_cipher_path_trivial, msg_upd, GENSIGN)
    repo_trivial.git.branch('-M', 'trivial')
    repo_trivial.create_remote('origin', url)
    output_trivial, push_time_trivial = git_push_with_details(repo_cipher_path_trivial, 'trivial')
    print(output_trivial)
    comm_cost_trivial = get_pack_size(output_trivial)
    print(comm_cost_trivial)
    e2e_time_trivial = trivial_enc_time + trivial_sign_time + push_time_trivial

    # print("enc finish")
    # repo_cipher = Repo(repo_cipher_path_trivial)
    # repo_trivial.index.add(['.'])
    # repo_cipher.index.commit(msg)
    # all_files = []
    # batch_size = 1000
    # for root, dirs, files in os.walk(encrypt_path):
    #     for file in files:
    #         full_path = os.path.join(root, file)
    #         rel_path = os.path.relpath(full_path, encrypt_path)
    #         all_files.append(rel_path)
    #
    # #
    # for i in range(0, len(all_files), batch_size):
    #     batch = all_files[i:i + batch_size]
    #     safe_remove_git_lock(repo_cipher.working_tree_dir)
    #     repo_cipher.index.add(batch)
    #     print(f"Added batch {i // batch_size + 1} with {len(batch)} files")
    # repo_cipher.index.add(['.'])
    # print("trivial all")
    # repo_trivial.index.commit(msg_upd)
    # print("trivial commit")

    # repo_trivial.git.branch('-M', 'trivial')
    # repo_trivial.create_remote('origin', url)
    # output_trivial, push_time_trivial = git_push_with_details(repo_cipher_path_trivial, 'trivial')
    # print(output_trivial)
    # comm_cost_trivial = get_pack_size(output_trivial)
    # print(comm_cost_trivial)

    logging.info('index %s', i)

    logging.info('Trivial-enc-sign %s', round(e2e_time_trivial, 4))

    logging.info('Trivial-enc-sign - enc %s', round(trivial_enc_time, 4))

    logging.info('Trivial-enc-sign - sign %s', round(trivial_sign_time, 4))

    logging.info('Trivial-enc-sign - push %s', round(push_time_trivial, 4))

    logging.info('The communication costs of an update (KB):')


    logging.info('Trivial-enc-sign (MB): %s', round(comm_cost_trivial / 1024, 4))


    return comm_cost_trivial


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate communication cost of a specific commit index.')
    parser.add_argument('--index', type=int, required=True, help='Index from 0 to 9 for commit selection.')
    args = parser.parse_args()

    index = args.index

    if not (0 <= index <= 9):
        raise ValueError("Index must be between 0 and 9.")

    test_num = 1
    REPO = FCC
    commit_SHA = repo_commit_map[REPO][index]

    result = test(REPO, commit_SHA, index)

    logging.info('The communication costs of update shown in Table 2 (KB):')
    logging.info('Repo: %s', REPO)
    logging.info('index: %s', index)
    logging.info('Trivial-enc-sign (MB): %s', round(result / 1024, 4))
