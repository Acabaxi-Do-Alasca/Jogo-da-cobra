import pygame
import random

# Inicialização do Pygame
pygame.init()

# Cores
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Dimensões da tela
largura_tela = 640
altura_tela = 480

# Configurações da cobrinha
tamanho_cobra = 20
velocidade_cobra = 10

# Criando a tela
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("GerascoFobia")

# Carregando imagens das cabeças da cobra para cada direção
cabeca_cobra_direita = pygame.image.load('imagens/frente-direita.png')
cabeca_cobra_esquerda = pygame.image.load('imagens/frente-esquerda.png')
cabeca_cobra_cima = pygame.image.load('imagens/frente-cima.png')
cabeca_cobra_baixo = pygame.image.load('imagens/frente-baixo.png')
corpo_cobra_img = pygame.image.load('imagens/corpo.png')

# Redimensionar as imagens
tamanho_cobra = 20
cabeca_cobra_direita = pygame.transform.scale(cabeca_cobra_direita, (tamanho_cobra, tamanho_cobra))
cabeca_cobra_esquerda = pygame.transform.scale(cabeca_cobra_esquerda, (tamanho_cobra, tamanho_cobra))
cabeca_cobra_cima = pygame.transform.scale(cabeca_cobra_cima, (tamanho_cobra, tamanho_cobra))
cabeca_cobra_baixo = pygame.transform.scale(cabeca_cobra_baixo, (tamanho_cobra, tamanho_cobra))
corpo_cobra_img = pygame.transform.scale(corpo_cobra_img, (tamanho_cobra, tamanho_cobra))

# Carregando imagem de abertura
imagem_abertura = pygame.image.load('imagens/abertura.png')
imagem_abertura = pygame.transform.scale(imagem_abertura, (largura_tela, 450))

# Mostrando imagem de abertura
tela.blit(imagem_abertura, (0, 0))
pygame.display.flip()

# Aguardando pressionamento de uma tecla
esperando_inicio = True
while esperando_inicio:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            esperando_inicio = False

# Classe para representar a cobrinha
class Cobrinha:
    def __init__(self):
        self.tamanho = 1
        self.segmentos = [(largura_tela // 2, altura_tela // 2)]
        self.direcao = 'direita'
        self.cabeca_imgs = {
            'direita': cabeca_cobra_direita,
            'esquerda': cabeca_cobra_esquerda,
            'cima': cabeca_cobra_cima,
            'baixo': cabeca_cobra_baixo
        }
        self.corpo_img = corpo_cobra_img

    def atualizar(self):
        if self.direcao == 'direita':
            cabeca_x = self.segmentos[0][0] + tamanho_cobra
            cabeca_y = self.segmentos[0][1]
            self.cabeca_img = cabeca_cobra_direita
        elif self.direcao == 'esquerda':
            cabeca_x = self.segmentos[0][0] - tamanho_cobra
            cabeca_y = self.segmentos[0][1]
            self.cabeca_img = cabeca_cobra_esquerda
        elif self.direcao == 'cima':
            cabeca_x = self.segmentos[0][0]
            cabeca_y = self.segmentos[0][1] - tamanho_cobra
            self.cabeca_img = cabeca_cobra_cima
        elif self.direcao == 'baixo':
            cabeca_x = self.segmentos[0][0]
            cabeca_y = self.segmentos[0][1] + tamanho_cobra
            self.cabeca_img = cabeca_cobra_baixo

        self.segmentos.insert(0, (cabeca_x, cabeca_y))

        if len(self.segmentos) > self.tamanho:
            self.segmentos.pop()

    def desenhar(self):
        for i, (segmento, img) in enumerate(
                zip(self.segmentos, [self.cabeca_imgs[self.direcao]] + [self.corpo_img] * (len(self.segmentos) - 1))):
            tela.blit(img, (segmento[0], segmento[1]))

    def colisao(self):
        cabeca = self.segmentos[0]
        if cabeca[0] < 0 or cabeca[0] >= largura_tela or cabeca[1] < 0 or cabeca[1] >= altura_tela:
            return True
        for segmento in self.segmentos[1:]:
            if cabeca == segmento:
                return True
        return False

    def comer(self, maca):
        if self.segmentos[0] == maca.posicao:
            self.tamanho += 1
            maca.mover()

# Classe para representar a maçã
class Maca:
    def __init__(self):
        self.tamanho = tamanho_cobra
        self.mover()

    def desenhar(self):
        pygame.draw.rect(tela, VERMELHO, (self.posicao[0], self.posicao[1], self.tamanho, self.tamanho))

    def mover(self):
        x = random.randint(0, largura_tela - tamanho_cobra)
        y = random.randint(0, altura_tela - tamanho_cobra)
        self.posicao = (x // tamanho_cobra * tamanho_cobra, y // tamanho_cobra * tamanho_cobra)

# Criando a cobrinha e a maçã
cobrinha = Cobrinha()
maca = Maca()

# Função para reiniciar o jogo
def reiniciar_jogo():
    cobrinha.__init__()  # Reinicia a cobra
    maca.mover()  # Move a maçã para uma nova posição


# Loop principal do jogo
rodando = True
clock = pygame.time.Clock()
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and cobrinha.direcao != 'esquerda':
                cobrinha.direcao = 'direita'
            elif event.key == pygame.K_LEFT and cobrinha.direcao != 'direita':
                cobrinha.direcao = 'esquerda'
            elif event.key == pygame.K_UP and cobrinha.direcao != 'baixo':
                cobrinha.direcao = 'cima'
            elif event.key == pygame.K_DOWN and cobrinha.direcao != 'cima':
                cobrinha.direcao = 'baixo'

    cobrinha.atualizar()

    if cobrinha.colisao():
        reiniciar_jogo()

    cobrinha.comer(maca)

    tela.fill(PRETO)

    cobrinha.desenhar()
    maca.desenhar()

    pygame.display.flip()

    clock.tick(velocidade_cobra)



# Encerramento do Pygame
pygame.quit()
