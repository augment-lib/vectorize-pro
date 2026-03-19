"""
Augment - Vectorize Pro
"""

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
_failed = []

# ── Flow Control ──
try:
    from .trigger import GateNode, make_wait_node, WAIT_TYPES
    NODE_CLASS_MAPPINGS["GateNode"] = GateNode
    NODE_DISPLAY_NAME_MAPPINGS["GateNode"] = "Trigger"
    for _name, _type_str in WAIT_TYPES.items():
        _cls_name = f"AugmentWait{_name}"
        try:
            NODE_CLASS_MAPPINGS[_cls_name] = make_wait_node(_name, _type_str)
            NODE_DISPLAY_NAME_MAPPINGS[_cls_name] = f"{_name} (Improved)"
        except Exception as e:
            _failed.append((_cls_name, e))
            print(f"[augment-vectorize] ⚠ {_cls_name} unavailable: {e}")
except Exception as e:
    _failed.append(("Wait nodes", e))
    print(f"[augment-vectorize] ⚠ Flow control nodes unavailable: {e}")

# ── PNG to SVG Pro (Paid) ──
try:
    from .png_to_svg_pro import AugmentPNGToSVGPro
    NODE_CLASS_MAPPINGS["AugmentPNGToSVGPro"] = AugmentPNGToSVGPro
    NODE_DISPLAY_NAME_MAPPINGS["AugmentPNGToSVGPro"] = "Vectorize Pro"
except Exception as e:
    _failed.append(("AugmentPNGToSVGPro", e))
    print(f"[augment-vectorize] ⚠ AugmentPNGToSVGPro unavailable: {e}")

# ── Summary ──
WEB_DIRECTORY = "./web/js"
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

if _failed:
    print(f"[augment-vectorize] ✓ Registered {len(NODE_CLASS_MAPPINGS)} nodes ({len(_failed)} failed)")
    for node_id, err in _failed:
        print(f"[augment-vectorize]   ✗ {node_id}: {err}")
else:
    print(f"[augment-vectorize] ✓ Registered {len(NODE_CLASS_MAPPINGS)} nodes")
