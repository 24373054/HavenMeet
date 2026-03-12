---
name: flux2-image-gen
description: Generate or edit images using your own Flux2 API server.
homepage: https://ptp.matrixlabs.cn
metadata:
  {
    "openclaw":
      {
        "emoji": "🎨",
        "requires": { "bins": [] },
        "primaryEnv": "FLUX2_API_URL",
        "install": [],
      },
  }
---

# Flux2 Image Generation

Use your own Flux2 API server to generate or edit images.

**API Base URL**: `https://ptp.matrixlabs.cn` (Public) / `http://140.143.183.163:38024` (Internal)

## Generate (Text-to-Image)

```bash
{baseDir}/scripts/flux2_generate.py --prompt "your image description" --filename "output.png" [--width 1024] [--height 1024]
```

## Edit (Image-to-Image)

```bash
{baseDir}/scripts/flux2_edit.py --prompt "edit instructions" --filename "output.png" -i "/path/to/input.png"
```

## Configuration

- `FLUX2_API_URL` env var (optional, defaults to `https://ptp.matrixlabs.cn`)
- Or set `skills."flux2-image-gen".env.FLUX2_API_URL` in `~/.openclaw/openclaw.json`

## Parameters

### Text-to-Image Generation
- `--prompt` / `-p`: Image description (required)
- `--filename` / `-f`: Output filename (required)
- `--width` / `-w`: Image width in pixels (256-2048, default: 1024)
- `--height`: Image height in pixels (256-2048, default: 1024)
- `--steps` / `-s`: Number of diffusion steps (1-50, default: 4)
- `--cfg` / `-c`: CFG scale (default: 1.0)

### Image-to-Image Editing
- `--prompt` / `-p`: Edit instructions (required)
- `--filename` / `-f`: Output filename (required)
- `--input-image`: Input image path (required)

## Notes

- Model: Flux2 Klein 9B FP8
- Processing time: 5-30 seconds
- The script prints a `MEDIA:` line for OpenClaw to auto-attach on supported chat providers
- Use timestamps in filenames: `yyyy-mm-dd-hh-mm-ss-name.png`
- Recommended resolution: 1024x1024 or 1024x1408 (portrait)