import pgzrun
import pygame
from pygame import Rect
import math
import random


musica_atual = "menu"
pygame.mixer.music.load("sounds/menu.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
som_recompensa = pygame.mixer.Sound("sounds/recompensa.mp3")
som_recompensa.set_volume(1)
som_batendo = pygame.mixer.Sound("sounds/batendo.mp3")
som_batendo.set_volume(1)
som_pulo = pygame.mixer.Sound("sounds/jump.mp3")
som_pulo.set_volume(1)
tocando_som_pulo = False
pulos_usados = 0
pontos_coletados = 0
musica_atual = None
WIDTH = 640
HEIGHT = 480
vel_y = 0
gravidade = 0.5
pulo_forca = -10
no_chao = False
chao_y = HEIGHT - 50  # altura do "chão"
scroll_x = 0
jogador = Rect((100, HEIGHT - 100), (50, 50))
area_nascimento = Rect(jogador.x - 50, jogador.y - 50, jogador.width + 100, jogador.height + 100)

def on_key_down(key):
    global tocando_som_pulo, vel_y, pulos_usados
    if key == keys.UP:
        if pulos_usados < 2:
            vel_y = pulo_forca
            pulos_usados += 1
            if not tocando_som_pulo:
                som_pulo.play(-1)  # toca em loop enquanto segura
                tocando_som_pulo = True

def on_key_up(key):
    global tocando_som_pulo
    if key == keys.UP and tocando_som_pulo:
        som_pulo.stop()
        tocando_som_pulo = False

#jump
# Criação de mapa
mapa = []
for i in range(100):
    bloco = Rect((i * 50, chao_y), (50, 50))
    mapa.append(bloco)  

plataformas = []
num_plataformas = 7
largura_plataforma = 100
altura_plataforma = 40
dist_min_horizontal = 150
dist_min_vertical = altura_plataforma + 20
tentativas_max = 100

def distancia_entre_rects(r1, r2):
    cx1, cy1 = r1.center
    cx2, cy2 = r2.center
    return math.hypot(cx2 - cx1, cy2 - cy1)

for _ in range(num_plataformas):
    for tentativa in range(tentativas_max):
        x = random.randint(0, len(mapa) * 50 - largura_plataforma)
        y = random.randint(chao_y - 250, chao_y - altura_plataforma)
        nova_plataforma = Rect((x, y), (largura_plataforma, altura_plataforma))
        if nova_plataforma.colliderect(area_nascimento):
            continue
        muito_perto = False
        for p in plataformas:
            if nova_plataforma.colliderect(p):
                muito_perto = True
                break
            if abs(nova_plataforma.centerx - p.centerx) < dist_min_horizontal and \
               abs(nova_plataforma.centery - p.centery) < dist_min_vertical:
                muito_perto = True
                break
        if not muito_perto:
            plataformas.append(nova_plataforma)
            break
passaros = []
for _ in range(10):  
    x = random.randint(0, len(mapa) * 50)  
    y = random.randint(chao_y - 250, chao_y - 100)  
    passaros.append(Rect((x, y), (50, 30)))
velocidade_passaros = -2
plantas = []
num_plantas = 5
largura_planta = 40
altura_planta = 40
distancia_minima_plantas = 80
def encontrar_chao_ou_plataforma_mais_baixa(x_pos):
    menor_y = chao_y
    for p in plataformas:
        if p.left <= x_pos <= p.right:
            if p.top < menor_y:
                menor_y = p.top
    return menor_y
for _ in range(num_plantas):
    for tentativa in range(tentativas_max):
        x = random.randint(0, len(mapa) * 50 - largura_planta)
        y_base = encontrar_chao_ou_plataforma_mais_baixa(x + largura_planta // 2)
        y = y_base - altura_planta
        nova_planta = Rect((x, y), (largura_planta, altura_planta))
        if nova_planta.colliderect(area_nascimento):
            continue
        muito_perto = False
        for pl in plantas:
            if distancia_entre_rects(nova_planta, pl) < distancia_minima_plantas:
                muito_perto = True
                break
        if not muito_perto:
            plantas.append(nova_planta)
            break
pontos = []
num_pontos = 7
largura_ponto = 20
altura_ponto = 20
distancia_minima_pontos = 80
for _ in range(num_pontos):
    for tentativa in range(tentativas_max):
        x = random.randint(0, len(mapa) * 50 - largura_ponto)
        y = random.randint(HEIGHT // 2, chao_y - altura_ponto)
        novo_ponto = Rect((x, y), (largura_ponto, altura_ponto))
        if novo_ponto.colliderect(area_nascimento):
            continue
        colide_com_chao = False
        for bloco in mapa + plataformas:
            if novo_ponto.colliderect(bloco):
                colide_com_chao = True
                break
        if colide_com_chao:
            continue
        muito_perto = False
        for p in pontos:
            if distancia_entre_rects(novo_ponto, p) < distancia_minima_pontos:
                muito_perto = True
                break
        if not muito_perto:
            pontos.append(novo_ponto)
            break
for _ in range(num_pontos):
    for tentativa in range(tentativas_max):
        x = random.randint(0, len(mapa) * 50 - largura_ponto)
        y = random.randint(HEIGHT // 2, chao_y - altura_ponto)  
        novo_ponto = Rect((x, y), (largura_ponto, altura_ponto))
        muito_perto = False
        for p in pontos:
            if distancia_entre_rects(novo_ponto, p) < distancia_minima_pontos:
                muito_perto = True
                break
        if not muito_perto:
            pontos.append(novo_ponto)
            break
    else:
        print("Não foi possível posicionar um ponto respeitando a distância mínima.")
tela_atual = "menu"
start_button = Rect((WIDTH//2 - 100, HEIGHT//2 - 60), (200, 50))
quit_button = Rect((WIDTH//2 - 100, HEIGHT//2 + 20), (200, 50))
vol_up_button = Rect((WIDTH - 150, 30), (40, 40))
vol_down_button = Rect((WIDTH - 200, 30), (40, 40))
volume = 0.5
jogador = Rect((100, HEIGHT - 100), (50, 50))
velocidade = 5
def draw():
    screen.clear()
    fundo_largura = 1024
    fundo_y = 0
    if tela_atual == "menu": 
        desenhar_menu() 
    elif tela_atual == "jogo":
        screen.draw.filled_rect(Rect(0, 0, WIDTH, HEIGHT), (10, 231, 255))
    if tela_atual == "jogo":
        fundo_largura = 1024
        parallax_scroll = int(scroll_x * 0.3)
        fundo_x = -(parallax_scroll % fundo_largura)
        for i in range((WIDTH // fundo_largura) + 2):
            x = fundo_x + i * (fundo_largura -75)
            screen.blit("fundo", (x, fundo_y))
        desenhar_jogo()
    elif tela_atual == "gameover":
        desenhar_gameover()
        screen.draw.text(f"Pontos: {pontos_coletados}", topleft=(10, 10), fontsize=30, color="white")
def desenhar_gameover():
    screen.draw.text("GAME OVER", center=(WIDTH//2, HEIGHT//2), fontsize=80, color="red")
def desenhar_menu():  
    screen.draw.text("MENU", center=(WIDTH//2, HEIGHT//2 - 120), fontsize=50, color="white")
    screen.draw.filled_rect(start_button, "green")
    screen.draw.text("Começar Jogo", center=start_button.center, fontsize=30, color="black")
    screen.draw.filled_rect(quit_button, "red")
    screen.draw.text("Fechar Jogo", center=quit_button.center, fontsize=30, color="black")
    screen.draw.filled_rect(vol_up_button, "gray")
    screen.draw.text("+", center=vol_up_button.center, fontsize=30, color="white")
    screen.draw.filled_rect(vol_down_button, "gray")
    screen.draw.text("-", center=vol_down_button.center, fontsize=30, color="white")
    screen.draw.text(f"Volume: {int(volume * 100)}%", topleft=(WIDTH - 140, 80), fontsize=25, color="white")
def desenhar_jogo():
    for bloco in mapa:
        bloco_visivel = bloco.move(-scroll_x, 0)
        screen.blit("chao", (bloco_visivel.x, bloco_visivel.y))
    for plataforma in plataformas:
        p_visivel = plataforma.move(-scroll_x, 0)
        screen.blit("plataforma", (p_visivel.x, p_visivel.y))
    jogador_visivel = jogador.move(-scroll_x, 0)
    screen.draw.filled_rect(jogador_visivel, "blue")
    for p in passaros:
        p_visivel = p.move(-scroll_x, 0)
        screen.draw.filled_rect(p_visivel, "red")
    for planta in plantas:
        p_visivel = planta.move(-scroll_x, 0)
        screen.draw.filled_rect(p_visivel, "green")
    
    for ponto in pontos:
        p_visivel = ponto.move(-scroll_x, 0)
        screen.draw.filled_circle(p_visivel.center, 10, "yellow")  # círculo amarelo
def on_mouse_down(pos):
    global tela_atual, volume, musica_atual
    if tela_atual == "menu":
        if start_button.collidepoint(pos):
            tela_atual = "jogo"
            if musica_atual != "jogo":
                pygame.mixer.music.load("sounds/game_inicio.mp3")
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)
                musica_atual = "jogo"
        elif quit_button.collidepoint(pos):
            exit()
        elif vol_up_button.collidepoint(pos):
            volume = min(1.0, volume + 0.1)
            pygame.mixer.music.set_volume(volume)  # só ajusta volume, sem reiniciar
        elif vol_down_button.collidepoint(pos):
            volume = max(0.0, volume - 0.1)
            pygame.mixer.music.set_volume(volume)  # idem
distancia_interacao = 100
planta_perto = None
def update():
    global tocando_som_pulo, vel_y, pulos_usados, planta_perto, no_chao, scroll_x, tela_atual
    
    planta_perto = None
    for planta in plantas:
        distancia = abs(planta.centerx - jogador.centerx)
        distancia_vertical = abs(planta.centery - jogador.centery)
        if distancia < distancia_interacao and distancia_vertical < 50:
            planta_perto = planta
            break
    if tela_atual != "jogo":
        if tocando_som_pulo:
            som_pulo.stop()
            tocando_som_pulo = False
        return
    vel_x = 0
    if keyboard.right:
        vel_x = velocidade
    elif keyboard.left:
        vel_x = -velocidade
    vel_x = verificar_colisao_horizontal(jogador, mapa + plataformas, vel_x)
    jogador.x += vel_x
    if jogador.left < 0:
        jogador.left = 0
    if jogador.right > len(mapa) * 50:
        jogador.right = len(mapa) * 50
    vel_y += gravidade
    vel_y, no_chao = verificar_colisao_vertical(jogador, mapa + plataformas, vel_y)
    jogador.y += vel_y
    if no_chao:
        pulos_usados = 0
    pulo_forca = -10
    max_pulos = 2
    if keyboard.up:
        if pulos_usados < max_pulos:
            if not tocando_som_pulo:
                som_pulo.play(-1)  
                tocando_som_pulo = True
            if vel_y >= 0:  
                vel_y = pulo_forca
                pulos_usados += 1
    else:
        if tocando_som_pulo:
            som_pulo.stop()
            tocando_som_pulo = False

    vel_y, no_chao = verificar_colisao_vertical(jogador, mapa + plataformas, vel_y)

    if no_chao:
        pulos_usados = 0
    margem = WIDTH // 2
    if jogador.centerx - scroll_x > WIDTH - margem:
        scroll_x = jogador.centerx - (WIDTH - margem)
    elif jogador.centerx - scroll_x < margem:
        scroll_x = jogador.centerx - margem
    scroll_x = max(0, scroll_x)
    for p in passaros:
        p.x += velocidade_passaros
        if jogador.colliderect(p):
            tela_atual = "gameover"
            pygame.mixer.music.load("sounds/game_over.mp3")
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play()
    for planta in plantas:
        if jogador.colliderect(planta):
            tela_atual = "gameover"
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sounds/game_over.mp3")
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play()
    global pontos_coletados
    for ponto in pontos[:]:
        if jogador.colliderect(ponto):
            pontos.remove(ponto)
            pontos_coletados += 1
            som_recompensa.play()

def on_key_down(key):
    global pontos_coletados, planta_perto

    if key == key.E and planta_perto is not None:
        som_batendo.play()
        plantas.remove(planta_perto)
        pontos_coletados += 5
        planta_perto = None 
def verificar_colisao_vertical(rect, plataformas, vel_y):
    nova_y = rect.y + vel_y
    rect_teste = rect.copy()
    rect_teste.y = nova_y
    for bloco in plataformas:
        if rect_teste.colliderect(bloco):
            if vel_y > 0 and rect.bottom <= bloco.top:
                rect.bottom = bloco.top
                return 0, True  
            elif vel_y < 0 and rect.top >= bloco.bottom:
                rect.top = bloco.bottom
                return 0, False
    return vel_y, False
def verificar_colisao_horizontal(rect, plataformas, vel_x):
    """Detecta e corrige colisão horizontal entre jogador e plataformas."""
    nova_x = rect.x + vel_x
    rect_teste = rect.copy()
    rect_teste.x = nova_x
    for bloco in plataformas:
        if rect_teste.colliderect(bloco):
            if vel_x > 0:  
                rect.right = bloco.left
            elif vel_x < 0:  
                rect.left = bloco.right
            return 0  
    return vel_x
pgzrun.go()