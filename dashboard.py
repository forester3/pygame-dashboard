import pygame
import requests
import os

os.environ["SDL_AUDIODRIVER"] = "dummy" # 音エラー対策
os.environ["DISPLAY"] = ":1"

def get_cpu_load():
    try:
        response = requests.get("http://localhost:9100/metrics", timeout=0.5)
        for line in response.text.splitlines():
            if line.startswith("node_load1 "):
                return float(line.split()[1])
    except:
        return 0.0
    return 0.0

pygame.init()
screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption("System Monitor v2")
font = pygame.font.SysFont("dejavusansmono", 30)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); exit()

    load_val = get_cpu_load()

    screen.fill((10, 10, 15)) # 背景（ほぼ黒）

    # テキスト表示
    label = font.render(f"CPU LOAD (1m): {load_val}", True, (255, 255, 255))
    screen.blit(label, (50, 50))

    # --- バーグラフの描画 ---
    # 枠を描く
    pygame.draw.rect(screen, (100, 100, 100), (50, 120, 500, 50), 2)
    # 中身を描く（load_val * 100 ピクセル分。最大5.0とする）
    bar_width = min(int(load_val * 100), 500)
    # 負荷が高いと赤くなるように
    bar_color = (0, 255, 100) if load_val < 1.0 else (255, 50, 50)
    pygame.draw.rect(screen, bar_color, (50, 120, bar_width, 50))

    pygame.display.flip()
    clock.tick(2)