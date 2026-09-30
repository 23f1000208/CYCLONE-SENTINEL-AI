import os
import sys
import subprocess

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    backend_path = os.path.join(root, "backend")
    
    env = os.environ.copy()
    env["PYTHONPATH"] = backend_path

    print("=" * 60)
    print("CYCLONE SENTINEL AI - COMPREHENSIVE TEST SUITE RUNNER")
    print("=" * 60)
    
    cmd = [sys.executable, "-m", "pytest", "backend/tests", "-v"]
    res = subprocess.run(cmd, cwd=root, env=env)
    sys.exit(res.returncode)

if __name__ == "__main__":
    main()
