# 🏥 Análise da Percepção Pública e Eficácia dos Investimentos na Saúde de Belo Horizonte

> **Trabalho final da disciplina de Mineração em Redes Sociais**  
> Universidade Federal de Viçosa (UFV)  
> **Autor:** [Cleidimar Lacerda dos Passos](mailto:cleidimar.passos@ufv.br)

---

## 📊 Sobre o Projeto

Este projeto explora **a correlação entre a satisfação dos cidadãos nas UPAs de BH (avaliada via Google Maps)** e **o volume dos investimentos públicos em saúde**. Aplicamos técnicas de web scraping, processamento de dados financeiros e análises em NLP.

---

## ✨ Principais Funcionalidades

| Script                  | Descrição                                                                                      |
|-------------------------|-----------------------------------------------------------------------------------------------|
| `scraper_engine.py`     | Coleta automática de reviews, notas e datas das UPAs (Scraping)                               |
| `preparar_dados_reais.py` | Processa e filtra grandes arquivos de despesas da PBH (ETL Financeiro)                      |
| `analise_nlp.py`        | Processamento de texto, N-grams e Modelagem de Tópicos (LDA)                                  |
| `analise_correlacao.py` | Geração de gráficos de correlação temporal (Nota vs. Execução Orçamentária)                   |

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- [Selenium](https://selenium.dev/) (coleta de dados)
- [Pandas](https://pandas.pydata.org/) (manipulação e limpeza)
- [Matplotlib](https://matplotlib.org/) & [Seaborn](https://seaborn.pydata.org/) (visualização)
- [Scikit-learn](https://scikit-learn.org/) & [NLTK](https://www.nltk.org/) (NLP e Modelagem)

---

## 🚀 Como Reproduzir os Resultados

### 0️⃣ Configuração Inicial

```sh
# Clone o repositório
git clone https://github.com/cleidimar-passos/tpfinal-analise-mineracao-midias.git
cd tpfinal-analise-mineracao-midias

# Instale as dependências
pip install -r requirements.txt
```
> ⚠️ **Atenção:** O Selenium requer um Chrome/Edge Driver compatível.

---

### 1️⃣ Obtenção e Preparação de Dados

#### A) Dados Financeiros (PBH - Obrigatório)

1. Baixe manualmente os arquivos de "Despesas Orçamentárias" (2020–2025) no [Portal de Dados Abertos da PBH](http://dados.pbh.gov.br/).
2. Crie a pasta `dados_oficiais` na raiz do projeto e coloque todos os arquivos CSV lá.
3. Execute:
   ```sh
   python preparar_dados_reais.py
   ```
   - **Saída:** `dados_investimentos_geral.csv` e `dados_investimentos_hob.csv`

#### B) Dados de Reviews (Google Maps)

1. Execute o script de coleta:
   ```sh
   python scraper_engine.py
   ```
2. Limpeza e processamento de datas (NLP básico):
   ```sh
   python processamento.py
   ```
   - **Saída:** `dados_limpos_upas.csv`

---

### 2️⃣ Análises Finais e Geração de Gráficos

#### Análise de Texto (NLP):
- Requer: `dados_limpos_upas.csv`
- Execute:
  ```sh
  python analise_nlp.py
  ```
- **Saída:** Imagens Bi/Tri-grams e LDA em `resultados_nlp/`

#### Gráficos Visuais:
- Requer: `dados_limpos_upas.csv`
- Execute:
  ```sh
  python analise_visual.py
  ```
- **Saída:** Gráficos de ranking, volume e evolução temporal em `resultados_visuais/`

#### Correlação Financeira:
- Requer: `dados_limpos_upas.csv` e os arquivos `dados_investimentos_*.csv`
- Configure o modo (`GERAL` ou `HOB`) em `analise_correlacao.py`
- Execute:
  ```sh
  python analise_correlacao.py
  ```
- **Saída:** Gráficos `correlacao_geral.png` e `correlacao_hob.png`

---

## ⚠️ Avisos Importantes

- Os datasets brutos originais da PBH **NÃO estão incluídos** devido à limitação de 100MB por arquivo do GitHub.
- O projeto é totalmente reprodutível se os dados oficiais forem baixados conforme as instruções.
- Os arquivos intermediários e finais (CSVs leves) **estão inclusos** no repositório.

---

## 📄 Artigo Científico

O artigo gerado a partir destas análises (`artigo_final.tex`) está disponível na raiz do projeto.

---

## 👨‍💻 Autor

**Cleidimar Lacerda dos Passos**  
Universidade Federal de Viçosa (UFV)  
[cleidimar.passos@ufv.br](mailto:cleidimar.passos@ufv.br)

<sub>Projeto acadêmico • Dados públicos • Uso exclusivamente educacional</sub>
