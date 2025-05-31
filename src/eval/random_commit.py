from src.lib.config import *
import random
from src.lib.repo_operation import *

def pick_random_commit(repo_path):
    try:
        repo = Repo(repo_path)
        if repo.bare:
            print('Empty repo')
            return

        commits = list(repo.iter_commits())
        if not commits:
            print('No commits')
            return

        commit_sha = selected_commit = random.choice(commits)
        print(f'randomly chosen commit: {selected_commit.hexsha}')

        return commit_sha

    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':

    base_dir = Path(__file__).parent

    REPO = DocRepo

    repository_path = base_dir.parent.parent / 'dataset' / REPO

    repo = Repo(repository_path)

    commit_sha = pick_random_commit(repository_path)

    # result = Get_git_diff(repo, str(commit_sha))

    # print(result)
