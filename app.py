import os
from dotenv import load_dotenv
import requests
import smtplib
import schedule
import time
from colorama import init, Fore, Back, Style

# Inicializa o Colorama
init(autoreset=True)

# Carrega as variáveis de ambiente
load_dotenv()

# Pega os dados de e-mail do arquivo .env
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")

# Logo desenvolvida com IA
def show_logo():
    logo = """
    ██████╗ ██╗ ██████╗  ██████╗ ████████╗██╗ ██████╗ ███╗   ██╗
    ██╔══██╗██║██╔═══██╗██╔═══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
    ██████╔╝██║██║   ██║██║   ██║   ██║   ██║██║   ██║██╔██╗ ██║
    ██╔═══╝ ██║██║   ██║██║   ██║   ██║   ██║██║   ██║██║╚██╗██║
    ██║     ██║╚██████╔╝╚██████╔╝   ██║   ██║╚██████╔╝██║ ╚████║
    ╚═╝     ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
                                                                
                 Monitoramento de Preço do Bitcoin
    """
    print(Fore.YELLOW + logo)

# Função para obter o preço do Bitcoin da API CoinGecko
def get_bitcoin_price():
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': 'bitcoin',
        'vs_currencies': 'brl'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Verifica se houve algum erro HTTP
        data = response.json()
        return data['bitcoin']['brl']
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Erro ao consultar API CoinGecko: {e}")
        return None

# Função para enviar e-mail
def send_email(price, user_email):
    subject = "Alerta: Preço do Bitcoin Abaixo do Esperado"
    body = f"O preço atual do Bitcoin é R${price:.2f}, abaixo do seu limite."
    
    # Configurar o e-mail com codificação UTF-8
    message = f"Subject: {subject}\n"
    message += "MIME-Version: 1.0\n"
    message += "Content-Type: text/plain; charset=utf-8\n"
    message += "Content-Transfer-Encoding: 8bit\n\n"
    message += body

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, user_email, message.encode('utf-8'))
            print(Fore.GREEN + f"E-mail enviado para {user_email}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# Função para verificar o preço e enviar alerta se necessário
def check_price(user_limit, user_email):
    price = get_bitcoin_price()
    if price is not None:
        # Exibir o preço atual no terminal
        print(f"O preço atual do Bitcoin é: R${price:.2f}")
        
        # Verificar se o preço está abaixo do limite
        if price < user_limit:
            print(f"Preço abaixo do limite de R${user_limit:.2f}. Enviando e-mail...")
            send_email(price, user_email)
        else:
            print("Preço ainda acima do limite.")
    else:
        print("Não foi possível obter o preço do Bitcoin.")

# Função para exibir o contador de tempo
def countdown_timer(duration):
    while duration:
        mins, secs = divmod(duration, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(f"\rPróxima consulta em: {timer}", end="")
        time.sleep(1)
        duration -= 1
    print("\rRealizando nova consulta...               ")  # Limpa a linha anterior

# Função principal
def main():
    show_logo()
    # Exibir o preço atual do Bitcoin ao iniciar
    print("Consultando o preço inicial do Bitcoin...")
    print("\n")
    price = get_bitcoin_price()
    if price is not None:
        print(f"O preço atual do Bitcoin é: R${price:.2f}")
    else:
        print("Não foi possível obter o preço inicial do Bitcoin.")
    print("\n")
    # Obter os dados do usuário
    user_limit = float(input("Informe o valor limite em R$ para o Bitcoin: "))
    print("\n")
    user_email = input("Informe o e-mail para receber as notificações: ")
    print("\n")
    # Agendar a verificação do preço a cada 10 minutos (600 segundos)
    schedule.every(10).minutes.do(check_price, user_limit=user_limit, user_email=user_email)
    
    print("Monitorando o preço do Bitcoin a cada 10 minutos...")
    print("\n")

    # Loop para manter o programa rodando
    while True:
        # Rodar tarefas agendadas
        schedule.run_pending()

        # Iniciar o contador de tempo de 10 minutos (600 segundos)
        countdown_timer(600)

if __name__ == "__main__":
    main()
