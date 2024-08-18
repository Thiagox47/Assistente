import speech_recognition as sr
import pyttsx3
from datetime import datetime
import json

# Inicializa o mecanismo de síntese de voz
maquina = pyttsx3.init()

# Carrega os comandos do arquivo JSON
try:
    with open('comandos.json', 'rb') as file:
        comandos = json.load(file)
    print("Comandos carregados com sucesso.")
except FileNotFoundError:
    print("Arquivo comandos.json não encontrado.")
    comandos = {}

def tratar_audio(comando):
    global acabou
    try:
        comando = comando.lower().strip()
        print(f"Comando recebido: {comando}")
        
        if "encerrar gravação" in comando:
            acabou = True
            maquina.say("Encerrando gravação")
            maquina.runAndWait()
            return
        
        elif 'josefa' in comando:
            comando = comando.replace('josefa', '').strip()
            print(f"Processando comando: {comando}")

            # Busca o comando no JSON
            resposta = comandos.get(comando, None)
            print(f"Resposta encontrada: {resposta}")

            if resposta:
                # Substitui placeholders por valores reais
                if '{hora}' in resposta:
                    hora = datetime.now().strftime('%H:%M')
                    resposta = resposta.replace('{hora}', hora)
                
                if '{data}' in resposta:
                    data = datetime.now().strftime('%d de %B de %Y')
                    resposta = resposta.replace('{data}', data)
                
                print(f"Resposta final: {resposta}")
                maquina.say(resposta)
            else:
                maquina.say('Não entendi o comando')

            maquina.runAndWait()

    except sr.UnknownValueError:
        print('Não entendi o que foi dito!')
    except sr.RequestError as e:
        print(f"Erro ao solicitar resultados do serviço de reconhecimento; {e}")

acabou = False
rec = sr.Recognizer()

with sr.Microphone(device_index=1) as microfone:
    rec.adjust_for_ambient_noise(microfone)
    rec.pause_threshold = 0.8
    print("Pronto para escutar...")

    while not acabou:
        try:
            print("Escutando...")
            audio = rec.listen(microfone)
            comando = rec.recognize_google(audio, language='pt-BR')
            print(f"Áudio reconhecido: {comando}")
            tratar_audio(comando)
        except sr.UnknownValueError:
            print('Não entendi o que foi dito!')
        except sr.RequestError as e:
            print(f"Erro ao solicitar resultados do serviço de reconhecimento; {e}")

print("Encerrando gravação.")
