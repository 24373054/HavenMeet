#!/usr/bin/env python3
"""
Flux2 Image Generation Tool for OpenClaw.
Generates or edits images using the Flux2 API.
"""

import sys
from pathlib import Path

# Add scripts directory to path
script_dir = Path(__file__).parent / "scripts"
sys.path.insert(0, str(script_dir))

from flux2_generate import main as generate_main
from flux2_edit import main as edit_main


def main():
    if len(sys.argv) < 2:
        print("Usage: flux2_image.py generate|edit [args...]")
        print("\nGenerate (Text-to-Image):")
        print("  flux2_image.py generate --prompt 'description' --filename 'output.png'")
        print("\nEdit (Image-to-Image):")
        print("  flux2_image.py edit --prompt 'edit instructions' --filename 'output.png' -i 'input.png'")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == "generate":
        sys.argv = ["flux2_generate.py"] + sys.argv[2:]
        generate_main()
    elif mode == "edit":
        sys.argv = ["flux2_edit.py"] + sys.argv[2:]
        edit_main()
    else:
        print(f"Unknown mode: {mode}", file=sys.stderr)
        print("Use 'generate' or 'edit'", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
