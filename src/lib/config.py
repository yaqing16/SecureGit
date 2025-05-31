ignore_list = ['.git', '.DS_Store']

GENSIGN = True
NOSIGN = False

token = 'Paste the Github token here'  # e.g., token = 'github_pat_XXX'


awesome = 'awesome'
FPB = 'free-programming-books'
bootstrap = 'bootstrap'
react = 'react'
FCC = 'freeCodeCamp'
DocRepo = 'DocRepo'

First_commit = {
    awesome: 'f680aaf',
    FPB: '9d12a9c3',
    bootstrap: 'eb81782cd',
    react: '75897c2dcd',
    FCC: '7a80dfe168',
    DocRepo: 'xxx'
}

'''
    The information about DocRepo:
    the number of commits: 71
    the number of lines (the latest commit): 18301
    the number of files (the latest commit): 67
    the size (including .git): 3.44 MB
'''

Latest_commit = {
    awesome: '36d8bf5835c35f691f0ecdac9b05118c800d1cd4',
    FPB: '82d11be9f39052184c70d5c20eea977693de115d',
    bootstrap: 'a5d430d526dcb330b3e0f12aa1321cf948d726f1',
    react: '3b009b4cd58d382cfde2a72232c87df1a34d56d5',
    FCC: '01273fb5bc89392996368f028fc3ead092e3b3f5',
    DocRepo: 'xxx'
}


'''
We randomly choose ten commits for each repo. The commit hash values are shown as follows.
'''

commit_SHA_FCC = [
    '61e07041a749c4e00c2ea7185bd0dbac087f547b',
    'e4f9f7796d471dafdf7596562f7936fe4fe15151',
    '8707bd819247cb9a1dc601e59215b512951e50bd',
    '0b4cdb07e9f4ece74c9048e712feaddd71848ff2',
    '82e21aca0e8357e52ff95ae5d7ccb7eba02e8bb2',
    'e135ab81aab9e382fe72105af3a741bed46f121b',
    '44f4b30890f1b402e5049c8c0ee55548552de76a',
    'ddb6aa13c778dd5e9fc014f6fc869643f490f1e4',
    '4300d0e0607b4eeffd38b340cf8ae16093745fb0',
    '97fcaa693f6896680e8ccc8eed20feee158c8105'
]

commit_SHA_awesome = [
    'efc2a482edd74dc7fdaa04f44af227226995cf49',
    '651ae50db0b85dc87ca6b14ed359e153193a453d',
    'bff4772e2c4733e152c373e0f5f246f264fd9f0d',
    '493cc514db32b3433d6efa801f17d26c792f4f0a',
    'ab18ee58883e4f2efc6f07c9447903f3326ada55',
    '16052905a379c66dc6a6433fb35c4e2643722bc6',
    '0ddd5e277a7a39b733438e1f4b788e6509f12c5c',
    'c75f8f05478a4c2f81d8df67bf6e2e043e5c95fd',
    '2b5a4927a5a2f5d7a93be41c2e7a0bff7dbd080e',
    '14a0396c930d0703ff64d02ad53b214d992bb824'
]

commit_SHA_FPB = [
    'f92b640593df32582e599ac4eec9676b3e4d10cb',
    '959285ed35d12b28ecc932c686c2d049bc96c026',
    '277153108c57962183d6c557633c03f8d6ee8219',
    'c5db16fbf93d9cffbbbd01d3af3718134d4509c1',
    '0be7b17e7d7e7ad1a3d39eb0b88f5d3b7fb40b01',
    '5682ded3c1d0e1bacdd9176c68f7a377a150f396',
    '3aa1be7729b8dca938d5c379d0c320d7f7367603',
    '833afdc8a7c36a32347fb582b4fa3c8fb2643747',
    '5261731a0c157dd8c5d26f05976ded669fabafb8',
    '30530e858bbd7f28dcd7323d37e3c3d35a640bea'
]

commit_SHA_react = [
    '6c785ed5246997c6d2b6bc1a84177e94f413cb27',
    '5dee15273fd044ebf83aa1ff903ddcaf346cec45',
    '4e6eec69be632c0c0177c5b1c8a70397d92ee181',
    '9faf389e79c647d7792e631f3d8e9a9ce1a70625',
    '8d7161e0047e5ae85701f5684d196e3898c65263',
    'bd5bf555e1167e7088a4391e5cd419dccb39714c',
    'd67f23fb0e1813aae26ff09d36eea9e32d8e3dae',
    'bfd5b1878e6eeebd8899bd221cb62ddc046c875d',
    'c45fa8b5813ef2f8332c39c51f1dc88f1acf5fcd',
    'a22880e5e59d5cb17fffe04af093ea54e356538d'
]

commit_SHA_bootstrap = [
    'bfd83c0a4756dfc6cde36e15e382997e102dc580',
    'b3a125e941fac35220ac94a892bb547547db4f8d',
    '8770b84e845d80c50a0f3c5712d3573adcec202f',
    'e38d08d4c0c23e678549b10f96286b37a7d8c7ed',
    '082723f3f4c12b7f5ca85aa1ebfe34b63ddb9d8c',
    '3dfad4f1addd50a066d28ca605f14d4dc9a2b82f',
    '01be344956791303ce1ac1bbd19ed1f86ed13145',
    '330e9b16c2fcb96ae350b170cda61d5937aa5a78',
    'b376a3d80d3ce7a9106bf42b890167ecc992f912',
    '6145fd293141963f9581d741bc0489eb06c276f5'
]

commit_SHA_Paper = [
    'xxx',
    'xxx',
    'xxx',
    'xxx',
    'xxx',
    'xxx',
    'xxx',
    'xxx',
    'xxx',
    'xxx'
]

repo_commit_map = {
    awesome: commit_SHA_awesome,
    FPB: commit_SHA_FPB,
    bootstrap: commit_SHA_bootstrap,
    react: commit_SHA_react,
    FCC: commit_SHA_FCC,
    DocRepo: commit_SHA_Paper
}


def basicurl():
    return f'https://{token}@github.com/hymanww/basic-test.git'

def remoteurl(REPO):
    return f'https://{token}@github.com/hymanww/{REPO}.git'

def remoteurl_init(REPO):
    return f'https://{token}@github.com/hymanww/{REPO}-test.git'

def remoteurl_e2e(REPO):
    return f'https://{token}@github.com/hymanww/{REPO}-e2e.git'
