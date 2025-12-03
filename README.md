# 🏥 Análise da Percepção Pública e Eficácia dos Investimentos na Saúde de Belo Horizonte

> **Trabalho final da disciplina de Mineração em Redes Sociais**  
> Universidade Federal de Viçosa (UFV) | Autor: Cleidimar Lacerda dos Passos  
> Contato: [cleidimar.passos@ufv.br](mailto:cleidimar.passos@ufv.br)

---

## 📊 Sobre o Projeto

Explora-se a correlação entre a satisfação do cidadão (avaliações do Google Maps das UPAs de BH) e o volume dos investimentos públicos em saúde. Utiliza técnicas de **Web Scraping** e **PLN** para analisar mais de **6.000 reviews** e dados oficiais da PBH (2020–2025).

---

## ✨ Principais Funcionalidades

- **🤖 Scraper Automatizado:**  
  Coleta automática de reviews, notas e datas das UPAs utilizando Selenium.

- **📈 Análise de Sentimentos:**  
  Processamento de texto e identificação de tópicos frequentes via N-grams.

- **💰 Correlação Financeira Temporal:**  
  Relacionamento entre nota média mensal dos atendimentos e execução orçamentária das unidades.

---

## 🛠️ Tecnologias Utilizadas

- `Python 3.x`
- `Selenium` (coleta de dados)
- `Pandas` (manipulação)
- `Matplotlib` & `Seaborn` (visualização)
- `LaTeX` (escrita do artigo)

---

## 🚀 Como Executar

1. **Clone o repositório**
    ```bash
    git clone https://github.com/cleidimar-passos/tpfinal-analise-mineracao-midias.git
    cd tpfinal-analise-mineracao-midias
    ```

2. **Instale as dependências**
    ```bash
    pip install -r requirements.txt
    ```
    <sub>*Necessário ter ChromeDriver instalado e configurado no PATH para uso com Selenium*</sub>

3. **Execute a coleta de dados (opcional)**
    ```bash
    python coleta_reviews.py
    ```

4. **Execute as análises**
    ```bash
    python analise_dados.py
    ```

---

## ⚠️ Aviso Importante sobre os Dados

> **Os datasets brutos NÃO estão incluídos no repositório devido à limitação de 100MB por arquivo do GitHub.**

- **Fontes oficiais das despesas**: Baixe manualmente no [Portal de Dados Abertos da PBH](https://dados.pbh.gov.br/) os arquivos de "Despesas Orçamentárias" (2020–2025).
- **Avaliações do Google Maps**: Gere com o scraping fornecido (`src/coleta_reviews.py`).
- **Arquivos intermediários de scraping**: Não adicionados para manter o repositório leve.

O projeto é totalmente reprodutível se as orientações acima forem seguidas.

---

## 📄 Artigo Científico

O artigo gerado a partir destas análises está disponível na raiz do projeto (`main.pdf`) ou pode ser compilado manualmente a partir do arquivo `.tex`.

---

## 👨‍💻 Autor

- **Cleidimar Lacerda dos Passos**
- Universidade Federal de Viçosa (UFV)
- [cleidimar.passos@ufv.br](mailto:cleidimar.passos@ufv.br)

<sub>Projeto acadêmico • Dados públicos • Uso exclusivamente educacional</sub>

---
