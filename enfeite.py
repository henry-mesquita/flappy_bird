import pygame as pg
from constants import *
from pygame import Vector2

class Enfeite:
    def __init__(
            self,
            tela: pg.Surface,
            sprite: pg.Surface,
            posicao: Vector2,
            velocidade: Vector2,
            dimensoes_sprite: Vector2
    ) -> None:
        """
        Inicializa o enfeite com suas características iniciais.

        Args:
            tela (pg.Surface): Superfície na qual é desenhado o enfeite.
            sprite (pg.Surface): Sprite do enfeite.
            posicao (Vector2): Posição inicial do enfeite.
            velocidade (Vector2): Velocidade do enfeite.
            dimensoes_sprite (Vector2): Dimensões dos sprites do enfeite (largura, altura).

        Returns:
            None
        """
        self.tela: pg.Surface           = tela
        self.posicao: Vector2           = posicao
        self.sprite: pg.Surface         = pg.transform.scale(sprite, dimensoes_sprite)
        self.velocidade: pg.Surface     = velocidade
        self.dimensoes_sprite: Vector2  = dimensoes_sprite
    
    def movimentar(self, delta_time) -> None:
        """
        Move o enfeite na tela.

        Args:
            delta_time (float): Tempo decorrido desde o ultimo frame.

        Returns:
            None
        """
        self.posicao.x += self.velocidade.x * delta_time
        self.posicao.y += self.velocidade.y * delta_time

    def desenhar(self) -> None:
        """
        Desenha o enfeite na tela.

        Returns:
            None
        """
        self.tela.blit(self.sprite, self.posicao)
