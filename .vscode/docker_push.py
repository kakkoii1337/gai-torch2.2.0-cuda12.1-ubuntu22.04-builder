import toml,os,subprocess

base_name="torch2.2.0-cuda12.1-ubuntu22.04-base"

## Update version in pyproject.toml
def __get_version(pyproject_path):
    with open(pyproject_path, "r+") as f:
        data = toml.load(f)
    return data["project"]["version"]

def main():
    here=os.path.dirname(__file__)
    pyproject_path=os.path.join(here,'..','pyproject.toml')

    # Push version from the pyproject.toml file
    version = __get_version(pyproject_path=pyproject_path)
    os.system(f"docker tag {base_name}:{version} kakkoii1337/{base_name}:{version}")
    os.system(f"docker push kakkoii1337/{base_name}:{version}")
    print(f"Pushed image kakkoii1337/{base_name}:{version}")

    # Push latest
    version = "latest"
    os.system(f"docker tag {base_name}:{version} kakkoii1337/{base_name}:{version}")
    os.system(f"docker push kakkoii1337/{base_name}:{version}")
    print(f"Pushed image kakkoii1337/{base_name}:{version}")

if __name__ == "__main__":
    main()
