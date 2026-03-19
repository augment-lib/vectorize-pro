# "Design-focused node suite for ComfyUI."
# Copyright 2026 Augment Studio
# Augmentstudio.app

import os
import json
import folder_paths


class AugmentExportSVG:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "svg": ("AUGMENT_SVG",),
                "filename_prefix": ("STRING", {"default": "svg/augment"}),
            },
            "optional": {
                "trigger": ("TRIGGER",),
            },
        }

    RETURN_TYPES = ("TRIGGER")
    RETURN_NAMES = ("trigger")
    FUNCTION = "execute"
    CATEGORY = "Augment/Enhance"
    OUTPUT_NODE = True

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        return True

    def execute(self, svg, filename_prefix="svg/export/asset", trigger=None):
        output_dir = folder_paths.get_output_directory()
        full_output_folder, filename, counter, subfolder, _ = (
            folder_paths.get_save_image_path(filename_prefix, output_dir)
        )

        os.makedirs(full_output_folder, exist_ok=True)

        file = f"{filename}_{counter:05}_.svg"
        filepath = os.path.join(full_output_folder, file)

        if isinstance(svg, bytes):
            svg_data = svg
        elif isinstance(svg, str):
            svg_data = svg.encode("utf-8")
        else:
            svg_data = bytes(svg)

        with open(filepath, "wb") as f:
            f.write(svg_data)

        size = len(svg_data)
        print(f"[Augment] Exported SVG ({size} bytes) to {filepath}")

        json_result = json.dumps({
            "node": "AugmentExportSVG",
            "file": file,
            "subfolder": subfolder,
            "size_bytes": size,
        })

        return {
            "ui": {"images": [{"filename": file, "subfolder": subfolder, "type": "output"}]},
            "result": (json_result, "done"),
        }


NODE_CLASS_MAPPINGS = {
    "AugmentExportSVG": AugmentExportSVG,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "AugmentExportSVG": "Export SVG",
}
