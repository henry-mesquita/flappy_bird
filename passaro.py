import pygame as pg
from pygame import Vector2
from constants import *

class Passaro:
    def __init__(
            self,
            tela:               pg.Surface,
            sprites:            list[pg.Surface],
            posicao:            Vector2,
            dimensoes_sprite:   Vector2
    ) -> None:
        """
        Inicializa o passaro com suas características iniciais.
        Args:
            tela (pg.Surface): Superfície na qual é desenhado o passaro.
            sprites (list[pg.Surface]): Sprites do passaro.
            posicao (Vector2): Posição inicial do passaro.
            dimensoes_sprite (Vector2): Dimensões dos sprites do passaro (largura, altura).
        Returns:
            None
        """
        self.tela: pg.Surface           = tela
        self.posicao: Vector2           = posicao
        self.sprites: list[pg.Surface]  = [pg.transform.scale(sprite, dimensoes_sprite) for sprite in sprites]
        self.velocidade_y: float        = 0
        self.dimensoes_sprite: Vector2  = dimensoes_sprite
        self.frame_atual: int           = 0
        self.tempo_animacao: float      = 0.0
        self.intervalo_frame: float     = 0.07
        self.angulo: int                = -20

    def aplicar_gravidade(self, delta_time: float) -> None:
        """
        Aplica a gravidade ao passaro.

        Args:
            delta_time (float): Tempo decorrido desde o ultimo frame.
        Returns:
            None
        """
        self.velocidade_y   += CONSTANTE_GRAVITACIONAL * delta_time
        self.posicao.y      += self.velocidade_y * delta_time

    def aplicar_pulo(self) -> None:
        """
        Aplica o pulo ao passaro.

        Returns:
            None
        """
        self.angulo = -20
        self.velocidade_y = -FORCA_PULO
    
    def aplicar_animacao(self, delta_time: float) -> None:
        """
        Aplica a animação ao passaro.

        Args:
            delta_time (float): Tempo decorrido desde o ultimo frame.
        Returns:
            None
        """
        self.tempo_animacao += delta_time
        if self.tempo_animacao > self.intervalo_frame:
            self.tempo_animacao = 0
            if self.frame_atual > len(self.sprites) - 1:
                self.frame_atual = 0
            else:
                self.frame_atual += 1
    
    def aplicar_angulo(self, delta_time: float) -> None:
        """
        Aplica o ângulo ao passaro.

        Args:
            delta_time (float): Tempo decorrido desde o ultimo frame.
        Returns:
            None
        """
        self.angulo = self.angulo + VELOCIDADE_ANGULO * delta_time
        self.sprite_rotacionado = pg.transform.rotate(self.sprites[self.frame_atual - 1], max(-100, -self.angulo))

    def desenhar(self) -> None:
        """
        Desenha o passaro na tela.

        Returns:
            None
        """
        self.tela.blit(self.sprite_rotacionado, self.posicao)
