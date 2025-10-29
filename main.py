from flappy import FlappyBird

def main() -> None:
    """
    Função principal do jogo.

    Returns:
        None
    """
    flappy: FlappyBird = FlappyBird()
    flappy.run()

if __name__ == '__main__':
    main()
