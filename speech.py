import time

import speech_recognition as sr
from pygame import mixer
import pandas as pd
import random


df = pd.read_csv('tabela.csv')

def pergunta_musica():
    index_musica = random.randint(0, len(df.index)-1)
    nome = df.iloc[index_musica,0]
    artista = df.iloc[index_musica,1]
    genero = df.iloc[index_musica,2]
    titulo = df.iloc[index_musica,3]
    duracao = df.iloc[index_musica,4]
    lingua = df.iloc[index_musica,5]

    toca_musica(nome, duracao)
    textoFalado = ouvir_microfone(artista,titulo)

    print("Você disse: " + textoFalado)
    if(textoFalado == artista):
        print('Correto !!')
        musica_correta()
        return True
    else:
        print('Errado !!')
        musica_errada()
        print("A musica é do " + artista)
        return False
    return False

def toca_musica(nome, duracao):
    print('SOM NA CAIXA DO CALDEIRÃO')
    mixer.init()
    mixer.music.load('musicas_dingdong/'+nome+'.mp3')
    mixer.music.play(start=random.randint(0,int(duracao)-10))
    time.sleep(5)
    mixer.music.stop()


# Funcao responsavel por ouvir e reconhecer a fala
def ouvir_microfone(artista,titulo):
    # Habilita o microfone para ouvir o usuario
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        # Chama a funcao de reducao de ruido disponivel na speech_recognition
        microfone.adjust_for_ambient_noise(source)
        # Avisa ao usuario que esta pronto para ouvir
        print("De quem é a musica ?")
        # Armazena a informacao de audio na variavel
        audio = microfone.listen(source)
        try:
            # Passa o audio para o reconhecedor de padroes do speech_recognition
            frase = microfone.recognize_google(audio, language='pt-BR')
            # Após alguns segundos, retorna a frase falada
        # Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
        except sr.UnkownValueError:
            print("Não entendi")
        return frase

def musica_correta():
    mixer.init()
    mixer.music.load('react/react.mp3')
    mixer.music.play(start=0)
    time.sleep(1)
    mixer.music.stop()

def musica_errada():
    mixer.music.load('react/react.mp3')
    mixer.music.play(start=2)
    time.sleep(1)
    mixer.music.stop()
