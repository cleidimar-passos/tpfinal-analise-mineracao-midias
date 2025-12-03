import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # Nova importação
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from alvos_upas import upas_bh_alvos

# --- CONFIGURAÇÕES ---
MAX_REVIEWS_POR_UPA = 5000 
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
    Estratégia V4: Scroll Híbrido (JS + Teclado + Foco no Elemento)
    """
    print("   > Iniciando scroll profundo (Modo Híbrido)...")
    try:
        # 1. Encontra o container principal
        scrollable_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"], .m6QErb.DxyBCb.kA9KIf.dS8AEf'))
        )
        
        # Clica no container para garantir que o navegador saiba que estamos lá (foco)
        driver.execute_script("arguments[0].click();", scrollable_div)
        
        last_count = 0
        tentativas_sem_mudanca = 0
        MAX_TENTATIVAS = 15 # Insiste bastante
        
        while True:
            # ESTRATÉGIA A: Scroll via JS direto no container
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(1)
            
            # ESTRATÉGIA B: Envia tecla END (Simula usuário)
            try:
                scrollable_div.send_keys(Keys.END)
            except:
                pass # Alguns elementos não aceitam keys, tudo bem
            
            time.sleep(2)
            
            # ESTRATÉGIA C: Encontra o ÚLTIMO review e foca nele
            # Isso força o Maps a carregar o que vem depois
            cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-review-id]')
            if cards:
                driver.execute_script("arguments[0].scrollIntoView(true);", cards[-1])
            
            time.sleep(2) # Espera carregar
            
            # Verificação de Progresso
            current_count = len(cards)
            print(f"   > Carregando... {current_count} reviews na tela.", end='\r')
            
            if current_count == last_count:
                tentativas_sem_mudanca += 1
                
                # Pulo do Gato: Sobe um pouco e desce de novo para destrancar
                if tentativas_sem_mudanca % 3 == 0:
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight - 2000", scrollable_div)
                    time.sleep(1)
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                
                if tentativas_sem_mudanca >= MAX_TENTATIVAS:
                    print(f"\n   > Scroll finalizado. Estagnou em {current_count} itens.")
                    break
            else:
                tentativas_sem_mudanca = 0 # Reset
                last_count = current_count
            
            if current_count >= MAX_REVIEWS_POR_UPA:
                print(f"\n   > Limite de segurança atingido ({MAX_REVIEWS_POR_UPA}).")
                break
                
    except Exception as e:
        print(f"\n   > Aviso no scroll: {e}")

def extrair_dados(driver, nome_upa):
    """Lê os cards de review visíveis."""
    print(f"   > Extraindo textos de {nome_upa}...")
    
    reviews_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-review-id]')
    dados_coletados = []
    
    # Clica nos botões "Ver mais" visíveis
    try:
        driver.execute_script("""
            document.querySelectorAll('button[aria-label="Ver mais"]').forEach(b => b.click());
        """)
        time.sleep(1)
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