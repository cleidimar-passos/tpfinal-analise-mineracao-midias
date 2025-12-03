import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- CONFIGURAÇÃO ---
ARQUIVO_DADOS = "dados_limpos_upas.csv"
PASTA_SAIDA = "resultados_nlp"

# Stopwords adicionais específicas do contexto de saúde que podem poluir a análise
# Adicionei 'nao' aqui para remover a negação dos tópicos
STOPWORDS_EXTRAS = [
    'atendimento', 'upa', 'hospital', 'dia', 'hoje', 'fui', 'ser', 'pra', 'tá', 'vc', 
    'pq', 'vcs', 'ter', 'tinha', 'veio', 'disse', 'falou', 'falar', 'cheguei', 
    'ficar', 'gente', 'pessoal', 'lugar', 'bhorizonte', 'bh', 'minas', 'gerais'
]

def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        print(f"❌ Erro: '{ARQUIVO_DADOS}' não encontrado.")
        return None
    return pd.read_csv(ARQUIVO_DADOS).dropna(subset=['Texto_Limpo'])

def plotar_ngrams(df, n=2, qtd=15, titulo="N-Grams"):
    """Gera gráfico de barras com as sequências de palavras mais comuns"""
    print(f"   > Calculando {titulo}...")
    
    # Configura o contador de palavras (Bi-gramas ou Tri-gramas)
    vec = CountVectorizer(ngram_range=(n, n), stop_words=STOPWORDS_EXTRAS).fit(df['Texto_Limpo'])
    bag_of_words = vec.transform(df['Texto_Limpo'])
    sum_words = bag_of_words.sum(axis=0) 
    
    # Lista de freqüência
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    
    # Prepara dados para o gráfico
    top_words = words_freq[:qtd]
    df_plot = pd.DataFrame(top_words, columns=['Termo', 'Frequencia'])
    
    # Plota
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Frequencia', y='Termo', data=df_plot, palette='rocket')
    plt.title(titulo, fontsize=16)
    plt.tight_layout()
    plt.savefig(f"{PASTA_SAIDA}/{titulo.replace(' ', '_').lower()}.png")
    plt.close()

def modelagem_topicos_lda(df, n_topicos=3, n_palavras=8):
    """
    Usa IA para descobrir os 3 assuntos principais nas reclamações.
    """
    print(f"   > Executando LDA (Modelagem de Tópicos) em {len(df)} textos...")
    
    # Vetorização (Transforma texto em números)
    vectorizer = CountVectorizer(max_df=0.9, min_df=5, stop_words=STOPWORDS_EXTRAS)
    dtm = vectorizer.fit_transform(df['Texto_Limpo'])
    
    # Cria o Modelo LDA
    lda = LatentDirichletAllocation(n_components=n_topicos, random_state=42)
    lda.fit(dtm)
    
    # Exibe e salva os tópicos
    plt.figure(figsize=(15, 5))
    feature_names = vectorizer.get_feature_names_out()
    
    # Cria um gráfico para cada tópico
    for index, topic in enumerate(lda.components_):
        plt.subplot(1, n_topicos, index + 1)
        
        # Pega as palavras mais importantes do tópico
        top_indices = topic.argsort()[-n_palavras:][::-1]
        top_features = [feature_names[i] for i in top_indices]
        top_weights = [topic[i] for i in top_indices]
        
        plt.barh(top_features, top_weights, color='#2ecc71')
        plt.gca().invert_yaxis()
        plt.title(f'Tópico {index + 1}', fontsize=14)
        plt.xlabel('Peso da Palavra')
    
    plt.suptitle('Tópicos Ocultos Descobertos (LDA)', fontsize=16)
    plt.tight_layout()
    plt.savefig(f"{PASTA_SAIDA}/topicos_lda.png")
    plt.close()
    
    print("   > Tópicos gerados. Verifique a imagem para interpretar o significado.")

def exportar_para_gephi(df):
    """
    Gera um arquivo CSV de arestas para ser importado no Gephi (Grafo de Co-ocorrência).
    Conecta palavras que aparecem na mesma frase.
    """
    print("   > Gerando arquivo para Gephi...")
    from itertools import combinations
    from collections import Counter
    
    todas_arestas = []
    
    # Pega apenas reclamações (Nota <= 2) para o grafo ficar focado nos problemas
    reviews = df[df['Nota'] <= 2]['Texto_Limpo'].head(1000) # Limita a 1000 para não travar
    
    for texto in reviews:
        palavras = [p for p in texto.split() if p not in STOPWORDS_EXTRAS and len(p) > 3]
        # Cria pares de palavras (arestas)
        pares = list(combinations(sorted(set(palavras)), 2))
        todas_arestas.extend(pares)
        
    # Conta frequência das conexões
    contagem = Counter(todas_arestas)
    
    # Salva CSV
    with open(f"{PASTA_SAIDA}/gephi_arestas.csv", "w", encoding='utf-8') as f:
        f.write("Source;Target;Weight\n")
        for (source, target), weight in contagem.most_common(500): # Top 500 conexões
            if weight > 2: # Filtra conexões fracas
                f.write(f"{source};{target};{weight}\n")
                
    print(f"   > Arquivo 'gephi_arestas.csv' salvo. Importe isso no Gephi!")

def main():
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)
        
    df = carregar_dados()
    if df is None: return
    
    print("--- 🧠 INICIANDO MINERAÇÃO DE TEXTO (NLP) ---")
    
    # Separa grupos
    ruins = df[df['Nota'] <= 2]
    bons = df[df['Nota'] >= 4]
    
    # 1. Bigramas em Reclamações (O que as pessoas falam juntas?)
    plotar_ngrams(ruins, n=2, titulo="Bi-gramas nas Reclamações (1-2 estrelas)")
    
    # 2. Trigramas em Reclamações (Frases curtas)
    plotar_ngrams(ruins, n=3, titulo="Tri-gramas nas Reclamações")
    
    # 3. Bigramas em Elogios (O que funciona?)
    plotar_ngrams(bons, n=2, titulo="Bi-gramas nos Elogios (4-5 estrelas)")
    
    # 4. Modelagem de Tópicos (A mágica da IA)
    # Vamos pedir para ele achar 3 grandes problemas ocultos nas reclamações
    modelagem_topicos_lda(ruins, n_topicos=3)
    
    # 5. Exportar para Gephi
    exportar_para_gephi(df)
    
    print(f"\n✅ SUCESSO! Resultados salvos na pasta '{PASTA_SAIDA}'.")

if __name__ == "__main__":
    main()