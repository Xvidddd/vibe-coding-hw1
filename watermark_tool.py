#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Image Watermark Tool
Adds timestamp watermark from EXIF data to images
"""

import os
import sys
import argparse
from PIL import Image, ImageDraw, ImageFont, ExifTags
from datetime import datetime
import glob

def get_exif_datetime(image_path):
    """Extract datetime from EXIF data"""
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag = ExifTags.TAGS.get(tag_id, tag_id)
                    if tag == 'DateTime':
                        # Parse datetime: YYYY:MM:DD HH:MM:SS
                        dt_str = value.replace(':', '-', 2)  # Convert to YYYY-MM-DD HH:MM:SS
                        dt_obj = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
                        return dt_obj.strftime('%Y-%m-%d')  # Return only date part
    except Exception as e:
        print(f"Warning: Could not read EXIF data from {image_path}: {e}")
    return None

def get_position_coordinates(img_width, img_height, text_width, text_height, position):
    """Calculate text position coordinates"""
    margin = 20
    
    if position == 'top-left':
        return (margin, margin)
    elif position == 'top-right':
        return (img_width - text_width - margin, margin)
    elif position == 'bottom-left':
        return (margin, img_height - text_height - margin)
    elif position == 'bottom-right':
        return (img_width - text_width - margin, img_height - text_height - margin)
    elif position == 'center':
        return ((img_width - text_width) // 2, (img_height - text_height) // 2)
    else:
        return (margin, margin)  # Default to top-left

def add_watermark(image_path, output_path, font_size=36, color='white', position='bottom-right'):
    """Add watermark to image"""
    try:
        # Get datetime from EXIF
        watermark_text = get_exif_datetime(image_path)
        if not watermark_text:
            watermark_text = 'No-Date'  # Fallback text
        
        # Open image
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            draw = ImageDraw.Draw(img)
            
            # Try to use system font, fallback to default
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("DejaVuSans.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            # Calculate text size
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Get position
            x, y = get_position_coordinates(img.width, img.height, text_width, text_height, position)
            
            # Add text shadow for better visibility
            shadow_color = 'black' if color == 'white' else 'white'
            draw.text((x+2, y+2), watermark_text, font=font, fill=shadow_color)
            
            # Add main text
            draw.text((x, y), watermark_text, font=font, fill=color)
            
            # Save image
            img.save(output_path, quality=95)
            print(f"Success: {image_path} -> {output_path}")
            
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def process_directory(input_dir, font_size=36, color='white', position='bottom-right'):
    """Process all images in directory"""
    # Create output directory
    output_dir = os.path.join(input_dir, f"{os.path.basename(input_dir)}_watermark")
    os.makedirs(output_dir, exist_ok=True)
    
    # Supported image formats
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.webp']
    
    processed_count = 0
    
    for ext in image_extensions:
        pattern = os.path.join(input_dir, ext)
        for image_path in glob.glob(pattern, recursive=False):
            if os.path.isfile(image_path):
                # Create output filename
                filename = os.path.basename(image_path)
                name, ext = os.path.splitext(filename)
                output_filename = f"{name}_watermarked{ext}"
                output_path = os.path.join(output_dir, output_filename)
                
                # Add watermark
                add_watermark(image_path, output_path, font_size, color, position)
                processed_count += 1
    
    if processed_count == 0:
        print("No image files found in the specified directory.")
    else:
        print(f"\nProcessed {processed_count} images. Output saved to: {output_dir}")

def main():
    parser = argparse.ArgumentParser(description='Add timestamp watermark to images from EXIF data')
    parser.add_argument('input_dir', help='Input directory containing images')
    parser.add_argument('--font-size', type=int, default=36, help='Font size for watermark (default: 36)')
    parser.add_argument('--color', default='white', choices=['white', 'black', 'red', 'blue', 'green'], 
                       help='Text color (default: white)')
    parser.add_argument('--position', default='bottom-right', 
                       choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'],
                       help='Watermark position (default: bottom-right)')
    
    args = parser.parse_args()
    
    # Validate input directory
    if not os.path.isdir(args.input_dir):
        print(f"Error: Directory '{args.input_dir}' does not exist.")
        sys.exit(1)
    
    print(f"Processing images in: {args.input_dir}")
    print(f"Settings: Font Size={args.font_size}, Color={args.color}, Position={args.position}")
    print("-" * 50)
    
    process_directory(args.input_dir, args.font_size, args.color, args.position)

if __name__ == "__main__":
    main()