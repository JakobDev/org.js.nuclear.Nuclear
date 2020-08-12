#!/usr/bin/python3.8
import json
import requests
import argparse
import hashlib
import os


def reconstruct(url):
    # opens file with op handler in read mode
    print("downloading nuclear")
    r = requests.get(url, allow_redirects=True)
    open("nuclear.tar.gz", "wb").write(r.content)
    sha256 = hashlib.sha256()
    print("calculating shasum")
    with open("nuclear.tar.gz", "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256.update(byte_block)
        f.close()
    shahash = sha256.hexdigest()
    with open("org.js.nuclear.Nuclear.json") as f:
        print("loading data")
        # loading json as dict
        data = json.load(f)
        # closing the file handler b/c it looks the file
        f.close()
        print("Modifying data")
        # updates the url value. the wierd formating is due to python loading the file
        # using python data types
        data["modules"][0]["sources"][0]["url"] = url
        data["modules"][0]["sources"][0]["sha256"] = shahash
        print("done")
        os.system("rm -rf nuclear.tar.gz")
    # opens file in write mode
    with open("org.js.nuclear.Nuclear.json", "w") as f:
        print("updating json")
        # formates data with some pretty printing
        formated_data = json.dumps(data, indent=4, sort_keys=True)
        # writes data to the file
        f.writelines(formated_data)
        # close file handler b/c best pratices
        f.close()
        print("updating done")


def git_push():
    os.system("git add .")
    os.system("git commit -m 'automated updated'")
    os.system("git push -u origin master")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, help="url to replace.")
    args = parser.parse_args()
    if args != None:
        reconstruct(args.url)
    else:
        print("No arguments give requires Url to continue")


if __name__ == "__main__":
    main()
    print("pushing to github")
    git_push()