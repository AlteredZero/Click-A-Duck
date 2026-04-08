import pygame
import random

base_width = 2560
base_height = 1440



def draw_duck_company_stock_button(screen, tarot_card_icon):

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height
    scale = min(scale_x, scale_y)

    s = lambda v: int(v * scale)
    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    background = (30, 30, 30)
    border = (255, 255, 255)

    rect = pygame.Rect(sx(20), screen_height - sy(550), sx(80), sy(80))

    pygame.draw.rect(screen, background, rect)
    pygame.draw.rect(screen, border, rect, s(3))

    icon = pygame.transform.scale(tarot_card_icon, (sx(50), sy(50)))
    icon_rect = icon.get_rect(center=rect.center)
    screen.blit(icon, icon_rect)

    return rect


def tick_stock_market(game_data):
    stock = game_data["extras"]["duck_stock"]
    change = random.uniform(-0.02, 0.02) 
    new_price = stock["current_price"] * (1 + change)
    
    stock["current_price"] = round(new_price, 2)
    stock["history"].append(stock["current_price"])
    
    if len(stock["history"]) > 30:
        stock["history"].pop(0)

def draw_stock_graph(screen, menu_rect, stock_history, sx, sy, fonts):
    if len(stock_history) < 2:
        return

    graph_area = pygame.Rect(menu_rect.x + sx(50), menu_rect.y + sy(100), sx(600), sy(200))
    
    pygame.draw.rect(screen, (20, 20, 20), graph_area)
    pygame.draw.rect(screen, (100, 100, 100), graph_area, 1)

    min_p, max_p = min(stock_history), max(stock_history)
    price_range = (max_p - min_p) if max_p != min_p else 1
    
    points = []
    for i, price in enumerate(stock_history):
        x = graph_area.x + (i / (len(stock_history) - 1)) * graph_area.width
        y = graph_area.bottom - ((price - min_p) / price_range) * graph_area.height
        points.append((int(x), int(y)))

    color = (4, 207, 116) if stock_history[-1] >= stock_history[0] else (207, 4, 4)

    fill_surface = pygame.Surface((graph_area.width, graph_area.height), pygame.SRCALPHA)
    fill_points = [(p[0] - graph_area.x, p[1] - graph_area.y) for p in points]
    fill_points += [(fill_points[-1][0], graph_area.height), (0, graph_area.height)]
    pygame.draw.polygon(fill_surface, (*color, 50), fill_points) # 50 is alpha/transparency
    screen.blit(fill_surface, (graph_area.x, graph_area.y))

    pygame.draw.lines(screen, color, False, points, 3)

    max_label = fonts["small"].render(f"${max_p:.2f}", True, (150, 150, 150))
    min_label = fonts["small"].render(f"${min_p:.2f}", True, (150, 150, 150))
    screen.blit(max_label, (graph_area.right + sx(10), graph_area.top))
    screen.blit(min_label, (graph_area.right + sx(10), graph_area.bottom - sy(20)))


def open_duck_company_stock_frame(screen, fonts, game_data, draw_animated_text):

    clickable_rects = []

    screen_width, screen_height = screen.get_size()

    scale_x = screen_width / base_width
    scale_y = screen_height / base_height
    scale = min(scale_x, scale_y)

    def sx(x): return int(x * scale)
    def sy(y): return int(y * scale)

    menu_rect = pygame.Rect(sx(135), sy(700), sx(700), sy(450))
    pygame.draw.rect(screen, (30, 30, 30), menu_rect)
    pygame.draw.rect(screen, (255, 255, 255), menu_rect, 3)

    draw_animated_text(
        screen,
        "Duck Company Stock",
        fonts["large"],
        (255, 255, 255),
        (menu_rect.centerx, menu_rect.top + sy(30)),
        "duck_company_stock_title"
    )

    buy_center_y = menu_rect.bottom - sy(80) + fonts["small"].get_height() // 2
    buy_rect = pygame.Rect(menu_rect.centerx - sx(200), buy_center_y - sy(20), sx(200), sy(40))

    btn_w, btn_h = sx(100), sy(40)
    padding = sx(20)

    sell_rect = pygame.Rect(menu_rect.right - btn_w - padding, menu_rect.bottom - btn_h - padding, btn_w, btn_h)
    buy_rect = pygame.Rect(sell_rect.left - btn_w - padding, menu_rect.bottom - btn_h - padding, btn_w, btn_h)

    pygame.draw.rect(screen, (4, 207, 116), buy_rect)
    draw_animated_text(
        screen, 
        "BUY", 
        fonts["small"], 
        (255, 255, 255), 
        (buy_rect.centerx, buy_rect.centery), "buy_button"
    )

    pygame.draw.rect(screen, (207, 4, 4), sell_rect)
    draw_animated_text(
        screen, 
        "SELL", 
        fonts["small"], 
        (255, 255, 255), 
        (sell_rect.centerx, sell_rect.centery), "sell_button"
    )

    stock_data = game_data["extras"].get("duck_stock", {"current_price": 100, "history": [100]})
    history = stock_data["history"]
    current_price = stock_data["current_price"]

    draw_animated_text(
        screen, 
        f"Price per share: {current_price:.2f} Ducks", 
        fonts["small"], 
        (255, 255, 255), 
        (menu_rect.centerx, menu_rect.top + sy(60)), "duck_price"
    )

    draw_stock_graph(screen, menu_rect, history, sx, sy, fonts)
    
    clickable_rects.append((buy_rect, "buy_button"))
    clickable_rects.append((sell_rect, "sell_button"))

    return clickable_rects