from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import pandas as pd  # Adicionando pandas para manipulação de dados
import os
import time

# Load environment variables (CPF and SENHA from .env file)
load_dotenv()

def initialize_browser():
    """Initialize the Edge browser and open COFIN website"""
    # Path to the Edge WebDriver
    webdriver_path = r"C:\Users\44641429820\Desktop\ITENS DA AREA DE TRABALHO\CMB\Repos\github\autocofin_consultas - Copia\msedgedriver.exe"
    
    # Set up Edge options
    edge_options = Options()
    edge_options.add_experimental_option("detach", True)  # Keep browser open after script ends
    edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress console messages
    
    # Initialize the Edge WebDriver service
    service = Service(executable_path=webdriver_path)
    
    # Create the WebDriver with the specified options
    driver = webdriver.Edge(service=service, options=edge_options)
    
    # Open the COFIN website
    driver.get("https://acesso.cofin.sp.gov.br/Account/Login?ReturnUrl=%2Fconnect%2Fauthorize%2Fcallback%3Fresponse_type%3Dcode%26client_id%3Dclient_id_angular%26state%3DTDhPY1VJVm1XcEZGdjB0MUhkNnZITEh-T09KZF80LmNPdk9qTDJkZHB-LU1Ssemicolonhttps%25253A%25252F%25252Fcofin.sp.gov.br%25252F%26redirect_uri%3Dhttps%253A%252F%252Fcofin.sp.gov.br%252Findex.html%26scope%3Dopenid%2520profile%2520email%2520offline_access%2520api%2520identity_api%2520diligencia_api%2520relatorios_api%2520sefaz_integration_api%2520gestao_patrimonial_api%26code_challenge%3DRXnXsEfK1ZPMOVw9qqPhpPXwwM_u7bUl2jWAjyFDUm8%26code_challenge_method%3DS256%26nonce%3DTDhPY1VJVm1XcEZGdjB0MUhkNnZITEh-T09KZF80LmNPdk9qTDJkZHB-LU1S")
    
    # Maximize the window for better visibility
    driver.maximize_window()
    
    print("Browser window opened successfully! It will remain open even if you close VS Code.")
    return driver

def login(driver):
    """Login to the COFIN website using credentials from .env file"""
    try:
        # Get credentials from environment variables
        cpf = os.getenv('CPF')
        senha = os.getenv('SENHA')
        
        if not cpf or not senha:
            print("Error: CPF or SENHA not found in .env file")
            return False
        
        # Wait for the CPF input field to be visible and enter CPF
        cpf_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "txtCpf"))
        )
        cpf_input.clear()
        cpf_input.send_keys(cpf)
        print("CPF entered successfully")
        
        # Wait for the Password input field to be visible and enter senha
        senha_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "Password"))
        )
        senha_input.clear()
        senha_input.send_keys(senha)
        print("Password entered successfully")
        
        # Optional: Add a slight delay to allow manual verification before any automatic submission
        time.sleep(1)
        
        print("Please solve the CAPTCHA and click the login button manually")
        return True
    except Exception as e:
        print(f"Error during login process: {str(e)}")
        return False

def wait_for_dashboard(driver, timeout=60):
    """Wait for the dashboard page to load after login"""
    try:
        print("Waiting for dashboard to load...")
        WebDriverWait(driver, timeout).until(
            lambda d: d.current_url.startswith("https://cofin.sp.gov.br/#/")
        )
        print(f"Dashboard loaded successfully! Current URL: {driver.current_url}")
        return True
    except Exception as e:
        print(f"Error while waiting for dashboard: {str(e)}")
        return False

def navigate_to_patrimonio_consultar(driver):
    """Navigate to Patrimônio > Consultar section"""
    try:
        # Wait for 5 seconds after dashboard is loaded
        print("Waiting 5 seconds before navigating...")
        time.sleep(5)
        
        # Click on Patrimônio menu item
        patrimonio_xpath = '//*[@id="pages-sidebar"]/app-sidebar/div[2]/ul/li/a'
        patrimonio_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, patrimonio_xpath))
        )
        print("Clicking on Patrimônio menu...")
        patrimonio_menu.click()
        time.sleep(1)  # Wait for submenu to appear
        
        # Click on Consultar submenu item
        consultar_xpath = '//*[@id="pages-sidebar"]/app-sidebar/div[2]/ul/li/ul/li[1]/a'
        consultar_menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, consultar_xpath))
        )
        print("Clicking on Consultar submenu...")
        consultar_menu.click()
        
        print("Successfully navigated to Patrimônio > Consultar section")
        return True
    except Exception as e:
        print(f"Error during navigation to Patrimônio > Consultar: {str(e)}")
        return False

def search_by_serial_number(driver, serial_number="SSL51514", max_attempts=20):
    """Wait for the serial number input field to become available and then search with retry logic"""
    attempt = 1
    while attempt <= max_attempts:
        try:
            print(f"Attempt {attempt}/{max_attempts} to interact with search form")
            
            # Check if the blocking UI is active
            try:
                block_ui = driver.find_element(By.CLASS_NAME, "block-ui-wrapper.block-ui-main.active")
                print("Blocking UI is still active, waiting for it to disappear...")
                time.sleep(2)
                continue  # Skip to next attempt if blocking UI is present
            except:
                print("No blocking UI detected, proceeding with input")
            
            # Try to find and interact with the serial number input field
            try:
                print("Looking for serial number input field...")
                input_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "inputTextNumeroSerie"))
                )
                
                # Clear and send input with retry logic
                try:
                    input_field.clear()
                    input_field.send_keys(serial_number)
                    print(f"Entered serial number: {serial_number}")
                except Exception as e:
                    print(f"Could not input serial number: {str(e)}")
                    time.sleep(2)
                    continue  # Try again
            except Exception as e:
                print(f"Could not find input field: {str(e)}")
                time.sleep(2)
                continue  # Try again
            
            # Try to find and click the search button
            try:
                print("Looking for 'Encontrar' button...")
                search_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "btnEncontrarMaterial"))
                )
                
                # Try regular click first
                try:
                    print("Attempting to click the button normally...")
                    search_button.click()
                    print("Clicked the 'Encontrar' button successfully")
                    return True
                except Exception as e:
                    print(f"Normal click failed: {str(e)}")
                    
                    # Try JavaScript click as fallback
                    try:
                        print("Attempting JavaScript click as fallback...")
                        driver.execute_script("arguments[0].click();", search_button)
                        print("JavaScript click on 'Encontrar' button successful")
                        return True
                    except Exception as js_e:
                        print(f"JavaScript click also failed: {str(js_e)}")
                        time.sleep(2)
                        continue  # Try again
            except Exception as e:
                print(f"Could not find button: {str(e)}")
                time.sleep(2)
                continue  # Try again
                
        except Exception as e:
            print(f"Error during attempt {attempt}: {str(e)}")
        
        # Increment attempt counter
        attempt += 1
        time.sleep(3)  # Wait between attempts
    
    print(f"Failed to complete search after {max_attempts} attempts")
    return False

def verify_search_result(driver, serial_number, max_attempts=30):
    """
    Verifica se a busca foi bem-sucedida através da mudança de URL
    Retenta a busca se necessário
    """
    initial_url = "https://cofin.sp.gov.br/#/menu/gestao-patrimonial/movimentacao-materiais/consultar-movimentacao"
    attempt = 1
    
    while attempt <= max_attempts:
        print(f"Verificação {attempt}/{max_attempts} do resultado da busca para {serial_number}")
        
        # Aguarda até 10 segundos para ver se a URL muda
        try:
            # Verifica se ainda estamos na URL inicial (o que indica que a busca não teve sucesso)
            current_url = driver.current_url
            print(f"URL atual: {current_url}")
            
            if current_url != initial_url:
                print(f"URL mudou: busca bem-sucedida para {serial_number}")
                return True
                
            print(f"URL não mudou após {attempt} tentativa(s). Tentando novamente...")
            
            # Tenta clicar no botão novamente
            try:
                search_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "btnEncontrarMaterial"))
                )
                
                # Tenta clique normal
                try:
                    search_button.click()
                    print(f"Tentativa {attempt}: botão Encontrar clicado")
                except Exception as e:
                    print(f"Clique normal falhou: {str(e)}")
                    
                    # Tenta JavaScript click como fallback
                    try:
                        driver.execute_script("arguments[0].click();", search_button)
                        print(f"Tentativa {attempt}: JavaScript click realizado no botão Encontrar")
                    except Exception as js_e:
                        print(f"JavaScript click também falhou: {str(js_e)}")
                
                # Aguarda 5 segundos para ver se a URL muda após a nova tentativa
                time.sleep(5)
                
            except Exception as e:
                print(f"Não foi possível encontrar o botão para nova tentativa: {str(e)}")
            
        except Exception as e:
            print(f"Erro ao verificar URL na tentativa {attempt}: {str(e)}")
        
        attempt += 1
        time.sleep(2)
    
    print(f"Falha na busca de {serial_number} após {max_attempts} tentativas: URL não mudou")
    return False

def extract_material_details(driver):
    """
    Extrai os detalhes do material da página
    Retorna um dicionário com os dados extraídos ou None se falhar
    """
    print("Aguardando carregamento da página de detalhes do material...")
    max_attempts = 30  # Número máximo de tentativas
    attempt = 1
    material_data = {}  # Dicionário para armazenar os dados extraídos
    
    # Caminho para o div principal que contém os detalhes
    details_xpath = '//*[@id="canvas-bookmark"]/div/div[2]/main/app-detalhar-material-visualizar/div/div/div/form/div[1]/div[2]'
    
    while attempt <= max_attempts:
        try:
            print(f"Tentativa {attempt}/{max_attempts} para extrair os detalhes do material")
            
            # Tenta localizar a div principal de detalhes
            try:
                details_container = WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located((By.XPATH, details_xpath))
                )
                
                # Verifica se encontrou a div de detalhes
                if not details_container:
                    print("Container de detalhes não encontrado, aguardando...")
                    time.sleep(2)
                    attempt += 1
                    continue
                    
                # Encontra todas as divs de coluna que contêm os campos
                columns = details_container.find_elements(By.CSS_SELECTOR, "div[class^='col-sm-']")
                
                if not columns or len(columns) < 5:  # Espera pelo menos 5 campos
                    print(f"Apenas {len(columns) if columns else 0} colunas encontradas, página pode não estar totalmente carregada")
                    time.sleep(2)
                    attempt += 1
                    continue
                
                # Processa cada coluna para extrair rótulo e valor
                for column in columns:
                    column_text = column.text.strip()
                    
                    # Pula colunas vazias
                    if not column_text:
                        continue
                        
                    # A maioria das colunas segue o formato "Rótulo:\nValor"
                    if ":" in column_text:
                        parts = column_text.split(":", 1)
                        label = parts[0].strip()
                        value = parts[1].strip()
                        material_data[label] = value
                
                # Se extraímos um número razoável de campos, podemos prosseguir
                if len(material_data) >= 5:
                    print(f"Extraídos com sucesso {len(material_data)} campos")
                    return material_data
                else:
                    print(f"Apenas {len(material_data)} campos extraídos, tentando novamente...")
                    material_data = {}  # Reinicia e tenta novamente
                    
            except Exception as e:
                print(f"Erro ao encontrar ou processar elementos: {str(e)}")
            
            attempt += 1
            time.sleep(2)
            
        except Exception as e:
            print(f"Erro geral durante a tentativa {attempt}: {str(e)}")
            attempt += 1
            time.sleep(2)
    
    print("Falha ao extrair detalhes do material após várias tentativas")
    return None

def go_back(driver, max_attempts=15):
    """
    Retorna à página de consulta navegando diretamente pela URL, recarrega a página e
    garante que estamos na página correta antes de continuar com a automação
    """
    search_url = "https://cofin.sp.gov.br/#/menu/gestao-patrimonial/movimentacao-materiais/consultar-movimentacao"
    attempt = 1
    
    while attempt <= max_attempts:
        try:
            print(f"Tentativa {attempt}/{max_attempts} para voltar à página de consulta")
            
            # Primeiro navega para a URL de consulta, independentemente da URL atual
            print("Navegando para a URL de consulta...")
            driver.get(search_url)
            
            # Aguarda para que a navegação complete
            time.sleep(3)
            
            # Verifica se a navegação foi bem-sucedida
            if driver.current_url != search_url:
                print(f"⚠️ Falha na navegação. URL atual: {driver.current_url}")
                attempt += 1
                continue
            
            # Sempre faz um refresh explícito para evitar bugs
            print("🔄 Recarregando a página para evitar bugs...")
            driver.refresh()
            
            # Aguarda pelo menos 5 segundos após o refresh
            print("⏱️ Aguardando 5 segundos para carregamento completo...")
            time.sleep(5)
            
            # Verifica se a página carregou corretamente validando a presença do campo de número de série
            try:
                print("Verificando se o campo de número de série está disponível...")
                input_field = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "inputTextNumeroSerie"))
                )
                
                # Tenta interagir com o campo para garantir que está realmente funcional
                input_field.clear()
                print("Campo de número de série está funcional")
                
                # Verifica também se o botão de pesquisa está presente
                search_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "btnEncontrarMaterial"))
                )
                print("Botão 'Encontrar' também está disponível")
                
                # Verifica se há bloqueio UI ativo
                try:
                    block_ui = driver.find_element(By.CLASS_NAME, "block-ui-wrapper.block-ui-main.active")
                    print("⚠️ Bloqueio UI detectado, aguardando desaparecer...")
                    time.sleep(5)  # Aguarda para o bloqueio desaparecer
                    continue  # Tenta novamente para garantir que o bloqueio desapareceu
                except:
                    print("✓ Nenhum bloqueio UI detectado, página pronta para uso")
                
                print("✅ Confirmado: Estamos na página de consulta e todos os elementos estão disponíveis")
                return True
                
            except Exception as e:
                print(f"⚠️ Elementos da página não estão disponíveis: {str(e)}")
                
                if attempt < max_attempts:
                    print("Tentando nova navegação e refresh...")
            
        except Exception as e:
            print(f"❌ Erro durante a tentativa {attempt} de voltar: {str(e)}")
        
        attempt += 1
        time.sleep(3)
    
    print(f"❌ Falha ao retornar à página de consulta após {max_attempts} tentativas")
    return False

def read_serial_numbers(file_path):
    """Lê os números de série da planilha Excel"""
    try:
        print(f"Lendo números de série do arquivo: {file_path}")
        df = pd.read_excel(file_path)
        
        # Assume que os números de série estão na primeira coluna, começando da segunda linha
        serial_numbers = df.iloc[:, 0].dropna().tolist()
        
        if not serial_numbers:
            print("Nenhum número de série encontrado na planilha")
            return []
            
        print(f"Encontrados {len(serial_numbers)} números de série para processamento")
        return serial_numbers
    
    except Exception as e:
        print(f"Erro ao ler a planilha de números de série: {str(e)}")
        return []

if __name__ == "__main__":
    # Caminho para a planilha de números de série
    serial_numbers_file = r"C:\Users\44641429820\Desktop\ITENS DA AREA DE TRABALHO\CMB\Repos\github\autocofin_consultas - Copia\n.xlsx"
    
    # Arquivo Excel para salvar os resultados
    output_file = r"C:\Users\44641429820\Desktop\ITENS DA AREA DE TRABALHO\CMB\Repos\github\autocofin_consultas - Copia\resultados_materiais.xlsx"
    
    # Lê os números de série da planilha
    serial_numbers = read_serial_numbers(serial_numbers_file)
    
    if not serial_numbers:
        print("Nenhum número de série para processar. Encerrando.")
        exit()
    
    # Lista para armazenar todos os resultados
    all_results = []
    
    # Initialize the browser
    driver = initialize_browser()
    
    # Login to the website
    login_success = login(driver)
    if login_success:
        print("Login credentials entered successfully")
        
        # Wait for user to solve CAPTCHA and complete login
        if wait_for_dashboard(driver):
            # Navigate to Patrimônio > Consultar
            if navigate_to_patrimonio_consultar(driver):
                
                # Processa cada número de série da lista
                for i, serial_number in enumerate(serial_numbers, 1):
                    print(f"\n--- Processando item {i}/{len(serial_numbers)}: {serial_number} ---\n")
                    
                    # Busca pelo número de série atual
                    search_success = search_by_serial_number(driver, serial_number)
                    
                    if search_success:
                        # Verifica se a busca realmente resultou em uma mudança de URL
                        result_success = verify_search_result(driver, serial_number)
                        
                        if result_success:
                            # Extrai os detalhes se a busca foi bem-sucedida e a URL mudou
                            material_data = extract_material_details(driver)
                            
                            if material_data:
                                # Adiciona o número de série explicitamente aos dados (caso não tenha sido extraído)
                                material_data['Numero_Serie_Pesquisado'] = serial_number
                                all_results.append(material_data)
                                print(f"Dados do item {serial_number} extraídos com sucesso")
                                
                                # Volta para a página de busca
                                go_back(driver)
                            else:
                                print(f"Falha ao extrair dados para o item {serial_number}")
                        else:
                            print(f"Item com número de série {serial_number} não foi encontrado (URL não mudou)")
                    else:
                        print(f"Não foi possível pesquisar o item com número de série: {serial_number}")
                
                # Salva todos os resultados em um único arquivo Excel
                if all_results:
                    try:
                        print(f"\nSalvando {len(all_results)} itens no arquivo Excel...")
                        df_results = pd.DataFrame(all_results)
                        df_results.to_excel(output_file, index=False)
                        print(f"Resultados salvos com sucesso em: {output_file}")
                    except Exception as e:
                        print(f"Erro ao salvar resultados: {str(e)}")
                        
                        # Fallback: exibe um resumo dos dados no console
                        print("\nResumo dos dados coletados:")
                        for i, result in enumerate(all_results, 1):
                            print(f"Item {i}: {result.get('Nº Série', 'Desconhecido')} - {result.get('Material', 'Desconhecido')}")
                else:
                    print("Nenhum dado foi extraído para salvar")
    else:
        print("Failed to enter login credentials")
    
    print("\nProcessamento completo. O navegador permanecerá aberto.")
    # The browser will stay open due to the "detach" option