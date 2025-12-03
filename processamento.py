import pandas as pd
import re
from datetime import datetime, timedelta
import unicodedata

# --- CONFIGURAÇÃO ---
ARQUIVO_ENTRADA = "dados_brutos_upas.csv"
ARQUIVO_SAIDA = "dados_limpos_upas.csv"

# Stopwords (Expandido para garantir limpeza)
STOPWORDS_PT = {
    "de", "a", "o", "que", "e", "do", "da", "em", "um", "para", "é", "com", "não", "uma", "os", "no", 
    "se", "na", "por", "mais", "as", "dos", "como", "mas", "foi", "ao", "ele", "das", "tem", "à", 
    "seu", "sua", "ou", "ser", "quando", "muito", "nos", "já", "está", "eu", "também", "só", "pelo", 
    "pela", "até", "isso", "ela", "entre", "era", "depois", "sem", "mesmo", "aos", "ter", "seus", 
    "quem", "nas", "me", "esse", "eles", "estão", "você", "tinha", "foram", "essa", "num", "nem", 
    "suas", "meu", "às", "minha", "têm", "numa", "pelos", "elas", "havia", "seja", "qual", "nós", 
    "lhe", "deles", "essas", "esses", "pelas", "este", "fosse", "dele", "tu", "te", "vocês", "vos", 
    "lhes", "meus", "minhas", "teu", "tua", "teus", "tuas", "nosso", "nossa", "nossos", "nossas", 
    "dela", "delas", "esta", "estes", "estas", "aquele", "aquela", "aqueles", "aquelas", "isto", 
    "aquilo", "estou", "está", "estamos", "estão", "estive", "esteve", "estivemos", "estiveram", 
    "estava", "estávamos", "estavam", "estivera", "estivéramos", "esteja", "estejamos", "estejam", 
    "estivesse", "estivéssemos", "estivessem", "estiver", "estivermos", "estiverem", "hei", "há", 
    "havemos", "hão", "houve", "houvemos", "houveram", "houvera", "houvéramos", "haja", "hajamos", 
    "hajam", "houvesse", "houvéssemos", "houvessem", "houver", "houvermos", "houverem", "houverei", 
    "houverá", "houveremos", "houverão", "houveria", "houveríamos", "houveriam", "sou", "somos", 
    "são", "era", "éramos", "eram", "fui", "foi", "fomos", "foram", "fora", "fôramos", "seja", 
    "sejamos", "sejam", "fosse", "fôssemos", "fossem", "for", "formos", "forem", "serei", "será",
    "seremos", "serão", "seria", "seríamos", "seriam", "tenho", "tem", "temos", "tém", "tinha", 
    "tínhamos", "tinham", "tive", "teve", "tivemos", "tiveram", "tivera", "tivéramos", "tenha", 
    "tenhamos", "tenham", "tivesse", "tivéssemos", "tivessem", "tiver", "tivermos", "tiverem", 
    "terei", "terá", "teremos", "terão", "teria", "teríamos", "teriam"
}

def converter_data_relativa(texto_data):
    if not isinstance(texto_data, str): return None
    texto = texto_data.lower().strip()
    hoje = datetime.now()
    
    try:
        if "momento" in texto or "agora" in texto: return hoje
        match_numero = re.search(r'(\d+)', texto)
        numero = int(match_numero.group(1)) if match_numero else 1
        
        if "minuto" in texto or "hora" in texto: return hoje
        elif "dia" in texto: return hoje - timedelta(days=numero)
        elif "semana" in texto: return hoje - timedelta(weeks=numero)
        elif "mês" in texto or "meses" in texto: return hoje - timedelta(days=numero * 30)
        elif "ano" in texto: return hoje - timedelta(days=numero * 365)
        else: return None
    except: return None

def limpar_texto(texto):
    """
    Limpeza agressiva para análise de sentimentos/tópicos.
    """
    if pd.isna(texto) or texto == "":
        return ""
    
    texto = str(texto) # Garante que é string
    
    # 1. Tudo minúsculo
    texto = texto.lower()
    
    # 2. Remover quebras de linha (crucial para o CSV não quebrar)
    texto = texto.replace('\n', ' ').replace('\r', '')
    
    # 3. Remover acentos
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')
    
    # 4. Manter apenas letras (remove números e pontuação)
    texto = re.sub(r'[^a-z\s]', '', texto)
    
    # 5. Remover stopwords e palavras curtas
    palavras = texto.split()
    palavras_uteis = [p for p in palavras if p not in STOPWORDS_PT and len(p) > 2]
    
    return " ".join(palavras_uteis)

def main():
    print("--- 🧹 INICIANDO LIMPEZA ---")
    
    try:
        df = pd.read_csv(ARQUIVO_ENTRADA)
        print(f"> Lendo {len(df)} linhas de '{ARQUIVO_ENTRADA}'...")
    except FileNotFoundError:
        print(f"❌ Erro: '{ARQUIVO_ENTRADA}' não encontrado.")
        return

    # Processamento
    df['Data_Real'] = df['Data_Relativa'].apply(converter_data_relativa)
    df = df.dropna(subset=['Data_Real'])
    df['Data_Formatada'] = df['Data_Real'].apply(lambda x: x.strftime('%Y-%m-%d'))
    
    # Preenche vazios antes de limpar
    df['Texto'] = df['Texto'].fillna("") 
    
    # Aplica a limpeza
    print("> Aplicando limpeza de texto (NLP)...")
    df['Texto_Limpo'] = df['Texto'].apply(limpar_texto)
    
    # --- DEBUG VISUAL: MOSTRA ANTES E DEPOIS ---
    print("\n--- 🔍 AMOSTRA DA LIMPEZA (Primeiros 5 com texto) ---")
    amostra = df[df['Texto'].str.len() > 10].head(5) # Pega só os que têm texto longo
    
    for index, row in amostra.iterrows():
        print(f"\n[ORIGINAL]: {row['Texto'][:60]}...")
        print(f"[LIMPO]   : {row['Texto_Limpo'][:60]}...")
    print("-----------------------------------------------------")

    # Filtra vazios no texto limpo (opcional, mas bom pra WordCloud)
    # df = df[df['Texto_Limpo'] != ""] 

    # Salva
    colunas = ['UPA', 'Data_Formatada', 'Nota', 'Texto', 'Texto_Limpo']
    df[colunas].to_csv(ARQUIVO_SAIDA, index=False, encoding='utf-8-sig')
    
    print(f"\n✅ SUCESSO! Arquivo salvo: {ARQUIVO_SAIDA}")
    print(f"   Total de linhas válidas: {len(df)}")

if __name__ == "__main__":
    main()