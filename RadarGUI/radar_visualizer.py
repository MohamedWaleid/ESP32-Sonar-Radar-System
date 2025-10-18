# radar_visualizer.py
# ESP32 Radar GUI using pygame
# Author: weLTon (adapted)
# License: MIT

import pygame
import serial
import math
import time
import argparse

# ---------------- CONFIG ----------------
DEFAULT_COM_PORT = "COM5"    # change to your serial port (e.g., "/dev/ttyUSB0" on Linux)
DEFAULT_BAUD = 9600
MAX_RANGE_CM = 50            # maximum displayed range in cm
FPS = 60

# ---------------- Serial setup ----------------
def open_serial(port, baud):
    try:
        s = serial.Serial(port, baud, timeout=0.1)
        time.sleep(2)  # allow device to initialize
        print(f"Serial opened: {port} @ {baud}")
        return s
    except Exception as e:
        print(f"Warning: could not open serial on {port}: {e}")
        print("Running in simulation mode (no real serial data).")
        return None

# ---------------- Pygame setup ----------------
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ESP32 Radar - SciCraft")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Consolas", 20)
FONT_SMALL = pygame.font.SysFont("Consolas", 14)

# ---------------- Radar geometry ----------------
CENTER = (WIDTH // 2, int(HEIGHT * 0.9))
RADAR_RADIUS = 400
CM_TO_PX = RADAR_RADIUS / float(MAX_RANGE_CM)

# ---------------- State ----------------
current_angle = 0.0
current_distance = 0.0
smoothed_angle = 0.0
detections = []  # list of tuples: (px, py, timestamp, distance)

# ---------------- Helper functions ----------------
def parse_line(line):
    """
    Parse a single line from the serial port.
    Expected format: "angle,distance." e.g. "90,35.50."
    Returns (angle:int, distance:float) or None on failure.
    """
    if not line:
        return None

    s = line.strip()
    # require trailing dot as end-of-line marker to reject incomplete lines
    if not s.endswith('.'):
        return None
    s = s[:-1]  # remove trailing dot

    parts = s.split(',')
    if len(parts) < 2:
        return None

    try:
        angle = int(float(parts[0]))
        dist = float(parts[1])
        return angle, dist
    except (ValueError, IndexError):
        return None

def add_detection(angle, distance_cm):
    """Add a detection point (convert polar to cartesian) if within range."""
    if distance_cm <= 0 or distance_cm > MAX_RANGE_CM:
        return

    rad = math.radians(angle)
    px = CENTER[0] + (distance_cm * CM_TO_PX) * math.cos(rad)
    py = CENTER[1] - (distance_cm * CM_TO_PX) * math.sin(rad)
    detections.append((px, py, time.time(), distance_cm))

def read_serial(ser):
    """Read one line from serial and update global state if valid."""
    global current_angle, current_distance
    if ser and ser.is_open:
        try:
            raw_line = ser.readline().decode(errors='ignore')
            parsed = parse_line(raw_line)
            if parsed:
                a, d = parsed
                if 0 <= a <= 180:
                    current_angle = a
                    current_distance = d
                    if 0 < d <= MAX_RANGE_CM:
                        add_detection(current_angle, current_distance)
        except serial.SerialException as e:
            print(f"Serial read error: {e}")
            try:
                ser.close()
            except Exception:
                pass
        except Exception as e:
            print(f"Unexpected error while reading serial: {e}")

# ---------------- Drawing functions ----------------
def draw_radar_background():
    """Draw concentric arcs and radial lines for the radar background."""
    for i in range(1, 5):
        r = int(RADAR_RADIUS * (i / 4.0))
        pygame.draw.arc(screen, (98, 245, 31),
                        (CENTER[0] - r, CENTER[1] - r, r * 2, r * 2),
                        math.pi, 2 * math.pi, 2)
    for a in range(0, 181, 30):
        rad = math.radians(a)
        x = CENTER[0] + RADAR_RADIUS * math.cos(rad)
        y = CENTER[1] - RADAR_RADIUS * math.sin(rad)
        pygame.draw.line(screen, (98, 245, 31), CENTER, (x, y), 1)

def draw_scan_line(angle):
    """Draw the current scan line and a soft cone glow behind it."""
    rad = math.radians(angle)
    x = CENTER[0] + RADAR_RADIUS * math.cos(rad)
    y = CENTER[1] - RADAR_RADIUS * math.sin(rad)
    pygame.draw.line(screen, (0, 220, 140), CENTER, (x, y), 3)

    cone_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for i in range(0, 40):
        angle_offset = i * 0.6
        r1 = math.radians(angle - angle_offset)
        r2 = math.radians(angle + angle_offset)
        p1 = (CENTER[0] + RADAR_RADIUS * math.cos(r1), CENTER[1] - RADAR_RADIUS * math.sin(r1))
        p2 = (CENTER[0] + RADAR_RADIUS * math.cos(r2), CENTER[1] - RADAR_RADIUS * math.sin(r2))
        alpha = max(6, 80 - i * 2)
        pygame.draw.polygon(cone_surface, (0, 255, 150, alpha), [CENTER, p1, p2])
    screen.blit(cone_surface, (0, 0))

def draw_detections():
    """Draw detected points with fading glow and distance label."""
    now = time.time()
    for det in detections[:]:
        px, py, t0, dist = det
        age = now - t0
        if age > 2.5:
            try:
                detections.remove(det)
            except ValueError:
                pass
            continue

        alpha = max(0, 255 - int(age * 100))

        glow = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 80, 80, int(alpha * 0.5)), (20, 20), 12)
        pygame.draw.circle(glow, (255, 40, 40, alpha), (20, 20), 6)
        screen.blit(glow, (px - 20, py - 20))

        dist_text = FONT_SMALL.render(f"{int(dist)} cm", True, (255, 150, 150))
        screen.blit(dist_text, (px + 15, py - 8))

def draw_info_panel():
    """Draw information panel with current angle and distance."""
    pygame.draw.rect(screen, (0, 0, 0), (0, HEIGHT - 48, WIDTH, 48))
    angle_text = FONT.render(f"Angle: {int(current_angle):3d}°", True, (98, 245, 31))
    dist_text = FONT.render(f"Distance: {current_distance:5.1f} cm", True, (98, 245, 31))
    title_text = FONT.render("SciCraft Radar (180°)", True, (120, 220, 180))

    screen.blit(angle_text, (18, HEIGHT - 36))
    screen.blit(dist_text, (220, HEIGHT - 36))
    screen.blit(title_text, (WIDTH - 260, HEIGHT - 36))

# ---------------- Main ----------------
def main(args):
    global smoothed_angle
    ser = None
    if args.port:
        ser = open_serial(args.port, args.baud)

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False

        read_serial(ser)

        # smooth angle movement for nicer visuals
        smoothed_angle += (current_angle - smoothed_angle) * 0.22

        screen.fill((10, 20, 10))  # dark green-black background
        draw_radar_background()
        draw_scan_line(smoothed_angle)
        draw_detections()
        draw_info_panel()
        pygame.display.flip()
        clock.tick(FPS)

    if ser and ser.is_open:
        ser.close()
        print("Serial port closed.")
    pygame.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ESP32 Radar GUI (pygame).")
    parser.add_argument("--port", type=str, default=DEFAULT_COM_PORT, help="Serial port (e.g. COM5 or /dev/ttyUSB0)")
    parser.add_argument("--baud", type=int, default=DEFAULT_BAUD, help="Serial baud rate")
    args = parser.parse_args()
    main(args)
