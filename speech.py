import time

import speech_recognition as sr
from pygame import mixer
import pandas as pd
import random

def poe_musica():
    df = pd.read_csv('tabela.csv')
    index_musica = random.randint(0, len(df.index)-1)
    nome = df.iloc[index_musica,0]
    artista = df.iloc[index_musica,1]
    genero = df.iloc[index_musica,2]
    titulo = df.iloc[index_musica,3]
    duracao = df.iloc[index_musica,4]
    lingua = df.iloc[index_musica,5]
    print('SOM NA CAIXA DO CALDEIRÃO')
    mixer.init()
    mixer.music.load('musicas_dingdong/'+nome+'.mp3')
    mixer.music.play(start=random.randint(0,int(duracao)-10))
    time.sleep(5)
    mixer.music.stop()

    ouvir_microfone(artista,titulo)
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
            print("Você disse: " + frase)
            if(frase == artista):
                print('Correto !!')
                mixer.init()
                mixer.music.load('react/react.mp3')
                mixer.music.play(start=0)
                time.sleep(1)
                mixer.music.stop()
            else:
                print('Errado !!')
                mixer.music.load('react/react.mp3')
                mixer.music.play(start=2)
                time.sleep(1)
                mixer.music.stop()
                print("A musica é do " + artista)
            # Caso nao tenha reconhecido o padrao de fala, exibe esta mensagem
        except sr.UnkownValueError:
            print("Não entendi")
        return frase
