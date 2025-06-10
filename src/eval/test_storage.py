from src.lib.config import *
from src.lib.repo_operation import *
from src.lib.file_operation import *
from pathlib import Path
import logging

base_dir = Path(__file__).parent

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    filename=base_dir.parent.parent / 'log' / 'test_storage_log.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.getLogger('git').setLevel(logging.CRITICAL)



def test(REPO, number):

    repository_path = base_dir.parent.parent / 'dataset' / REPO

    # print(repository_path)

    cipher_path = base_dir.parent.parent / 'output' / 'test-storage' / REPO

    repo_cipher_path_line = cipher_path / 'linecipher'
    repo_cipher_path_patch = cipher_path / 'patchcipher'
    repo_cipher_path_file = cipher_path / 'filecipher'
    repo_cipher_path_trivial = cipher_path / 'trivialcipher'
    repo_plain_path = cipher_path / 'plain'

    delete_all_files_in_directory(repo_cipher_path_line)
    delete_all_files_in_directory(repo_cipher_path_patch)
    delete_all_files_in_directory(repo_cipher_path_file)
    delete_all_files_in_directory(repo_cipher_path_trivial)
    delete_all_files_in_directory(repo_plain_path)

    Repo.init(repo_cipher_path_line)
    Repo.init(repo_cipher_path_patch)
    Repo.init(repo_cipher_path_file)
    Repo.init(repo_plain_path)
    Repo.init(repo_cipher_path_trivial)

    repo = Repo(repository_path)
    repo_line = Repo(repo_cipher_path_line)
    repo_patch = Repo(repo_cipher_path_patch)
    repo_file = Repo(repo_cipher_path_file)
    repo_plain = Repo(repo_plain_path)
    repo_trivial = Repo(repo_cipher_path_trivial)

    repo.git.checkout(Latest_commit[REPO])

    all_commits = []


    for commit in repo.iter_commits('main', first_parent=True):
        all_commits.append(commit.hexsha)
    if len(all_commits) < 2:
        raise Exception('error! not enough commits')

    commit_number = len(all_commits)

    repo.git.checkout(all_commits[commit_number - 1])  #first version
    # print(all_commits[commit_number - 1])
    #print(all_commits[commit_number - 1])
    #print(type(all_commits[commit_number - 1]))

    sum_line_time, sum_patch_time, sum_DE_time, sum_Trivial_time = 0, 0, 0, 0


    commit_init = repo.commit(all_commits[commit_number - 1])

    msg_init = commit_init.message.strip()

    # print('msg init:', msg_init)

    # Line Init
    init_line_time = Init_for_line(repository_path, repo_cipher_path_line, msg_init, GENSIGN)

    init_patch_time = Init_for_patch(repository_path, repo_cipher_path_patch, msg_init, GENSIGN)

    init_DE_time = Init_for_DE(repository_path, repo_cipher_path_file, msg_init, NOSIGN)

    init_Trivial_time = Init_for_Trivial(repository_path, repo_cipher_path_trivial, msg_init, GENSIGN)

    # plain init
    copy_repo_and_files(repository_path, repo_plain_path)
    repo_plain.git.add('--all')
    repo_plain.index.commit(msg_init)

    repo_plain.git.gc('--aggressive', '--prune=now')
    repo_trivial.git.gc('--aggressive', '--prune=now')
    repo_file.git.gc('--aggressive', '--prune=now')
    repo_line.git.gc('--aggressive', '--prune=now')
    repo_patch.git.gc('--aggressive', '--prune=now')

    plain_size = get_folder_size(repo_plain_path)

    line_size = get_folder_size(repo_cipher_path_line)

    patch_size = get_folder_size(repo_cipher_path_patch)

    DE_size = get_folder_size(repo_cipher_path_file)

    Trivial_size = get_folder_size(repo_cipher_path_trivial)

    # print("Init")
    # print("plain size:", plain_size)
    # print("line size:", line_size)
    # print("patch size:", patch_size)
    # print("DE size:", DE_size)
    # print("Trivial size:", Trivial_size)
    #
    # print("init line time:", init_line_time)
    # print("init patch time:", init_patch_time)
    # print("init DE time:", init_DE_time)
    # print("init Trivial time:", init_Trivial_time)


    for i in range(2, number):
        commit_sha = all_commits[commit_number - i]
        print(f"{i}-th update")
        print(commit_sha)
        repo.git.checkout(commit_sha)

        commit_upd = repo.commit(commit_sha)

        commit_msg = commit_upd.message.strip()

        # print('msg upd:', commit_msg)

        # commit_msg = f'{i}-th update'

        # line update
        line_comp_time, line_diff_time, line_update_time, line_ciphersize = update_line_diff(repository_path, repo_cipher_path_line, commit_sha, commit_msg, GENSIGN)
        #repo_line.git.gc()

        # patch update
        patch_comp_time, patch_diff_time, patch_enc_time, patch_ciphersize = update_patch_diff(repository_path, repo_cipher_path_patch, commit_sha, commit_msg, GENSIGN)
        #repo_patch.git.gc()

        # update DE
        DE_comp_time, DE_enc_time, DE_ciphersize = update_file_diff(repository_path, repo_cipher_path_file, commit_sha, commit_msg, GENSIGN)
        #repo_file.git.gc()

        # update trivial
        delete_all_except_git(repo_cipher_path_trivial)
        Trival_comp_time = Init_for_Trivial(repository_path, repo_cipher_path_trivial, commit_msg, GENSIGN)
        #repo_trivial.git.gc()

        # update plain
        delete_all_except_git(repo_plain_path)
        copy_repo_and_files(repository_path, repo_plain_path)
        repo_plain.git.add('--all')
        repo_plain.index.commit(commit_msg)
        #repo_plain.git.gc()


        if i%10 == 0:
            repo_plain.git.gc('--aggressive', '--prune=now')
            repo_trivial.git.gc('--aggressive', '--prune=now')
            repo_file.git.gc('--aggressive', '--prune=now')
            repo_line.git.gc('--aggressive', '--prune=now')
            repo_patch.git.gc('--aggressive', '--prune=now')

            # git_gc(repo_cipher_path_line)
            # git_gc(repo_cipher_path_patch)
            # git_gc(repo_cipher_path_file)
            # git_gc(repo_cipher_path_trivial)
            # git_gc(repo_plain_path)

            plain_size = get_folder_size(repo_plain_path)

            line_size = get_folder_size(repo_cipher_path_line)

            patch_size = get_folder_size(repo_cipher_path_patch)

            DE_size = get_folder_size(repo_cipher_path_file)

            Trivial_size = get_folder_size(repo_cipher_path_trivial)

            logging.info("The storage costs shown in the figures")
            logging.info('The number of updates: %s', i)
            logging.info("Repo: %s", REPO)
            logging.info("Git: %s", round(plain_size, 4))
            logging.info("Git-crypt: %s", round(DE_size, 4))
            logging.info("Trivial-enc-sign: %s", round(Trivial_size, 4))
            logging.info("SGitLine: %s", round(line_size, 4))
            logging.info("SGitChar: %s", round(patch_size, 4))
    git_gc(repo_cipher_path_line)
    git_gc(repo_cipher_path_patch)
    git_gc(repo_cipher_path_file)
    git_gc(repo_cipher_path_trivial)
    git_gc(repo_plain_path)

    repo.git.checkout(all_commits[0])

if __name__ == '__main__':
    '''
        set the parameter REPO to `awesome/FPB/bootstrap/react/FCC`, respectively
    '''
    REPO = awesome 
    commit_number = 51
    test(REPO, commit_number)