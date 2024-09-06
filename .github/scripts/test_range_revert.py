import subprocess
import sys

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def main():
    # Get all tags ending with -range
    res = run_cmd("git tag --list '*-range'")
    if res.returncode != 0:
        print("Failed to list tags")
        sys.exit(1)
    
    tags = res.stdout.strip().split('\n')
    tags = [t for t in tags if t]
    
    if not tags:
        print("No *-range tags found.")
        sys.exit(0)

    failures = []
    
    # Get current HEAD
    res_head = run_cmd("git rev-parse HEAD")
    if res_head.returncode != 0:
        print("Failed to get HEAD")
        sys.exit(1)
    head_commit = res_head.stdout.strip()
    
    print(f"Current HEAD: {head_commit}")

    for tag in tags:
        # Check if tag is ancestor of HEAD
        is_ancestor = run_cmd(f"git merge-base --is-ancestor {tag} HEAD")
        if is_ancestor.returncode != 0:
            # Tag not in current history, skip
            continue
            
        print(f"----------------------------------------")
        print(f"Checking tag: {tag}")
        
        # Get Commit B (Tag)
        res_b = run_cmd(f"git rev-parse {tag}")
        commit_b = res_b.stdout.strip()
        
        # Get Commit A (Parent of B)
        res_a = run_cmd(f"git rev-parse {tag}^")
        if res_a.returncode != 0:
            print(f"  Failed to get parent of {tag}")
            failures.append(tag)
            continue
        commit_a = res_a.stdout.strip()
        
        # Get Commit C (Child of B in path to HEAD)
        # git rev-list --ancestry-path commit_b..HEAD lists commits from HEAD down to child of B
        # The last one is the immediate child
        res_c = run_cmd(f"git rev-list --ancestry-path {commit_b}..HEAD | tail -1")
        commit_c = res_c.stdout.strip()
        
        if not commit_c:
            print(f"  No child commit found for {tag} (it might be the tip)")
            continue
            
        print(f"  Commit A (Before): {commit_a}")
        print(f"  Commit B (Tag):    {commit_b}")
        print(f"  Commit C (After):  {commit_c}")
        
        # Compare A and C
        diff_cmd = f"git diff --exit-code {commit_a} {commit_c}"
        res_diff = run_cmd(diff_cmd)
        
        if res_diff.returncode != 0:
            print(f"  FAILURE: Diff detected between {commit_a} and {commit_c}")
            # Show summary of diff
            print(run_cmd(f"git diff --stat {commit_a} {commit_c}").stdout)
            failures.append(tag)
        else:
            print(f"  OK: No diff between {commit_a} and {commit_c}")

    print(f"----------------------------------------")
    if failures:
        print(f"Failures found in tags: {', '.join(failures)}")
        sys.exit(1)
    else:
        print("All checks passed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
