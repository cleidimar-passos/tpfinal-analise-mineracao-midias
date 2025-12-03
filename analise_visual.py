import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import os
import unicodedata
import re

# --- CONFIGURAÇÃO ---
ARQUIVO_DADOS = "dados_limpos_upas.csv"
PASTA_SAIDA = "resultados_visuais"

# Configuração de estilo
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

def sanitizar_nome(nome):
    """Remove acentos e espaços para criar nomes de arquivo seguros."""
    if not isinstance(nome, str): return "desconhecido"
    nfkd = unicodedata.normalize('NFKD', nome)
    sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
    limpo = re.sub(r'[^a-zA-Z0-9 ]', '', sem_acento)
    return limpo.strip().replace(' ', '_').lower()

def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        print(f"❌ Erro: '{ARQUIVO_DADOS}' não encontrado.")
        return None
    
    df = pd.read_csv(ARQUIVO_DADOS)
    df['Data_Formatada'] = pd.to_datetime(df['Data_Formatada'])
    return df

def gerar_ranking_upas(df):
    print("1. Gerando Ranking das UPAs...")
    media_por_upa = df.groupby('UPA')['Nota'].mean().sort_values(ascending=True)
    
    plt.figure(figsize=(10, 8))
    grafico = media_por_upa.plot(kind='barh', color='#3498db', edgecolor='black')
    
    plt.title('Ranking de Aprovação: UPAs de BH (Média de Estrelas)', fontsize=16)
    plt.xlabel('Média de Estrelas (1 a 5)')
    plt.ylabel('')
    plt.xlim(0, 5.2)
    
    for index, value in enumerate(media_por_upa):
        plt.text(value + 0.05, index, str(round(value, 2)), va='center', fontweight='bold')

    plt.tight_layout()
    plt.savefig(f"{PASTA_SAIDA}/grafico_1_ranking_upas.png")
    plt.close()

def gerar_serie_temporal_geral(df):
    print("2. Gerando Linha do Tempo Geral...")
    df_tempo = df.set_index('Data_Formatada').sort_index()
    media_mensal = df_tempo['Nota'].resample('ME').mean()
    tendencia = media_mensal.rolling(window=4, min_periods=1).mean()
    
    plt.figure(figsize=(14, 6))
    plt.scatter(media_mensal.index, media_mensal.values, color='gray', alpha=0.3, s=30, label='Média Bruta')
    plt.plot(tendencia.index, tendencia.values, color='#c0392b', linewidth=3, label='Tendência (Média Móvel)')
    
    plt.title('Evolução da Qualidade Percebida - Rede BH (Geral)', fontsize=16)
    plt.xlabel('Ano')
    plt.ylabel('Nota Média')
    plt.ylim(1, 5.2)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{PASTA_SAIDA}/grafico_2_evolucao_tempo_geral.png")
    plt.close()

def gerar_evolucao_por_upa(df):
    print("3. Gerando gráficos individuais por UPA...")
    pasta_indiv = f"{PASTA_SAIDA}/por_upa"
    if not os.path.exists(pasta_indiv):
        os.makedirs(pasta_indiv)
    
    upas = df['UPA'].unique()
    
    for upa in upas:
        print(f"   > Processando: {upa}...", end='\r')
        df_upa = df[df['UPA'] == upa].set_index('Data_Formatada').sort_index()
        if len(df_upa) < 5: continue 
        
        media_mensal = df_upa['Nota'].resample('ME').mean()
        tendencia = media_mensal.rolling(window=3, min_periods=1).mean()
        
        plt.figure(figsize=(12, 6))
        plt.scatter(media_mensal.index, media_mensal.values, color='gray', alpha=0.3, s=20)
        plt.plot(tendencia.index, tendencia.values, color='#8e44ad', linewidth=2.5, label='Tendência')
        
        plt.title(f'Histórico de Qualidade: {upa}', fontsize=16)
        plt.xlabel('Ano')
        plt.ylabel('Nota (1-5)')
        plt.ylim(0.5, 5.5)
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        nome_arquivo = sanitizar_nome(upa)
        plt.tight_layout()
        plt.savefig(f"{pasta_indiv}/evolucao_{nome_arquivo}.png")
        plt.close()
    print("\n   > Gráficos individuais concluídos.")

def gerar_distribuicao_notas(df):
    print("4. Gerando Histograma de Notas...")
    plt.figure(figsize=(8, 6))
    sns.countplot(x=df['Nota'], palette='viridis')
    plt.title('Distribuição Geral das Avaliações', fontsize=14)
    plt.tight_layout()
    plt.savefig(f"{PASTA_SAIDA}/grafico_3_distribuicao_notas.png")
    plt.close()

def gerar_volume_avaliacoes_anual(df):
    print("5. Gerando Gráfico de Volume de Avaliações por Ano...")
    
    # Cria uma coluna temporária só com o Ano para agrupar
    df['Ano'] = df['Data_Formatada'].dt.year
    
    # Conta quantas avaliações existem por ano
    contagem_anual = df['Ano'].value_counts().sort_index()

    plt.figure(figsize=(14, 8))
    
    # Cria o gráfico de barras
    ax = sns.barplot(x=contagem_anual.index, y=contagem_anual.values, palette="viridis")
    
    plt.title('Volume Total de Avaliações por Ano', fontsize=16)
    plt.xlabel('Ano')
    plt.ylabel('Quantidade de Reviews')
    plt.grid(True, axis='y', alpha=0.3)
    
    # Adiciona o número exato no topo de cada barra para facilitar a leitura
    for i in ax.containers:
        ax.bar_label(i,)
    
    plt.tight_layout()
    plt.savefig(f"{PASTA_SAIDA}/grafico_5_volume_anual.png")
    plt.close()

def gerar_nuvem_palavras(df):
    print("6. Gerando Nuvens de Palavras...")
    reviews_ruins = df[df['Nota'] <= 2]['Texto_Limpo'].dropna().astype(str).str.cat(sep=' ')
    reviews_bons = df[df['Nota'] >= 4]['Texto_Limpo'].dropna().astype(str).str.cat(sep=' ')
    
    if not reviews_ruins or not reviews_bons: return

    wc_ruim = WordCloud(width=800, height=400, background_color='black', colormap='Reds').generate(reviews_ruins)
    wc_boa = WordCloud(width=800, height=400, background_color='white', colormap='Greens').generate(reviews_bons)
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    axes[0].imshow(wc_ruim, interpolation='bilinear')
    axes[0].set_title('Reclamações (⭐ 1-2)', fontsize=16, color='red')
    axes[0].axis('off')
    
    axes[1].imshow(wc_boa, interpolation='bilinear')
    axes[1].set_title('Elogios (⭐ 4-5)', fontsize=16, color='green')
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.savefig(f"{PASTA_SAIDA}/grafico_4_nuvem_palavras.png")
    plt.close()

def main():
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)
        
    df = carregar_dados()
    if df is None: return
    
    print(f"--- 📊 INICIANDO ANÁLISE COMPLETA ({len(df)} registros) ---")
    
    gerar_ranking_upas(df)
    gerar_serie_temporal_geral(df)
    gerar_evolucao_por_upa(df)
    gerar_distribuicao_notas(df)
    gerar_volume_avaliacoes_anual(df)
    gerar_nuvem_palavras(df)
    
    print(f"\n✅ SUCESSO! Verifique a pasta '{PASTA_SAIDA}'.")

if __name__ == "__main__":
    main()