import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os

# --- CONFIGURAÇÃO ---
ARQUIVO_DADOS = "dados_limpos_upas.csv"
PASTA_SAIDA = "resultados_visuais"

# Configuração de estilo dos gráficos (para ficarem bonitos)
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        print(f"❌ Erro: '{ARQUIVO_DADOS}' não encontrado.")
        return None
    
    df = pd.read_csv(ARQUIVO_DADOS)
    # Garante que a coluna de data é entendida como data pelo Python
    df['Data_Formatada'] = pd.to_datetime(df['Data_Formatada'])
    return df

def gerar_ranking_upas(df):
    print("1. Gerando Ranking das UPAs...")
    media_por_upa = df.groupby('UPA')['Nota'].mean().sort_values(ascending=True)
    
    plt.figure(figsize=(10, 8))
    # Cria gráfico de barras horizontais
    grafico = media_por_upa.plot(kind='barh', color='#3498db', edgecolor='black')
    
    plt.title('Ranking de Aprovação: UPAs de BH (Média de Estrelas)', fontsize=16)
    plt.xlabel('Média de Estrelas (1 a 5)')
    plt.ylabel('')
    plt.xlim(0, 5) # Garante que a escala vai de 0 a 5
    
    # Adiciona o valor na ponta da barra
    for index, value in enumerate(media_por_upa):
        plt.text(value + 0.05, index, str(round(value, 2)), va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(f"{PASTA_SAIDA}/grafico_1_ranking_upas.png")
    plt.close()

def gerar_serie_temporal(df):
    print("2. Gerando Linha do Tempo...")
    # Agrupa por Mês/Ano (resample 'M')
    # Precisamos setar a data como índice para usar resample
    df_tempo = df.set_index('Data_Formatada')
    media_mensal = df_tempo['Nota'].resample('ME').mean() # ME = Month End
    
    plt.figure(figsize=(14, 6))
    plt.plot(media_mensal.index, media_mensal.values, marker='o', linestyle='-', color='#e74c3c', linewidth=2)
    
    plt.title('Evolução da Qualidade Percebida (Média Mensal)', fontsize=16)
    plt.xlabel('Data')
    plt.ylabel('Nota Média')
    plt.ylim(1, 5)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{PASTA_SAIDA}/grafico_2_evolucao_tempo.png")
    plt.close()

def gerar_distribuicao_notas(df):
    print("3. Gerando Histograma de Notas...")
    plt.figure(figsize=(8, 6))
    
    sns.countplot(x=df['Nota'], palette='viridis')
    
    plt.title('Distribuição das Avaliações (Quantas pessoas deram cada nota?)', fontsize=14)
    plt.xlabel('Estrelas')
    plt.ylabel('Quantidade de Reviews')
    
    plt.tight_layout()
    plt.savefig(f"{PASTA_SAIDA}/grafico_3_distribuicao_notas.png")
    plt.close()

def gerar_nuvem_palavras(df):
    print("4. Gerando Nuvens de Palavras (Isso pode demorar um pouquinho)...")
    
    # Separa reviews bons (4 e 5) e ruins (1 e 2)
    reviews_ruins = df[df['Nota'] <= 2]['Texto_Limpo'].dropna().astype(str).str.cat(sep=' ')
    reviews_bons = df[df['Nota'] >= 4]['Texto_Limpo'].dropna().astype(str).str.cat(sep=' ')
    
    # Se não tiver texto suficiente, evita erro
    if not reviews_ruins or not reviews_bons:
        print("   ⚠️ Aviso: Poucos textos para gerar nuvem.")
        return

    # Nuvem Ruim
    wordcloud_ruim = WordCloud(width=800, height=400, background_color='black', colormap='Reds').generate(reviews_ruins)
    
    # Nuvem Boa
    wordcloud_boa = WordCloud(width=800, height=400, background_color='white', colormap='Greens').generate(reviews_bons)
    
    # Plota as duas lado a lado
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    axes[0].imshow(wordcloud_ruim, interpolation='bilinear')
    axes[0].set_title('O que dizem nas reclamações (⭐ 1 e 2)', fontsize=16, color='red')
    axes[0].axis('off')
    
    axes[1].imshow(wordcloud_boa, interpolation='bilinear')
    axes[1].set_title('O que dizem nos elogios (⭐ 4 e 5)', fontsize=16, color='green')
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.savefig(f"{PASTA_SAIDA}/grafico_4_nuvem_palavras.png")
    plt.close()

def main():
    # Cria pasta de resultados se não existir
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)
        
    df = carregar_dados()
    if df is None: return
    
    print(f"--- 📊 INICIANDO ANÁLISE VISUAL ({len(df)} registros) ---")
    
    gerar_ranking_upas(df)
    gerar_distribuicao_notas(df)
    gerar_serie_temporal(df)
    gerar_nuvem_palavras(df)
    
    print(f"\n✅ SUCESSO! 4 Gráficos gerados na pasta '{PASTA_SAIDA}'")
    print("   Abra a pasta para ver os resultados!")

if __name__ == "__main__":
    main()