import subprocess
import re

def list_and_delete_images(prefix):
    try:
        # List all Docker images
        result = subprocess.run(
            ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"],
            capture_output=True,
            text=True,
            check=True
        )
        # Filter images based on prefix
        pattern = re.compile(f'^{prefix}.*')
        images = result.stdout.split('\n')
        filtered_images = [image for image in images if pattern.match(image)]

        # Delete filtered images
        for image in filtered_images:
            if image:  # Ensure the image string is not empty
                print(f"Deleting image: {image}")
                delete_result = subprocess.run(
                    ["docker", "rmi", "-f", image],
                    capture_output=True,
                    text=True
                )
                if delete_result.stderr:
                    print(f"Error deleting image {image}: {delete_result.stderr}")
                else:
                    print(f"Successfully deleted image {image}")

    except subprocess.CalledProcessError as e:
        print("Failed to execute Docker command:", e)
    except Exception as e:
        print("An error occurred:", e)

# Example usage
image_prefix = "vsc-gai-ttt-svr-"
list_and_delete_images(image_prefix)
