import pygame as pg
from pygame import Vector2
from constants import *
from cano import Cano
from passaro import Passaro
from enfeite import Enfeite
from os.path import join
from time import time
from random import randint

class FlappyBird:
    def __init__(self, criar_passaro: bool = True) -> None:
        """
        Inicializa o jogo Flappy Bird.

        Returns:
            None
        """
        pg.init()
        pg.display.set_caption('Flappy Bird')
        self.tela: pg.Surface = pg.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        self.clock: pg.time.Clock = pg.time.Clock()
        self.passaro_morto = False
        self.tempo_inicial = 0
        self.caminho_pasta_img = join('img')
        self.caminho_pasta_font = join('font')
        self.criar_enfeites()
        if criar_passaro:
            self.criar_passaro()
        self.criar_canos()
        self.atualizar_icone()
        self.teclas_permitidas = [pg.K_UP, pg.K_SPACE]
        self.pontuacao = 0
        
        if QUANTIDADE_CANO > 0:
            self.idx_cano_atual = 0
    
    def atualizar_icone(self) -> None:
        """
        Atualiza o icone do jogo.

        Returns:
            None
        """
        icone = pg.image.load(join(self.caminho_pasta_img, 'flap1.png')).convert_alpha()
        pg.display.set_icon(icone)
    
    def escrever_texto(self, info: str | int, x: int, y: int, tamanho: int = 30) -> None:
        """
        Escreve um texto na tela.

        Args:
            info (str): Texto que será escrito na tela.
            x (int): Coordenada X do texto.
            y (int): Coordenada Y do texto.
        Returns:
            None
        """
        fonte = pg.font.Font(join(self.caminho_pasta_font, 'flappy_bird.ttf'), tamanho)
        superficie_texto = fonte.render(str(info), True, (255, 255, 255))
        retangulo_texto = superficie_texto.get_rect(center=(x, y))
        self.tela.blit(superficie_texto, retangulo_texto)

    def atualizar_placar(self) -> None:
        """
        Atualiza e desenha o placar do jogo.

        Returns:
            None
        """
        if self.idx_cano_atual == QUANTIDADE_CANO:
            self.idx_cano_atual = 0
        cano_atual: Cano = self.canos_sup[self.idx_cano_atual]
        x_cano_atual = cano_atual.posicao.x
        x_passaro = self.passaro.posicao.x
        passou_do_cano: bool = x_passaro > x_cano_atual + DIMENSOES_CANO.x
        if passou_do_cano:
            self.pontuacao += 1
            self.idx_cano_atual += 1
        self.escrever_texto(self.pontuacao, x=LARGURA_TELA // 2, y=100, tamanho=70)

    def criar_enfeites(self) -> None:
        """
        Cria os enfeites do jogo (fundo, chão, nuvens, prédios e árvores).

        Returns:
            None
        """
        caminho_sprite_fundo        = join(self.caminho_pasta_img, 'fundo.png')
        caminho_sprite_chao         = join(self.caminho_pasta_img, 'chao.png')
        caminho_sprite_nuvem        = join(self.caminho_pasta_img, 'nuvens.png')
        caminho_sprite_predio       = join(self.caminho_pasta_img, 'predios.png')
        caminho_sprite_arvore       = join(self.caminho_pasta_img, 'arvores.png')

        sprite_fundo: pg.Surface    = pg.image.load(caminho_sprite_fundo).convert_alpha()
        sprite_chao: pg.Surface     = pg.image.load(caminho_sprite_chao).convert_alpha()
        sprite_nuvem: pg.Surface    = pg.image.load(caminho_sprite_nuvem).convert_alpha()
        sprite_predio: pg.Surface   = pg.image.load(caminho_sprite_predio).convert_alpha()
        sprite_arvore: pg.Surface   = pg.image.load(caminho_sprite_arvore).convert_alpha()

        self.fundo = Enfeite(
            tela=self.tela,
            sprite=sprite_fundo,
            posicao=Vector2(0, 0),
            velocidade=Vector2(0, 0),
            dimensoes_sprite=Vector2(LARGURA_TELA, ALTURA_TELA)
        )

        self.chaos: list[Enfeite] = []
        for chao in range(QUANTIDADE_CHAO):
            x_chao = 0 + (DIMENSOES_CHAO.x * chao)
            y_chao = ALTURA_TELA - DIMENSOES_CHAO.y
            self.chaos.append(Enfeite(
                tela=self.tela,
                sprite=sprite_chao,
                posicao=Vector2(x_chao, y_chao),
                velocidade=VELOCIDADE_CHAO.copy(),
                dimensoes_sprite=DIMENSOES_CHAO.copy()
            ))

        self.arvores: list[Enfeite] = []
        for arvore in range(QUANTIDADE_ARVORE):
            x_arvore = 0 + (DIMENSOES_ARVORE.x * arvore)
            y_arvore = ALTURA_TELA - (DIMENSOES_CHAO.y + DIMENSOES_ARVORE.y)
            self.arvores.append(Enfeite(
                tela=self.tela,
                sprite=sprite_arvore,
                posicao=Vector2(x_arvore, y_arvore),
                velocidade=VELOCIDADE_ARVORE.copy(),
                dimensoes_sprite=DIMENSOES_ARVORE.copy()
            ))

        self.predios: list[Enfeite] = []
        for predio in range(QUANTIDADE_PREDIO):
            x_predio = 0 + (DIMENSOES_PREDIO.x * predio)
            y_predio = ALTURA_TELA - (DIMENSOES_CHAO.y + DIMENSOES_ARVORE.y + DIMENSOES_PREDIO.y - 10)
            self.predios.append(Enfeite(
                tela=self.tela,
                sprite=sprite_predio,
                posicao=Vector2(x_predio, y_predio),
                velocidade=VELOCIDADE_PREDIO.copy(),
                dimensoes_sprite=DIMENSOES_PREDIO.copy()
            ))

        self.nuvens: list[Enfeite] = []
        for nuvem in range(QUANTIDADE_NUVEM):
            x_nuvem = 0 + (DIMENSOES_NUVEM.x * nuvem)
            y_nuvem = ALTURA_TELA - (DIMENSOES_CHAO.y + DIMENSOES_ARVORE.y + DIMENSOES_PREDIO.y + 20)
            self.nuvens.append(Enfeite(
                tela=self.tela,
                sprite=sprite_nuvem,
                posicao=Vector2(x_nuvem, y_nuvem),
                velocidade=VELOCIDADE_NUVEM.copy(),
                dimensoes_sprite=DIMENSOES_NUVEM.copy()
            ))

    def criar_passaro(self) -> None:
        """
        Cria o passaro do jogo.

        Returns:
            None
        """
        caminhos: list[str] = [
            join(self.caminho_pasta_img, 'flap1.png'),
            join(self.caminho_pasta_img, 'flap2.png'),
            join(self.caminho_pasta_img, 'flap3.png')
        ]

        frames: list[pg.Surface] = [
            pg.image.load(caminhos[0]).convert_alpha(),
            pg.image.load(caminhos[1]).convert_alpha(),
            pg.image.load(caminhos[2]).convert_alpha()
        ]

        self.passaro: Passaro = Passaro(
            tela=self.tela,
            sprites=frames,
            posicao=POSICAO_INICIAL_PASSARO.copy(),
            dimensoes_sprite=DIMENSOES_PASSARO.copy()
        )

    def criar_canos(self) -> None:
        """
        Cria os canos do jogo.

        Returns:
            None
        """
        caminho_sprite_cano = join(self.caminho_pasta_img, 'cano.png')
        sprite_cano         = pg.image.load(caminho_sprite_cano).convert_alpha()

        self.canos_sup: list[Cano] = []
        self.canos_inf: list[Cano] = []

        for cano in range(QUANTIDADE_CANO):
            x_cano_sup = LARGURA_TELA + DIMENSOES_CANO.x * (cano + 1) + DISTANCIA_ENTRE_CANOS * (cano + 1)
            x_cano_inf = LARGURA_TELA + DIMENSOES_CANO.x * (cano + 1) + DISTANCIA_ENTRE_CANOS * (cano + 1)

            rng = randint(
                int((ALTURA_TELA - DIMENSOES_CHAO.y) // 2 - CONSTANTE_RNG),
                int((ALTURA_TELA - DIMENSOES_CHAO.y) // 2  + CONSTANTE_RNG)
            )

            y_cano_sup = rng - DIMENSOES_CANO.y - ABERTURA_CANO
            y_cano_inf = rng + ABERTURA_CANO

            self.canos_sup.append(Cano(
                tela=self.tela,
                sprite=sprite_cano,
                posicao=Vector2(x_cano_sup, y_cano_sup),
                velocidade=VELOCIDADE_CANO.copy(),
                dimensoes_sprite=DIMENSOES_CANO.copy(),
                angulo=0
            ))
            
            self.canos_inf.append(Cano(
                tela=self.tela,
                sprite=sprite_cano,
                posicao=Vector2(x_cano_inf, y_cano_inf),
                velocidade=VELOCIDADE_CANO.copy(),
                dimensoes_sprite=DIMENSOES_CANO.copy(),
                angulo=180
            ))

    def resetar_enfeites(self) -> None:
        """
        Reseta o enfeite do jogo quando ele ultrapassa o lado esquerdo da tela.

        Returns:
            None
        """
        for chao in self.chaos:
            if chao.posicao.x + DIMENSOES_CHAO.x < 0:
                chao.posicao.x += (QUANTIDADE_CHAO - 1) * DIMENSOES_CHAO.x

        for arvore in self.arvores:
            if arvore.posicao.x + DIMENSOES_ARVORE.x < 0:
                arvore.posicao.x += (QUANTIDADE_ARVORE - 1) * DIMENSOES_ARVORE.x

        for predio in self.predios:
            if predio.posicao.x + DIMENSOES_PREDIO.x < 0:
                predio.posicao.x += (QUANTIDADE_PREDIO - 1) * DIMENSOES_PREDIO.x

        for nuvem in self.nuvens:
            if nuvem.posicao.x + DIMENSOES_NUVEM.x < 0:
                nuvem.posicao.x += (QUANTIDADE_NUVEM - 1) * DIMENSOES_NUVEM.x

    def resetar_canos(self) -> None:
        """
        Reseta o cano do jogo quando ele ultrapassa o lado esquerdo da tela.

        Returns:
            None
        """
        offset_cano = QUANTIDADE_CANO * DIMENSOES_CANO.x + DISTANCIA_ENTRE_CANOS * QUANTIDADE_CANO
        for cano in range(QUANTIDADE_CANO):
            if self.canos_sup[cano].posicao.x + DIMENSOES_CANO.x < 0:
                self.canos_sup[cano].posicao.x += offset_cano
                self.canos_inf[cano].posicao.x += offset_cano
                rng = randint(
                    int((ALTURA_TELA - DIMENSOES_CHAO.y) // 2 - CONSTANTE_RNG),
                    int((ALTURA_TELA - DIMENSOES_CHAO.y) // 2  + CONSTANTE_RNG)
                )

                novo_y_cano_sup = 0 - DIMENSOES_CANO.y + rng - ABERTURA_CANO
                novo_y_cano_inf = rng + ABERTURA_CANO

                self.canos_sup[cano].posicao.y = novo_y_cano_sup
                self.canos_inf[cano].posicao.y = novo_y_cano_inf

    def verificar_colisao_canos(self, passaro: Passaro) -> bool:
        """
        Verifica se o passaro colidiu com o cano.

        Args:
            passaro (Passaro): O passaro a ser verificado.
        Returns:
            bool: True se houver colisão, False caso contrário.
        """
        for cano in range(QUANTIDADE_CANO):
            x_passaro = passaro.posicao.x
            y_passaro = passaro.posicao.y
            x_cano_inf = self.canos_inf[cano].posicao.x
            y_cano_inf = self.canos_inf[cano].posicao.y
            rect_cano_inf = self.canos_inf[cano].sprite.get_rect(topleft=(x_cano_inf, y_cano_inf))

            x_cano = self.canos_sup[cano].posicao.x
            y_cano = self.canos_sup[cano].posicao.y
            rect_cano_sup = self.canos_sup[cano].sprite.get_rect(topleft=(x_cano, y_cano))

            try:
                rect_passaro = passaro.sprite_rotacionado.get_rect(topleft=(x_passaro, y_passaro))
            except AttributeError:
                rect_passaro = passaro.sprites[self.passaro.frame_atual - 1].get_rect(topleft=(x_passaro, y_passaro))

            colisao_superior = rect_passaro.colliderect(rect_cano_inf)
            colisao_inferior = rect_passaro.colliderect(rect_cano_sup)

            if colisao_superior or colisao_inferior:
                return True
        return False

    def verificar_colisao_tela(self, passaro: Passaro) -> bool:
        """
        Verifica se o passaro colidiu com o teto ou com o chão.

        Args:
            passaro (Passaro): O passaro a ser verificado.
        Returns:
            bool: True se houver colisão, False caso contrário.
        """
        return self.verificar_colisao_teto(passaro) or self.verificar_colisao_chao(passaro)
        
    def verificar_colisao_chao(self, passaro: Passaro) -> bool:
        """
        Verifica se o passaro colidiu com o chão.

        Args:
            passaro (Passaro): O passaro a ser verificado.
        Returns:
            bool: True se houver colisão, False caso contrário.
        """
        return passaro.posicao.y + DIMENSOES_PASSARO.y > ALTURA_TELA - DIMENSOES_CHAO.y

    def verificar_colisao_teto(self, passaro: Passaro) -> bool:
        """
        Verifica se o passaro colidiu com o teto.

        Args:
            passaro (Passaro): O passaro a ser verificado.
        Returns:
            bool: True se houver colisão, False caso contrário.
        """
        return passaro.posicao.y < 0

    def zerar_velocidade_tudo(self) -> None:
        """
        Zera a velocidade de todos os elementos do jogo.

        Returns:
            None
        """
        for cano_inf in self.canos_inf:
            cano_inf.velocidade = Vector2(0, 0)
        
        for cano_sup in self.canos_sup:
            cano_sup.velocidade = Vector2(0, 0)
        
        for predio in self.predios:
            predio.velocidade = Vector2(0, 0)
        
        for arvore in self.arvores:
            arvore.velocidade = Vector2(0, 0)
        
        for nuvem in self.nuvens:
            nuvem.velocidade = Vector2(0, 0)
        
        for chao in self.chaos:
            chao.velocidade = Vector2(0, 0)

    def reiniciar_velocidade_tudo(self) -> None:
        """
        Reinicia a velocidade de todos os elementos do jogo (mantendo o parallax).

        Returns:
            None
        """
        for cano_inf in self.canos_inf:
            cano_inf.velocidade = VELOCIDADE_CANO
        
        for cano_sup in self.canos_sup:
            cano_sup.velocidade = VELOCIDADE_CANO
        
        for predio in self.predios:
            predio.velocidade = VELOCIDADE_PREDIO
        
        for arvore in self.arvores:
            arvore.velocidade = VELOCIDADE_ARVORE
        
        for nuvem in self.nuvens:
            nuvem.velocidade = VELOCIDADE_NUVEM
        
        for chao in self.chaos:
            chao.velocidade = VELOCIDADE_CHAO

    def verificar_morte(self, delta_time) -> bool:
        """
        Verifica se o passaro colidiu com a tela ou com o cano.

        Returns:
            bool: True se houver colisão, False caso contrário.
        """
        if self.verificar_colisao_canos(self.passaro):
            if not self.passaro_morto:
                self.passaro.velocidade_y = 0
                self.passaro_morto = True
            self.resetar_jogo(delta_time)
        if self.verificar_colisao_tela(self.passaro):
            if not self.passaro_morto:
                self.passaro.velocidade_y = 0
                self.passaro_morto = True
            self.resetar_jogo(delta_time)

    def resetar_jogo(self, delta_time: float) -> None:
        """
        Reseta o jogo para o estado inicial.

        Args:
            delta_time (float): Tempo decorrido desde o ultimo frame.

        Returns:
            None
        """
        self.zerar_velocidade_tudo()

        if self.tempo_inicial < 3:
            self.tempo_inicial += delta_time
            return

        self.pontuacao = 0
        self.idx_cano_atual = 0
        self.tempo_inicial          = 0
        self.passaro.velocidade_y   = 0
        self.passaro.posicao        = POSICAO_INICIAL_PASSARO.copy()
        self.passaro.angulo         = 0
        self.passaro_morto          = False
        
        for cano in range(QUANTIDADE_CANO):
            x_cano_sup = LARGURA_TELA + DIMENSOES_CANO.x * (cano + 1) + DISTANCIA_ENTRE_CANOS * (cano + 1)
            x_cano_inf = LARGURA_TELA + DIMENSOES_CANO.x * (cano + 1) + DISTANCIA_ENTRE_CANOS * (cano + 1)

            rng = randint(ALTURA_TELA // 2 - CONSTANTE_RNG, ALTURA_TELA // 2 + CONSTANTE_RNG)

            y_cano_sup = 0 - DIMENSOES_CANO.y + rng - ABERTURA_CANO
            y_cano_inf = rng + ABERTURA_CANO

            self.canos_sup[cano].posicao = Vector2(x_cano_sup, y_cano_sup)
            self.canos_inf[cano].posicao = Vector2(x_cano_inf, y_cano_inf)
            self.canos_sup[cano].velocidade = VELOCIDADE_CANO
            self.canos_inf[cano].velocidade = VELOCIDADE_CANO

        self.reiniciar_velocidade_tudo()

    def desenhar_tudo(self, delta_time: float) -> None:
        """
        Desenha todos os elementos do jogo.

        Args:
            delta_time (float): Tempo decorrido desde o ultimo frame.

        Returns:
            None
        """
        self.fundo.desenhar()

        for grupo in (self.nuvens, self.predios, self.arvores):
            for enfeite in grupo:
                enfeite.movimentar(delta_time)
                enfeite.desenhar()

        for cano in range(QUANTIDADE_CANO):
            self.canos_inf[cano].movimentar(delta_time)
            self.canos_inf[cano].desenhar()
            self.canos_sup[cano].movimentar(delta_time)
            self.canos_sup[cano].desenhar()

        self.passaro.desenhar()

        for chao in self.chaos:
            chao.movimentar(delta_time)
            chao.desenhar()

    def event_loop(self) -> None:
        """
        Loop de eventos.

        Returns:
            None
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key in self.teclas_permitidas and not self.passaro_morto:
                    self.passaro.aplicar_pulo()

    def run(self) -> None:
        """
        Método que executa o jogo.

        Returns:
            None
        """
        pg.init()
        self.running: bool = True

        last_time = time()
        while self.running:
            try:
                # ATUALIZAR
                current_time = time()
                delta_time = current_time - last_time
                last_time = current_time

                self.verificar_morte(delta_time)
                self.event_loop()
                self.resetar_enfeites()
                self.resetar_canos()
                if not self.verificar_colisao_chao(self.passaro):
                    self.passaro.aplicar_gravidade(delta_time)
                    self.passaro.aplicar_angulo(delta_time)
                if not self.passaro_morto:
                    self.passaro.aplicar_animacao(delta_time)

                # DESENHAR
                self.desenhar_tudo(delta_time)
                if QUANTIDADE_CANO > 0:
                    self.atualizar_placar()
                pg.display.flip()
                self.clock.tick(FRAMERATE)
            except KeyboardInterrupt:
                self.running = False
        pg.quit()
