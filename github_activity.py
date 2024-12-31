import argparse
import json
import time
import urllib.request
import urllib.error

def fetch_github_activity(username, token=None):
    url = f'https://api.github.com/users/{username}/events'
    headers = {}
    
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            remaining = int(response.getheader('X-RateLimit-Remaining'))
            if remaining == 0:
                reset_time = int(response.getheader('X-RateLimit-Reset'))
                wait_time = reset_time - time.time()
                if wait_time > 0:
                    print(f"Rate limit reached. Retrying in {int(wait_time)} seconds...")
                    time.sleep(wait_time)

                return fetch_github_activity(username, token)

            data = json.loads(response.read())

        activities = []
        for event in data:
            if event['type'] == 'PushEvent':
                repo_name = event['repo']['name']
                commits = len(event['payload']['commits'])
                activities.append(f"Pushed {commits} commit{'s' if commits > 1 else ''} to {repo_name}")
            elif event['type'] == 'IssuesEvent' and event['payload']['action'] == 'opened':
                repo_name = event['repo']['name']
                activities.append(f"Opened a new issue in {repo_name}")
            elif event['type'] == 'WatchEvent' and event['payload']['action'] == 'star':
                repo_name = event['repo']['name']
                activities.append(f"Starred {repo_name}")
            elif event['type'] == 'PullRequestEvent' and event['payload']['action'] == 'opened':
                repo_name = event['repo']['name']
                activities.append(f"Opened a new pull request in {repo_name}")
            elif event['type'] == 'ForkEvent':
                repo_name = event['repo']['name']
                activities.append(f"Forked the repository {repo_name}")
        
        return activities
    
    except urllib.error.URLError as e:
        print(f"Error: Could not fetch data for user '{username}'. {e}")
        return []
    except Exception as e:
        print(f"Error: An unexpected error occurred. {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Fetch recent GitHub activity for a user.')
    parser.add_argument('username', type=str, help='GitHub username to fetch activity for.')
    parser.add_argument('--token', type=str, help='GitHub token for authentication (optional).')
    
    args = parser.parse_args()
    
    activities = fetch_github_activity(args.username, args.token)
    
    if activities:
        print(f"Recent activity for GitHub user '{args.username}':")
        for activity in activities:
            print(f"- {activity}")
    else:
        print(f"No activity found for GitHub user '{args.username}'.")

if __name__ == '__main__':
    main()
