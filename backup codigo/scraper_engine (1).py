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
MAX_REVIEWS_POR_UPA = 5000 # Aumentado para garantir captura total
HEADLESS_MODE = False      

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
    """Clica no botão 'Avaliações'."""
    print("   > Procurando aba 'Avaliações'...")
    try:
        wait = WebDriverWait(driver, 10)
        # Tenta diferentes seletores para garantir
        botao_avaliacoes = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@aria-label, 'Avaliações') or contains(text(), 'Avaliações')]")
        ))
        botao_avaliacoes.click()
        time.sleep(3)
        print("   > Aba 'Avaliações' aberta.")
        return True
    except Exception as e:
        print(f"   > Erro ao abrir aba: {e}")
        return False

def fazer_scroll_infinito(driver):
    """
    Estratégia de scroll agressiva: insiste até ter certeza absoluta que acabou.
    """
    print("   > Iniciando scroll profundo...")
    try:
        # Localiza o container que tem a barra de rolagem
        scrollable_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"], .m6QErb.DxyBCb.kA9KIf.dS8AEf'))
        )
        
        last_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
        tentativas_sem_mudanca = 0
        MAX_TENTATIVAS_SEM_MUDANCA = 10 # Tenta 10 vezes antes de desistir (aprox 30 segundos parado)
        
        while True:
            # Rola para o fundo
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(3) # Tempo para o ícone de carregamento girar
            
            new_height = driver.execute_script("return arguments[0].scrollHeight", scrollable_div)
            
            # Feedback visual no terminal
            reviews_visiveis = len(driver.find_elements(By.CSS_SELECTOR, 'div[data-review-id]'))
            print(f"   > Carregando... {reviews_visiveis} reviews na tela.", end='\r')
            
            if new_height == last_height:
                tentativas_sem_mudanca += 1
                
                # TRUQUE: Rola um pouco pra cima e volta pra baixo pra tentar destravar
                if tentativas_sem_mudanca > 2:
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight - 1500", scrollable_div)
                    time.sleep(1)
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                    time.sleep(2)
                
                if tentativas_sem_mudanca >= MAX_TENTATIVAS_SEM_MUDANCA:
                    print(f"\n   > Scroll finalizado. Parece que chegamos ao fim ({reviews_visiveis} itens).")
                    break
            else:
                tentativas_sem_mudanca = 0 # Reseta o contador se a página cresceu
            
            last_height = new_height
            
            if reviews_visiveis >= MAX_REVIEWS_POR_UPA:
                print(f"\n   > Atingiu limite de segurança ({MAX_REVIEWS_POR_UPA}). Parando.")
                break
                
    except Exception as e:
        print(f"\n   > Aviso no scroll: {e}")

def extrair_dados(driver, nome_upa):
    """Lê os cards de review visíveis."""
    print(f"   > Extraindo textos de {nome_upa}...")
    
    reviews_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-review-id]')
    dados_coletados = []
    
    # Vamos clicar em todos os "Ver mais" de uma vez antes de ler
    try:
        botoes_mais = driver.find_elements(By.CSS_SELECTOR, 'button[aria-label="Ver mais"]')
        if botoes_mais:
            # Clica via JS para ser rápido
            driver.execute_script("arguments[0].click();", botoes_mais[0]) 
            # Nota: clicar em todos pode ser lento, o script foca em pegar o texto que já está lá
    except:
        pass

    for element in reviews_elements:
        try:
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
            try: 
                # Tenta pegar o texto. wiI7pd é a classe padrão do texto
                texto_obj = element.find_element(By.CSS_SELECTOR, '.wiI7pd')
                texto = texto_obj.text
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
            
            if abrir_aba_avaliacoes(driver):
                fazer_scroll_infinito(driver)
                dados_upa = extrair_dados(driver, nome)
                print(f"   > ✅ {len(dados_upa)} reviews coletados.")
                todos_dados.extend(dados_upa)
            else:
                print(f"   > ❌ Falha ao acessar avaliações de {nome}")
            
    finally:
        driver.quit()
        
    if todos_dados:
        df = pd.DataFrame(todos_dados)
        df.to_csv("dados_brutos_upas.csv", index=False, encoding='utf-8-sig')
        print(f"\n📁 Arquivo salvo: dados_brutos_upas.csv ({len(df)} registros totais)")

if __name__ == "__main__":
    main()