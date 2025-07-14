from src.lib.config import *
from src.lib.repo_operation import *
import logging
import argparse

base_dir = Path(__file__).parent

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    filename=base_dir.parent.parent / 'evaluationlog' / 'test_recovery_log.log',
    filemode='a',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.getLogger('git').setLevel(logging.CRITICAL)


def test(REPO, commit_sha, i):
    base_dir = Path(__file__).parent

    repository_path = base_dir.parent.parent / 'dataset' / REPO

    # print(repository_path)

    cipher_path = base_dir.parent.parent / 'output' / 'test-update-comp' / REPO

    repo_cipher_path_line = cipher_path / 'linecipher' / str(i)
    repo_cipher_path_patch = cipher_path / 'patchcipher' / str(i)
    repo_cipher_path_file = cipher_path / 'filecipher' / str(i)
    repo_cipher_path_trivial = cipher_path / 'trivialcipher' / str(i)
    repo_plain_path_pre = cipher_path / 'plain_pre' / str(i)
    repo_plain_path_current = cipher_path / 'plain_current' / str(i)

    recover_path = base_dir.parent.parent / 'output' / 'test-recover' / REPO


    repo_recover_path_line = recover_path / 'linecipher' / str(i)
    repo_recover_path_patch = recover_path / 'patchcipher' / str(i)
    repo_recover_path_file = recover_path / 'filecipher' / str(i)
    repo_recover_path_trivial = recover_path / 'trivialcipher' / str(i)
    repo_recover_path_line_diff = recover_path / 'linediff' / str(i)

    Dec_trivial_time = 0

    repo = Repo(repository_path)

    result = Get_git_diff(repo, commit_sha)

    Dec_line_time = Dec_line(result, repo_cipher_path_line, repo_plain_path_pre, repo_plain_path_current, repo_recover_path_line)

    Dec_patch_time = Dec_patch(result, repo_cipher_path_patch, repo_plain_path_pre, repo_plain_path_current, repo_recover_path_patch)

    print('patch:', Dec_patch_time)
    Dec_DE_time = Dec_DE(result, repo_cipher_path_file, repo_plain_path_pre, repo_plain_path_current, repo_recover_path_file)

    Dec_trivial_time = Dec_Trivial(repo_cipher_path_trivial, repo_recover_path_trivial)

    # Dec_line_time_diff = Dec_line_eff(repo_cipher_path_line, repo_plain_path_pre, repo_plain_path_current, repo_recover_path_line_diff)

    result = [Dec_line_time, Dec_patch_time, Dec_DE_time, Dec_trivial_time]

    print(result)

    return result

def main(REPO, commit_SHA):
    result = [0] * 4

    for i in range(len(commit_SHA)):
        result = [sum(x) for x in zip(result, test(REPO, commit_SHA[i], i))]

    result = [round(x / 10, 7) for x in result] # 10 commits

    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate recovery computation costs.')
    parser.add_argument('--repo', required=True, help='Repository name: awesome, FPB, bootstrap, react, FCC')
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

    REPO = repo_map[args.repo]
    commit_SHA = repo_commit_map[REPO]

    result = [0] * 5
    test_num = 10

    for _ in range(test_num):
        result = [sum(x) for x in zip(result, main(REPO, commit_SHA))]

    result = [round(x / test_num, 4) for x in result]

    logging.info('The computation costs of recovery shown in Table 4 (s):')
    logging.info('Repo: %s', REPO)
    logging.info('SGitChar: %s', result[1])
    logging.info('SGitLine: %s', result[0])
    logging.info('Git-crypt: %s', result[2])
    logging.info('Trivial-enc-sign: %s', result[3])

    # print('SGitLine (using git diff):', result[4])
