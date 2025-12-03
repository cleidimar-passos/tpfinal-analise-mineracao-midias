🏥 Análise da Percepção Pública e Eficácia dos Investimentos na Saúde de Belo Horizonte

Trabalho final da disciplina de Mineração em Redes Sociais
Universidade Federal de Viçosa (UFV) | Autor: Cleidimar Lacerda dos Passos
Contato: cleidimar.passos@ufv.br

📊 Sobre o Projeto

Este projeto explora a correlação entre a satisfação do cidadão (avaliações do Google Maps das UPAs de BH) e o volume dos investimentos públicos em saúde. Utilizamos técnicas de Web Scraping e PLN para analisar mais de 6.000 reviews e dados oficiais da PBH (2020–2025). O trabalho visa diagnosticar a eficácia do gasto público.

✨ Principais Funcionalidades (Scripts Chave)

scraper_engine.py: Coleta automática de reviews, notas e datas das UPAs (Scraping).

preparar_dados_reais.py: Processa e filtra os grandes arquivos de despesas da PBH (ETL Financeiro).

analise_nlp.py: Processamento de texto, N-grams e Modelagem de Tópicos (LDA).

analise_correlacao.py: Geração de gráficos de correlação temporal (Nota vs. Execução Orçamentária).

🛠️ Tecnologias Utilizadas

Python 3.x

Selenium (coleta de dados)

Pandas (manipulação e limpeza)

Matplotlib & Seaborn (visualização)

Scikit-learn & NLTK (NLP e Modelagem)

🚀 Como Reproduzir os Resultados (Passo a Passo)

Etapa 0: Configuração Inicial

Clone o repositório:

git clone [https://github.com/cleidimar-passos/tpfinal-analise-mineracao-midias.git](https://github.com/cleidimar-passos/tpfinal-analise-mineracao-midias.git)
cd tpfinal-analise-mineracao-midias




Instale as dependências:

pip install -r requirements.txt




<sub>Atenção: O Selenium requer um Chrome/Edge Driver compatível.</sub>

Etapa 1: Obtenção e Preparação de Dados

A. Dados Financeiros (Oficiais da PBH - Obrigatório):

Baixe manualmente no Portal de Dados Abertos da PBH os arquivos de "Despesas Orçamentárias" (2020–2025).

Crie a pasta dados_oficiais na raiz do projeto e coloque todos os arquivos CSV baixados dentro dela.

Execute o script de preparo financeiro:

python preparar_dados_reais.py




Resultado: Isso gera os arquivos dados_investimentos_geral.csv e dados_investimentos_hob.csv na raiz, necessários para a correlação.

B. Dados de Reviews (Coleta e Limpeza):

Execute o script de coleta de reviews do Google Maps:

python scraper_engine.py




Execute o script de limpeza e tratamento de datas (NLP Básico). Este passo é crucial:

python processamento.py




Resultado: Isso gera o arquivo dados_limpos_upas.csv, unindo reviews e datas, que será a base de todas as análises subsequentes.

Etapa 2: Análises Finais e Gráficos (Dependem da Etapa 1)

Análise de Texto (NLP):
(Requer dados_limpos_upas.csv)

python analise_nlp.py




Resultado: Imagens de Bi/Tri-grams e Modelagem de Tópicos (LDA) salvas em resultados_nlp/.

Geração de Gráficos Visuais (Rankings, Tempo):
(Requer dados_limpos_upas.csv)

python analise_visual.py




Resultado: Todos os gráficos de ranking, volume e evolução temporal salvos em resultados_visuais/.

Correlação Financeira:
(Requer dados_limpos_upas.csv E os arquivos dados_investimentos_*.csv)

Para rodar a análise Geral, abra analise_correlacao.py e defina MODO_ANALISE = "GERAL".
Para rodar a análise HOB, defina MODO_ANALISE = "HOB".

python analise_correlacao.py




Resultado: Gráficos correlacao_geral.png e correlacao_hob.png gerados.

⚠️ Aviso Importante sobre Limitações

Os datasets brutos originais da PBH (Despesas Orçamentárias) NÃO estão incluídos no repositório devido à limitação de 100MB por arquivo do GitHub.

O projeto é totalmente reprodutível se os dados oficiais forem baixados conforme a Etapa 1.

Os arquivos de dados finais e intermediários (CSV leves) estão incluídos no repositório.

📄 Artigo Científico

O artigo gerado a partir destas análises (artigo_final.tex) está disponível na raiz do projeto.

👨‍💻 Autor

Cleidimar Lacerda dos Passos

Universidade Federal de Viçosa (UFV)

cleidimar.passos@ufv.br

<sub>Projeto acadêmico • Dados públicos • Uso exclusivamente educacional</sub>