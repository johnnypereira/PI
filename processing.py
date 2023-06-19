import pandas as pd
import requests
import json
import re
import csv
import itertools

API_KEY = "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"
headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
link = "https://api.openai.com/v1/chat/completions"
id_modelo = "gpt-3.5-turbo-0301"

def get_comments(item):
    if item == 'iphone x':
        response = {
            'comentarios': [
                "Estou impressionado com a qualidade da câmera do iPhone X! As fotos saem nítidas e com cores vibrantes.",

                "A tela OLED do iPhone X é simplesmente incrível. As cores são vivas e os pretos são realmente profundos.",

                "A falta do botão Home pode ser um pouco confusa no início, mas depois de me acostumar, percebi o quão intuitivo é usar os gestos no iPhone X.",

                "A vida útil da bateria do iPhone X é decepcionante. Preciso recarregá-lo mais de uma vez por dia, mesmo com uso moderado.",

                "O Face ID é um recurso impressionante. É rápido, confiável e oferece uma camada extra de segurança para desbloquear o telefone.",

                "Acho o design do iPhone X muito elegante. As bordas de aço inoxidável e o vidro traseiro dão um toque premium ao dispositivo.",

                "A câmera frontal do iPhone X é ótima para selfies. A tecnologia de iluminação de retrato cria resultados impressionantes.",

                "A capacidade de armazenamento do iPhone X é um pouco limitada. Com tantos aplicativos e fotos, é fácil encher o espaço rapidamente.",

                "Adoro a fluidez do sistema operacional iOS no iPhone X. Tudo funciona de maneira suave e responsiva.",

                "A resistência à água do iPhone X é um recurso conveniente. Posso usar o telefone na chuva sem me preocupar.",

                "O recurso Animoji no iPhone X é hilário! É divertido criar emojis animados com base nas minhas expressões faciais.",

                "O tamanho compacto do iPhone X é perfeito para uso com uma mão. É confortável segurá-lo e usar o telefone durante longos períodos.",

                "A ausência do conector de fones de ouvido tradicional é frustrante. Preciso usar um adaptador ou fones de ouvido sem fio.",

                "O desempenho do processador no iPhone X é impressionante. Os aplicativos abrem rapidamente e a multitarefa é suave.",

                "A falta de um leitor de impressão digital no iPhone X é um inconveniente. Às vezes, preferiria desbloquear o telefone com minha digital.",

                "A capacidade de capturar vídeos em 4K no iPhone X é excelente. As gravações ficam nítidas e cheias de detalhes.",

                "A tecnologia TrueDepth do iPhone X permite desbloquear o telefone com facilidade, mesmo em condições de pouca luz.",

                "A duração da bateria no iPhone X melhorou consideravelmente após a atualização do sistema operacional. Agora consigo usar o telefone o dia todo sem precisar recarregar.",

                "O iPhone X é extremamente caro para o que oferece. Existem opções mais acessíveis no mercado com recursos similares.",

                "A durabilidade do vidro traseiro do iPhone X é questionável. É preciso ter muito cuidado para evitar arranhões e rachaduras.",

                "O armazenamento limitado do iPhone X é um grande inconveniente. É frustrante ter que constantemente gerenciar o espaço para evitar ficar sem memória.",

                "A qualidade das chamadas no iPhone X deixa a desejar. Muitas vezes tenho problemas de áudio e a conexão parece fraca.",

                "O reconhecimento facial do Face ID no iPhone X falha com frequência. É frustrante ter que inserir a senha manualmente várias vezes ao dia.",

                "A qualidade das fotos tiradas com o iPhone X é decente, mas não tão impressionante quanto eu esperava.",

                "O tamanho da tela do iPhone X é adequado, mas sinto falta de um pouco mais de espaço para visualizar conteúdo.",

                "O desempenho geral do iPhone X é bom, mas percebo algumas pequenas quedas de velocidade ao alternar entre aplicativos pesados."
            ],
            'preço': '2500.00',
            'imagem-url': 'https://i.zst.com.br/thumbs/12/3/39/-13306456.jpg'
            
        }
        return response
    



def classify_comments(comments):
    classifications = {
        "comentario": [],
        "polaridade": [],
        "caracteristicas": []
    }
    
    for i in comments:
        msg_user = f"Comentário: {i} Características: [Lista das características mencionadas no comentário] Polaridade: [Polaridade do sentimento expresso no comentário] retorne apenas as características e a polaridade"

        body_msg = {
            "model": id_modelo,
            "messages": [{"role": "user", "content": msg_user}]
        }
        body_msg = json.dumps(body_msg)

        request = requests.post(link, headers=headers, data=body_msg)

        resposta = request.json()

        try:
            mensagem = resposta["choices"][0]["message"]["content"]

            polaridade_match = re.search(r'Polaridade:\s*(\w+)', mensagem)
            if polaridade_match:
                polaridade = polaridade_match.group(1).lower()
                if polaridade == "positiva":
                    polaridade = "positivo"
                elif polaridade == "negativa":
                    polaridade = "negativo"
                else:
                    polaridade = "neutro"

            caracteristicas_match = re.search(r'Características:\s*(.*?)\n', mensagem)
            if caracteristicas_match:
                caracteristicas = caracteristicas_match.group(1).strip()
            else:
                caracteristicas = None

            classifications["comentario"].append(i)
            classifications["polaridade"].append(polaridade)
            classifications["caracteristicas"].append(caracteristicas)

        except KeyError:
            pass
        
    return classifications

    

def evaluate_comments(classified):
    polaridades = classified['polaridade']

    valores_polaridades = {
        'positiva': 1,
        'neutra': 0,
        'negativa': -1,
        'positivo': 1,
        'neutro': 0,
        'negativo': -1,
    }

    score_ponderado = 0
    total_polaridades = len(polaridades)

    try:
        for polaridade in polaridades:
            polaridade_lower = polaridade.lower()
            if polaridade_lower in valores_polaridades:
                score_ponderado += valores_polaridades[polaridade_lower]
            else:
                pass
    except (KeyError, AttributeError) as e:
        pass

    score_normalizado = (score_ponderado / total_polaridades) * 100

    primeiras_caracteristicas = classified['caracteristicas'][:3]

    return score_normalizado, primeiras_caracteristicas





