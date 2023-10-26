import os
import json
import shutil
import argparse
import subprocess
import concurrent.futures

config_file = ""


def clean_workers():
    root_dir = "."
    for dir in os.listdir(root_dir):
        if "TrueWorker" in dir and os.path.isdir(os.path.join(root_dir, dir)):
            complete_dir = os.path.join(root_dir, dir)
            subprocess.run(f"rm -rf {complete_dir}", shell=True, check=True)


def clean():
    root_dir = "."
    for dir in os.listdir(root_dir):
        if "Slayer" in dir and os.path.isdir(os.path.join(root_dir, dir)):
            complete_dir = os.path.join(root_dir, dir)
            subprocess.run(f"rm -rf {complete_dir}", shell=True, check=True)


def create_worker(data: json):
    original = "Slayer07BaseWorker"
    copy = f"Slayer07TrueWorker{data['workerId']}"
    shutil.copytree(original, copy)
    root_dir = "."
    complete_dir = os.path.join(root_dir, copy)

    with open(os.path.join(complete_dir, "src/clientcfg.json"), "w") as json_file:
        json.dump(data, json_file, indent=2)


def read_config_file():
    with open(config_file, "r") as file:
        jdata: json = json.load(file)
        for config in jdata:
            if config["name"] == "worker":
                workercfg = config
                del workercfg["name"]
                create_worker(workercfg)
            else:
                print(f"Unknown config name {config['name']}")


def build_worker(path):
    try:
        print(f"Building worker at {path}")
        subprocess.run(f"cd {path} && npm i && npm run prepare", shell=True, check=True)
    except subprocess.CalledProcessError:
        print("npm build failed")


def build_workers():
    root_dir = "."
    for dir in os.listdir(root_dir):
        if "TrueWorker" in dir and os.path.isdir(os.path.join(root_dir, dir)):
            complete_dir = os.path.join(root_dir, dir)
            build_worker(complete_dir)


def main():
    parser = argparse.ArgumentParser(description="Slayer07 Worker config")

    parser.add_argument("-b", "--build", action="store_true", help="Build flag")

    parser.add_argument("-cfg", "--config", type=str, help="Config file")

    parser.add_argument("-c", "--clean", action="store_true", help="Clean")

    args = parser.parse_args()

    if args.clean:
        clean()

    if args.config:
        clean_workers()
        global config_file
        config_file = args.config
        read_config_file()

    if args.build:
        try:
            build_workers()
        except subprocess.CalledProcessError:
            print("Build failed")


if __name__ == "__main__":
    main()
