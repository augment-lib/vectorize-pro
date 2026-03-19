# "Design-focused node suite for ComfyUI."
# Copyright 2026 Augment Studio
# Paid Node, credit values may change.
# Augmentstudio.app

import io
import json
import requests
import time
import numpy as np
from PIL import Image


NODE_ID = "png_to_svg_pro"
API_URL = "https://augmentstudio.app/api"


class AugmentPNGToSVGPro:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "api_key": ("STRING", {"default": ""}),
                "image": ("IMAGE",),
            },
            "optional": {
                "trigger": ("TRIGGER",),
            },
        }

    RETURN_TYPES = ("AUGMENT_SVG", "AUGMENT_JSON", "TRIGGER")
    RETURN_NAMES = ("svg", "json_result", "trigger")
    FUNCTION = "execute"
    CATEGORY = "Augment/Enhance"
    OUTPUT_NODE = True

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return time.time()

    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        return True

    def execute(self, api_key, image, trigger=None):
        api_url = API_URL.rstrip("/")
        auth = {"Authorization": f"Bearer {api_key}"}

        img_np = (image[0].cpu().numpy() * 255).astype(np.uint8)
        pil_img = Image.fromarray(img_np, "RGB")
        buf = io.BytesIO()
        pil_img.save(buf, format="PNG")
        img_bytes = buf.getvalue()

        print(f"[Augment API] PNG to SVG Pro: submitting {img_np.shape[1]}x{img_np.shape[0]} image ({len(img_bytes)} bytes)")
        try:
            r = requests.post(
                f"{api_url}/process",
                files={"image": ("image_input.png", img_bytes, "image/png")},
                data={"node_id": NODE_ID},
                headers=auth,
                timeout=30,
            )
        except requests.exceptions.RequestException as e:
            print(f"[Augment API] Submit failed: {e}")
            raise

        if r.status_code != 200:
            raise RuntimeError(f"Submit error {r.status_code}: {r.text[:500]}")

        request_id = r.json().get("request_id")
        if not request_id:
            raise RuntimeError(f"No request_id: {r.text[:500]}")

        print(f"[Augment API] Job submitted: {request_id}")

        max_wait = 60
        elapsed = 0
        job_status = "unknown"

        while elapsed < max_wait:
            time.sleep(1)
            elapsed += 1
            try:
                status_r = requests.get(
                    f"{api_url}/job/{request_id}/status",
                    headers=auth, timeout=10,
                )
                job_status = status_r.json().get("status", "unknown")
            except Exception as e:
                print(f"[Augment API] Poll error: {e}")
                continue

            if job_status == "done":
                break
            elif job_status == "error":
                raise RuntimeError(f"Job failed: {status_r.json().get('error')}")

        if job_status != "done":
            raise RuntimeError(f"Timed out after {max_wait}s")

        svg_r = requests.get(
            f"{api_url}/job/{request_id}/image",
            headers=auth, timeout=60,
        )
        if svg_r.status_code != 200:
            raise RuntimeError(f"SVG fetch error: {svg_r.status_code}")

        svg_content = svg_r.content
        size = len(svg_content)
        print(f"[Augment API] Done! Received SVG ({size} bytes)")

        json_result = json.dumps({"node": "PNGToSVGPro", "size_bytes": size})
        return {"ui": {"text": [svg_r.text[:500]]}, "result": (svg_content, json_result, "done")}


NODE_CLASS_MAPPINGS = {
    "AugmentPNGToSVGPro": AugmentPNGToSVGPro,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "AugmentPNGToSVGPro": "PNG to SVG Pro",
}
