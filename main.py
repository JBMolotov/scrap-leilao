import requests
from bs4 import BeautifulSoup

def extrair_informacoes_lote(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extrair informações do leilão
    leiloes = soup.select('.col-md-6 .card .card-body a:nth-child(1)')
    print("Quantidade de leilões para leitura: ", len(leiloes))
    print("Tempo estimado: ", int(len(leiloes) * 2 / 60), "minuto(s) e ", int(len(leiloes) * 2 % 60), "segundos")

    for i in range(0, len(leiloes), 2):

        link_leilao = leiloes[i].get('href')
        # titulo_leilao = soup.select()

        # Conseguir lista de lotes
        response = requests.get(link_leilao)
        soup = BeautifulSoup(response.content, 'html.parser')

        titulo_leilao = soup.select_one('.header-leilao h1').text.strip()

        # Extrair quantidade e link de lotes
        total_lotes = soup.select_one('.lista-lotes div:nth-child(1)').text.strip()
        total_lotes = ''.join(filter(str.isdigit, total_lotes))
        total_lotes = int(total_lotes)

        lote = soup.select_one('.lote .card-body .text-center a') # trocar pra select depois
        if not lote:
            return        
        link_lote = lote.get('href')

        # Extrair número do link
        numero_link = link_lote.split('/')
        numero_link = int(numero_link[4])

        # Extrair data da primeira praça
        soup.select_one('.header-leilao .row .col-lg-9 .small strong').decompose()
        data_primeira_praca = soup.select_one('.header-leilao .row .col-lg-9 .small')
        data_primeira_praca = data_primeira_praca.text.strip()[:10]

        for j in range(numero_link, numero_link + total_lotes):
            link_lote = lote.get('href')
            link_lote = link_lote.replace(str(numero_link), str(j))
               
            # Extrair informações de cada lote
            response = requests.get(link_lote)
            soup = BeautifulSoup(response.content, 'html.parser')

            titulo_lote = soup.select_one('.px-1 h4:nth-child(2)').text.strip()
            imagem_lote = soup.select_one('.carousel-item a')
            if imagem_lote:
                imagem_lote = imagem_lote.get('href')
            else:
                imagem_lote = "N/I"
            link_documento = soup.select_one('.arquivos-lote p a')
            if link_documento:
                link_documento = link_documento.get('href')
            else:
                link_documento = "N/I"
            valor_avaliacao = soup.select_one('h6:contains("Valor de Avaliação")')
            if valor_avaliacao:
                valor_avaliacao = valor_avaliacao.text.strip().replace('Valor de Avaliação: ', '')
            else:
                valor_avaliacao = "N/I"
            valor_segunda_praca = soup.select_one('h6:contains("Lance Inicial")')
            if valor_segunda_praca:
                valor_segunda_praca = valor_segunda_praca.text.strip().replace('Lance Inicial: ', '')
            else:
                valor_segunda_praca = "N/I"
            endereco = soup.select_one('h5:contains("Local")')
            if endereco:
                endereco = endereco.find_parent('div')
                endereco = endereco.text.strip().replace('Localização do Imóvel', '').replace('Endereço:', '').replace('\n', '').replace('                 ', '').replace('Cidade:', ', Cidade:')
            else:
                endereco = "N/I"
                
            # # Imprimir as informações
            # print('Título do leilão:', titulo_leilao)
            # print('Link do Leilão:', link_leilao)
            # print('Total de Lotes:', total_lotes)
            # print('Data da Primeira Praça:', data_primeira_praca)

            # print(lote)
            # # print(link_lote)

            # print('Título do lote:', titulo_lote)
            # print('Imagem do lote:', imagem_lote)
            # print('Link do documento:', link_documento)
            # print('Valor de avaliação:', valor_avaliacao)
            # print('Valor da segunda praça:', valor_segunda_praca)
            # print('Endereço:', endereco)

            # Escrever as informações em um arquivo
            with open('Agostinho Leilões lotes.txt', "a") as arquivo:
                # arquivo.write('Título do leilão: ' + titulo_leilao + '\n')
                # arquivo.write('Link do Leilão: ' + link_leilao + '\n')
                # arquivo.write('Total de Lotes: ' + total_lotes + '\n')
                arquivo.write('Título do lote: ' + titulo_lote + '\n')
                arquivo.write('Data da Primeira Praça: ' + data_primeira_praca + '\n')
                arquivo.write('Imagem do lote: ' + imagem_lote + '\n')
                arquivo.write('Link do documento: ' + link_documento + '\n')
                arquivo.write('Valor de avaliação: ' + valor_avaliacao + '\n')
                arquivo.write('Valor da segunda praça: ' + valor_segunda_praca + '\n')
                arquivo.write('Endereço: ' + endereco + '\n')
                arquivo.write('Link do Lote: ' + link_lote + '\n')
                arquivo.write('\n')

    print('Arquivo salvo com sucesso!')

extrair_informacoes_lote('https://agostinholeiloes.com.br/')

# # Path: main.py
