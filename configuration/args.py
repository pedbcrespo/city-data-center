import argparse

parser = argparse.ArgumentParser(description="Argumento para executar o projeto em modo local sem o uso do Docker.")
parser.add_argument('--dev', action='store_true', help='Ativa o modo de desenvolvimento local sem o uso do Docker.')
args = parser.parse_args()

