import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from alvos_upas import upas_bh_alvos

# --- CONFIGURAÇÕES ---
MAX_REVIEWS_POR_UPA = 3000 # Aumentei um pouco para garantir
HEADLESS_MODE = False      # False = Vê o navegador; True = Escondido

def iniciar_driver():
    """Inicializa o navegador Chrome."""
    chrome_options = Options()
    if HEADLESS_MODE:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--lang=pt-BR") 
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def abrir_aba_avaliacoes(driver):
    """
    Clica no botão 'Avaliações' para carregar a lista de reviews.
    """
    print("   > Procurando aba 'Avaliações'...")
    try:
        # Tenta achar o botão que contem o texto "Avaliações" ou "Reviews"
        # O Google muda muito as classes, então busca por texto é mais seguro (XPath)
        wait = WebDriverWait(driver, 10)
        botao_avaliacoes = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@aria-label, 'Avaliações') or contains(text(), 'Avaliações')]")
        ))
        botao_avaliacoes.click()
        time.sleep(3) # Espera a aba carregar
        print("   > Aba 'Avaliações' aberta com sucesso.")
        return True
    except Exception as e:
        print(f"   > Erro ao abrir aba de avaliações: {e}")
        return False

def fazer_scroll_infinito(driver):
    """Rola a lista de reviews."""
    print("   > Iniciando scroll...")
    try:
        # A lista de reviews fica dentro de um container com role='feed' ou classes específicas
        # Vamos tentar achar o elemento que contém os reviews
        scrollable_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"], .m6QErb.DxyBCb.kA9KIf.dS8AEf'))
        )
        
        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
        
        # Contador de tentativas sem mudança para evitar loop infinito
        tentativas_sem_mudanca = 0
        
        while True:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(2)
            
            new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
            
            # Conta quantos reviews já apareceram
            reviews_visiveis = len(driver.find_elements(By.CSS_SELECTOR, 'div[data-review-id]'))
            
            if new_height == last_height:
                tentativas_sem_mudanca += 1
                if tentativas_sem_mudanca >= 3: # Se tentou 3x e não desceu mais, acabou
                    print("   > Fim da lista de reviews (ou travou).")
                    break
            else:
                tentativas_sem_mudanca = 0 # Reseta se houve movimento
            
            last_height = new_height
            
            if reviews_visiveis >= MAX_REVIEWS_POR_UPA:
                print(f"   > Atingiu limite de {MAX_REVIEWS_POR_UPA} reviews.")
                break
                
    except Exception as e:
        print(f"   > Aviso no scroll: {e}")

def extrair_dados(driver, nome_upa):
    """Lê os cards de review visíveis."""
    print(f"   > Lendo dados de {nome_upa}...")
    
    # Seleciona todos os cards de review
    reviews_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-review-id]')
    
    dados_coletados = []
    
    for element in reviews_elements:
        try:
            # Tenta expandir textos longos ("Ver mais")
            try:
                botao_mais = element.find_element(By.CSS_SELECTOR, 'button[aria-label="Ver mais"]')
                driver.execute_script("arguments[0].click();", botao_mais)
            except:
                pass 

            # Autor
            try: autor = element.find_element(By.CSS_SELECTOR, '.d4r55').text
            except: autor = "Anônimo"

            # Data Relativa
            try: data_relativa = element.find_element(By.CSS_SELECTOR, '.rsqaWe').text
            except: data_relativa = "Desconhecida"

            # Nota
            try:
                nota_texto = element.find_element(By.CSS_SELECTOR, '.kvMYJc').get_attribute("aria-label")
                nota = float(nota_texto.split(" ")[0].replace(",", "."))
            except: nota = 0

            # Texto
            try: texto = element.find_element(By.CSS_SELECTOR, '.wiI7pd').text
            except: texto = ""

            dados_coletados.append({
                "UPA": nome_upa,
                "Autor": autor,
                "Data_Relativa": data_relativa,
                "Nota": nota,
                "Texto": texto
            })
            
        except:
            continue

    return dados_coletados

def main():
    driver = iniciar_driver()
    todos_dados = []

    try:
        for nome, url in upas_bh_alvos.items():
            if not url: continue

            print(f"\n--- 🏥 Processando: {nome} ---")
            driver.get(url)
            time.sleep(5) 
            
            # 1. Abre a aba de avaliações (CRÍTICO)
            if abrir_aba_avaliacoes(driver):
                # 2. Faz o scroll
                fazer_scroll_infinito(driver)
                # 3. Extrai
                dados_upa = extrair_dados(driver, nome)
                print(f"   > ✅ {len(dados_upa)} reviews coletados.")
                todos_dados.extend(dados_upa)
            else:
                print(f"   > ❌ Falha ao acessar avaliações de {nome}")
            
    finally:
        driver.quit()
        
    # Salva
    if todos_dados:
        df = pd.DataFrame(todos_dados)
        df.to_csv("dados_brutos_upas.csv", index=False, encoding='utf-8-sig')
        print(f"\n📁 Arquivo salvo: dados_brutos_upas.csv ({len(df)} registros)")

if __name__ == "__main__":
    main()