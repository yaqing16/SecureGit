import subprocess
import re

from git import Repo

def Get_git_diff(repository, commit_sha):
    #commit = repository.commit(commit_sha)

    # get the output of `git diff -U0`
    diff_text = repository.git.diff(commit_sha + "~1", commit_sha, "--unified=0")
    # with open('E:/Yanan/test_diff/result.py', 'w') as f:
    #     f.writelines(diff_text)

    # print(diff_text)

    if diff_text == '':
        return ''

    #print(diff_text)
    added_files = []  # newly added filenames
    added_files_content = []  # newly added file content
    deleted_files = []  # the filename list to delete
    renamed_files = []  # the filename list to rename [(old_name, new_name)]
    modified_files = []  # the filename list to modify
    deleted_lines = []  # List of deleted line numbers for each modified file
    inserted_lines = []  # List of insert line numbers for each modified file
    inserted_content = []  # A list of inserts for each modified file

    # Parse diff_text
    diff_blocks = diff_text.split("\ndiff --git")[0:]  #  `diff --git`
    for block in diff_blocks:
        lines = block.splitlines()
        #print(lines)
        first_line = lines[0].strip()
        second_line = lines[1].strip()
        # print(first_line)
        # print(second_line)

        if first_line.startswith("diff --git"):
            match = re.match(r"diff --git a/(.+?) b/(.+)", first_line)
            # file_a = first_line.split()[2][2:]  # remove prefix "a/"
            # file_b = first_line.split()[3][2:]  # remove prefix "b/"
            file_a = match.group(1)
            file_b = match.group(2)
        else:
            # file_a = first_line.split()[0][2:]  # remove prefix "a/"
            # file_b = first_line.split()[1][2:]  # remove prefix "b/"
            match = re.match(r'^a/(.*?) b/(.*)', first_line)
            file_a = match.group(1)
            file_b = match.group(2)
            # print("file_b:", file_b)
        #print(file_a, file_b)

        #print('file a:', file_a)
        current_deleted_lines = []
        current_inserted_lines = []
        current_inserted_content = []
        old_line, new_line = None, None

        if second_line.startswith("new file mode"):
            added_files.append(file_b)
            # print('file_b:', file_b)
            content = repository.git.show(f"{commit_sha}:{file_b}")
            added_files_content.append(content)
            continue

        elif second_line.startswith("deleted file mode"):
            deleted_files.append(file_a)
            continue

        #print("line 0:", lines[0])
        #print("second line:", second_line)

        elif second_line.startswith("similarity index 100%"):
            #print(first_line)
            renamed_files.append((file_a, file_b))
            continue

        elif second_line.startswith("similarity index"):
            renamed_files.append((file_a, file_b))

        for line in lines[1:]:
            line = line.strip()
            if line.startswith("@@"):
                # extract the line idex
                parts = line.split()
                old_range = parts[1][1:].split(",")
                new_range = parts[2][1:].split(",")
                old_line = int(old_range[0]) if old_range else 0
                new_line = int(new_range[0]) if new_range else 0
            elif line.startswith("-") and old_line is not None:
                # lines to be deleted
                current_deleted_lines.append(old_line)
                old_line += 1
            elif line.startswith("+") and new_line is not None:
                # lines to be inserted
                current_inserted_lines.append(new_line)
                current_inserted_content.append(line[1:])
                new_line += 1
        modified_files.append(file_b)
        deleted_lines.append(current_deleted_lines)
        inserted_lines.append(current_inserted_lines)
        inserted_content.append(current_inserted_content)

    # print("modified file:", modified_files)
    # print("delete index:", deleted_lines)
    # print("insert index:", inserted_lines)

    return {
        "added_files": added_files,
        "added_files_content": added_files_content,
        "deleted_files": deleted_files,
        "renamed_files": renamed_files,
        "modified_files": modified_files,
        "deleted_lines": deleted_lines,
        "inserted_lines": inserted_lines,
        "inserted_content": inserted_content,
    }

def git_gc(repo_path):
    try:
        # run "git gc --aggressive --prune=now"
        result = subprocess.run(
            ['git', 'gc', '--aggressive', '--prune=now'],
            cwd=repo_path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # if succeed
        print("Git garbage collection (aggressive) successful!")
        print(result.stdout.decode())
    except subprocess.CalledProcessError as e:
        # if fail
        print("Error during git gc:")
        print(e.stderr.decode())

def get_commit_bytes(commit):
    # Get parent commit hash
    parent_hashes = [parent.hexsha for parent in commit.parents] if commit.parents else [b'']

    # Get tree hash
    tree_hash = commit.tree.hexsha

    # Get author information
    author_name = commit.author.name
    author_email = commit.author.email
    author_time = commit.authored_date

    # Get committer information
    committer_name = commit.committer.name
    committer_email = commit.committer.email
    committer_time = commit.committed_date

    # Get commit message
    commit_message = commit.message.strip()

    parent_hashes = [parent.hexsha for parent in commit.parents]

    parent_hashes_str = ', '.join(parent_hashes)

    result_str = (
        f"parents: {parent_hashes_str}, "
        f"tree: {tree_hash}, "
        f"author: {author_name} <{author_email}>, {author_time}, "
        f"committer: {committer_name} <{committer_email}>, {committer_time}, "
        f"message: {commit_message}"
    )

    # print("original string:", result_str)

    # transform to bytes
    result_bytes = result_str.encode('utf-8')

    #print(result_bytes)

    return result_bytes, f"{committer_time}", commit_message

def test():
    # example
    repository_path = 'path'
    repo = Repo(repository_path)
    result = Get_git_diff(repo, commit_sha)

    repository = Repo(repository_path)

    #current_commit = repository.head.commit
    #previous_commit = current_commit.parents[0] if current_commit.parents else None

    print("added files:", result["added_files"])
    print("added files content:", result["added_files_content"])
    print("deleted files:", result["deleted_files"])
    print("renamed files:", result["renamed_files"])
    print("modified files:", result["modified_files"])
    print("deleted lines index:", result["deleted_lines"])
    print("inserted lines index:", result["inserted_lines"])
    print("inserted content:", result["inserted_content"])



    # for one_file, one_del, one_add, one_add_lines in zip(result["modified_files"], result["deleted_lines"], result["inserted_lines"], result["inserted_content"]):
    #     parent_content = previous_commit.tree / one_file
    #     original_text = parent_content.data_stream.read()
    #     cipher_lines, enc_time, upd_time, del_time, ins_time = reencrypt_one_file_content(original_text, one_del, one_add, one_add_lines)
    #     #encrypt_time = encrypt_time + enc_time
    #
    #     print("updated cipher:", cipher_lines)


if __name__ == '__main__':
    test()

#print(result["renamed_files"][0][0])

