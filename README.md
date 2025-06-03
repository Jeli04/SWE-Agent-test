# SWE-Agent-test

Clone with submodules 
```
    git clone --recurse-submodules https://github.com/Jeli04/SWE-Agent-test.git
```

Setup the requirements for ollama-tools
```
    cd ollama-tools
    pip install -r requirements.txt
```

When running anything Github related please set your token (run this below in terminal)
```
    export GITHUB_TOKEN=your_token
```

### merge_pr_accept_theirs

`merge_pr_accept_theirs(owner, repo, pull_number, base='main')` fetches the pull
request information and performs a local merge of the PR branch into the `base`
branch using `git merge -X theirs`. The merge is pushed back to GitHub and the
pull request is closed if the push succeeds.

