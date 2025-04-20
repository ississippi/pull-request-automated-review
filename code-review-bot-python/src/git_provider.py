import requests

owner = "ccxt"
repo = "ccxt"
pull_number = 25653  # Replace with the desired PR number
url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}"
diff_url = f"https://github.com/{owner}/{repo}/pull/{pull_number}.diff"

headers = {
    "Accept": "application/vnd.github.v3+json",
    # Optional: Add token for higher rate limits
    # "Authorization": "Bearer YOUR_TOKEN"
}
diff_headers = {
    "Accept": "application/vnd.github.v3.diff",
}

def get_pr_details():
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        pr_data = response.json()
        print("PR Title:", pr_data["title"])
        print("Source Branch:", pr_data["head"]["ref"])
        print("Target Branch:", pr_data["base"]["ref"])
        print("Diff URL:", pr_data["diff_url"])
    else:
        print(f"Error: {response.status_code}, {response.json().get('message')}")

def get_pr_diff():
    response = requests.get(diff_url, headers=diff_headers)
    if response.status_code == 200:
        diff = response.text
        #with open("pr_diff.patch", "w") as f:
        #    f.write(diff)
        #print("Diff saved to pr_diff.patch")
        print(diff)
        return diff
    else:
        print(f"Error: {response.status_code}")

def get_pr_files():
    files_url = f"{url}/files"
    response = requests.get(files_url, headers=headers)
    if response.status_code == 200:
        files_data = response.json()
        for file in files_data:
            print(f"File: {file['filename']}, Changes: {file['changes']}")
    else:
        print(f"Error: {response.status_code}, {response.json().get('message')}")

if __name__ == "__main__":
    get_pr_details()
    get_pr_files()  # Uncomment to fetch and print file changes in the PR
    get_pr_diff()
