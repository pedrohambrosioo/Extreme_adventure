import pgzrun
import pygame
from pygame import Rect



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

# Criar um mapa simples com blocos de chão
mapa = []
for i in range(100):  # 50 blocos (50 x 50 = 2500px de largura de mapa)
    bloco = Rect((i * 50, chao_y), (50, 50))
    mapa.append(bloco)  
plataformas = [
    Rect((400, chao_y - 80), (100, 40)),
    Rect((800, chao_y - 150), (100, 40)),
    Rect((1200, chao_y - 80), (100, 40)),
    Rect((1600, chao_y - 130), (100, 40)),
    Rect((2000, chao_y - 100), (100, 40)),
    Rect((2400, chao_y - 120), (100, 40)),
    Rect((2800, chao_y - 90), (100, 40)),
]
passaros = [
    Rect((700, chao_y - 200), (50, 30)),
    Rect((1300, chao_y - 240), (50, 30)),
    Rect((2100, chao_y - 180), (50, 30)),
]
velocidade_passaros = -2
plantas = [
    Rect((400, chao_y - 40), (40, 40)),    # em cima da segunda plataforma
    Rect((1600, chao_y - 170), (40, 40)),   # em cima da quarta plataforma
    Rect((2400, chao_y - 160), (40, 40)),   # em cima da nova
    # adicione mais conforme quiser
]
pontos = [
    Rect((500, chao_y - 100), (20, 20)),
    Rect((900, chao_y - 180), (20, 20)),
    Rect((1300, chao_y - 130), (20, 20)),
]



# Estados: "menu" ou "jogo"
tela_atual = "menu"

# Botões
start_button = Rect((WIDTH//2 - 100, HEIGHT//2 - 60), (200, 50))
quit_button = Rect((WIDTH//2 - 100, HEIGHT//2 + 20), (200, 50))
vol_up_button = Rect((WIDTH - 150, 30), (40, 40))
vol_down_button = Rect((WIDTH - 200, 30), (40, 40))

volume = 0.5

# Exemplo de jogador (objeto simples no jogo)
jogador = Rect((100, HEIGHT - 100), (50, 50))
velocidade = 5

def draw():
    screen.clear()
    
    

    if tela_atual == "menu": 
        desenhar_menu()
    elif tela_atual == "jogo":
        fundo_x = -scroll_x * 0.3
        fundo_x = fundo_x % 1024  # 1024 é a largura da imagem

        screen.blit("fundo", (fundo_x - 1024, -50))  # desenha a imagem anterior
        screen.blit("fundo", (fundo_x, -50))         # desenha a imagem atual
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
    
  # Desenhar mapa (chão)
    for bloco in mapa:
        bloco_visivel = bloco.move(-scroll_x, 0)
        screen.blit("chao", (bloco_visivel.x, bloco_visivel.y))


    # Desenhar plataformas
    for plataforma in plataformas:
        p_visivel = plataforma.move(-scroll_x, 0)
        screen.blit("plataforma", (p_visivel.x, p_visivel.y))

    # Desenhar jogador com scroll
    jogador_visivel = jogador.move(-scroll_x, 0)
    screen.draw.filled_rect(jogador_visivel, "blue")

    # Desenhar pássaros com scroll
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
    global planta_perto
    planta_perto = None
    
    for planta in plantas:
        distancia = abs(planta.centerx - jogador.centerx)
        distancia_vertical = abs(planta.centery - jogador.centery)
        if distancia < distancia_interacao and distancia_vertical < 50:
            planta_perto = planta
            break
    global vel_y, no_chao, scroll_x, tela_atual, pulos_usados 
    if tela_atual != "jogo":
        return
    if tela_atual != "jogo":
        return
    
    global vel_y, no_chao, scroll_x

    if tela_atual == "jogo":
        # Movimento lateral
        vel_x = 0
        if keyboard.right:
            vel_x = velocidade
        elif keyboard.left:
            vel_x = -velocidade

        # Verifica colisão lateral antes de mover
        vel_x = verificar_colisao_horizontal(jogador, mapa + plataformas, vel_x)
        jogador.x += vel_x


        # Impedir que o jogador saia dos limites do mapa
        if jogador.left < 0:
            jogador.left = 0
        if jogador.right > len(mapa) * 50:
            jogador.right = len(mapa) * 50

        # Aplicar gravidade
        vel_y += gravidade

        # Verificar colisão antes de aplicar movimento vertical
        vel_y, no_chao = verificar_colisao_vertical(jogador, mapa + plataformas, vel_y)

        # Aplicar movimento vertical ajustado
        jogador.y += vel_y
        if no_chao:
            pulos_usados = 0
        
        # Pulo
        if (keyboard.up) and no_chao:
            som_pulo.play()
            vel_y = pulo_forca
            no_chao = False

        # Atualizar scroll (câmera)
        margem = WIDTH // 2
        if jogador.centerx - scroll_x > WIDTH - margem:
            scroll_x = jogador.centerx - (WIDTH - margem)
        elif jogador.centerx - scroll_x < margem:
            scroll_x = jogador.centerx - margem
        scroll_x = max(0, scroll_x)

        # Atualizar posição dos pássaros e verificar colisão
    for p in passaros:
        p.x += velocidade_passaros

        # Se colidir com o jogador, fecha o jogo
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
            pygame.mixer.music.play()  # Toca só uma vez
    global pontos_coletados

    for ponto in pontos[:]:  # percorre uma cópia da lista
        if jogador.colliderect(ponto):
            pontos.remove(ponto)  # remove ponto da lista para "sumir"
            pontos_coletados += 1
            som_recompensa.play()
            # (Opcional) tocar som de coleta aqui


def on_key_down(key):
    global pontos_coletados, planta_perto

    if key == key.E and planta_perto is not None:
        som_batendo.play()
        plantas.remove(planta_perto)
        pontos_coletados += 5
        planta_perto = None  # limpa a referência
        # aqui você pode tocar som se quiser


def verificar_colisao_vertical(rect, plataformas, vel_y):
    """Detecta e corrige colisão vertical entre jogador e plataformas."""
    nova_y = rect.y + vel_y
    rect_teste = rect.copy()
    rect_teste.y = nova_y

    for bloco in plataformas:
        if rect_teste.colliderect(bloco):
            if vel_y > 0 and rect.bottom <= bloco.top:
                rect.bottom = bloco.top
                return 0, True  # Zera vel_y e confirma que está no chão
            # Colisão vindo de baixo (opcional)
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
            if vel_x > 0:  # indo para a direita
                rect.right = bloco.left
            elif vel_x < 0:  # indo para a esquerda
                rect.left = bloco.right
            return 0  # para o movimento
    return vel_x



pgzrun.go()