import os
import pygame as pg
from pygame.time import Clock
import neat
from neat.nn import FeedForwardNetwork
from flappy import FlappyBird
from passaro import Passaro
from constants import *

def eval_genomes(genomes, config) -> None:
    """
    Função que evalua os genomas e cria os passaros.

    Args:
        genomes (list): Lista de genomas.
        config (neat.Config): Configuração do NEAT.

    Returns:
        None
    """
    redes:      list[FeedForwardNetwork]    = []
    ge:         list[neat.DefaultGenome]    = []
    passaros:   list[Passaro]               = []

    jogo: FlappyBird        = FlappyBird(criar_passaro=False, configuracoes_iniciais=True)
    clock: Clock            = Clock()

    for _, g in genomes:
        net: FeedForwardNetwork = FeedForwardNetwork.create(g, config)
        redes.append(net)
        g.fitness = 0
        ge.append(g)

        passaros.append(Passaro(
            tela=jogo.tela,
            posicao=POSICAO_INICIAL_PASSARO.copy(),
            dimensoes_sprite=DIMENSOES_PASSARO.copy(),
            hitbox=pg.Rect(
                POSICAO_INICIAL_PASSARO.x,
                POSICAO_INICIAL_PASSARO.y,
                DIMENSOES_PASSARO.x,
                DIMENSOES_PASSARO.y
            )
        ))

    class AbortTraining(Exception):
        pass

    rodando = True
    idx_cano_atual = 0
    while rodando and len(passaros) > 0:
        delta_time = clock.tick(FRAMERATE) / 1000
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                rodando = False
                raise AbortTraining()
        
        jogo.resetar_enfeites()
        jogo.resetar_canos()

        if idx_cano_atual == QUANTIDADE_CANO:
            idx_cano_atual = 0
        
        cano_sup_ref    = jogo.canos_sup[idx_cano_atual]
        cano_inf_ref    = jogo.canos_inf[idx_cano_atual]
        x_passaro       = passaros[0].posicao.x

        passou_do_cano = x_passaro > cano_sup_ref.posicao.x + DIMENSOES_CANO.x - 10
        if passou_do_cano:
            idx_cano_atual += 1
        
        for i, passaro in enumerate(passaros):
            entrada = (
                cano_sup_ref.posicao.x - passaro.posicao.x,
                cano_inf_ref.posicao.y - passaro.posicao.y,
                cano_sup_ref.posicao.y + DIMENSOES_CANO.y - passaro.posicao.y, # posição de entrada corrigida
                passaro.velocidade_y,
                passaro.angulo
            )

            output = redes[i].activate(entrada)
            if output[0] > 0.5:
                passaro.aplicar_pulo()
            
            passaro.aplicar_gravidade(delta_time)
            passaro.aplicar_angulo(delta_time)
            passaro.aplicar_animacao(delta_time)

            ge[i].fitness += 10

            passaro.atualizar_hitbox()

            colidiu_tela = jogo.verificar_colisao_tela(passaro)
            colidiu_cano = jogo.verificar_colisao_canos(passaro)
            
            if colidiu_tela or colidiu_cano:
                ge[i].fitness -= 50
                passaros.pop(i)
                redes.pop(i)
                ge.pop(i)
                continue

        jogo.fundo.desenhar()
        for grupo in (jogo.nuvens, jogo.predios, jogo.arvores):
            for enfeite in grupo:
                enfeite.movimentar(delta_time)
                enfeite.desenhar()

        for idx in range(QUANTIDADE_CANO):
            jogo.canos_inf[idx].movimentar(delta_time)
            jogo.canos_inf[idx].desenhar()
            jogo.canos_sup[idx].movimentar(delta_time)
            jogo.canos_sup[idx].desenhar()

        for passaro in passaros:
            passaro.desenhar()

        for chao in jogo.chaos:
            chao.movimentar(delta_time)
            chao.desenhar()

        global geracao

        jogo.escrever_texto(f"Individuos:{len(passaros)}", LARGURA_TELA // 2, 30)
        jogo.escrever_texto(f"Geracao:{geracao}", LARGURA_TELA // 2, 60)

        pg.display.flip()
        if len(passaros) == 0:
            geracao += 1
            rodando = False

geracao: int = 0

def rodar(config_path) -> None:
    """
    Função que executa o NEAT.

    Args:
        config_path (str): Caminho para o arquivo de configuração do NEAT.

    Returns:
        None
    """
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    global geracao
    populacao = neat.Population(config)
    geracao = populacao.generation
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())
    populacao.run(eval_genomes, 30)

if __name__ == "__main__":
    caminho_config = os.path.join(os.path.dirname(__file__), "config-feedforward.txt")
    rodar(caminho_config)
