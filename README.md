# GithubActivityTracker
A simple command-line tool to fetch and display a GitHub user's recent activity, such as commits, issues, stars, pull requests, and forks. The tool interacts with the GitHub API to retrieve user events and display them in the terminal.
Features:
Fetches recent activity for a specified GitHub user.
Supports various event types like pushes, issues, stars, pull requests, and forks.
Handles rate limiting and supports GitHub authentication to bypass limits.
Easy-to-use CLI interface.
Usage:

python github_activity.py <username>


For authentication (optional):
python github_activity.py <username> --token <your_github_token>

https://roadmap.sh/projects/github-user-activity
