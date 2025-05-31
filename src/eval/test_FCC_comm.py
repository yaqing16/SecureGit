from src.lib.config import *
from src.lib.repo_operation import *
from src.lib.file_operation import *
import logging

base_dir = Path(__file__).parent

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)


logging.basicConfig(
    filename=base_dir.parent.parent / 'log' / 'test_FCC_comm_log.log',
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

    msg_upd = 'update'

    sum_plain, sum_line, sum_patch, sum_DE, sum_trivial = 0, 0, 0, 0, 0

    # make the parent version of commit_sha is shown in repository_path.

    result = Get_git_diff(repo, commit_sha)
    print(commit_sha)
    print(result)

    repo.git.checkout(commit_sha)


    # Trivial

    run_time = copy_repo_and_enc_files(repository_path, repo_cipher_path_trivial)
    # print("enc finish")
    repo_cipher = Repo(repo_cipher_path_trivial)
    repo_cipher.index.add(['.'])
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
    print("trivial all")
    repo_cipher.index.commit(msg_upd)
    print("trivial commit")

    repo_trivial.git.branch('-M', 'trivial')
    repo_trivial.create_remote('origin', url)
    output_trivial, push_time_trivial = git_push_with_details(repo_cipher_path_trivial, 'trivial')
    print(output_trivial)
    comm_cost_trivial = get_pack_size(output_trivial)
    print(comm_cost_trivial)


    return comm_cost_trivial


if __name__ == '__main__':

    test_num = 1

    '''
        set the parameter index to 0~9, respectively
    '''

    index = 9

    REPO = FCC  # choose one repo
    commit_SHA = repo_commit_map[REPO][index]

    result = test(REPO, commit_SHA, index)

    logging.info('The communication costs of update shown in Table 2 (KB):')

    logging.info('Repo: %s', REPO)

    logging.info('index: %s', index)

    logging.info('Trivial-enc-sign (MB): %s', round(result / 1024, 4))
