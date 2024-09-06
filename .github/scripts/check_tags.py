import subprocess
import sys
from collections import defaultdict

def run_git_command(args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Git command failed: {result.stderr}")
    return result.stdout.strip()

def main():
    try:
        print("Checking tags...")

        # Get all tags
        tags_output = run_git_command(['git', 'tag'])
        tags = tags_output.splitlines()
        
        if not tags:
            print("No tags found.")
            return

        # Determine target branch (book)
        target_branch = 'origin/book'
        try:
            run_git_command(['git', 'rev-parse', '--verify', target_branch])
        except:
            target_branch = 'book'
            try:
                run_git_command(['git', 'rev-parse', '--verify', target_branch])
            except:
                 print(f"Error: Could not find branch 'book' or 'origin/book'.")
                 sys.exit(1)

        print(f"Target branch is {target_branch}")

        # Get all commits in book branch
        book_commits_output = run_git_command(['git', 'rev-list', target_branch])
        book_commits = set(book_commits_output.splitlines())

        tags_per_commit = defaultdict(list)
        errors = []

        for tag in tags:
            # Get commit for tag
            tag_commit = run_git_command(['git', 'rev-list', '-n', '1', tag])
            
            # Check Constraint 1: Tag must be in book branch
            if tag_commit not in book_commits:
                errors.append(f"Tag '{tag}' (commit {tag_commit}) is not in '{target_branch}' history.")
            
            tags_per_commit[tag_commit].append(tag)

        # Check Constraint 2: No more than 1 tag per commit
        for commit, tag_list in tags_per_commit.items():
            if len(tag_list) > 1:
                errors.append(f"Commit {commit} has multiple tags: {', '.join(tag_list)}")

        if errors:
            print("Tag validation failed:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        
        print("All tags valid.")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
