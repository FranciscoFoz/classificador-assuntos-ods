# GERADOR

import PyPDF2
import tempfile
from google import genai
from google.genai import types

class GeradorAssuntoODS:
    def __init__(self, api_key, caminho_pdf):
        self.client = self.configurar_client(api_key)
        self.caminho_pdf = caminho_pdf


    def configurar_client(self, api_key):
        client = genai.Client(api_key=api_key)
        return client

    def transformar_pdf_texto(self):
        arquivo_pdf = open(self.caminho_pdf, 'rb')
        leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
        texto = ''

        for pagina_num in range(len(leitor_pdf.pages)):
            page = leitor_pdf.pages[pagina_num]
            texto += page.extract_text()
            texto += '\n\n'

        arquivo_pdf.close()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w', encoding='utf-8') as arquivo_saida:
            arquivo_saida.write(texto)
            caminho_arquivo_txt = arquivo_saida.name

        return caminho_arquivo_txt

    def carregar_arquivo_genai(self, caminho_arquivo):
        arquivo = self.client.files.upload(
            file=caminho_arquivo,
            config=types.UploadFileConfig(
                display_name='pdf_texto'
            ),
            )
        return arquivo

    def processar_arquivo(self):
        caminho_txt = self.transformar_pdf_texto()
        arquivo = self.carregar_arquivo_genai(caminho_txt)

        return arquivo


    def get_safety_settings(self):
        return [
            {
                'category': 'HARM_CATEGORY_HARASSMENT',
                'threshold': 'BLOCK_NONE'
            },
            {
                'category': 'HARM_CATEGORY_HATE_SPEECH',
                'threshold': 'BLOCK_NONE'
            },
            {
                'category': 'HARM_CATEGORY_SEXUALLY_EXPLICIT',
                'threshold': 'BLOCK_NONE'
            },
            {
                'category': 'HARM_CATEGORY_DANGEROUS_CONTENT',
                'threshold': 'BLOCK_NONE'
            },
        ]
    def catalogar_assunto(self):
        arquivo = self.processar_arquivo()
        
        

        prompt = '''
        Catalogue os assuntos desse documento conforme o campo 653$a do MARC 21.

        - Analise o documento e insira apenas 5 assuntos/termos indexadores, em PT-BR, mais relevantes de acordo com o conteúdo.
        - Responda apenas os assuntos.
        - Liste os assuntos.
        - Não explique.
        - Não descreva o documento.
        - Não use frases.
        - Apenas devolva a lista final.
        '''
        
        
        response = self.client.models.generate_content(
            model='models/gemini-2.5-flash-lite',
            contents=[
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {
                        "file_data": {
                            "file_uri": arquivo.uri,
                            "mime_type": "text/plain"
                        }
                    }
                ]
            }
        ],
            config=types.GenerateContentConfig(
                safety_settings=self.get_safety_settings(),
                max_output_tokens=200,
                temperature=1,
                top_p=1,
                top_k=0
            ),
        )
        
        return response.text

    def catalogar_ODS(self):
      
        arquivo = self.processar_arquivo()
        
        prompt = '''
        Catalogue a ODS (Objetivos do Desenvolvimento Sustentável) que esse documento representa.

        - Analise o documento e imprima de 1 a 3 (Objetivos do Desenvolvimento Sustentável) PERTINENTES de acordo com o conteúdo.

        Seguem ODS's:
        """
        ODS 1. Erradicação da pobreza: 
        Acabar com a pobreza em todas as suas formas, em todos os lugares.
        
        ODS 2. Erradicação da fome:
        Acabar com a fome, alcançar a segurança alimentar e melhoria da nutrição e promover a agricultura sustentável.     
        
        ODS 3. Saúde e bem-estar:
        Assegurar uma vida saudável e promover o bem-estar para todas e todos, em todas as idades.
        
        ODS 4. Educação de qualidade:
        Objetivo 4. Assegurar a educação inclusiva e equitativa e de qualidade, e promover oportunidades de aprendizagem ao longo da vida para todas e todos.
        
        ODS 5. Igualdade de gênero:
        Objetivo 5. Alcançar a igualdade de gênero e empoderar todas as mulheres e meninas.
        
        ODS 6. Água potável e saneamento:
        Objetivo 6. Assegurar a disponibilidade e gestão sustentável da água e saneamento para todas e todos.
        
        ODS 7. Energia acessível e limpa:
        Objetivo 7. Assegurar o acesso confiável, sustentável, moderno e a preço acessível à energia para todas e todos.
        
        ODS 8. Trabalho decente e crescimento econômico:
        Objetivo 8. Promover o crescimento econômico sustentado, inclusivo e sustentável, emprego pleno e produtivo e trabalho decente para todas e todos.
        
        ODS 9. Inovação e infraestrutura:
        Objetivo 9. Construir infraestruturas resilientes, promover a industrialização inclusiva e sustentável e fomentar a inovação.
        
        ODS 10. Redução das desigualdades:
        Objetivo 10. Reduzir a desigualdade dentro dos países e entre eles.
        
        ODS 11. Cidades e comunidades sustentáveis:
        Objetivo 11. Tornar as cidades e os assentamentos humanos inclusivos, seguros, resilientes e sustentáveis.
        
        ODS 12. Consumo e produção responsáveis:
        Objetivo 12. Assegurar padrões de produção e de consumo sustentáveis
        
        ODS 13. Ação contra a mudança global do clima:
        Objetivo 13. Tomar medidas urgentes para combater a mudança climática e seus impactos.
        
        ODS 14. Vida na água:
        Objetivo 14. Conservação e uso sustentável dos oceanos, dos mares e dos recursos marinhos para o desenvolvimento sustentável.
        
        ODS 15. Vida terrestre:
        Objetivo 15. Proteger, recuperar e promover o uso sustentável dos ecossistemas terrestres, gerir de forma sustentável as florestas, combater a desertificação, deter e reverter a degradação da terra e deter a perda de biodiversidade.
        
        ODS 16. Paz, justiça e instituições eficazes:
        Objetivo 16. Promover sociedades pacíficas e inclusivas para o desenvolvimento sustentável, proporcionar o acesso à justiça para todos e construir instituições eficazes, responsáveis e inclusivas em todos os níveis.
        
        ODS 17. Parcerias e meios de implementação:
        Objetivo 17. Fortalecer os meios de implementação e revitalizar a parceria global para o desenvolvimento sustentável.
        
        """
        
        - Responda apenas o número e nome da ODS.
        - Não explique.
        - Não descreva o conteúdo.
        - Apenas liste as ODS.
        - Caso haja mais que uma, responda em formato de lista, como no exemplo:
            - ODS 10. Redução das desigualdades
            - ODS 8. Trabalho decente e crescimento econômico
       
        '''
        response = self.client.models.generate_content(
            model='models/gemini-2.5-flash-lite',
                    contents=[
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {
                        "file_data": {
                            "file_uri": arquivo.uri,
                            "mime_type": "text/plain"
                        }
                    }
                ]
            }
        ],
            config=types.GenerateContentConfig(
                safety_settings=self.get_safety_settings(),
                max_output_tokens=200,
                temperature=1,
                top_p=1,
                top_k=0
            )
        )
        return response.text
    
    
