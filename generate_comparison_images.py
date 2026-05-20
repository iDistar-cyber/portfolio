import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

def create_images():
    width = 1200
    height = 675
    center_x = width // 2
    center_y = height // 2

    # Colors
    bg_color = (10, 11, 14)       # Deep dark theme background #0a0b0e
    grid_color = (25, 27, 34)     # Subtle CAD technical grid lines
    cyan = (0, 229, 255)          # Cyan for anchor handles / nodes
    lime = (204, 255, 0)          # Cyber Lime accent
    dark_gray = (50, 52, 60)      # Inactive paths
    
    # -------------------------------------------------------------
    # 1. DRAWING THE BASE SHAPES (Reusable calculation)
    # -------------------------------------------------------------
    def get_gear_points(cx, cy, r_in, r_out, num_teeth):
        points = []
        angle_step = 2 * math.pi / num_teeth
        for i in range(num_teeth):
            angle = i * angle_step
            # For each tooth, we have 4 states of transition
            a1 = angle
            a2 = angle + angle_step * 0.3
            a3 = angle + angle_step * 0.5
            a4 = angle + angle_step * 0.8
            
            # Inner radius point
            points.append((cx + r_in * math.cos(a1), cy + r_in * math.sin(a1)))
            # Outer radius points (tooth start and end)
            points.append((cx + r_out * math.cos(a2), cy + r_out * math.sin(a2)))
            points.append((cx + r_out * math.cos(a3), cy + r_out * math.sin(a3)))
            # Inner radius point
            points.append((cx + r_in * math.cos(a4), cy + r_in * math.sin(a4)))
        return points

    def get_inner_star_points(cx, cy, r_in, r_out, num_rays):
        points = []
        angle_step = math.pi / num_rays
        for i in range(num_rays * 2):
            angle = i * angle_step
            r = r_out if i % 2 == 0 else r_in
            points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        return points

    # -------------------------------------------------------------
    # 2. GENERATING "AFTER.PNG" (Crisp, High-Tech Vector Design)
    # -------------------------------------------------------------
    img_after = Image.new("RGBA", (width, height), bg_color)
    draw_after = ImageDraw.Draw(img_after)

    # Draw CAD Grid
    grid_size = 40
    for x in range(0, width, grid_size):
        draw_after.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, grid_size):
        draw_after.line([(0, y), (width, y)], fill=grid_color, width=1)
        
    # Draw nice technical target circles in background
    for r in [280, 240, 90]:
        draw_after.ellipse(
            [center_x - r, center_y - r, center_x + r, center_y + r], 
            outline=(35, 38, 48), 
            width=1
        )

    # Get Gear vertices
    gear_pts = get_gear_points(center_x, center_y, 160, 200, 10)
    
    # Draw gear vector outline (lime)
    draw_after.polygon(gear_pts, outline=lime, width=3)
    
    # Draw secondary gear outline (slightly offset/inset dark outline)
    draw_after.ellipse(
        [center_x - 130, center_y - 130, center_x + 130, center_y + 130], 
        outline=lime, 
        width=2
    )

    # Draw inner star/wing shape
    star_pts = get_inner_star_points(center_x, center_y, 40, 100, 6)
    draw_after.polygon(star_pts, outline=lime, width=2)
    
    # Draw anchor nodes & tangent handles (this simulates the vector editor look!)
    # Let's draw bezier handles for the inner star vertices
    for i, pt in enumerate(star_pts):
        if i % 2 == 0:  # Only for outer ray tips
            # Handle endpoints (tangent line)
            angle = i * (math.pi / 6)
            dx = 30 * math.sin(angle)
            dy = -30 * math.cos(angle)
            h1 = (pt[0] + dx, pt[1] + dy)
            h2 = (pt[0] - dx, pt[1] - dy)
            
            # Draw dashed-looking handles (simulated with standard lines)
            draw_after.line([pt, h1], fill=(0, 229, 255, 100), width=1)
            draw_after.line([pt, h2], fill=(0, 229, 255, 100), width=1)
            
            # Draw handle endpoint dots
            draw_after.ellipse([h1[0]-3, h1[1]-3, h1[0]+3, h1[1]+3], fill=cyan, outline=(255, 255, 255))
            draw_after.ellipse([h2[0]-3, h2[1]-3, h2[0]+3, h2[1]+3], fill=cyan, outline=(255, 255, 255))
            
            # Draw anchor point
            draw_after.rectangle([pt[0]-4, pt[1]-4, pt[0]+4, pt[1]+4], fill=bg_color, outline=cyan, width=2)

    # Draw anchor nodes on the outer gear
    for pt in gear_pts:
        draw_after.rectangle([pt[0]-3, pt[1]-3, pt[0]+3, pt[1]+3], fill=bg_color, outline=cyan, width=2)

    # Draw inner circle anchor points
    for i in range(8):
        angle = i * (math.pi / 4)
        pt = (center_x + 130 * math.cos(angle), center_y + 130 * math.sin(angle))
        draw_after.rectangle([pt[0]-3, pt[1]-3, pt[0]+3, pt[1]+3], fill=bg_color, outline=cyan, width=2)

    # Draw Center mark
    draw_after.line([(center_x - 15, center_y), (center_x + 15, center_y)], fill=cyan, width=1)
    draw_after.line([(center_x, center_y - 15), (center_x, center_y + 15)], fill=cyan, width=1)
    draw_after.ellipse([center_x - 6, center_y - 6, center_x + 6, center_y + 6], outline=cyan, width=1)

    # Add technical text markings
    draw_after.text((30, 30), "LAYER: VECTOR_CONTOURS", fill=lime)
    draw_after.text((30, 50), "STATUS: OPTIMIZED", fill=cyan)
    draw_after.text((30, 70), "NODES: 48 (CLEAN)", fill=(255, 255, 255))
    draw_after.text((width - 200, 30), "SCALE: 100% (1:1)", fill=(255, 255, 255))
    draw_after.text((width - 200, 50), "CONTOUR: CLOSED", fill=lime)
    
    img_after.convert("RGB").save("after.png", "PNG")
    print("after.png generated successfully.")

    # -------------------------------------------------------------
    # 3. GENERATING "BEFORE.JPG" (Messy, Blurry Raster Client Sketch)
    # -------------------------------------------------------------
    # We want a messy hand-sketched/dirty-photocopy look on a dark blue/gray grid
    img_before = Image.new("RGBA", (width, height), (15, 18, 24))
    draw_before = ImageDraw.Draw(img_before)

    # Draw a dirty, faint grid
    for x in range(0, width, grid_size):
        draw_before.line([(x, 0), (x, height)], fill=(30, 34, 44), width=1)
    for y in range(0, height, grid_size):
        draw_before.line([(0, y), (width, y)], fill=(30, 34, 44), width=1)

    # Draw the main gear outline but dirty, thicker, and with a mismatched offset
    # Simulate hand sketch/poor quality raster with thick uneven red-orange outline
    gear_pts_messy = get_gear_points(center_x + 3, center_y - 2, 160, 200, 10)
    
    # Draw thick irregular strokes for the gear to simulate bleeding ink / low res scan
    draw_before.polygon(gear_pts_messy, outline=(220, 80, 80), width=8)
    # Inside overlap (simulating multiple bad sketch lines)
    draw_before.polygon(get_gear_points(center_x - 1, center_y + 1, 159, 202, 10), outline=(180, 50, 50), width=2)
    
    # Draw messy inner circle
    draw_before.ellipse(
        [center_x - 128, center_y - 132, center_x + 132, center_y + 128], 
        outline=(200, 70, 70), 
        width=5
    )
    
    # Draw messy inner star
    star_pts_messy = get_inner_star_points(center_x + 1, center_y - 1, 38, 102, 6)
    draw_before.polygon(star_pts_messy, outline=(220, 90, 90), width=6)

    # Add scan lines, noise, and dirty background splotches
    # Draw some "grease/dirt" spots
    for _ in range(15):
        sx = random.randint(100, width - 100)
        sy = random.randint(50, height - 50)
        s_rad = random.randint(10, 80)
        # Translucent dust/dirt blobs
        draw_before.ellipse(
            [sx - s_rad, sy - s_rad, sx + s_rad, sy + s_rad], 
            fill=(40, 45, 60, 40)
        )
        
    # Draw messy hand-written technical notes
    draw_before.text((30, 30), "LAYER: Unknown (merged)", fill=(180, 100, 100))
    draw_before.text((30, 50), "STATUS: BITMAP RASTER", fill=(200, 80, 80))
    draw_before.text((30, 70), "NODES: NONE (NOISY)", fill=(200, 100, 100))
    draw_before.text((width - 250, 30), "RESOLUTION: 72 DPI (LOW)", fill=(200, 80, 80))
    draw_before.text((width - 250, 50), "UNCONNECTED CONTOURS", fill=(200, 50, 50))
    
    # Apply pixelating filter
    # To do this beautifully in PIL: 
    # 1. Blur the image slightly
    img_before = img_before.filter(ImageFilter.GaussianBlur(radius=3))
    
    # 2. Resize it down to 300 x 168 (low res)
    low_res_w = 300
    low_res_h = 168
    img_low = img_before.resize((low_res_w, low_res_h), Image.Resampling.BILINEAR)
    
    # 3. Resize it back up to 1200 x 675 using NEAREST to create nice chunky pixelation
    img_chunky = img_low.resize((width, height), Image.Resampling.NEAREST)
    
    # 4. Apply a small Blur to smooth the pixelated block edges slightly (like a bad JPEG compression stream)
    img_final = img_chunky.filter(ImageFilter.GaussianBlur(radius=1.5))
    
    # 5. Add overlay grain noise
    # Create noise overlay
    noise_img = Image.new("RGBA", (width, height))
    noise_draw = ImageDraw.Draw(noise_img)
    for _ in range(25000):
        nx = random.randint(0, width - 1)
        ny = random.randint(0, height - 1)
        n_val = random.randint(0, 40)
        noise_draw.point((nx, ny), fill=(n_val, n_val, n_val, 25))
    
    img_final = Image.alpha_composite(img_final, noise_img)
    
    # Save as JPEG with a very low compression setting to introduce real compression rings
    img_final.convert("RGB").save("before.jpg", "JPEG", quality=15)
    print("before.jpg generated successfully.")

if __name__ == "__main__":
    create_images()
