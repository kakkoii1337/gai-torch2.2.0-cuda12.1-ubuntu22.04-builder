import toml,os,subprocess,argparse
from rich import console
console = console.Console()

from gai.scripts._docker_utils import _docker_build,_docker_push


# def _cmd(cmd):
#     try:
#         subprocess.run(cmd, shell=True, check=True)
#     except subprocess.CalledProcessError as e:
#         print("Error: ", e)
#         return

# ## Update version in pyproject.toml
# def _update_version(pyproject_path): 
#     with open(pyproject_path, "r+") as f:
#         data = toml.load(f)
#         # Extract and update the version number
#         version_parts = data["project"]["version"].split(".")
#         version_parts[-1] = str(int(version_parts[-1]) + 1)  # Increment the patch version
#         data["project"]["version"] = ".".join(version_parts)

#         # Write the updated data back to pyproject.toml
#         f.seek(0)
#         f.write(toml.dumps(data))
#         f.truncate()  # Ensure file is truncated if new data is shorter

#         return data["project"]["version"]

# def _docker_image_exists(image_name):
#     try:
#         # Execute docker images to list all images
#         result = subprocess.run(
#             ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"],
#             capture_output=True,
#             text=True,
#             check=True
#         )
#         # Check if the specified image name is in the output
#         return image_name in result.stdout.split('\n')
#     except subprocess.CalledProcessError:
#         # If there is an error executing docker images, assume the image does not exist
#         return False  

# def _get_version(pyproject_path):
#     data = toml.load(pyproject_path)
#     if data.get("project",None):
#         version = data['project']['version']
#     else:
#         version = data["tool"]["poetry"]['version']
#     return version

# def _docker_push(
#         pyproject_path,
#         repo_name, 
#         image_name, 
#         ):
#     version = _get_version(pyproject_path)
#     versioned_image=f"{repo_name}/{image_name}:{version}"
#     _cmd(f"docker push {versioned_image}")
#     console.print(f"""[green bold]Push {versioned_image} Done[/]""")
#     latest_image=f"{repo_name}/{image_name}:latest"
#     _cmd(f"docker push {latest_image}")
#     console.print(f"""[green bold]Push {latest_image} Done[/]""")

# def _docker_build(
#     pyproject_path,
#     repo_name,
#     image_name,                
#     dockerfile_path, 
#     dockercontext_path, 
#     no_cache):

#     here=os.path.dirname(__file__)

#     # initialize project path
#     if not pyproject_path:
#         console.print(f"[red]pyproject_path cannot be empty.[/]")
#         return
#     pyproject_path = os.path.abspath(os.path.join(here,pyproject_path))
#     if not pyproject_path.endswith('pyproject.toml'):
#         console.print(f"[red]{pyproject_path}[/] does not end with 'pyproject.toml'")
#         return
#     if not os.path.exists(pyproject_path):
#         console.print(f"[red]{pyproject_path}[/] does not exist.")
#         return
#     console.print(f"[yellow]{pyproject_path}[/] exists")

#     # Initialize image_name
#     if not image_name:
#         # extract image_name from pyproject name if image_name is not provided
#         with open(pyproject_path,"r+") as f:
#             data = toml.load(f)
#             image_name = data["project"]["name"]
       
#     # initialize dockerfile path
#     if not dockerfile_path:
#         # If dockerfile_path is not provided, we will assume it is a Dockerfile and resides in the same directory as pyproject.toml
#         dockerfile_path = f"{dockercontext_path}/Dockerfile"
#     else:
#         dockerfile_path = os.path.abspath(os.path.join(here,dockerfile_path))
#     if not os.path.exists(dockerfile_path):
#         console.print(f"[red]{dockerfile_path}[/] does not exist.")
#         return
#     console.print(f"[yellow]{dockerfile_path}[/] exists")

#     # initialize docker context path
#     if not dockercontext_path:
#         # If dockercontext_path is not provided, we will assume it is the same directory as Dockerfile
#         dockercontext_path = os.path.dirname(dockerfile_path)
#     else:
#         dockercontext_path = os.path.abspath(os.path.join(here,dockercontext_path))
#     console.print(f"""[white]projectfile: {pyproject_path}[/]""")        
#     console.print(f"""[white]dockerfile: {dockerfile_path}[/]""")
#     console.print(f"""[white]context: {dockercontext_path}[/]""")

#     # Extract and update version from pyproject.toml
#     version = _update_version(pyproject_path)
#     versioned_image=f"{repo_name}/{image_name}:{version}"      
#     console.print(f"""[yellow]**Build {versioned_image}**[/]""")

#     # Build
#     if no_cache:
#         console.print(f"""[blue]--no-cache[/]""")
#     if _docker_image_exists(versioned_image):
#         console.print(f"""[white]Removing existing {versioned_image}[/]""")
#         _cmd(f"""docker rmi -f {versioned_image}""")
#     cmd=f"""docker buildx build """ + ("""--no-cache""" if no_cache else "") + f""" \
#         --progress=plain \
#         -f {dockerfile_path} \
#         -t {versioned_image} \
#         {dockercontext_path}"""
#     print(f"Building image: {cmd}")
#     _cmd(cmd)

#     latest_image=f"{repo_name}/{image_name}:latest"
#     if _docker_image_exists(latest_image):
#         _cmd(f"docker rmi {latest_image}")
#     _cmd(f"docker tag {versioned_image} {latest_image}")
    
#     console.print(f"""[green bold]Build {image_name}:{version} Done[/]""")

def _parse_arguments():
    parser = argparse.ArgumentParser(description="Build Docker images with updated version number.")
    parser.add_argument("task", choices=["build", "push"], help="Task to perform: build or push.")
    parser.add_argument("pyproject_path",help="path of pyproject.toml")
    parser.add_argument("--repo_name", default="kakkoii1337", help="Repository name for Docker image.")
    parser.add_argument("--image_name", help="Base name for Docker image, which is required.")
    parser.add_argument("--dockerfile_path", default="./Dockerfile", help="Path to the Dockerfile used for building the image.")
    parser.add_argument("--dockercontext_path", default="..", help="Path to the Dockerfile used for building the image.")
    parser.add_argument("--no-cache", action="store_true", help="Do not use cache when building the image.")
    return parser.parse_args()

"""
Example: 
- python .vscode/docker_tools.py build my_image --repo_name kakkoii1337 --docker_file ./Dockerfile
- python .vscode/docker_tools.py push my_image --repo_name kakkoii1337 --docker_file ./Dockerfile

"""
def main():
    args = _parse_arguments()

    if args.task == "build":
        # build (pyproject_path) [repo_name="kakkoii1337"] [image_name=None] [dockerfile_path"../Dockerfile"] [dockercontext_path=".."] [no_cache=False]
        _docker_build(
            pyproject_path=args.pyproject_path,
            repo_name=args.repo_name,
            image_name=args.image_name,
            dockerfile_path=args.dockerfile_path,
            dockercontext_path=args.dockercontext_path,
            no_cache=args.no_cache
        )
    elif args.task == "push":
        _docker_push(
            pyproject_path=args.pyproject_path,
            repo_name=args.repo_name,
            image_name=args.image_name,
        )
    else:
        console.print(f"[red]Invalid task: {args.task}[/]")

if __name__ == "__main__":
    main()