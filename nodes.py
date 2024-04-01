import os
import re


class SaveImagePlus:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "folder": ("STRING", {"default": "/tmp/comfyui"}),
                "filename_base": ("STRING", {"default": "all"})
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save"
    CATEGORY = "Jiffies"

    def save(self, image, folder='/tmp/comfyui', filename_base='all'):
        if not os.path.exists(folder):
            os.makedirs(folder)

        # Format for filename with counter and additional info
        filename_format = f"{{:0>4d}}_{filename_base}.png"

        # Get the latest file number in the folder using filename_format
        files = os.listdir(folder)
        pattern = filename_format.replace("{:0>4d}", r"(\d+)")
        filtered_files = [file for file in files if re.match(pattern, file)]
        list.sort(filtered_files, reverse=True)
        if len(filtered_files) > 0:
            latest_number = int(re.match(pattern, filtered_files[0]).group(1))
        else:
            latest_number = -1

        if latest_number >= 999:
            raise ValueError("There is too much content in the current folder.")

        # Generate the filename using the latest file number
        filename = filename_format.format(latest_number + 1)
        file_path = os.path.join(folder, filename)
        if not os.path.exists(file_path):
            image_data = image.get("data", None)
            if image_data:
                with open(file_path, "wb") as f:
                    f.write(image_data)

        return {"ui": {"images": filename}}


NODE_CLASS_MAPPINGS = {
    "SaveImagePlus": SaveImagePlus
}

if __name__ == '__main__':
    s = SaveImagePlus()
    s.save(None, "./motion-01/dwpose")
