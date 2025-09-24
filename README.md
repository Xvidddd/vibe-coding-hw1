# vibe-coding-hw1
Photo Watermark 1
=======
# Image Watermark Tool

A Python command-line tool that adds timestamp watermarks to images using EXIF data.

## Features

- Extracts shooting date from EXIF metadata
- Supports multiple image formats (JPEG, PNG, BMP, TIFF, WebP)
- Customizable font size, color, and position
- Avoids Chinese characters to prevent encoding issues
- Automatically creates watermark directory

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python watermark_tool.py /path/to/images
```

With custom options:
```bash
python watermark_tool.py /path/to/images --font-size 48 --color black --position top-left
```

## Options

- `--font-size`: Font size for watermark text (default: 36)
- `--color`: Text color - white, black, red, blue, green (default: white)
- `--position`: Watermark position - top-left, top-right, bottom-left, bottom-right, center (default: bottom-right)

## Output

Processed images are saved in a new directory named `original_directory_watermark` within the input directory.

## Supported Image Formats

- JPEG/JPG
- PNG
- BMP
- TIFF
- WebP
