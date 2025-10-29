import pygame as pg
from pygame import Vector2

class Cano:
    def __init__(
            self,
            tela:               pg.Surface,
            sprite:             pg.Surface,
            posicao:            Vector2,
            velocidade:         Vector2,
            dimensoes_sprite:   Vector2,
            angulo:             int
    ) -> None:
        """
        Inicializa o cano com suas características iniciais.
        
        Args:
            tela (pg.Surface): Superfície na qual é desenhado o cano.
            sprite (pg.Surface): Sprite do cano.
            posicao (Vector2): Posição inicial do cano.
            velocidade (Vector2): Velocidade do cano.
            dimensoes_sprite (Vector2): Dimensões dos sprites do cano (largura, altura).
            angulo (int): Ângulo do cano (0 para cano superior, 180 para cano inferior).

        Returns:
            None
        """
        self.tela: pg.Surface           = tela
        self.posicao: Vector2           = posicao
        self.sprite: pg.Surface         = pg.transform.scale(sprite, dimensoes_sprite)
        self.velocidade: Vector2        = velocidade
        self.dimensoes_sprite: Vector2  = dimensoes_sprite
        self.angulo: int                = angulo

    def movimentar(self, delta_time: float) -> None:
        """
        Move o cano na tela.

        Args:
            delta_time (float): Tempo decorrido desde o ultimo frame.

        Returns:
            None
        """
        self.posicao.x += self.velocidade.x * delta_time
        self.posicao.y += self.velocidade.y * delta_time

    def desenhar(self) -> None:
        """
        Desenha o cano na tela.

        Returns:
            None
        """
        sprite_rotacionado = pg.transform.rotate(self.sprite, self.angulo)
        self.tela.blit(sprite_rotacionado, self.posicao)
