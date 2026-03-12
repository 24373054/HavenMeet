#!/usr/bin/env python3
"""
Generate images using Flux2 API (Text-to-Image).

Usage:
    python flux2_generate.py --prompt "your image description" --filename "output.png" [--width 1024] [--height 1024]

Examples:
    python flux2_generate.py --prompt "A vintage motorcycle at sunset" --filename "motorcycle.png"
    python flux2_generate.py -p "Cyberpunk cityscape" -f "city.png" -w 1024 -h 1408
"""

import argparse
import os
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import requests


def get_api_url(provided_url: str | None) -> str:
    """Get API URL from argument or environment."""
    if provided_url:
        return provided_url
    return os.environ.get("FLUX2_API_URL", "https://ptp.matrixlabs.cn")


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument or environment."""
    if provided_key:
        return provided_key
    return os.environ.get("FLUX2_API_KEY", "ptp2025")  # Default beta code


def generate_image(
    api_url: str,
    api_key: str | None,
    prompt: str,
    output_path: Path,
    width: int = 1024,
    height: int = 1024,
    steps: int = 4,
    cfg: float = 1.0,
) -> str | None:
    """Generate image from text prompt using Flux2 API."""
    
    endpoint = urljoin(api_url.rstrip("/"), "/api/generate")
    
    payload = {
        "prompt": prompt,
        "width": width,
        "height": height,
        "steps": steps,
        "cfg": cfg,
        "accessCode": api_key,
    }
    
    print(f"Generating image: '{prompt[:50]}...'")
    print(f"Resolution: {width}x{height}, Steps: {steps}, CFG: {cfg}")
    print(f"API URL: {endpoint}")
    
    # Build headers with API key if provided
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    
    try:
        response = requests.post(
            endpoint,
            json=payload,
            headers=headers,
            timeout=300,  # 5 minutes timeout
        )
        response.raise_for_status()
        result = response.json()
        
        if not result.get("success"):
            print(f"Error: {result.get('error', 'Unknown error')}", file=sys.stderr)
            return None
        
        image_path = result["image"]
        full_image_url = urljoin(api_url, image_path.lstrip("/"))
        
        # Download the generated image
        print("Downloading generated image...")
        image_response = requests.get(full_image_url, timeout=60)
        image_response.raise_for_status()
        
        # Save to local file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(image_response.content)
        
        full_path = output_path.resolve()
        print(f"\nImage saved: {full_path}")
        print(f"MEDIA:{full_path}")
        
        return str(full_path)
        
    except requests.RequestException as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Flux2 API (Text-to-Image)"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description/prompt"
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output filename (e.g., sunset-mountains.png)"
    )
    parser.add_argument(
        "--width", "-w",
        type=int,
        default=1024,
        help="Image width in pixels (256-2048, default: 1024)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=1024,
        help="Image height in pixels (256-2048, default: 1024)"
    )
    parser.add_argument(
        "--steps", "-s",
        type=int,
        default=4,
        help="Number of diffusion steps (1-50, default: 4)"
    )
    parser.add_argument(
        "--cfg", "-c",
        type=float,
        default=1.0,
        help="CFG scale (default: 1.0)"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Flux2 API key/beta code (overrides FLUX2_API_KEY env var, default: ptp2025)"
    )

    args = parser.parse_args()

    # Validate parameters
    if not (256 <= args.width <= 2048):
        print("Error: Width must be between 256 and 2048", file=sys.stderr)
        sys.exit(1)
    
    if not (256 <= args.height <= 2048):
        print("Error: Height must be between 256 and 2048", file=sys.stderr)
        sys.exit(1)
    
    if not (1 <= args.steps <= 50):
        print("Error: Steps must be between 1 and 50", file=sys.stderr)
        sys.exit(1)

    # Get API URL and key
    api_url = get_api_url(os.environ.get("FLUX2_API_URL"))
    api_key = get_api_key(args.api_key)
    
    # Set up output path
    output_path = Path(args.filename)
    
    # Generate image
    result = generate_image(
        api_url=api_url,
        api_key=api_key,
        prompt=args.prompt,
        output_path=output_path,
        width=args.width,
        height=args.height,
        steps=args.steps,
        cfg=args.cfg,
    )
    
    if result is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
