import folium
from folium.plugins import HeatMap
import pandas as pd
import os
from upas_geodata import upas_geodata # Importa suas coordenadas validadas

# --- CONFIGURAÇÃO ---
ARQUIVO_DADOS = "dados_limpos_upas.csv"
PASTA_SAIDA = "resultados_visuais"
ARQUIVO_MAPA = f"{PASTA_SAIDA}/mapa_saude_bh.html"

def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        print(f"❌ Erro: '{ARQUIVO_DADOS}' não encontrado.")
        return None
    return pd.read_csv(ARQUIVO_DADOS)

def gerar_mapa():
    print("--- 🌍 INICIANDO GERAÇÃO DO MAPA ---")
    
    df = carregar_dados()
    if df is None: return

    # 1. Calcular a média atual de cada UPA
    # Agrupamos por UPA e pegamos a média das notas
    metricas_upa = df.groupby('UPA')['Nota'].agg(['mean', 'count']).reset_index()
    metricas_upa.columns = ['UPA', 'Nota_Media', 'Total_Reviews']

    # 2. Criar o Mapa Base (Centralizado em BH)
    # Coordenadas médias de BH
    mapa = folium.Map(location=[-19.916681, -43.934493], zoom_start=12, tiles='cartodbpositron')

    # Lista para o Heatmap (Latitude, Longitude, Peso)
    dados_calor = []

    print("   > Adicionando marcadores das UPAs...")

    # 3. Adicionar Marcadores para cada UPA
    for index, row in metricas_upa.iterrows():
        nome_upa = row['UPA']
        nota = row['Nota_Media']
        qtd = row['Total_Reviews']

        # Busca coordenadas no nosso dicionário validado
        # O nome no CSV pode variar ligeiramente, vamos tentar casar
        geo_info = None
        
        # Tenta achar a chave do dicionário que está contida no nome do CSV ou vice-versa
        for chave_geo, dados in upas_geodata.items():
            # Normalização simples para comparação
            if chave_geo.lower() in nome_upa.lower() or nome_upa.lower() in chave_geo.lower():
                geo_info = dados
                break
        
        if not geo_info:
            print(f"   ⚠️ Aviso: Coordenadas não encontradas para {nome_upa}")
            continue

        lat, lon = geo_info['coords']

        # Define cor baseada na nota
        if nota < 2.5:
            cor = 'red'
            icone = 'thumbs-down'
        elif nota < 3.8:
            cor = 'orange'
            icone = 'exclamation-sign'
        else:
            cor = 'green'
            icone = 'thumbs-up'

        # Texto do Popup (HTML)
        html_popup = f"""
        <div style="width:200px">
            <h4>{nome_upa}</h4>
            <p><b>Nota Média:</b> {nota:.2f} ⭐</p>
            <p><b>Total Avaliações:</b> {qtd}</p>
        </div>
        """

        # Adiciona Marcador
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(html_popup, max_width=250),
            tooltip=f"{nome_upa} ({nota:.1f}⭐)",
            icon=folium.Icon(color=cor, icon=icone)
        ).add_to(mapa)

        # 4. Preparar dados para Heatmap
        # AQUI O PULO DO GATO: Vamos fazer o calor ser baseado no volume de RECLAMAÇÕES.
        # Peso = Quantidade de Reviews * (5 - Nota). 
        # Ou seja: UPA com muita gente e nota baixa esquenta mais o mapa.
        fator_problema = qtd * (5 - nota) 
        dados_calor.append([lat, lon, fator_problema])

    # 5. Adicionar Camada de Calor
    print("   > Gerando camada de calor (Baseada em volume de problemas)...")
    HeatMap(dados_calor, radius=25, blur=15, max_zoom=10).add_to(mapa)

    # Salvar
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)
        
    mapa.save(ARQUIVO_MAPA)
    print(f"\n✅ SUCESSO! Mapa salvo em: {ARQUIVO_MAPA}")
    print("   -> Abra este arquivo no seu navegador para ver o mapa interativo.")

if __name__ == "__main__":
    gerar_mapa()