import sys
import re
import os

def processar_arquivo(arquivo_entrada, arquivo_saida):
    with open(arquivo_entrada, 'r') as entrada:
        conteudo = entrada.read()

    conteudo_processado = processar_conteudo(conteudo)

    with open(arquivo_saida, 'w') as saida:
        saida.write(conteudo_processado)

def processar_conteudo(conteudo):
    # Remove comentários de múltiplas linhas (/* ... */) em todo o conteúdo
    conteudo = re.sub(r'/\*.*?\*/', '', conteudo, flags=re.DOTALL)

    # Agora processa cada linha individualmente
    linhas = conteudo.split('\n')
    linhas_processadas = []
    for linha in linhas:
        if linha.strip() == '':
            continue
        linha = remover_comentarios_e_espacos(linha)
        linha = expandir_biblioteca(linha)
        if linha:
            linhas_processadas.append(linha)
    return ''.join(linhas_processadas)  # Junta as linhas sem espaço extra

def remover_comentarios_e_espacos(linha):
    # Remove comentários de linha única (//)
    linha = re.sub(r'//.*', '', linha)

    # Divide a linha em partes, preservando strings
    partes = re.split(r'("[^"]*"|\'[^\']*\')', linha)
    for i in range(0, len(partes), 2):
        # Substitui múltiplos espaços por um único espaço nas partes fora de strings
        partes[i] = re.sub(r'\s+', ' ', partes[i])

        # Mantém espaço após palavras-chave específicas
        partes[i] = re.sub(r'\b(if|for|while|return|int|float|char|void)\s+', r'\1 ', partes[i])

        # Remove espaços ao redor dos operadores
        partes[i] = re.sub(r'\s*([+\-*/=<>!&|^%]+)\s*', r'\1', partes[i])

        # Remove espaços ao redor de chaves, colchetes e pontos e vírgulas
        partes[i] = re.sub(r'\s*([{};])\s*', r'\1', partes[i])

        # Remove espaços antes de parênteses em chamadas de função, mas mantém após palavras-chave
        partes[i] = re.sub(r'\b(if|for|while)\s*\(', r'\1(', partes[i])  # Sem espaço antes de parênteses após palavras-chave
        partes[i] = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*)\s+\(', r'\1(', partes[i])  # Nomes de função e parênteses de abertura

        # Remove espaços depois das vírgulas
        partes[i] = re.sub(r',\s*', ',', partes[i])

        # Remove espaços em branco no início e no final de cada parte
        partes[i] = partes[i].strip()

    # Reúne partes e garante que não haja espaços extras ao redor de chaves e pontos e vírgulas
    linha_final = ''.join(partes)
    linha_final = re.sub(r'\s*([{};])\s*', r'\1', linha_final)

    return linha_final

def expandir_biblioteca(linha):
    if linha.startswith("#include"):
        match = re.match(r'#include\s*[<"]([^>"]+)[>"]', linha)
        if match:
            nome_biblioteca = match.group(1)

            # Lista de locais comuns para arquivos de cabeçalho C, priorizando o diretório atual
            caminhos_busca = [
                '.',  # Diretório atual
                '/usr/include',
                '/usr/local/include',
                '/usr/lib/gcc/x86_64-linux-gnu/*/include',  # Ajuste para o seu sistema
            ]

            for caminho in caminhos_busca:
                caminho_completo = os.path.join(caminho, nome_biblioteca)
                if os.path.exists(caminho_completo):
                    try:
                        with open(caminho_completo, "r") as biblioteca:
                            return biblioteca.read()
                    except IOError:
                        print(f"Aviso: Não foi possível ler a biblioteca '{nome_biblioteca}' no caminho: {caminho_completo}")
                        return linha

            print(f"Aviso: Biblioteca '{nome_biblioteca}' não encontrada em nenhum dos caminhos de busca.")
            return linha
        else:
            print(f"Aviso: Diretiva #include malformada: {linha}")
            return linha
    return linha

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python preprocessor.py <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)

    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2]
    processar_arquivo(arquivo_entrada, arquivo_saida)
