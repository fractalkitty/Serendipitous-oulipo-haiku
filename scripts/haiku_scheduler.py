#!/usr/bin/env python3
"""
Scheduled haiku updater - replaces cron
Runs continuously and updates haikus every hour
"""

import time
import schedule
import subprocess
import os
import sys
from datetime import datetime

def run_command(cmd, cwd=None):
    """Run a command and return success status and output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def update_haiku():
    """Main haiku update function - runs every hour"""
    print(f"\n{'='*50}")
    print(f"Starting haiku update at {datetime.now()}")
    print(f"{'='*50}")

    try:
        # Get directories
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)

        # Step 1: Generate new haiku
        print("Generating new haiku...")
        success, stdout, stderr = run_command("python3 generate_haiku.py", cwd=script_dir)
        if not success:
            print(f"ERROR: Failed to generate haiku: {stderr}")
            return
        print("✓ Haiku generated")

        # Step 2: Update archive
        print("Updating archive...")
        success, stdout, stderr = run_command("python3 update_archive.py", cwd=script_dir)
        if not success:
            print(f"ERROR: Failed to update archive: {stderr}")
            return
        print("✓ Archive updated")

        # Step 3: Update RSS
        print("Updating RSS feed...")
        success, stdout, stderr = run_command("python3 update_rss.py", cwd=script_dir)
        if not success:
            print(f"ERROR: Failed to update RSS: {stderr}")
            return
        print("✓ RSS updated")

        # Step 4: Git operations from project root
        os.chdir(project_root)

        # Add files
        print("Adding files to git...")
        success, stdout, stderr = run_command("git add .")
        if not success:
            print(f"ERROR: Failed to add files: {stderr}")
            return

        # Commit
        commit_msg = f"Update haiku {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        print(f"Committing: {commit_msg}")
        success, stdout, stderr = run_command(f'git commit -m "{commit_msg}"')
        if not success:
            if "nothing to commit" in stderr:
                print("No changes to commit")
                return
            print(f"ERROR: Failed to commit: {stderr}")
            return

        # Push
        print("Pushing to remote...")
        success, stdout, stderr = run_command("git push origin main")
        if success:
            print(f"✓ Push successful at {datetime.now()}")
        else:
            print(f"✗ Push failed: {stderr}")
            print("Commits are saved locally, will retry next time")

        print(f"Update completed at {datetime.now()}")

    except Exception as e:
        print(f"Update failed with exception: {e}")

def main():
    print("Starting Haiku Scheduler...")
    print(f"Current time: {datetime.now()}")
    print("Will update every 6 hours")

    # Schedule the job every hour
    schedule.every(6).hours.do(update_haiku)

    # Optional: run immediately for testing
    # update_haiku()

    print("Scheduler running... Press Ctrl+C to stop")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\nScheduler stopped by user")

if __name__ == "__main__":
    main()