import requests
import re
import urllib.parse
import argparse

token = ""
pattern = '(?<="full_name":")([^"]+)'

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"
}

def request_api(query):
    results = []
    i = 1
    while True:
        url = f"https://api.github.com/search/code?q={urllib.parse.quote(query)}&per_page=100&page={i}"
        r = requests.get(url, headers=headers)
        content = re.findall(pattern, r.text)
        results.extend(content)
        i+=1
        if len(content) != 100:
            break
    return [*set(results)]


def output(filename, content):
    with open(filename, "w") as f:
        f.write(str(content))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-q','--query', help='Query', required=True)
    parser.add_argument('-f','--filename', help='filename', required=True)

    args = parser.parse_args()
    query = args.query
    filename = args.filename

    results = request_api(query)
    output(filename, results)
