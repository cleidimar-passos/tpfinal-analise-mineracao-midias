Análise da Percepção Pública e Eficácia dos Investimentos na Saúde de Belo Horizonte

Este repositório contém o código fonte e a documentação do trabalho final da disciplina de Mineração em Redes Sociais. O projeto analisa a correlação entre a satisfação dos usuários (via Google Maps) e os investimentos financeiros nas Unidades de Pronto Atendimento (UPAs) de Belo Horizonte.

⚠️ Aviso Importante sobre os Dados

Devido às restrições de armazenamento do GitHub (limite de 100MB por arquivo), os datasets brutos não foram incluídos neste repositório.

Isso afeta principalmente:

Dados Oficiais de Despesas: Os arquivos CSV baixados do Portal de Dados Abertos da PBH (anos 2020-2025) excedem o tamanho permitido.

Backup de Coletas: Alguns arquivos intermediários de scraping também foram excluídos.

Como obter os dados?

O projeto foi desenhado para ser reprodutível. Você pode obter os dados das seguintes formas:

Dados Financeiros: Utilize os links oficiais indicados no código ou acesse diretamente o Portal de Dados Abertos da PBH e baixe os arquivos de "Despesas Orçamentárias" para os anos desejados.

Dados de Avaliações: Execute o script de scraping incluído no projeto para realizar uma nova coleta atualizada diretamente do Google Maps.

📋 Sobre o Projeto

O estudo utiliza técnicas de Web Scraping e Processamento de Linguagem Natural (PLN) para coletar e analisar mais de 6.000 avaliações de cidadãos. O objetivo é investigar se o aumento nos repasses financeiros para a saúde resulta em uma percepção de melhora imediata na qualidade do serviço.

Principais Funcionalidades

Scraper Automatizado: Coleta reviews, notas e datas das UPAs usando Selenium.

Análise de Sentimentos: Processamento de texto para identificar tópicos frequentes (N-Grams).

Correlação Financeira: Cruzamento temporal entre a nota média mensal e a execução de despesas.

🛠️ Tecnologias Utilizadas

Python 3.x

Selenium (Coleta de dados)

Pandas (Manipulação de dados)

Matplotlib & Seaborn (Visualização)

LaTeX (Escrita do artigo)

🚀 Como Executar

Clone o repositório:

git clone [https://github.com/cleidimar-passos/tpfinal-analise-mineracao-midias.git](https://github.com/cleidimar-passos/tpfinal-analise-mineracao-midias.git)
cd tpfinal-analise-mineracao-midias


Instale as dependências:

pip install -r requirements.txt


(Certifique-se de ter o WebDriver do Chrome instalado e configurado no PATH para o Selenium).

Execute a coleta (opcional se já tiver os dados):

python src/coleta_reviews.py


Execute a análise:

python src/analise_dados.py


📄 Artigo

O artigo completo gerado a partir desta análise encontra-se na pasta raiz ou pode ser compilado a partir do arquivo .tex fornecido.

👤 Autor

Cleidimar Lacerda dos Passos

Universidade Federal de Viçosa (UFV)

Contato: cleidimar.passos@ufv.br

Este projeto é de cunho acadêmico e utiliza dados públicos.
