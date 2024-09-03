import json
import os
import subprocess

def load_and_clean_json(file_path):
    cleaned_lines = []
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                # Strip leading and trailing whitespace to ensure detection of line comments
                stripped_line = line.strip()
                # Check if the line starts with // and ignore it if true
                if not stripped_line.startswith("//"):
                    cleaned_lines.append(line)
        # Join cleaned lines and load as JSON
        cleaned_json = json.loads(''.join(cleaned_lines))
        return cleaned_json
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def find_image_name_starts_with(startswith):
    try:
        # Execute the command to get a list of all Docker images
        result = subprocess.run(
            ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"],
            capture_output=True,
            text=True,
            check=True
        )
        # Split the output by new lines to get each image name
        all_images = result.stdout.strip().split('\n')
        
        # Filter images whose names start with the specified prefix
        filtered_images = [image for image in all_images if image.startswith(startswith)]
        
        return filtered_images
    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocess
        print("Failed to list Docker images:", e)
    except Exception as e:
        # Handle other possible errors
        print("An error occurred:", e)

def find_containers(image):
    try:
        # Execute the command to get a list of all Docker containers
        result = subprocess.run(
            ["docker", "ps", "-a", "--format", "{{.ID}},{{.Image}},{{.Names}}"],
            capture_output=True,
            text=True,
            check=True
        )
        # Split the output by new lines to get each container entry
        all_containers = result.stdout.strip().split('\n')
        
        # Filter containers that are created from the specified image
        filtered_containers=[]
        for container in all_containers:
            container_id=container.split(",")[0]
            container_image=container.split(",")[1]
            if container_image.startswith(image):
                filtered_containers.append(container_id)

        return filtered_containers
    except subprocess.CalledProcessError as e:
        # Handle errors in the subprocess, e.g., docker command not found or executed incorrectly
        print("Failed to list Docker containers:", e)
        return []
    except Exception as e:
        # Handle other possible errors, e.g., decoding issues, unexpected output formats
        print("An error occurred:", e)
        return []

def find_volume(container):
    try:
        # Execute the Docker inspect command to get detailed information about the container
        result = subprocess.run(
            ["docker", "inspect", container],
            capture_output=True,
            text=True,
            check=True
        )
        # Load the output as JSON, which returns a list where each element is details about one container
        container_info = json.loads(result.stdout)

        # Check if the container has mounted volumes and extract their IDs
        volume_ids = []
        if container_info and 'Mounts' in container_info[0]:
            for mount in container_info[0]['Mounts']:
                if mount['Type'] == 'volume':
                    print("mount:")
                    print(mount)
                    volume_ids.append(mount['Name'])  # Append the volume ID (Name in this context)

        return volume_ids
    except subprocess.CalledProcessError as e:
        # Handle errors from the subprocess, like if the docker command fails or the container doesn't exist
        print("Failed to inspect the container:", e)
        return []
    except json.JSONDecodeError as e:
        # Handle errors if the output is not valid JSON
        print("Failed to decode JSON from Docker inspect output:", e)
        return []
    except Exception as e:
        # Handle any other exceptions
        print("An error occurred:", e)
        return []

def main():
    # Load .devcontainer.json
    here = os.path.dirname(__file__)
    file = os.path.abspath(os.path.join(here,"../.devcontainer/devcontainer.json"))
    jsoned=load_and_clean_json(file)
    # Get name
    matches=find_image_name_starts_with(f"vsc-{jsoned['name']}")
    for match in matches:
        match = match.split(":")[0]
        containers=find_containers(match)
        print(containers)
        for container in containers:
            volume=find_volume(container)
            print(volume)

main()


