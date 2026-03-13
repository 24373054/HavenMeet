#!/usr/bin/env python3
"""
Edit images using Flux2 API (Image-to-Image).

Usage:
    python flux2_edit.py --prompt "edit instructions" --filename "output.png" -i "input.png"

Examples:
    python flux2_edit.py --prompt "Replace background with sunset beach" --filename "edited.png" -i "photo.jpg"
    python flux2_edit.py -p "Change sky to starry night" -f "night.png" -i "landscape.png"
"""

import argparse
import os
import sys
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


def edit_image(
    api_url: str,
    api_key: str | None,
    input_path: Path,
    prompt: str,
    output_path: Path,
) -> str | None:
    """Edit image using Flux2 API (Image-to-Image)."""
    
    endpoint = urljoin(api_url.rstrip("/"), "/api/edit")
    
    print(f"Editing image: '{prompt[:50]}...'")
    print(f"Input: {input_path}")
    print(f"API URL: {endpoint}")
    
    try:
        # Check if input file exists
        if not input_path.exists():
            print(f"Error: Input file not found: {input_path}", file=sys.stderr)
            return None
        
        # Upload image with prompt
        with open(input_path, "rb") as f:
            files = {
                "image": (input_path.name, f),
            }
            data = {
                "prompt": prompt,
                "accessCode": api_key if api_key else "ptp2025",
            }
            
            # Build headers with API key if provided
            headers = {}
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"
            
            response = requests.post(
                endpoint,
                files=files,
                data=data,
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
            
            # Download the edited image
            print("Downloading edited image...")
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
        print(f"Error editing image: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Edit images using Flux2 API (Image-to-Image)"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Edit instructions"
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output filename (e.g., edited-image.png)"
    )
    parser.add_argument(
        "--input-image",
        required=True,
        metavar="IMAGE",
        help="Input image path to edit"
    )
    parser.add_argument(
        "--api-url", "-u",
        help="Flux2 API URL (overrides FLUX2_API_URL env var)"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Flux2 API key/beta code (overrides FLUX2_API_KEY env var, default: ptp2025)"
    )

    args = parser.parse_args()

    # Get API URL and key
    api_url = get_api_url(args.api_url)
    api_key = get_api_key(args.api_key)
    
    # Set up paths
    input_path = Path(args.input_image)
    output_path = Path(args.filename)
    
    # Edit image
    result = edit_image(
        api_url=api_url,
        api_key=api_key,
        input_path=input_path,
        prompt=args.prompt,
        output_path=output_path,
    )
    
    if result is None:
        sys.exit(1)


if __name__ == "__main__":
    main()
