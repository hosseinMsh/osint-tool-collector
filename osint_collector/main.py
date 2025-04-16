import os
import requests
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("📍 Project Root Directory:", BASE_DIR)

# List of GitHub repositories to extract OSINT tools from
REPOS = [
    {
        "url": "https://github.com/jivoi/awesome-osint",
        "name": "jivoi/awesome-osint",
        "custom_function": "extract_default"
    },
    {
        "url": "https://github.com/Astrosp/Awesome-OSINT-For-Everything",
        "name": "Astrosp/Awesome-OSINT-For-Everything",
        "custom_function": "extract_default"
    },
    {
        "url": "https://github.com/tracelabs/awesome-osint",
        "name": "tracelabs/awesome-osint",
        "custom_function": "extract_default"
    },
    {
        "url": "https://github.com/lockfale/awesome-web-security",
        "name": "lockfale/awesome-web-security",
        "custom_function": "extract_default"
    },
    {
        "url": "https://github.com/obsidianmd/awesome-cyber-security",
        "name": "obsidianmd/awesome-cyber-security",
        "custom_function": "extract_default"
    },
    {
        "url": "https://github.com/danielmiessler/SecLists",
        "name": "danielmiessler/SecLists",
        "custom_function": "extract_default"
    },
    {
        "url": "https://github.com/PhantomEuphoria/awesome-osint-tools",
        "name": "PhantomEuphoria/awesome-osint-tools",
        "custom_function": "extract_default"
    },
    {
        "url": "https://github.com/tiagoad/awesome-social-engineering",
        "name": "tiagoad/awesome-social-engineering",
        "custom_function": "extract_default"
    },
    {
        "url": "https://github.com/infosecguru/awesome-internet-of-things",
        "name": "infosecguru/awesome-internet-of-things",
        "custom_function": "extract_default"
    },
    {
        "url": "https://github.com/felko/awesome-osint-tools",
        "name": "felko/awesome-osint-tools",
        "custom_function": "extract_default"
    },
    {
        "url": "https://github.com/pgaref/awesome-privacy",
        "name": "pgaref/awesome-privacy",
        "custom_function": "extract_default"
    },
    {
        "url": "https://github.com/SigNoz/awesome-appsec",
        "name": "SigNoz/awesome-appsec",
        "custom_function": "extract_default"
    },
    {
        "url": "https://github.com/GrayHatWASP/awesome-open-source-cybersecurity-tools",
        "name": "GrayHatWASP/awesome-open-source-cybersecurity-tools",
        "custom_function": "extract_default"
    },
    {
        "url": "https://github.com/vitalysim/Awesome-Hacking-Resources",
        "name": "vitalysim/Awesome-Hacking-Resources",
        "custom_function": "extract_default"
    }
]

def get_updated_repo_url(old_url):
    """
    Check if the repo has been moved or renamed using GitHub API.
    If moved, return the new URL.
    """
    response = requests.get(old_url, allow_redirects=True)

    if response.history:
        print("🚚 The repository has been moved.")
        print("Redirect history:", [resp.url for resp in response.history])
        print("New repository URL:", response.url)
        return response.url
    else:
        print("📍 The repository is at the original URL.")
        return old_url

def get_readme_content(url):
    """
    Tries to fetch the README content using both 'master' and 'main' branches.
    """
    base_url = url.replace("github.com", "raw.githubusercontent.com").replace("/tree/", "/")

    for branch in ["master", "main"]:
        raw_url = base_url + f"/{branch}/README.md"
        response = requests.get(raw_url)

        if response.status_code == 200:
            return response.text

    print(f"❌ Failed to read README: {url}")
    return None


def extract_default(url):
    # First, try to get the readme content
    readme = get_readme_content(url)

    # If failed to fetch README, try to get updated repo info using GitHub API
    if not readme:
        print(f"❌ Trying to fetch updated repo info from GitHub API for: {url}")

        # Use the GitHub API to check if the repo has been moved or renamed
        updated_url = get_updated_repo_url(url)

        # Try to fetch the README content again from the updated URL
        readme = get_readme_content(updated_url)
        if not readme:
            print(f"🚫 Still failed to fetch README for updated repo: {updated_url}")
            return []

        # Update the URL for logging purposes
        url = updated_url

    # Now, parse the README and extract tools
    lines = readme.splitlines()
    tools = []

    for line in lines:
        if "](" in line and "http" in line:
            try:
                name = line.split("[")[1].split("]")[0].strip()
                link = line.split("](")[1].split(")")[0].strip()
                desc = line.split(" - ")[1].strip() if " - " in line else ""

                tools.append({
                    "name": name,
                    "url": link,
                    "description": desc,
                    "source_repo": url
                })
            except Exception:
                continue
    return tools


def main():
    all_tools = []

    for repo in REPOS:
        print(f"🔍 Collecting tools from: {repo['url']}")
        custom_function = globals().get(repo["custom_function"])
        if custom_function:
            tools = custom_function(repo["url"])
            print(f"  ➜ {len(tools)} tools found.")
            all_tools += tools

    print(f"\n✅ Total tools collected: {len(all_tools)}")

    if not os.path.exists(BASE_DIR + "/data"):
        os.makedirs(BASE_DIR + "/data")

    # Save the tools to a JSON file
    try:
        with open(BASE_DIR + "/data/tools.json", "w", encoding="utf-8") as f:
            json.dump(all_tools, f, indent=2, ensure_ascii=False)
        print("✅ Tools saved to data/tools.json")
    except Exception as e:
        print(f"❌ Failed to save file: {e}")


if __name__ == "__main__":
    main()
