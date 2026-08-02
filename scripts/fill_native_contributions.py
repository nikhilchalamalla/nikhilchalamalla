import os
import subprocess
from datetime import datetime, timedelta

def fill_contributions_calendar(days=365):
    print(f"Generating backdated commits for the past {days} days...")
    today = datetime.now()
    start_date = today - timedelta(days=days)
    
    # We will generate 2 to 4 empty commits for every single day
    total_commits = 0
    
    for i in range(days + 1):
        target_date = start_date + timedelta(days=i)
        date_iso = target_date.strftime("%Y-%m-%dT12:00:00")
        
        # 2 commits per day to ensure solid green levels
        for c in range(2):
            env = dict(os.environ)
            env["GIT_AUTHOR_DATE"] = date_iso
            env["GIT_COMMITTER_DATE"] = date_iso
            
            cmd = ["git", "commit", "--allow-empty", "-m", f"chore: activity commit for {target_date.strftime('%Y-%m-%d')}"]
            res = subprocess.run(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res.returncode == 0:
                total_commits += 1

    print(f"Successfully generated {total_commits} backdated commits across {days} days!")

if __name__ == "__main__":
    fill_contributions_calendar(365)
