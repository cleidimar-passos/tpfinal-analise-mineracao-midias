import pandas as pd
import os
import glob

# --- CONFIGURAÇÃO ---
PASTA_ENTRADA = "dados_oficiais"
ARQUIVO_FMS = "dados_investimentos_geral.csv"
ARQUIVO_HOB = "dados_investimentos_hob.csv"

def carregar_e_processar():
    print("--- 🏛️ PROCESSANDO DADOS OFICIAIS (COLUNAS EXATAS) ---")
    
    arquivos = glob.glob(f"{PASTA_ENTRADA}/*.csv")
    if not arquivos:
        print(f"❌ Erro: Nenhum arquivo CSV na pasta '{PASTA_ENTRADA}'.")
        return

    df_total_fms = pd.DataFrame()
    df_total_hob = pd.DataFrame()

    for arq in arquivos:
        print(f"   > Lendo: {os.path.basename(arq)}...", end='\r')
        try:
            # Lê o CSV usando ponto-e-vírgula como separador (padrão PBH)
            df = pd.read_csv(arq, sep=';', encoding='latin1', on_bad_lines='skip', low_memory=False)
            
            # Remove espaços em branco dos nomes das colunas (ex: "AC AO " -> "AC AO")
            df.columns = [c.strip() for c in df.columns]

            # Verifica se as colunas essenciais existem
            colunas_necessarias = ['DT_MOVIMENTO', 'UNIDADE_ORCAMENTARIA', 'VL_PAGO']
            if not all(col in df.columns for col in colunas_necessarias):
                print(f"\n   ⚠️ Aviso: Colunas oficiais não encontradas em {arq}. Pulando.")
                continue

            # Converte unidade para maiúsculo para facilitar a busca
            df['UNIDADE_ORCAMENTARIA'] = df['UNIDADE_ORCAMENTARIA'].astype(str).str.upper()

            # --- FILTRO 1: FUNDO MUNICIPAL (GERAL) ---
            mask_fms = df['UNIDADE_ORCAMENTARIA'].str.contains('FUNDO MUNICIPAL', na=False)
            df_fms = df[mask_fms][['DT_MOVIMENTO', 'VL_PAGO']].copy()
            df_fms.columns = ['Data', 'Valor']
            df_total_fms = pd.concat([df_total_fms, df_fms])

            # --- FILTRO 2: HOSPITAL ODILON BEHRENS (HOB) ---
            mask_hob = df['UNIDADE_ORCAMENTARIA'].str.contains('ODILON', na=False)
            df_hob = df[mask_hob][['DT_MOVIMENTO', 'VL_PAGO']].copy()
            df_hob.columns = ['Data', 'Valor']
            df_total_hob = pd.concat([df_total_hob, df_hob])

        except Exception as e:
            print(f"\n   ❌ Erro em {arq}: {e}")

    # --- FUNÇÃO DE LIMPEZA E SALVAMENTO ---
    def processar_e_salvar(df_bruto, nome_arquivo, nome_cofre):
        if df_bruto.empty:
            print(f"\n❌ Nenhum dado encontrado para {nome_cofre}.")
            return

        # Limpeza de Valores (Trata formatos brasileiros: 1.000,00)
        def limpar_valor(v):
            if isinstance(v, (int, float)): return v
            # Remove R$, remove ponto de milhar, troca vírgula decimal por ponto
            v = str(v).replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
            try: return float(v)
            except: return 0.0

        df_bruto['Valor'] = df_bruto['Valor'].apply(limpar_valor)
        
        # Limpeza de Datas (Padrão DD/MM/YYYY ou YYYY-MM-DD)
        df_bruto['Data'] = pd.to_datetime(df_bruto['Data'], dayfirst=True, errors='coerce')
        df_bruto = df_bruto.dropna(subset=['Data'])

        # Soma Mensal
        df_final = df_bruto.set_index('Data').resample('MS')['Valor'].sum().reset_index()
        df_final.columns = ['Data', 'Investimento_Total_R$']

        # Salva CSV limpo
        df_final.to_csv(nome_arquivo, index=False)
        print(f"\n✅ {nome_cofre}: Salvo em '{nome_arquivo}' ({len(df_final)} meses).")
        print(f"   -> Média Mensal: R$ {df_final['Investimento_Total_R$'].mean():,.2f}")

    print("\n\n--- RESUMO DO PROCESSAMENTO ---")
    processar_e_salvar(df_total_fms, ARQUIVO_FMS, "Fundo Municipal (Geral)")
    processar_e_salvar(df_total_hob, ARQUIVO_HOB, "Hosp. Odilon Behrens (HOB)")

if __name__ == "__main__":
    carregar_e_processar()