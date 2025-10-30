import os
import pygame as pg
import neat
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
    redes: list[neat.nn.FeedForwardNetwork] = []
    passaros: list[Passaro] = []
    ge = []

    jogo = FlappyBird(criar_passaro=False)
    clock = pg.time.Clock()

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        redes.append(net)
        g.fitness = 0
        ge.append(g)

        passaro = Passaro(
            tela=jogo.tela,
            sprites=[pg.image.load(os.path.join("img", f"flap{i}.png")).convert_alpha() for i in range(1, 4)],
            posicao=POSICAO_INICIAL_PASSARO.copy(),
            dimensoes_sprite=DIMENSOES_PASSARO.copy()
        )

        passaros.append(passaro)
    

    rodando = True
    idx_cano_atual = 0
    while rodando and len(passaros) > 0:
        delta_time = clock.tick(FRAMERATE) / 1000
    
        for event in pg.event.get():
            if event.type == pg.QUIT:
                rodando = False
                pg.quit()
                return
        
        jogo.resetar_enfeites()
        jogo.resetar_canos()

        if idx_cano_atual == QUANTIDADE_CANO:
            idx_cano_atual = 0
        
        cano_sup_ref = jogo.canos_sup[idx_cano_atual]
        cano_inf_ref = jogo.canos_inf[idx_cano_atual]
        x_passaro = passaros[0].posicao.x

        passou_do_cano = x_passaro > cano_sup_ref.posicao.x + DIMENSOES_CANO.x - 10
        if passou_do_cano:
            idx_cano_atual += 1
        
        for i, passaro in enumerate(passaros):
            entrada = (
                cano_sup_ref.posicao.x - passaro.posicao.x,
                cano_inf_ref.posicao.y - passaro.posicao.y,
                cano_sup_ref.posicao.y - passaro.posicao.y,
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

            colidiu_tela = (
                passaro.posicao.y < 0 or
                passaro.posicao.y + DIMENSOES_PASSARO.y > ALTURA_TELA - DIMENSOES_CHAO.y
            )

            colidiu_cano = False

            for cano in range(QUANTIDADE_CANO):
                x_passaro = passaro.posicao.x
                y_passaro = passaro.posicao.y
                x_cano_inf = jogo.canos_inf[cano].posicao.x
                y_cano_inf = jogo.canos_inf[cano].posicao.y
                rect_cano_inf = jogo.canos_inf[cano].sprite.get_rect(topleft=(x_cano_inf, y_cano_inf))

                x_cano = jogo.canos_sup[cano].posicao.x
                y_cano = jogo.canos_sup[cano].posicao.y
                rect_cano_sup = jogo.canos_sup[cano].sprite.get_rect(topleft=(x_cano, y_cano))

                try:
                    rect_passaro = passaro.sprite_rotacionado.get_rect(topleft=(x_passaro, y_passaro))
                except AttributeError:
                    rect_passaro = passaro.sprites[passaro.frame_atual - 1].get_rect(topleft=(x_passaro, y_passaro))

                colisao_superior: bool = rect_passaro.colliderect(rect_cano_inf)
                colisao_inferior: bool = rect_passaro.colliderect(rect_cano_sup)

                if colisao_superior or colisao_inferior:
                    colidiu_cano = True
            
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

        for chao in jogo.chaos:
            chao.movimentar(delta_time)
            chao.desenhar()

        for passaro in passaros:
            passaro.desenhar()
        
        jogo.escrever_texto(f"Individuos: {len(passaros)}", LARGURA_TELA // 2, 30)
        pg.display.flip()

        if len(passaros) == 0:
            rodando = False

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

    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())
    populacao.run(eval_genomes, 100)

if __name__ == "__main__":
    caminho_config = os.path.join(os.path.dirname(__file__), "config-feedforward.txt")
    rodar(caminho_config)
