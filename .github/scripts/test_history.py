import subprocess
import sys
import os

def run_cmd(cmd, cwd=None):
    return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)

def main():
    # Get all tags
    res = run_cmd("git tag")
    if res.returncode != 0:
        print("Failed to get tags")
        sys.exit(1)
    
    tags = res.stdout.strip().split('\n')
    # Filter tags: exclude empty strings and tags ending with "-range"
    tags = [t for t in tags if t and not t.endswith("-range")]
    
    print(f"Found {len(tags)} tags to test: {', '.join(tags)}")
    
    failures = []
    
    for tag in tags:
        print(f"----------------------------------------")
        print(f"Testing tag: {tag}")
        
        # Checkout tag
        res = run_cmd(f"git checkout -f {tag}")
        if res.returncode != 0:
            print(f"Failed to checkout {tag}: {res.stderr}")
            failures.append((tag, "Checkout failed"))
            continue
            
        # Check if core directory exists
        if not os.path.exists("core"):
            print(f"Skipping {tag}: core directory not found")
            continue
            
        # Check format
        print("Running veryl fmt...")
        fmt_res = run_cmd("veryl fmt", cwd="core")
        if fmt_res.returncode != 0:
             print(f"veryl fmt failed for {tag}")
             print(fmt_res.stderr)
             failures.append((tag, "veryl fmt failed"))
             continue
             
        # Check for changes
        diff_res = run_cmd("git diff --exit-code", cwd="core")
        if diff_res.returncode != 0:
            print(f"Format check failed for {tag} (files modified)")
            failures.append((tag, "Format check failed"))
            continue
            
        # Build
        print("Running veryl build...")
        build_res = run_cmd("veryl build", cwd="core")
        if build_res.returncode != 0:
            print(f"Build failed for {tag}")
            print(build_res.stderr)
            failures.append((tag, "Build failed"))
            continue
            
        print(f"Tag {tag} passed")

    print(f"----------------------------------------")
    if failures:
        print("\nSummary of failures:")
        for tag, reason in failures:
            print(f"  {tag}: {reason}")
        sys.exit(1)
    else:
        print("\nAll tags passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
