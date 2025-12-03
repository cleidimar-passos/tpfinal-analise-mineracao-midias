import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from scipy.stats import pearsonr

# --- ESCOLHA AQUI QUAL ANÁLISE RODAR ---
# Opção 1: "GERAL" (Todas as UPAs vs Fundo Municipal)
# Opção 2: "HOB"   (UPA Odilon/Noroeste vs Hospital Odilon)
MODO_ANALISE = "HOB"  # <--- ALTERNE AQUI ENTRE "GERAL" E "HOB"

# Configurações Automáticas baseadas no modo
if MODO_ANALISE == "GERAL":
    ARQUIVO_FINANCEIRO = "dados_investimentos_geral.csv"
    FILTRO_UPA = None 
    TITULO_GRAFICO = "Correlação Geral: Fundo Municipal vs. Rede de UPAs"
    COR_LINHA = "tab:blue"
elif MODO_ANALISE == "HOB":
    ARQUIVO_FINANCEIRO = "dados_investimentos_hob.csv"
    FILTRO_UPA = ["Hosp. Odilon Behrens", "UPA Noroeste II", "UPA Odilon Behrens"] 
    TITULO_GRAFICO = "Correlação Específica: Orçamento HOB vs. UPA Odilon"
    COR_LINHA = "tab:purple"

ARQUIVO_REVIEWS = "dados_limpos_upas.csv"
PASTA_SAIDA = "resultados_visuais"

def carregar_dados():
    if not os.path.exists(ARQUIVO_REVIEWS):
        print("❌ Erro: Arquivo de reviews não encontrado.")
        return None, None
    df_reviews = pd.read_csv(ARQUIVO_REVIEWS)
    df_reviews['Data_Formatada'] = pd.to_datetime(df_reviews['Data_Formatada'])
    
    if FILTRO_UPA:
        print(f"   > Filtrando reviews apenas para: {FILTRO_UPA}")
        df_reviews = df_reviews[df_reviews['UPA'].isin(FILTRO_UPA)]
    
    if not os.path.exists(ARQUIVO_FINANCEIRO):
        print(f"❌ Erro: Arquivo '{ARQUIVO_FINANCEIRO}' não encontrado.")
        return None, None
    df_financas = pd.read_csv(ARQUIVO_FINANCEIRO)
    df_financas['Data'] = pd.to_datetime(df_financas['Data'])
    
    return df_reviews, df_financas

def analisar_correlacao():
    print(f"--- 📉 ANÁLISE DE CORRELAÇÃO: {MODO_ANALISE} ---")
    
    df_reviews, df_financas = carregar_dados()
    if df_reviews is None or df_reviews.empty:
        print("⚠️ Sem dados de reviews.")
        return

    # 1. Agrupar Reviews (Média Mensal)
    reviews_mensal = df_reviews.set_index('Data_Formatada').resample('MS')['Nota'].mean().reset_index()
    reviews_mensal.columns = ['Data', 'Nota_Media']
    
    # 2. Agrupar Investimento (Soma Mensal)
    financas_mensal = df_financas.set_index('Data').resample('MS')['Investimento_Total_R$'].sum().reset_index()
    
    # 3. Cruzamento (Merge)
    # Usamos 'inner' para garantir que só analisamos meses que têm OS DOIS dados
    df_final = pd.merge(reviews_mensal, financas_mensal, on='Data', how='inner')
    
    # --- CORREÇÃO CRÍTICA: REMOVER NAN/INFINITOS ---
    df_final = df_final.replace([np.inf, -np.inf], np.nan).dropna()
    df_final = df_final.sort_values('Data') # Garante ordem cronológica
    
    # Filtra apenas anos relevantes
    df_final = df_final[df_final['Data'].dt.year >= 2020]

    if len(df_final) < 6:
        print(f"⚠️ Dados insuficientes após limpeza ({len(df_final)} meses).")
        return

    # 4. Cálculo de Pearson
    try:
        corr_coef, p_value = pearsonr(df_final['Nota_Media'], df_final['Investimento_Total_R$'])
        texto_pearson = f"{corr_coef:.4f}"
    except Exception as e:
        print(f"Erro no cálculo: {e}")
        corr_coef = 0
        texto_pearson = "Erro"

    print(f"\n📊 RESULTADO ({MODO_ANALISE}):")
    print(f"   > Correlação de Pearson: {texto_pearson}")
    
    # --- VISUALIZAÇÃO ---
    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Eixo 1: Nota (Com Suavização para ficar bonito)
    ax1.set_xlabel('Data')
    ax1.set_ylabel('Nota Média (Tendência)', color='tab:red', fontweight='bold')
    
    # Calcula tendência da nota para plotar
    df_final['Nota_Smooth'] = df_final['Nota_Media'].rolling(window=3, min_periods=1).mean()
    
    # Plot Nota (Usando ax.plot padrão para evitar bugs de legenda do seaborn)
    ax1.plot(df_final['Data'], df_final['Nota_Smooth'], color='tab:red', linewidth=2.5, label='Qualidade (Nota)')
    ax1.tick_params(axis='y', labelcolor='tab:red')
    ax1.set_ylim(1, 5)

    # Eixo 2: Investimento
    ax2 = ax1.twinx()
    ax2.set_ylabel('Investimento (Milhões R$)', color=COR_LINHA, fontweight='bold')
    
    # Transforma em Milhões
    df_final['Invest_M'] = df_final['Investimento_Total_R$'] / 1_000_000
    
    # SUAVIZAÇÃO DO INVESTIMENTO (Para tirar os picos agudos e ver a tendência de gasto)
    df_final['Invest_Smooth'] = df_final['Invest_M'].rolling(window=3, min_periods=1).mean()

    # Plota o investimento suavizado (linha cheia) e o bruto (linha fina transparente)
    ax2.plot(df_final['Data'], df_final['Invest_M'], color=COR_LINHA, alpha=0.3, linewidth=1)
    ax2.plot(df_final['Data'], df_final['Invest_Smooth'], color=COR_LINHA, linestyle='--', linewidth=2, label='Investimento (Tendência)')
    
    ax2.tick_params(axis='y', labelcolor=COR_LINHA)
    ax2.grid(False)

    plt.title(f'{TITULO_GRAFICO}\nPearson: {texto_pearson}', fontsize=16)
    
    # Adiciona legenda unificada e DEDUPLICADA
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    
    # Combina as legendas
    lines = lines_1 + lines_2
    labels = labels_1 + labels_2
    
    # Truque para remover duplicatas: cria um dicionário (chave=label, valor=handle)
    by_label = dict(zip(labels, lines))
    ax1.legend(by_label.values(), by_label.keys(), loc='upper left')

    fig.tight_layout()
    
    nome_arquivo = f"correlacao_{MODO_ANALISE.lower()}.png"
    caminho = f"{PASTA_SAIDA}/{nome_arquivo}"
    plt.savefig(caminho)
    print(f"\n✅ Gráfico salvo: {caminho}")

if __name__ == "__main__":
    analisar_correlacao()