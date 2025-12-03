import pandas as pd
import os

# --- CONFIGURAÇÃO ---
ARQUIVO_DADOS = "dados_limpos_upas.csv"
ARQUIVO_SAIDA = "resultados_visuais/resumo_estatistico.txt"

def gerar_relatorio():
    print("--- 📝 GERANDO RELATÓRIO ESTATÍSTICO FINAL ---")
    
    if not os.path.exists(ARQUIVO_DADOS):
        print(f"❌ Erro: '{ARQUIVO_DADOS}' não encontrado.")
        return

    df = pd.read_csv(ARQUIVO_DADOS)
    df['Data_Formatada'] = pd.to_datetime(df['Data_Formatada'])
    
    # --- CÁLCULOS MACRO ---
    total_reviews = len(df)
    nota_media_geral = df['Nota'].mean()
    nota_mediana = df['Nota'].median()
    
    # Contagem de Positivos/Negativos
    negativos = len(df[df['Nota'] <= 2])
    positivos = len(df[df['Nota'] >= 4])
    neutros = len(df[df['Nota'] == 3])
    
    pct_neg = (negativos / total_reviews) * 100
    pct_pos = (positivos / total_reviews) * 100

    # --- CÁLCULOS POR ANO (Evolução Numérica) ---
    df['Ano'] = df['Data_Formatada'].dt.year
    media_por_ano = df.groupby('Ano')['Nota'].mean().round(2)
    volume_por_ano = df.groupby('Ano').size()

    # --- MONTAGEM DO TEXTO ---
    relatorio = []
    relatorio.append("="*50)
    relatorio.append("RELATÓRIO FINAL: PERCEPÇÃO DA SAÚDE PÚBLICA (BH)")
    relatorio.append("="*50)
    relatorio.append(f"\n1. ESTATÍSTICAS GERAIS DO SISTEMA")
    relatorio.append(f"- Total de Avaliações Coletadas: {total_reviews}")
    relatorio.append(f"- NOTA MÉDIA GERAL (Histórica): {nota_media_geral:.2f} / 5.00")
    relatorio.append(f"- Nota Mediana: {nota_mediana} (A nota 'do meio')")
    relatorio.append(f"\n2. SENTIMENTO DO CIDADÃO")
    relatorio.append(f"- Insatisfeitos (Nota 1-2): {negativos} ({pct_neg:.1f}%)")
    relatorio.append(f"- Satisfeitos (Nota 4-5):   {positivos} ({pct_pos:.1f}%)")
    relatorio.append(f"- Neutros (Nota 3):         {neutros}")
    
    relatorio.append(f"\n3. EVOLUÇÃO TEMPORAL (A Queda/Melhora)")
    for ano in media_por_ano.index:
        nota = media_por_ano[ano]
        vol = volume_por_ano[ano]
        relatorio.append(f"- {ano}: Média {nota} ⭐ ({vol} reviews)")

    relatorio.append("\n4. RANKING FINAL (Melhores e Piores)")
    ranking = df.groupby('UPA')['Nota'].mean().sort_values(ascending=False)
    for upa, nota in ranking.items():
        relatorio.append(f"- {upa}: {nota:.2f}")

    # Salva em arquivo
    texto_final = "\n".join(relatorio)
    
    # Cria pasta se não existir
    if not os.path.exists("resultados_visuais"):
        os.makedirs("resultados_visuais")
        
    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
        f.write(texto_final)
    
    # Imprime no terminal
    print(texto_final)
    print(f"\n✅ Relatório salvo em: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    gerar_relatorio()