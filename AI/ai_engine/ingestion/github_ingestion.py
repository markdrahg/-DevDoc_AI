import os
import shutil
import git


class GitHubIngestion:

    def __init__(self, repo_url, clone_dir="workspace/repository"):

        self.repo_url = repo_url
        self.clone_dir = clone_dir

    def clean_workspace(self):

        if os.path.exists(self.clone_dir):
            shutil.rmtree(self.clone_dir)

    def clone_repository(self):

        self.clean_workspace()

        print(f"Cloning repository: {self.repo_url}")

        try:
            git.Repo.clone_from(
                self.repo_url,
                self.clone_dir
            )

            print("Repository cloned successfully")

            return self.clone_dir
            
        except Exception as e:
            print(f"Git clone failed: {e}")
            raise ValueError(f"Failed to clone repository: {self.repo_url}. Check URL and network connection.")