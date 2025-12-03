# Dicionário contendo Nome, Link Original e Coordenadas (Lat, Lon)
# Corrigido e formatado para uso no Geopandas / Folium

upas_geodata = {
    "UPA Barreiro": {
        "coords": (-19.9793418, -44.0319955),
        "link": "https://www.google.com/maps/place/Unidade+de+Pronto+Atendimento+-+UPA+Barreiro/..."
    },
    "UPA Centro-Sul": {
        "coords": (-19.9221242, -43.9281276),
        "link": "https://www.google.com/maps/place/UPA+Centro-Sul/..."
    },
    "UPA Pampulha": {
        "coords": (-19.8705858, -44.0039212),
        "link": "https://www.google.com/maps/place/Unidade+de+Pronto+Atendimento+-+UPA+Pampulha/..."
    },
    "UPA Nordeste": {
        "coords": (-19.8664867, -43.9282931),
        "link": "https://www.google.com/maps/place/UPA+Nordeste/..."
    },
    "UPA Oeste": {
        "coords": (-19.9511764, -43.970977),
        "link": "https://www.google.com/maps/place/Unidade+de+Pronto+Atendimento+-+UPA+Oeste/..."
    },
    "UPA Norte": {
        "coords": (-19.8456559, -43.9170806),
        "link": "https://www.google.com/maps/place/Unidade+de+Pronto+Atendimento+-+UPA+Norte/..."
    },
    "Hosp. Odilon Behrens": {
        "coords": (-19.9044341, -43.9504307),
        "link": "https://www.google.com/maps/place/UPA+ODILON+BEHRENS/..."
    },
    "UPA Noroeste II": {
        "coords": (-19.9044341, -43.9504307), # Corrigido sinal negativo (Hemisfério Sul)
        "link": "https://www.google.com/maps/place/Unidade+de+Pronto+Atendimento+-+UPA+Noroeste+II+(HOB)/..."
    },
    "UPA Leste": {
        "coords": (-19.9056924, -43.8994673),
        "link": "https://www.google.com/maps/place/Unidade+de+Pronto+Atendimento+-+UPA+Leste/..."
    },
    "UPA Venda Nova": {
        "coords": (-19.8201638, -43.9560789),
        "link": "https://www.google.com/maps/place/UPA+Venda+Nova/..."
    }
}

print(f"✅ Dados geográficos carregados para {len(upas_geodata)} unidades.")