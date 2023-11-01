
# * IMPORTS *
# ***********
try:
    # ? Selenium  
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver import ActionChains

    # ? Table
    from rich.console import Console
    from rich.table import Table

    # ? Config custom file
    from config import Config

    # ? Import Date
    from datetime import date
    from datetime import timedelta

    # ? Standard libraries
    import sys, pickle, os, time, html, maskpass

    # ? Pretty text for CMD
    from pyfiglet import Figlet

    # ? Text colored in CMD
    from colored import fg
except ImportError:
    print("""
    Debes ejecutar el siguiente comando antes de ejecutar Zinkee CMD:
        - pip install -r requirements.txt
    """)
# * ------- *


# * SCRAPPING WEB *
# ***************** 
def init_chrome(): # ? Init chrome driver for scrapping

    options=Options() # ? init options for chrome

    # ? Adding options for chrome
    options.add_experimental_option("detach", True) # ? I dont know who do that exactly but fix a error of chrome
    options.add_argument("--window-size=1920,1080") # ? Window size
    options.add_argument("--disable-web-security")
    
    # ? Disable notificatiosn of chrome
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxy-server") # ? No proxy in chrome
    options.add_argument("--disable-blink-features=AutomationControlled") # ? VERY IMPORTANT | Neccesary for driver of chrome

    # ? More options...
    exp_opt = [
        'enable-automation',
        'ignore-certificate-errors',
        'enable-logging',
    ]

    options.add_experimental_option("excludeSwitches", exp_opt)

    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "intl.accept_languages": ['es-ES', 'es'], # ? Language
        "credentials_enable_service": False, # ? Language
    }

    options.add_experimental_option("prefs", prefs)

    s = ChromeService() # ? Init service of chrome (neccesary for execute chrome driver)

    driver = webdriver.Chrome(service=s, options=options)

    user_agent=driver.execute_script("return navigator.userAgent;") # ? Get auto. chrome User Agent
    options.add_argument(f"user-agent={user_agent}") # ? Set User Agent
    
    driver.set_window_position(0,0) # ? Window position

    return driver    

def login_zinkee(driver_z, wait): # ? Login in Zinkee with your credentials

    print("Abriendo Zinkee...", end="")
    
    # ! Important ! Is recommended not activate this function, 
    # ! Zinkee dont save credentials in cookies and this proccess affects performance
    # ? Checking credentials in Zinkee cookies. If havent this file, the script will create
    if config.get_save_cookies() and os.path.isfile('zinkee.cookies'):
        cookies=pickle.load(open('zinkee.cookies', 'rb'))
        driver_z.get("https://app.zinkee.cloud/login")
        
        time.sleep(3)
        
        for cookie in cookies:
            driver_z.add_cookie(cookie) # ? Adding cookies to the driver

        driver_z.get("https://app.zinkee.cloud/home")

        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".toolbar-button")))
        except TimeoutException:
            pass
    else:
        driver_z.get("https://app.zinkee.cloud/login")

    print(success_color+"OK"+light_color)

    print("Iniciando sesión...", end="")
    
    # ? Getting email field of login form
    try:
        email_field = wait.until(EC.visibility_of_element_located((By.ID, "mat-input-0")))    
        email_field.send_keys(config.get_email())
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" Finalizó el tiempo de espera. No se pudo recoger el campo 'Email' ")
        return "ERROR"
    
    except Exception:
        print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        return "ERROR"

    # ? Getting password field of login form
    try:
        password_field = wait.until(EC.visibility_of_element_located((By.ID, "mat-input-1")))
        password_field.send_keys(config.get_passw())
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" Finalizó el tiempo de espera. No se pudo recoger el campo 'Password' ")
        return "ERROR"
    
    except Exception:
        print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        return "ERROR"

    # ? Clicking submit btn to login
    submit_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "submit-button")))
    submit_btn.click()

    # ? Check if toolbar btn is loaded and exists, that means that login was succesfully
    try:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".toolbar-button")))
        print(success_color+"OK"+light_color)
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" No se ha podido iniciar sesión correctamente")
        return "ERROR"

    except Exception:
        print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        return "ERROR"

    # ! Important ! Is recommended not activate this function
    # ? If have config cookies option in true, save cookies of login
    if config.get_save_cookies():
        cookies = driver_z.get_cookies()
        
        try: 
            pickle.dump(cookies, open('zinkee.cookies', 'wb'))
            print(success_color+" (Se han guardado las cookies) "+light_color)
        except Exception:
            print(error_color+" (No se pudieron guardar las cookies) " + light_color)
        
    return "OK"

def open_daily_track(driver_z, wait): # ? Open Daily track Page in Zinkee
    print("Abriendo track diario...", end='')
    
    # ? Open sidebar dashboard
    try:
        toolbar_btn=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".toolbar-button")))
        toolbar_btn.click()        
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" No se ha podido abrir el track diario")
        return "ERROR"
    
    except Exception:
        print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        return "ERROR"

    # ? Open pages dropdown in sidebar
    try:
        dropdown_aside=wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/layout-main/div/router-content/app-home/div/zinkee-sidebar[1]/home-left-sidebar-no-locked-open/div/div[3]/div/div/mat-accordion/mat-expansion-panel/div/div/mat-tree/mat-tree-node[2]/div[1]/button/span[1]/mat-icon')))
        dropdown_aside.click()        
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" No se ha podido abrir el desplegable 'Time Tracking'")
        return "ERROR"
    
    except Exception:
        print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        return "ERROR"

    # ? Getting and clicking Daily Track sidebar option to open Daily Track Page
    try:
        track_today=wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/layout-main/div/router-content/app-home/div/zinkee-sidebar[1]/home-left-sidebar-no-locked-open/div/div[3]/div/div/mat-accordion/mat-expansion-panel/div/div/mat-tree/mat-tree-node[3]')))
        track_today.click()        
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" No se ha podido abrir el desplegable 'Time Tracking / Hoy'")
        return "ERROR"
    
    except Exception:
        print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        return "ERROR"

    print(success_color+"OK"+light_color)

def open_track(driver_z, wait): # ? Open all tracks Page in Zinkee
    print("Abriendo track diario...", end='')
    
    # ? Open sidebar dashboard and clicking to open Track Page
    try:
        dashboard_track=wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/layout-main/div/router-content/app-home/div/div/router-content/dashboard/div/div/div[3]")))
        dashboard_track.click()        
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" No se ha podido abrir el track")
        return "ERROR"
    
    except Exception:
        print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        return "ERROR"


    print(success_color+"OK"+light_color)

def add_new_register(driver_z, wait, values): # ? Add new register with your data
    print("Añandiendo registro...", end='')

    time.sleep(1.2)

    # ? Getting btn to add register and clicking
    try:
        btn_add=wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/layout-main/div/router-content/app-home/div/div/router-content/app-mant/div/div/mant-toolbar/div/div[1]/button")))
        btn_add.click()        
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" No se ha podido clickar en el botón de añadir registro")
        return "ERROR"
    
    except Exception:
        print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        return "ERROR"

    time.sleep(1.2)

    # ? Getting values separately
    project_value = values[0].strip()
    name_task_value = values[1].strip()
    start_time_value = values[2].strip().replace(":", "")
    end_time_value = values[3].strip().replace(":", "")
    
    # ? Check if details value exists
    if len(values) >= 5:
        details_value = values[4].strip()
    else:
        details_value = ""

    # ? Getting select to add project and double clicking
    try:
        project_selector=wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/layout-main/div/router-content/app-home/div/div/router-content/app-mant/div/div/app-ag-grid-custom/ag-grid-angular/div/div[2]/div[2]/div[2]/div[2]/div/div/div[6]")))
        action = ActionChains(driver_z)
        action.double_click(project_selector).perform()
        
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" No se ha podido añadir el proyecto al registro")
        return "ERROR"
    
    except Exception:
        print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        return "ERROR"

    time.sleep(1.2)

    # ? Getting select to add project and selecting project
    try:
        project_selector_dropdown=wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'"+ project_value +"')]"))) # Hacer string tarea modificable
        project_selector_dropdown.click()
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" No se ha podido añadir el proyecto al registro")
        return "ERROR"
    
    except Exception:
       print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
       return "ERROR"

    # ? Getting description field to add name task and double clicking
    try:
        description=wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/layout-main/div/router-content/app-home/div/div/router-content/app-mant/div/div/app-ag-grid-custom/ag-grid-angular/div/div[2]/div[2]/div[2]/div[2]/div/div/div[8]"))) 
        action = ActionChains(driver_z)
        action.double_click(description).perform()

        desc_input=wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/layout-main/div/router-content/app-home/div/div/router-content/app-mant/div/div/app-ag-grid-custom/ag-grid-angular/div/div[2]/div[2]/div[2]/div[2]/div/div/div[8]/cell-editor-texto/input"))) 
        desc_input.send_keys(name_task_value)  # ? Sending value to name task input
        
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" No se ha podido añadir la descripción al registro")
        return "ERROR"
    
    except Exception:
        print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        return "ERROR"

    # ? Getting time of entry field and sending a letter to activate input
    try:
        start_time=wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/layout-main/div/router-content/app-home/div/div/router-content/app-mant/div/div/app-ag-grid-custom/ag-grid-angular/div/div[2]/div[2]/div[2]/div[2]/div/div/div[9]"))) 
        start_time.send_keys("X")

        start_time_input=wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/layout-main/div/router-content/app-home/div/div/router-content/app-mant/div/div/app-ag-grid-custom/ag-grid-angular/div/div[2]/div[2]/div[2]/div[2]/div/div/div[9]/cell-editor-hora/app-hora/mat-form-field/div/div[1]/div/input"))) 
        start_time_input.send_keys(start_time_value) # ? Sending real value
        
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" No se ha podido añadir la hora de inicio al registro")
        return "ERROR"
    
 
    # ? Getting departure time field and sending a letter to activate input
    try:
        end_time=wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/layout-main/div/router-content/app-home/div/div/router-content/app-mant/div/div/app-ag-grid-custom/ag-grid-angular/div/div[2]/div[2]/div[2]/div[2]/div/div/div[10]"))) 
        end_time.send_keys("X")

        end_time_input=wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/layout-main/div/router-content/app-home/div/div/router-content/app-mant/div/div/app-ag-grid-custom/ag-grid-angular/div/div[2]/div[2]/div[2]/div[2]/div/div/div[10]/cell-editor-hora/app-hora/mat-form-field/div/div[1]/div/input"))) 
        end_time_input.send_keys(end_time_value) # ? Sending real value
        
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" No se ha podido añadir la hora de fin al registro")
        return "ERROR"
    
    except Exception:
        print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        return "ERROR"

    # ? If details value is not empty, select details field and sent details value
    if details_value != "":
        try:
            blur=wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/layout-main/div/router-content/app-home/div/div/router-content/app-mant/div/div/app-ag-grid-custom/ag-grid-angular/div/div[2]/div[2]/div[2]/div[2]/div/div/div[11]"))) 
            blur.click()
            
            # ? Double clicking to open textarea
            extra_info=wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/layout-main/div/router-content/app-home/div/div/router-content/app-mant/div/div/app-ag-grid-custom/ag-grid-angular/div/div[2]/div[2]/div[2]/div[2]/div/div/div[12]"))) 
            action = ActionChains(driver_z)
            action.double_click(extra_info).perform()

            extra_info_input=wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/layout-main/div/router-content/app-home/div/div/router-content/app-mant/div/div/app-ag-grid-custom/ag-grid-angular/div/div[6]/div/cell-editor-texto-largo/div[1]/textarea"))) 
            extra_info_input.send_keys(details_value) # ? Sending value     

            # ? Clicking OK btn to apply details value
            ok_btn=wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/app-root/layout-main/div/router-content/app-home/div/div/router-content/app-mant/div/div/app-ag-grid-custom/ag-grid-angular/div/div[6]/div/cell-editor-texto-largo/div[2]/button[1]"))) 
            ok_btn.click()
                
        except TimeoutException:
            print(error_color+"ERROR:"+light_color+" No se ha podido añadir la observación")
            return "ERROR"
        
        except Exception:
            print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
            return "ERROR"

    # ? Getting btn 'Aceptar' to add register and clicking
    try:   
        apply_btn=wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/app-root/layout-main/div/router-content/app-home/div/div/router-content/app-mant/div/div/mant-toolbar/div/div[2]/button[1]")))
        apply_btn.click()    

    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" No se ha podido pulsar sobre el botón 'Aplicar'")
        return "ERROR"
    
    except Exception:
        print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        return "ERROR"

    print(success_color+"OK"+light_color)

def fast_login(driver): # ? Other way to login in Zinkee
    print("Abriendo Zinkee...", end="")
    
    # ! Important ! Is recommended not activate this function, 
    # ! Zinkee dont save credentials in cookies and this proccess affects performance
    # ? Checking credentials in Zinkee cookies. If havent this file, the script will create
    if config.get_save_cookies() and os.path.isfile('zinkee.cookies'):
        cookies=pickle.load(open('zinkee.cookies', 'rb'))
        driver.get("https://app.zinkee.cloud/home/mant/3/kpi/8")
        
        time.sleep(3)
        
        for cookie in cookies:
            driver.add_cookie(cookie) # ? Adding cookies to the driver

        driver.get("https://app.zinkee.cloud/home/mant/3/kpi/8")

    else:
        driver.get("https://app.zinkee.cloud/home/mant/3/kpi/8")

    print(success_color+"OK"+light_color)

    print("Iniciando sesión...", end="")
    time.sleep(2)

    # ? Getting email field of login form
    try:
        email_field = driver.find_element(By.ID, "mat-input-0")    
        email_field.send_keys(config.get_email())
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" Finalizó el tiempo de espera. No se pudo recoger el campo 'Email' ")
        return "ERROR"
    except Exception:
        print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        return "ERROR"

    # ? Getting password field of login form
    try:
        password_field = driver.find_element(By.ID, "mat-input-1")
        password_field.send_keys(config.get_passw())
    except TimeoutException:
        print(error_color+"ERROR:"+light_color+" Finalizó el tiempo de espera. No se pudo recoger el campo 'Password' ")
        return "ERROR"
    
    except Exception:
        print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        return "ERROR"

    # ? Getting submit btn of login form
    submit_btn = driver.find_element(By.CLASS_NAME, "submit-button")
    submit_btn.click()

    print(success_color+"OK"+light_color)

    time.sleep(4)

def fill_registers(driver_z): # ? Get all register of Daily track (with or withour filter added) and set it in a dict
    array = []
    registers_readed = driver_z.find_elements(By.CSS_SELECTOR, ".ag-center-cols-container > div") # ? Getting parent element of registers to loop
    
    for register in registers_readed: # ? Loop registers
        try:
            # ? Getting data of each field
            creation_date = register.find_element(By.CSS_SELECTOR, ".ag-center-cols-container > div .fecha").text
            project = register.find_element(By.CSS_SELECTOR, ".ag-center-cols-container div[aria-colindex='5']:not(.ag-header-cell)").get_attribute('title')
            service_family = register.find_element(By.CSS_SELECTOR, ".ag-center-cols-container div[aria-colindex='6']:not(.ag-header-cell)").get_attribute('title')
            task_name = register.find_element(By.CSS_SELECTOR, ".ag-center-cols-container div[aria-colindex='7']:not(.ag-header-cell)").get_attribute('title')
            time_start = register.find_element(By.CSS_SELECTOR, ".ag-center-cols-container div[aria-colindex='8']:not(.ag-header-cell) .ag-cell-value").text
            time_end = register.find_element(By.CSS_SELECTOR, ".ag-center-cols-container div[aria-colindex='9']:not(.ag-header-cell) .ag-cell-value").text
            total_hours = register.find_element(By.CSS_SELECTOR, ".ag-center-cols-container div[aria-colindex='10']:not(.ag-header-cell) .ag-cell-value").text
        
        except TimeoutException:
            print(error_color+"ERROR:"+light_color+" Finalizó el tiempo de espera. No se pudo recoger el valor de los campos ")
            
        except Exception:
            print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        
        # ? Append this data to array and return
        array.append({'Fecha de creación': creation_date,
                            'Proyecto': project, 
                            'Familia de Servicios': service_family, 
                            'Nombre Tarea': task_name, 
                            'Hora Inicio': time_start, 
                            'Hora Fin': time_end, 
                            'Total Horas': total_hours})
        
    return array

def list_registers_last_week(days): # ? List and print all register of last week in differents tables 
    driver_z = init_chrome() # ? Init chrome driver, service...

    result = fast_login(driver_z) # ? Login in Zinkee
    check_scrapping(result, driver_z) # ? Check that last scrapping have no errors

    days_allowed = [] # ? Days allowed to select (23-05-2023, 24-05-2023...)
    week_registers = [] # ? Registers of the week sorted by days

    # ? Fill search input with each day of the week (with this format dd-mm-YYYY) and get/print the registers
    for day in days:
        time.sleep(1)

        search_input = driver_z.find_element(By.CSS_SELECTOR, "#mant-main-container > mant-toolbar > div > div.toolbar-group-button-center.ng-star-inserted > div.px-8.px-md-16.input-search-container > input")
        search_input.send_keys(day) # ? Sending value to write in search input
        
        time.sleep(2.5)

        registers = fill_registers(driver_z) # ? Getting registers from value written in seach input
        
        # ? Printing registers in table
        if len(registers) > 0:
            days_allowed.append(day)
            week_registers.append({"day": day, "week_registers": registers})
            print_table(registers, "Filtro por " + day)
        else:
            print(info_color+"\nINFO:"+light_color+" NO EXISTEN REGISTROS DEL DÍA " + primary_color+day+light_color)

        # ? Deleting value of search input
        search_input.send_keys(Keys.CONTROL, 'a')
        search_input.send_keys(Keys.BACKSPACE)
    
    print("\nMostrando últimos 7 días..."+success_color+"OK"+light_color) 
    
    return driver_z, week_registers, days_allowed

def list_registers(is_filter, default_value, close): # ? List and print all register (with or withour filter added)
    
    driver_z = init_chrome() # ? Init chrome driver, service...

    result = fast_login(driver_z) # ? Login in Zinkee
    check_scrapping(result, driver_z) # ? Check that last scrapping have no errors
    
    # ? If is_filter is true means that the results must be filtered

    if is_filter:

        # ? If default_value have any value means that the script wont ask to user for filter
        if default_value == "":
            print(info_color+"\nINFO:"+light_color+" Puedes buscar por las columnas 'Fecha de creación', 'Proyecto', 'Familia de Servicios', 'Nombre Tarea', 'Hora Inicio', 'Hora Fin' y 'Total Horas'")
            value = sanitize_text(array_allowed=[], label="\nValor a buscar")
        else:
            value = default_value
        
        # ? Getting Search input in Zinkee Page 
        try:
            search_input = driver_z.find_element(By.CSS_SELECTOR, "#mant-main-container > mant-toolbar > div > div.toolbar-group-button-center.ng-star-inserted > div.px-8.px-md-16.input-search-container > input")
        except TimeoutException:
            print(error_color+"ERROR:"+light_color+" Finalizó el tiempo de espera. No se pudo recoger el campo 'Search' ")
        except Exception:
            print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
        
        search_input.send_keys(value) # ? Sending value to write in search input
        
        time.sleep(1.5)

        print("Obteniendo registros...", end='')
        registers = fill_registers(driver_z) # ? Getting registers from value written in seach input
        print(success_color+"OK"+light_color)
        
        if len(registers) > 0:
            print_table(registers, "Filtro por " + value) # ? Printing registers in a table
        else:
            print(info_color+"\nINFO:"+light_color+" NO EXISTEN REGISTROS PARA EL VALOR " + primary_color+value+light_color)
        
        # ? If 'close' parameter is true, chrome will must close
        if close == True:
            driver_z.quit()

    else:
        print("Obteniendo registros...", end='')
        
        try:
            time.sleep(1)
            
            registers = fill_registers(driver_z) # ? Getting registers
            print(success_color+"OK"+light_color)

            if len(registers) > 0:
                print_table(registers, "Últimos 30 registros") # ? Printing registers in a table
            else:
                print(info_color+"\nINFO:"+light_color+" NO EXISTEN REGISTROS")
            
            # ? If 'close' parameter is true, chrome will must close
            if close == True:
                driver_z.quit()
                
        except TimeoutException:
            print(error_color+"ERROR:"+light_color+" No se ha podido obtener los registros")
            return "ERROR"
        
        except Exception:
            print(error_color+"ERROR:"+light_color+" Algo salió mal. Comprueba tu conexión a internet y vuelve a intentarlo más tarde")
            return "ERROR"

    # ? If 'close' parameter is true, the menu options will show
    if close:
        show_menu() # ? Show options menu
        op_menu = select_menu([0,1,2,3,4,5]) # ? Select option from menu
        do_action_menu(op_menu) # ? Execute option selected from menu
    else: # ? If not, return chrome driver
        return driver_z


# * ----------- *


# * MANAGING SYSTEM *
# ******************* 
def show_menu(): # ? Show menu options to select one
    f = Figlet(font='doom') # ? Font used for 'Zinkee CMD' word

    print(primary_color)
    print(f.renderText('Zinkee CMD'), end="")
    print(light_color)
    
    print("+-------------------+")
    print("| Autor:"+primary_color+" jedahee"+light_color+" |")
    print("+-------------------+\n")
    print(info_color+"[1]"+light_color+" -> Listar registros")
    print(info_color+"[2]"+light_color+" -> Añadir registro")
    print(info_color+"[3]"+light_color+" -> Añadir día de forma automática")
    print(info_color+"[4]"+light_color+" -> Copiar día añadido en los últimos 7 días")
    print(info_color+"[5]"+light_color+" -> Modificar opciones\n")
    print(info_color+"[0]"+light_color+" -> Salir\n")

def select_menu(array_allowed): # ? Select option from menu printed with validations
    op = -1
    op_allow = array_allowed
    
    while op not in op_allow:
        try:
            op = int(input("Selecciona una opción ["+info_color+str(array_allowed[0])+" - "+str(array_allowed[len(array_allowed)-1])+light_color+"] >> "))

            if op not in op_allow:
                print(error_color+"ERROR:"+light_color+" Debes elegir una opción correcta ["+error_color+str(array_allowed[0])+" - "+str(array_allowed[len(array_allowed)-1])+light_color+"]\n")

        except ValueError:
            print(error_color+"ERROR:"+light_color+" Debes elegir una opción correcta ["+error_color+str(array_allowed[0])+" - "+str(array_allowed[len(array_allowed)-1])+light_color+"]\n")
    
    return op

def sanitize_text(array_allowed=[], label="", isTime=False, isPassword=False, isNumber=False): # ? Validate input type
    text = ""
    text_allow = array_allowed
    
    # ? Validate length of input
    if len(text_allow) > 0:
        label = light_color + label + " ["+info_color+ ', '.join(text_allow) +light_color+"]" + info_color + " >> " + light_color

        while text not in text_allow:
            try:
                if not isPassword:
                    text = input(label)
                else:
                    text = maskpass.askpass(prompt=label, mask="*") # ? Format of password input

                if text not in text_allow:
                    print(error_color+"ERROR:"+light_color+" Debes elegir una opción correcta\n")

            except ValueError:
                print(error_color+"ERROR:"+light_color+" Debes elegir una opción correcta\n")     
    else:
        label = light_color + label + info_color + " >> " + light_color
        
        # ? Validating text/password input type
        if not isTime and not isNumber:
            while len(text) <= 0 or text == "":
                try:
                    if not isPassword:
                        text = input(label)
                    else:
                        text = maskpass.askpass(prompt=label, mask="*") # ? Format of password input

                    if len(text) <= 0 or text == "":
                        print(error_color+"ERROR:"+light_color+" El texto no puede estar vacio\n")

                except ValueError:
                    print(error_color+"ERROR:"+light_color+" El texto no puede estar vacio\n")
        
        # ? Validating time input type
        elif not isNumber and isTime:
            not_err = False

            while len(text) != 5 or text[2] != ":" or not not_err:
                try:
                    text = input(label)
                    val1=int(text[:2]) # ? First part of time (08 of 08:10)
                    val2=int(text[3:]) # ? Second part of time (10 of 08:10)

                    if len(text) != 5 or text[2] != ":" or val1 > 23 or val2 > 59: # ? Validating parts...
                        print(error_color+"ERROR:"+light_color+" El formato del horario debe ser 00:00 \n")
                    else:
                        not_err = True
                except ValueError:
                    print(error_color+"ERROR:"+light_color+" El formato del horario debe ser 00:00 \n")
        
        # ? Validating number input type
        elif isNumber and not isTime:
            not_err = False

            while not not_err:
                try:
                    text = int(input(label))
                    not_err = True
                except ValueError:
                    print(error_color+"ERROR:"+light_color+" Debes introducir un número")
            
    return html.escape(str(text).strip()) # ? Return text formatted (withour escapes and blank spaces)

def check_scrapping(result, driver_z): # ? Check if the last scrapping page went wrong
    if result == 'ERROR':
        input("Pulsa "+primary_color+"ENTER"+light_color+" para salir...")
        driver_z.quit()
        sys.exit(1)
    
    elif result == "OK":
        pass

def print_table(array, title_text): # ? List and print register params in a table
    print("\n")

    table = Table(title=title_text)

    rows = []
    
    for a in array:
        rows.append(list(a.values())) # ? Getting values of registers
    
    columns = list(array[0]) # ? Getting headers of registers
    
    for column in columns: # ? Setting headers in table
        table.add_column(column)

    for row in rows:
        table.add_row(*row, style='bright_green') # ? Setting values in table

    console = Console()
    console.print(table) # ? Print table

def do_action_menu(op): # ? Execute action sent in params
    
    if op == 1: # ? List registers 

        # ? Want filter?
        do_filter = sanitize_text(array_allowed=['si', 'no'], label="\n¿Quieres filtrar los resultados?")
        is_filter = True if do_filter == "si" else False

        # ? List registers (if 'is_filter' is False then will list registers without filter, if is True, will list registers by the filter value)
        list_registers(is_filter, "", True)
        
    elif op == 2: # ? Add register
        actual_year = date.today().year 
        actual_month = date.today().month 
        actual_day = date.today().day
        
        # ? Getting register added today
        driver_z = list_registers(True, str(actual_day) + "-" + str(actual_month) + "-" + str(actual_year), False)
        
        # ? Printing info
        print(info_color+"\nINFO:"+light_color+" Escribe los valores de cada columna separados por coma (,)")
        print(info_color+"INFO:"+light_color+" El orden de los valores es 'Proyecto, Nombre Tarea, Hora Inicio, Hora Fin, Observaciones'")

        values=""
        
        # ? Validating values to set in register
        while len(values.split(",")) < 4 or values.split(",")[0] == "" or values.split(",")[1] == "" or values.split(",")[2] == "" or values.split(",")[3] == "":
            values = sanitize_text(array_allowed=[], label="\nEscribe los valores")

            if len(values.split(",")) < 4 or values.split(",")[0] == "" or values.split(",")[1] == "" or values.split(",")[2] == "" or values.split(",")[3] == "":
                print(error_color+"\nERROR:"+light_color+": Deben estar rellenos todos los valores (Observaciones es opcional)")
        
        # ? Wait Webdriver
        wait = WebDriverWait(driver_z, config.get_max_timeout())

        # ? Open Daily track page
        result = open_daily_track(driver_z,wait)
        check_scrapping(result, driver_z) # ? Check that last scrapping have no errors
        
        # ? Adding register with new value 
        result = add_new_register(driver_z, wait, values.split(","))
        check_scrapping(result, driver_z) # ? Check that last scrapping have no errors
        
        driver_z.quit() # ? Quit chrome

        # ? Show menu again
        show_menu() 
        op_menu = select_menu([0,1,2,3,4,5])
        do_action_menu(op_menu)

    elif op == 3: # ? Add registers auto. to complete day, you insert project, task name and details (details is optional) and add registers with the values and times entered in config object
        actual_year = date.today().year 
        actual_month = date.today().month 
        actual_day = date.today().day
        i = 0
        max_registers_loop = 2
        values=""

        # ? Getting register added today
        driver_z = list_registers(True, str(actual_day) + "-" + str(actual_month) + "-" + str(actual_year), False)
        
        # ? Wait Webdriver
        wait = WebDriverWait(driver_z, config.get_max_timeout())

        # ? Open Daily track page
        result = open_daily_track(driver_z,wait)
        print()
        check_scrapping(result, driver_z) # ? Check that last scrapping have no errors
        
        # ? Printing info
        print(info_color+"\nINFO:"+light_color+" Escribe los valores de cada columna separados por coma (,)")
        print(info_color+"INFO:"+light_color+" El orden de los valores es 'Proyecto, Nombre Tarea, Observaciones' (Las horas se añaden automaticamente)")
        
        # ? Validating values to set in register
        while len(values.split(",")) < 2 or values.split(",")[0] == "" or values.split(",")[1] == "":
            values = sanitize_text(array_allowed=[], label="\nEscribe los valores")

            if len(values.split(",")) < 2 or values.split(",")[0] == "" or values.split(",")[1] == "":
                print(error_color+"ERROR:"+light_color+" Deben estar rellenos todos los valores (Observaciones es opcional)")
        
        # ? For each loop change the time to add in register
        while i <= max_registers_loop:

            if (i == 0):
                if len(values.split(",")) >= 3: # ? If the register have details field...
                    details_value = values.split(",")[-1]
                    values = values.split(",")
                    values.pop(-1)

                    values.append(config.get_time_entry_morning())
                    values.append(config.get_time_entry_break())
                    values.append(details_value)
                    
                    values = ",".join(values)
                else:
                    values = values.split(",")
                    
                    values.append(config.get_time_entry_morning())
                    values.append(config.get_time_entry_break())
                    
                    values = ",".join(values) 

            elif (i == 1):
                if len(values.split(",")) >= 5:  # ? If the register have details field...
                    values = values.split(",")
                    
                    values.pop(2)
                    values.pop(2)
                    
                    values.insert(2, config.get_time_departure_break())
                    values.insert(3, config.get_time_departure_morning())
                    
                    values = ",".join(values)
                else:
                    values = values.split(",")
                    
                    values.pop(3)
                    values.pop(2)
                    
                    values.insert(2, config.get_time_departure_break())
                    values.insert(3, config.get_time_departure_morning())
                    
                    values = ",".join(values)
                
            elif (i == 2):
                if len(values.split(",")) >= 5: # ? If the register have details field...
                    values = values.split(",")
                    
                    values.pop(2)
                    values.pop(2)
                    
                    values.insert(2, config.get_time_entry_afternoon())
                    values.insert(3, config.get_time_departure_afternoon())
                    
                    values = ",".join(values)
                else:
                    values = values.split(",")
                    
                    values.pop(3)
                    values.pop(2)
                    
                    values.insert(2, config.get_time_entry_afternoon())
                    values.insert(3, config.get_time_departure_afternoon())
                    
                    values = ",".join(values)
            
            result = add_new_register(driver_z, wait, values.split(",")) # ? Adding new register
            check_scrapping(result, driver_z) # ? Check that last scrapping have no errors
            i+=1
        
        driver_z.quit()
        
        # ? Show menu again
        show_menu()
        op_menu = select_menu([0,1,2,3,4,5])
        do_action_menu(op_menu)

    elif op == 4: # ? List the las week registers, select one day and copy registers of this, then, add a new register for each register copied with the same value 

        today = date.today()
        week_ago = [(today - timedelta(days=i+1)).strftime("%d-%m-%Y") for i in range(7)] # ? Filling array with days of last week
        day_to_add = [] 

        driver_z, week_registers, days_allowed = list_registers_last_week(week_ago) # ? List and print registers of last week | return driver of chrome, 
                                                                                    # ? an array with the registers of week sorted for day and
                                                                                    # ? an array with the days allowed to select

        # ? Select day to copy registers
        day_selected = sanitize_text(array_allowed=days_allowed, label="\nEscoge una fecha")
        
        # ? Wait Webdriver
        wait = WebDriverWait(driver_z, config.get_max_timeout())

        # ? Select registers of day selected
        for week_register in week_registers:
            if str(week_register["day"]) == str(day_selected):
                day_to_add = week_register["week_registers"]

        # ? Open Daily track page        
        result = open_daily_track(driver_z,wait)
        check_scrapping(result, driver_z) # ? Check that last scrapping have no errors
        
        time.sleep(2)

        # ? Formatting array to pass in params to add_new_register
        for day in day_to_add:
            day = list(day.values())
            day = day[1:-1] # ? Removing the first and the last item from list (data that not useful to copy and add register)
            day.pop(1) # ? Removing element with index 1 (data that not useful to copy and add register)
            result = add_new_register(driver_z, wait, day)
            check_scrapping(result, driver_z) # ? Check that last scrapping have no errors

        driver_z.quit() # ? Quit chrome
        
        # ? Show menu again
        show_menu()
        op_menu = select_menu([0,1,2,3,4,5])
        do_action_menu(op_menu)

    elif op == 5: # ? Update config object options
        update_config()
        
    elif op == 0: # ? Exit script
        print("\n¡Hasta mañana! "+primary_color+";)"+light_color)
        sys.exit(0)

def check_settings(): # ? Check if settings in config object have errors
    print("\nCargando opciones...",end="")
    try:
        # ? Check if file exists and exists data in it
        with open('data.pkl', 'rb') as filename:
            data = pickle.load(filename)
            
            config.set_email(data.EMAIL)
            config.set_passw(data.PASSW)
            config.SAVE_COOKIES = data.SAVE_COOKIES
            config.set_time_entry_morning(data.TIME_ENTRY_MORNING)
            config.set_time_departure_morning(data.TIME_DEPARTURE_MORNING)
            config.set_time_entry_afternoon(data.TIME_ENTRY_AFTERNOON)
            config.set_time_departure_afternoon(data.TIME_DEPARTURE_AFTERNOON)
            config.set_time_entry_break(data.TIME_ENTRY_BREAK)
            config.set_time_departure_break(data.TIME_DEPARTURE_BREAK)
            
            print(success_color+"OK"+light_color)
    
    except FileNotFoundError:
        print(error_color+"NO"+light_color)
        
    # ? Getting values from file of config options
    EMAIL = config.get_email()
    PASSW = config.get_passw()
    SAVE_COOKIES = config.get_save_cookies()
    TIME_ENTRY_MORNING = config.get_time_entry_morning()
    TIME_DEPARTURE_MORNING = config.get_time_departure_morning()
    TIME_ENTRY_AFTERNOON = config.get_time_entry_afternoon()
    TIME_DEPARTURE_AFTERNOON = config.get_time_departure_afternoon()
    TIME_ENTRY_BREAK = config.get_time_entry_break()
    TIME_DEPARTURE_BREAK = config.get_time_departure_break()


    # ? Check the empty value options and asks the user for new values
    if EMAIL == "" or EMAIL == None:
        email_val = sanitize_text(array_allowed=[], label="\nIntroduce tu email de Zinkee")
        config.set_email(email_val)
    
    if PASSW == "" or PASSW == None:
        passw_val = sanitize_text(array_allowed=[], label="\nIntroduce tu contraseña de Zinkee", isPassword=True)
        config.set_passw(passw_val)
    
    if SAVE_COOKIES == -1 or SAVE_COOKIES == "" or SAVE_COOKIES == None:
        save_cookies_val = sanitize_text(array_allowed=['si', 'no'], label="\n¿Guardar cookies?")
        config.set_save_cookies(save_cookies_val)

    if TIME_ENTRY_MORNING == "" or TIME_ENTRY_MORNING == None:
        time_entry_morning_val = sanitize_text(array_allowed=[], label="\nHora de entrada por la mañana (Formato: 00:00)", isTime=True)
        config.set_time_entry_morning(time_entry_morning_val)
    
    if TIME_DEPARTURE_MORNING == "" or TIME_DEPARTURE_MORNING == None:
        time_departure_morning_val = sanitize_text(array_allowed=[], label="\nHora de salida por la mañana (Formato: 00:00)", isTime=True)
        config.set_time_departure_morning(time_departure_morning_val)
    
    if TIME_ENTRY_AFTERNOON == "" or TIME_ENTRY_AFTERNOON == None:
        time_entry_afternoon_val = sanitize_text(array_allowed=[], label="\nHora de entrada por la tarde (Formato: 00:00)", isTime=True)
        config.set_time_entry_afternoon(time_entry_afternoon_val)
    
    if TIME_DEPARTURE_AFTERNOON == "" or TIME_DEPARTURE_AFTERNOON == None:
        time_departure_afternoon_val = sanitize_text(array_allowed=[], label="\nHora de salida por la tarde (Formato: 00:00)", isTime=True)
        config.set_time_departure_afternoon(time_departure_afternoon_val)
    
    if TIME_ENTRY_BREAK == "" or TIME_ENTRY_BREAK == None:
        time_entry_break_val = sanitize_text(array_allowed=[], label="\nHora de entrada al desayuno (Formato: 00:00)", isTime=True)
        config.set_time_entry_break(time_entry_break_val)
    
    if TIME_DEPARTURE_BREAK == "" or TIME_DEPARTURE_BREAK == None:
        time_departure_break_val = sanitize_text(array_allowed=[], label="\nHora de salida del desayuno (Formato: 00:00)", isTime=True)
        config.set_time_departure_break(time_departure_break_val)
    
    # ? Saving data of new values
    with open('data.pkl', 'wb') as filename:
        pickle.dump(config, filename, pickle.HIGHEST_PROTOCOL)

def update_config(): # ? Update config object and save
    op = -1
    
    while int(op) != 0:
        print(config) # ? Printing options config
        op = int(select_menu([0,1,2,3,4,5,6,7,8,9,10]))

        print() # Salto de línea

        # ? Setting new values for config options
        if (op == 1):
            email_val = sanitize_text(array_allowed=[], label="\nIntroduce tu email de Zinkee")
            config.set_email(email_val)
        if (op == 2):
            passw_val = sanitize_text(array_allowed=[], label="\nIntroduce tu contraseña de Zinkee", isPassword=True)
            config.set_passw(passw_val)
        if (op == 3):
            save_cookies_val = sanitize_text(array_allowed=['si', 'no'], label="\n¿Guardar cookies?")
            config.set_save_cookies(save_cookies_val)
        if (op == 4):
            timeout_val = sanitize_text(array_allowed=[], label="\nTiempo máximo de espera para cargar las webs (aumentar si tu conexión es lenta)", isNumber=True)
            config.set_max_timeout(timeout_val)
        if (op == 5):
            time_entry_morning_val = sanitize_text(array_allowed=[], label="\nHora de entrada por la mañana (Formato: 00:00)", isTime=True)
            config.set_time_entry_morning(time_entry_morning_val)
        if (op == 6):
            time_departure_morning_val = sanitize_text(array_allowed=[], label="\nHora de salida por la mañana (Formato: 00:00)", isTime=True)
            config.set_time_departure_morning(time_departure_morning_val)
        if (op == 7):
            time_entry_afternoon_val = sanitize_text(array_allowed=[], label="\nHora de entrada por la tarde (Formato: 00:00)", isTime=True)
            config.set_time_entry_afternoon(time_entry_afternoon_val)
        if (op == 8):
            time_departure_afternoon_val = sanitize_text(array_allowed=[], label="\nHora de salida por la tarde (Formato: 00:00)", isTime=True)
            config.set_time_departure_afternoon(time_departure_afternoon_val)
        if (op == 9):
            time_entry_break_val = sanitize_text(array_allowed=[], label="\nHora de entrada por al desayuno (Formato: 00:00)", isTime=True)
            config.set_time_entry_break(time_entry_break_val)
        if (op == 10):
            time_departure_break_val = sanitize_text(array_allowed=[], label="\nHora de salida del desayuno (Formato: 00:00)", isTime=True)
            config.set_time_departure_break(time_departure_break_val)
        
    else:
        print("Guardando opciones...", end="")

        # ? Saving new config options
        with open('data.pkl', 'wb') as filename:
            pickle.dump(config, filename, pickle.HIGHEST_PROTOCOL)
            print(success_color+"OK"+light_color)

        # ? Show menu again
        show_menu()
        op_menu = select_menu([0,1,2,3,4,5])
        do_action_menu(op_menu)

# * ----------- *


# * MAIN EXECUTION *
# ****************** 
if __name__ == '__main__': # ! This script only execute if it is called from CMD directly (and not called of other script)
    # ? Color vars for cmd
    light_color = fg('white')
    primary_color = fg('light_green')
    error_color = fg('red')
    info_color = fg('light_blue')
    success_color = fg('green')

    # ? Config object
    config = Config()

    check_settings() # ? Check setting of config before script starts
    show_menu() # ? Show options menu
    op_menu = select_menu([0,1,2,3,4,5]) # ? Select option from menu
    do_action_menu(op_menu) # ? Execute option selected from menu

# * ----------- *
