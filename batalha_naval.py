class BatalhaNaval:
    def __init__(self):
        self.tabuleiro_j1 = [[' ' for _ in range(15)] for _ in range(15)]
        self.tabuleiro_j2 = [[' ' for _ in range(15)] for _ in range(15)]
        self.pontuacao_j1 = 0
        self.pontuacao_j2 = 0

    def validar_posicao(self, posicao):
        letra, numero = posicao[:-1], int(posicao[-1])
        if letra not in 'ABCDEFGHIJKLMNO' or numero < 1 or numero > 15:
            return False
        return True

    def posicionar_peca(self, tabuleiro, codigo, posicao, direcao):
        if not self.validar_posicao(posicao):
            return False

        tamanho = 4 if codigo == 1 else 5

        if direcao == 'H':
            for i in range(tamanho):
                if tabuleiro[ord(posicao[0]) - ord('A') + i][int(posicao[1:]) - 1] != ' ':
                    return False
                tabuleiro[ord(posicao[0]) - ord('A') + i][int(posicao[1:]) - 1] = codigo
        elif direcao == 'V':
            for i in range(tamanho):
                if tabuleiro[ord(posicao[0]) - ord('A')][int(posicao[1:]) - 1 + i] != ' ':
                    return False
                tabuleiro[ord(posicao[0]) - ord('A')][int(posicao[1:]) - 1 + i] = codigo

        return True

    def validar_jogada(self, tabuleiro, posicoes):
        for posicao in posicoes:
            if not self.validar_posicao(posicao):
                return False
            letra, numero = posicao[:-1], int(posicao[-1])
            if tabuleiro[ord(letra) - ord('A')][numero - 1] == ' ':
                return False
        return True

    def processar_rodada(self, jogador, instrucoes):
        for instrucao in instrucoes:
            partes = instrucao.split(';')
            codigo = partes[0]
            posicoes = partes[1]
            
            if len(partes) == 3:
                direcao = partes[2]

            if codigo == 'T':
                if not self.validar_jogada(self.tabuleiro_j2 if jogador == 'J1' else self.tabuleiro_j1, posicoes.split('|')):
                    return f'{jogador} ERROR_POSITION_NONEXISTENT_VALIDATION'
                for posicao in posicoes.split('|'):
                    letra, numero = posicao[:-1], int(posicao[-1])
                    tabuleiro = self.tabuleiro_j2 if jogador == 'J1' else self.tabuleiro_j1
                    if tabuleiro[ord(letra) - ord('A')][numero - 1] != ' ':
                        codigo_peca = tabuleiro[ord(letra) - ord('A')][numero - 1]
                        tabuleiro[ord(letra) - ord('A')][numero - 1] = ' '
                        if codigo_peca == 3:
                            self.pontuacao_j1 += 3 if jogador == 'J1' else 3
                            self.pontuacao_j2 += 3 if jogador == 'J2' else 3
                        else:
                            parte_acertada = sum([1 for linha in tabuleiro for peca in linha if peca == codigo_peca])
                            self.pontuacao_j1 += 3 * parte_acertada if jogador == 'J1' else 0
                            self.pontuacao_j2 += 3 * parte_acertada if jogador == 'J2' else 0
                            if parte_acertada == (4 if codigo_peca == 1 else 5):
                                self.pontuacao_j1 += 5 if jogador == 'J1' else 0
                                self.pontuacao_j2 += 5 if jogador == 'J2' else 0
            else:
                if not self.posicionar_peca(self.tabuleiro_j1 if jogador == 'J1' else self.tabuleiro_j2, int(codigo), posicoes, ''):
                    return f'{jogador} ERROR_OVERWRITE_PIECES_VALIDATION'

        return None

    def validar_quantidade_pecas_tiros(self, instrucoes):
        quantidade_pecas_tiros = {'1': 0, '2': 0, '3': 0, '4': 0, 'T': 0}
        
        for instrucao in instrucoes:
            partes = instrucao.split(';')
            codigo = partes[0]
            posicoes = partes[1]
            
            if len(partes) == 3:
                direcao = partes[2]
            
            if codigo == 'T':
                quantidade_pecas_tiros['T'] += 1
            else:
                quantidade_pecas_tiros[codigo] += 1

        return (
            quantidade_pecas_tiros['1'] == 5 and
            quantidade_pecas_tiros['2'] == 2 and
            quantidade_pecas_tiros['3'] == 10 and
            quantidade_pecas_tiros['4'] == 5 and
            quantidade_pecas_tiros['T'] == 25
        )

    def jogar(self, arquivo_j1, arquivo_j2):
        with open(arquivo_j1, 'r') as f:
            instrucoes_j1 = f.read().strip().split('\n')
        with open(arquivo_j2, 'r') as f:
            instrucoes_j2 = f.read().strip().split('\n')

        if not self.validar_quantidade_pecas_tiros(instrucoes_j1) or not self.validar_quantidade_pecas_tiros(instrucoes_j2):
            return 'ERROR_NR_PARTS_VALIDATION'

        resultado_j1 = self.processar_rodada('J1', instrucoes_j1)
        if resultado_j1:
            return resultado_j1

        resultado_j2 = self.processar_rodada('J2', instrucoes_j2)
        if resultado_j2:
            return resultado_j2

        if self.pontuacao_j1 > self.pontuacao_j2:
            resultado = f'J1 {self.pontuacao_j1} {self.pontuacao_j2} {self.pontuacao_j1 - self.pontuacao_j2}'
        elif self.pontuacao_j2 > self.pontuacao_j1:
            resultado = f'J2 {self.pontuacao_j2} {self.pontuacao_j1} {self.pontuacao_j2 - self.pontuacao_j1}'
        else:
            resultado = f'EMPATE J1 {self.pontuacao_j1} {self.pontuacao_j2} {self.pontuacao_j1 - self.pontuacao_j2}\n' \
                        f'J2 {self.pontuacao_j2} {self.pontuacao_j1} {self.pontuacao_j2 - self.pontuacao_j1}'

        with open('resultado.txt', 'w') as f:
            f.write(resultado)

        return resultado

if __name__ == '__main__':
    jogo = BatalhaNaval()
    resultado = jogo.jogar('jogador1.txt', 'jogador2.txt')
    print(resultado)


