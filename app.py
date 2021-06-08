# ======================================================= #
# INÍCIO DA CLASSE BASE
# ======================================================= #
botao2 = "";
botao1 = "";
janelaAtual = '1jogador'
# gráficas 'tkinter'
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk  
import numpy as np
import speech
import pandas as pd
from math import *
import random
import time

class JanelaBase():
    'Classe geradora da janela gráfica'    

    # Importando um pacote interno do python
    import sys

    def __init__(
        self       : object,
        comprimento: [int,float] = 425,
        altura     : [int,float] = 445,
        titulo     : str         = 'DingDong',
        corFundo   : str         = 'light blue'
        ):

        #Dados necessarios
        self.df = pd.read_csv('tabela.csv')
        #Tornando variáveis 'visíveis' fora do método construtor
        #serão úteis para mudar certas características da janela
        #durante a mudança do frame normal para o frame científica
        #Os argumentos default serão adotados no frame científica
        #No frame normal faremos certas alterações
        self.numJogadores = 1
        self.comprimentoPadrao = comprimento
        self.alturaPadrao = altura
        self.titulo = titulo
        self.corFundo= corFundo
##===========================================================================================================


        'Construindo estrutura da janela base'
        # Instanciando uma janela do Tkinter
        self.janela = Tk()

        self.__create_circle(corFundo=corFundo)

       # Definindo as configurações da janela gráfica
        self.__configurarJanela(
            comprimento, altura, titulo, corFundo
        )

        # Criando os atributos necessários
        self.__criarAtributos()

        # Criando e posicionando os widgets na janela
        self.__criarWidgetsETextos()

        # Definindo ações de teclado
        self.__definirAcoesTeclado()

        return None

    def __create_circle(self: object, corFundo): #center coordinates, radius
        self.canvasJogador1 = Canvas(self.janela, width=50, height=50, background=corFundo, highlightthickness=0)
        self.canvasJogador2 = Canvas(self.janela, width=50, height=50, background=corFundo, highlightthickness=0)
        self.canvasJogador1.grid(row=4, column=0)
        self.canvasJogador2.grid(row=4, column=1)

        self.canvasJogador1.grid_remove()
        self.canvasJogador2.grid_remove()

        # specify bottom-left and top-right as a set of four numbers named # 'xy'
        xy = 20, 20, 50, 50         
    
        self.canvasJogador1.create_oval(xy, fill='red')
        self.canvasJogador2.create_oval(xy, fill='red')

    def __criarAtributos(
        self: object
        ):
        'Criando os atributos necessarios'
        
        self.pontos2Jogadores = [0,0]

        # no of musics played
        self.numPerguntas=0

        # keep a counter of correct answers
        self.correct=0

        # keep a counter of correct answers
        self.vidas=5
        
        return None


    # Método Privado
    def __configurarJanela(
        self       : object,
        comprimento: [int,float],
        altura     : [int,float],
        titulo     : str,
        corFundo   : str,
        ):
        'Configurando alguns parâmetros da janela'

        # Definindo a cor de fundo da janela gráfica
        self.janela.configure(background=corFundo)

        # Definindo o título da janela gráfica
        self.janela.title(titulo)

        # Definindo o tamanho da janela gráfica
        self.janela.geometry(f'{comprimento}x{altura}')

        return None    

    # Método Privado
    def __criarWidgetsETextos(
        self: object
        ):
        'Criando e posicionando os widgets na janela'
        # Criando caixa para digitação de textos na janela
        # gráfica e direcionando seu conteúdo ao atributo
        # 'equação'
        
        self.textoTipoJogo = Label(self.janela, 
            text = "",
            borderwidth=10,
            fg="navy blue",
            bg='light blue',
            justify="center",
            font="Helvetica 27 bold"
        )

        self.textoPrincipal = Label(self.janela, 
            text = "",
            borderwidth=10,
            fg="navy blue",
            bg='light blue',
            justify="center",
            font="Helvetica 27 bold"
        )

        self.textoCoracoes = Label(self.janela, 
            text = "",
            borderwidth=10,
            fg="navy blue",
            bg='light blue',
            justify="center",
            font="Helvetica 27 bold"
        )

        # Posicionando a caixa de texto considerando a
        # mescalgem de 5 colunas de espaço, tendo 70 px
        # de distância entre a borda desse espaço e a caixa
        self.textoTipoJogo.grid(
            row=0,
            columnspan=2,
            ipadx=0,
            ipady=0
        )

        self.textoPrincipal.grid(
            row=1,
            columnspan=2,
            ipadx=0,
            ipady=0
        )

        self.textoTipoJogo.configure(font="Helvetica 20")
        self.textoTipoJogo.configure(text="Modo " + str(self.numJogadores) + " jogador" + ("es" if (self.numJogadores==2) else ""))

        self.textoPrincipal.configure(font="Helvetica 27 bold")
        self.textoPrincipal.configure(text="Clique play (space)")

        self.textoCoracoes.grid(
            row=2,
            columnspan=2,
            ipadx=0,
            ipady=0
        )

        self.textoCoracoes.configure(font="Helvetica 27 bold")
        self.textoCoracoes.configure(text="❤ ❤ ❤ ❤ ❤")

        self.textoAcertouErrou = Label(self.janela, 
            text = "",
            borderwidth=10,
            fg="navy blue",
            bg='light blue',
            justify="center",
            font="Helvetica 27 bold"
        )

        # Posicionando a caixa de texto considerando a
        # mescalgem de 5 colunas de espaço, tendo 70 px
        # de distância entre a borda desse espaço e a caixa
        self.textoAcertouErrou.grid(
            row=3,
            columnspan=2,
            ipadx=0,
            ipady=0
        )

        self.textoAcertouErrou.configure(font="Helvetica 10 bold")
        self.textoAcertouErrou.configure(text="")       

        # Gerando uma barra de menu para janela
        self.barraMenu = Menu(
            self.janela
        )

        # Adicionando um botao de escolha chamado
        # 'Normal', usado para ativar o modo 'normal'
        # da calculadora
        self.barraMenu.add_radiobutton(
            label='1 jogador',
            indicator=True,
            command=lambda:self.__mudarJanela('1jogador')
        )

        self.barraMenu.add_radiobutton(
            label='2 jogadores',
            indicator=True,
            command=lambda:self.__mudarJanela('2jogadores')
        )


#=====================================================================================

        # Adicionando mais um separador à barra de menu
        #self.barraMenu.add_command(
        #    label="★",
        #    activebackground=self.barraMenu.cget(
        #        "background"
        #    )
        #)
#=====================================================================================
        # Adicionando um botao de escolha chamado
        # 'Cientifica', usado para ativar o modo
        # 'cientifica' da calculadora
        #self.barraMenu.add_radiobutton(
        #    label='𝓒𝓲𝓮𝓷𝓽𝓲𝓯𝓲𝓬𝓪',
        #    indicator=True,
        #    command=lambda:self.__mudarJanela('cientifica')
        #)
        self.janela.config( bg='light blue')
        #Ativando o modo 'normal' de início
        self.barraMenu.invoke(1)
        # O valor é 3, pois foi o quarto elemento
        # a ser inserido no menu.

        # Configurando/habilitando menu na janela
        self.janela.config(
            menu=self.barraMenu,
        )
        
        return None

    def __mudarJanela(
        self: object,
        tipo: str = '1jogador'
        ):
        'Mudando configuração da janela'

        # Verificando se tem algum frame aberto
        try:
            # Fechando o frame atual
            self.__frame.destroy()

        except: pass

        global janelaAtual;

        if(janelaAtual == '1jogador'):
            tipo = '2jogadores'
        else:
            tipo = '1jogador';
        # Atualizando frame
        if   (tipo == '1jogador'):
            janelaAtual = '1jogador';
            self.__frame = FramePlay(self).frame
##=================================================================================================================
            # Definindo as configurações da janela gráfica quando entrar no frame 'normal'
            self.__configurarJanela(
                337,
                325,
                self.titulo,
                self.corFundo
            )
            self.textoPrincipal.configure(font="Helvetica 22 bold")
            self.numJogadores = 1;
            self.__criarAtributos()
            self.textoPrincipal.configure(text="Clique play (space)")
            self.textoCoracoes.grid()
            self.textoCoracoes.configure(text="❤ ❤ ❤ ❤ ❤")
            self.textoAcertouErrou.configure(text="")
            self.textoTipoJogo.configure(text="Modo " + str(self.numJogadores) + " jogador" + ("es" if (self.numJogadores==2) else ""))
            self.canvasJogador1.grid_remove()
            self.canvasJogador2.grid_remove()
        else:
            janelaAtual = '2jogadores';
            self.__frame = FrameCientifica(self).frame
##=================================================================================================================
            # Definindo as configurações da janela gráfica quando entrar no frame 'normal'
            self.__configurarJanela(
                337,
                325,
                self.titulo,
                self.corFundo
            )
            self.textoPrincipal.configure(font="Helvetica 22 bold")
            self.numJogadores = 2;
            self.__criarAtributos()
            self.textoPrincipal.configure(text="Clique play (space)")
            self.textoCoracoes.grid_remove()
            self.textoAcertouErrou.configure(text="")
            self.textoTipoJogo.configure(text="Modo " + str(self.numJogadores) + " jogador" + ("es" if (self.numJogadores==2) else ""))
            self.canvasJogador1.grid()
            self.canvasJogador2.grid()
        # Posicioanando frame
        self.__frame.grid()        

        return None

    # Método Privado
    def __fecharJanela(
        self: object
        ):
        'Fechando janela'

        # Excutando fechamento
        self.janela.destroy()

        return None


##================================================================================================================================
    # Método Privado
    def __perguntarPraSair(
        self : object,
        event: 'Event' = None
        ):
        'Exibe uma janela perguntando se deseja fechar a janela'

        # Abrindo janela com o diálogo
        decisao = messagebox.askyesno(
            'Fechar',
            'Deseja realmente fechar?'
        )

        # Verificando decisão
        if decisao == True:
            # Fechando a janela
            self.__fecharJanela()

        else:
            # Faça nada
            pass

        return None



    def __definirAcoesTeclado(
        self: object
        ):
        'Definindo as ações de teclado'

        # Habilitando ESC para fechar a janela
        self.janela.bind('<Escape>', self._JanelaBase__perguntarPraSair)

        # Habilitando SPACE para rodar musica
        self.janela.bind('<space>', self._JanelaBase__ouvirMusicaEChecarResposta)

        # Habilitando SETA DIREITA para proxima musica
        self.janela.bind('<Right>', self._JanelaBase__nextButton)

        # Habilitando SETA DIREITA para proxima musica
        self.janela.bind('1', self._JanelaBase__jogadorSelecionado1)

        # Habilitando SETA DIREITA para proxima musica
        self.janela.bind('2', self._JanelaBase__jogadorSelecionado2)

        # Habilitando SETA DIREITA para proxima musica
        self.janela.bind('m', self._JanelaBase__mudarJanela)

        return None

    # Método Público
    def rodarJanela(
        self       : object
        ):
    
        'Executando janela'        

        # Rodando aplicação
        self.janela.mainloop()

        return None
    
    # Método Privado
    def __display_result(self):
        print(self.numPerguntas, self.correct)
        wrong_count = self.numPerguntas - self.correct
        correct = f"Correct: {self.correct}"
        wrong = f"Wrong: {wrong_count}"

        score = int(self.correct / self.numPerguntas * 100)
        result = f"Score: {score}%"

        messagebox.showinfo("Result", f"{result}\n{correct}\n{wrong}")

    # Método Privado
    def __defineAtributosPorIndiceAleatorio(self):
        index_musica = random.randint(0, len(self.df.index)-1)
        self.nome = self.df.iloc[index_musica,0]
        self.artista = self.df.iloc[index_musica,1]
        self.genero = self.df.iloc[index_musica,2]
        self.titulo = self.df.iloc[index_musica,3]
        self.duracao = self.df.iloc[index_musica,4]
        self.lingua = self.df.iloc[index_musica,5]

    # Método Privado
    def __checaResposta(
        self : object,
        respostaFalada,
        respostaCorreta,
        pontosGanhos
        ):
        acertou = False
        if(respostaFalada == respostaCorreta):
            speech.musica_correta()
            self.correct+=pontosGanhos
            self.textoAcertouErrou.configure(text=f"Correto!! a resposta é {respostaCorreta}")
            acertou = True
        else:
            speech.musica_errada()
            self.textoAcertouErrou.configure(text=f"Errado!! a resposta é {respostaCorreta}")
            self.vidas -= 1
            self.textoCoracoes.configure(text="❤ "*self.vidas)
            if(self.vidas == 0):
                self.textoPrincipal.configure(text = "Fim de Jogo")
                self.textoAcertouErrou.configure(text="Você atingiu "+ str(self.correct) + "pontos")
                #implementar fim de jogo
                while(True):
                    pass
            acertou = False
        
        return acertou

    def __respondeTitulo(
        self : object,
        botao2
        ):
        tituloFalado = speech.ouvir_microfone()
        self.__checaResposta(tituloFalado, self.titulo, 2)
        self.textoPrincipal.after(250, self.cliqueNext, botao2)
        return True

    def __respondeTitulo2Jogadores(
        self : object,
        botaonext,
        numJog,
        jogadorQueApertouOBotao
        ):
        tituloFalado = speech.ouvir_microfone()

        acertou = self.__checaResposta2jogadores(tituloFalado, self.titulo, numJog, jogadorQueApertouOBotao,'titulo')
        
        if(numJog!=jogadorQueApertouOBotao):
            self.textoPrincipal.after(250, self.cliqueNext2Jogadores, botaonext)
        elif(acertou):
            self.textoPrincipal.after(250, self.cliqueNext2Jogadores, botaonext)
        else:
            numJogNovo = 3 - numJog
            self.textoAcertouErrou.configure(text="Errou! Jogador "+str(numJogNovo)+" responda")
            self.textoPrincipal.after(250, self.__respondeTitulo2Jogadores, botaonext, numJogNovo, jogadorQueApertouOBotao)

        return True

    def cliqueNext(
        self : object,
        botaonext
        ):
        botaonext.grid()
        self.textoPrincipal.configure(text = str(self.correct) + " pontos acumulados")
    
    def cliqueNext2Jogadores(
        self : object,
        botaonext
        ):
        botaonext.grid()
        self.textoPrincipal.configure(text = " pontos: " + str(self.pontos2Jogadores[0]) + " / " + str(self.pontos2Jogadores[1]))
        # specify bottom-left and top-right as a set of four numbers named # 'xy'
        xy = 20, 20, 50, 50
        self.canvasJogador1.create_oval(xy, fill='red')
        self.canvasJogador2.create_oval(xy, fill='red')

    def __respondeAutor(
        self : object,
        botaonext,
        numJog: int = 1,
        ):
        autorFalado = speech.ouvir_microfone()

        self.__checaResposta(autorFalado, self.artista, 1)
        self.textoPrincipal.configure(text="Qual o título?")
        self.textoPrincipal.after(250, self.__respondeTitulo, botaonext)
        return True

    def __respondeAutor2Jogadores(
        self : object,
        botaonext,
        numJog: int,
        jogadorQueApertouOBotao: int
        ):
        autorFalado = speech.ouvir_microfone()
        
        acertou = self.__checaResposta2jogadores(autorFalado, self.artista, numJog, jogadorQueApertouOBotao, 'Autor')
        if(jogadorQueApertouOBotao != numJog):
            numJogNovo = 3-numJog
            self.textoPrincipal.configure(text="Qual o título?")
            self.textoPrincipal.after(250, self.__respondeTitulo2Jogadores, botaonext, numJogNovo, jogadorQueApertouOBotao)
        elif(acertou):
            self.textoPrincipal.configure(text="Qual o título?")
            self.textoPrincipal.after(250, self.__respondeTitulo2Jogadores, botaonext, numJog, jogadorQueApertouOBotao)
        else:
            numJogNovo = 3-numJog
            self.textoPrincipal.configure(text="Qual o intérprete?")
            self.textoAcertouErrou.configure(text="Errou! Jogador " + str(numJogNovo)+" responda")
            self.textoPrincipal.after(250, self.__respondeAutor2Jogadores, botaonext, numJogNovo, jogadorQueApertouOBotao)

        return True

    def __checaResposta2jogadores(
        self : object,
        respostaFalada,
        respostaCorreta,
        numJog: int,
        jogadorQueApertouOBotao,
        tipoPergunta = 'autor'
    ):
        if(tipoPergunta == 'autor'):
            pontosGanhos = 1
        elif(tipoPergunta == 'titulo'):
            pontosGanhos = 2

        acertou = False

        if(respostaFalada == respostaCorreta):
            speech.musica_correta()
            self.pontos2Jogadores[numJog-1] = self.pontos2Jogadores[numJog-1] + pontosGanhos
            if(tipoPergunta == 'Autor'):
                self.textoAcertouErrou.configure(text=f"Correto!! a resposta é {respostaCorreta},\n jogador {numJog} responda")
            elif(jogadorQueApertouOBotao==numJog):
                self.textoAcertouErrou.configure(text="Correto!! a resposta é "+str(respostaCorreta)+", \n jogador "+str(numJog)+" responda")
            else:
                self.textoAcertouErrou.configure(text="Correto!! a resposta é "+str(respostaCorreta))
            acertou = True
            if(self.pontos2Jogadores[numJog-1] >= 15):
                self.textoPrincipal.configure(text = "Fim de Jogo")
                self.textoAcertouErrou.configure(text=f"Jogador {numJog} atingiu "+ str(self.pontos2Jogadores[numJog-1]) + "pontos")
                #implementar fim de jogo
                while(True):
                    pass
                    
        else:
            speech.musica_errada()
            print(tipoPergunta)
            if(tipoPergunta == 'Autor'):
                self.textoAcertouErrou.configure(text=f"Errado!! a resposta é {respostaCorreta},\n jogador {3-numJog} responda")
            elif(jogadorQueApertouOBotao==numJog):
                self.textoAcertouErrou.configure(text=f"Errado!! a resposta é "+str(respostaCorreta)+", \n jogador "+str(numJog)+" responda")
            else:
                self.textoAcertouErrou.configure(text=f"Errado!! a resposta é "+str(respostaCorreta))
            acertou = False

        return acertou


    def responder(
        self : object,
        botaonext
    ):
        self.__defineAtributosPorIndiceAleatorio()

        speech.toca_musica(self.nome, self.duracao)
        self.numPerguntas += 2
        
        # Problema: Apenas mostra o texto depois que o reconhecimento da fala - (trava durante o assincronismo?).
        # self.display_text("De quem é a música?", 70, 180)
        self.textoPrincipal.configure(text="Qual o intérprete?")
        self.textoPrincipal.after(250, self.__respondeAutor, botaonext)

    def __contadorParaBotao(
        self : object,
        start_time
    ):
        max_time = 5
        if(self.selecionandoJogador):
            tempo_passado = int(time.time()-start_time)
            if(tempo_passado >= max_time):
                self.textoPrincipal.configure(text=f"Aperte o Botão!!!! 0s")
                numJogador = np.random.choice([1,2])
                if(numJogador == 1):
                    self.__jogadorSelecionado1()
                elif(numJogador == 2):
                    self.__jogadorSelecionado2()
            elif(tempo_passado >= 4):
                self.textoPrincipal.configure(text=f"Aperte o Botão!!!! 1s")
                self.textoPrincipal.after(250, self.__contadorParaBotao, start_time)
            elif(tempo_passado >= 3):
                self.textoPrincipal.configure(text=f"Aperte o Botão!!!! 2s")
                self.textoPrincipal.after(250, self.__contadorParaBotao, start_time)
            elif(tempo_passado >= 2):                
                self.textoPrincipal.configure(text=f"Aperte o Botão!!!! 3s")
                self.textoPrincipal.after(250, self.__contadorParaBotao, start_time)
            elif(tempo_passado >= 1):
                self.textoPrincipal.configure(text=f"Aperte o Botão!!!! 4s")
                self.textoPrincipal.after(250, self.__contadorParaBotao, start_time)
            elif(tempo_passado >= 0):
                self.textoPrincipal.configure(text=f"Aperte o Botão!!!! 5s")
                self.textoPrincipal.after(250, self.__contadorParaBotao, start_time)
            

    def __setSelecionandoJogador(
        self : object
    ):
        self.selecionandoJogador = 1
        print(self.selecionandoJogador)

    def tocaMusica2Jogadores(
        self : object
    ):
        self.__defineAtributosPorIndiceAleatorio()

        speech.toca_musica(self.nome, self.duracao)
        self.numPerguntas += 2
        
        # Problema: Apenas mostra o texto depois que o reconhecimento da fala - (trava durante o assincronismo?).
        # self.display_text("De quem é a música?", 70, 180)
        start_time = time.time()
    
        self.selecionandoJogador = 0
        self.textoPrincipal.after(250, self.__setSelecionandoJogador)
        self.textoPrincipal.after(500, self.__contadorParaBotao, start_time)

        #self.textoPrincipal.after(250, self.__respondeAutor, botao2)

    def __jogadorSelecionado1(
        self : object,
        event: 'Event' = None
    ):
        if(self.selecionandoJogador):
            self.selecionandoJogador=0
            xy = 20, 20, 50, 50
            self.canvasJogador1.create_oval(xy, fill='green')
            self.textoPrincipal.configure(text="Qual o intérprete?")
            self.textoAcertouErrou.configure(text="Jogador 1 responda")
            self.textoAcertouErrou.after(250, self.__respondeAutor2Jogadores, botao2, 1, 1)  
    
    def __jogadorSelecionado2(
        self : object,
        event: 'Event' = None
    ):
        if(self.selecionandoJogador):
            self.selecionandoJogador=0
            xy = 20, 20, 50, 50
            self.canvasJogador2.create_oval(xy, fill='green')
            self.textoAcertouErrou.configure(text="Jogador 2 responda")
            self.textoPrincipal.configure(text="Qual o intérprete?")
            self.textoPrincipal.after(250, self.__respondeAutor2Jogadores, botao2, 2, 2)  


    def __ouvirMusicaEChecarResposta(
        self : object,
        event: 'Event' = None
        ):
        self.textoPrincipal.configure(text="Tocando Musica...")
        botao1.grid_remove()
        if(self.numJogadores==1):
            botao1.after(250, self.responder, botao2)
        else:
            botao1.after(250, self.tocaMusica2Jogadores)

    def __nextButton(
        selfbase : object,
        self : object,
        event: 'Event' = None
        ):
        
        #if self.numPerguntas==self.data_size:
        #selfbase.__display_result()
        selfbase.textoPrincipal.configure(text="Clique play (space)")
        botao2.grid_remove()
        botao1.grid()
        selfbase.textoAcertouErrou.configure(text="")
##===================================================================================================================


class ToolTip():
    'Classe para texto explicativo'

    def __init__(self, widget):
        'Construtor'

        # Tornando, o respectivo widget, um atributo
        self.widget = widget

        # Predefinindo que caixa de dica nao existe        
        self.tipwindow = None

        # Numero de identificação da caixa de dica
        self.id = None

        # Predefinindo as posições da caixa de dica
        self.x = self.y = 0

        return None

    def exibirDica(self, text):
        "Display text in tooltip window"

        # Definindo texto como atributo
        self.text = text

        # Verificando se caixa de dica não existe
        # ou se a mensagem é vazia
        if self.tipwindow or not self.text:
            return None
        
        # Criando e obtendo a posicao da caixa
        # de dica
        x, y, cx, cy = self.widget.bbox("insert")

        # Ajustando posicao
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27

        # Habilitando a caixa de dica
        self.tipwindow = tw = Toplevel(self.widget)

        # Redimensionando
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))

        # Preenchendo com a mensagem
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))

        # Posicionando texto na caixa de dica
        label.pack(ipadx=1)

        return None

    def esconderDica(self):
        'Hide the tooltip'

        # Verificando se caixa de dica está ativa
        if self.tipwindow:
            # Redefinindo e fechando
            self.tipwindow, _ = None, self.tipwindow.destroy()

        return None
    













class FramePlay(JanelaBase):
    '''Classe referente às configuracoes de
       botoes do modo normal'''

    def __init__(
        self            : object,
        base            : 'Tk_object',
        corFundoBotao   : str         = 'navy blue',
        corTextoBotao   : str         = 'white',
        alturaBotao     : [int,float] = 2,
        comprimentoBotao: [int,float] = 8,
##========================================================================================================
        fonte           : str         = ("mathjax_ams","10","bold"),
        espessuraBorda  : int         = 7,
        relevo          : str         = 'groove'
##========================================================================================================        
        ):
        'Construindo a estrutura do frame'
        
        # Criando o atributo base
        self.base = base

        # Associando frame à base dada
        self.frame = Frame(
            base.janela,
            background='light blue',
            )

        # Configurando botoes
        self.__configurarBotao(
            corTextoBotao,  
            corFundoBotao,    
            alturaBotao,     
            comprimentoBotao,
            fonte,
            relevo,
            espessuraBorda,
        )

        # Criando os widgets
        self.__criarWidgets()

        # Habilitando acoes do teclado/mouse
        self.__definirAcoesBotoes()
        
        return None


    # Método Privado
    def __configurarBotao(
        self           : object,
        corTexto       : str,
        corFundo       : str,
        altura         : [int,float],
        comprimento    : [int,float],
        fonte          : str,
        relevo         : [int,float],
        espessuraBorda : [int,float]
        ):
        'Configurando alguns parâmetros dos botoes'

        # Criando atributos privados com os parametros
        self.corBotaoTexto    = corTexto
        self.corBotaoBg       = corFundo
        self.alturaBotao      = altura
        self.comprimentoBotao = comprimento
        self.fonte            = fonte
        self.relevo           = relevo
        self.espessuraBorda   = espessuraBorda

        return None

    def limparDica(
        self : object,
        event: 'Event_object'
        ):
        'Limpar caixa de dica'

        # Escondendo dica
        self.caixaDica.esconderDica()

        return None

    def mostrarDica(
        self    : object,
        elemento: [int,str],
        widget  : 'Widget_object'
        ):
        'Exibindo respectiva dica'

        # Estrutura com as dicas
        respectivaDica = {
            1  : 'Número 1',
            2  : 'Número 2'
##=====================================================================================================            
        }[elemento]


        # Criando uma caixa de dicas para o
        # respectivo widget
        self.caixaDica = ToolTip(widget)

        # Exibindo dica
        self.caixaDica.exibirDica(respectivaDica)

        return None

    def __definirAcoesBotoes(
        self: object
        ):
        'Definindo as ações de teclado/mouse'

        # Habilitando a dica referente ao botao        
        self.botao1.bind       ("<Enter>",lambda event: self.mostrarDica(1,self.botao1))
        self.botao2.bind       ("<Enter>",lambda event: self.mostrarDica(2,self.botao2))

        
##============================================================================================================================
        # Desabilitando dz
        self.botao1.bind       ("<Leave>",self.limparDica)
        self.botao2.bind       ("<Leave>",self.limparDica)

##================================================================================================================================
        return None


    def __criarWidgets(self):
        'Criando os widgets deste frame'
        
        # Criando um botão funcional com o texto '1'
        self.botao1 = Button(
            self.frame,                    # Onde será colocado o botão
            text='Play',                     # Texto a ser exibido no botão
            fg=self.corBotaoTexto,         # Cor do texto
            bg=self.corBotaoBg,            # Cor de fundo do botão
            height=self.alturaBotao,       # Altura do botão
            width=self.comprimentoBotao,   # Comprimento do botão
##=====================================================================================================
            relief=self.relevo,            # Estilo de relevo
            font=self.fonte,               # Fonte do texto
            bd=self.espessuraBorda,        # Espessura da boda
            command=lambda:JanelaBase._JanelaBase__ouvirMusicaEChecarResposta(
                self.base
                )                          # Função a ser executada ao clicar no botão
##======================================================================================================          
        )        

        # Criando um botão funcional com o texto '2'
        self.botao2 = Button(
            self.frame,
            text='>',
            font=self.fonte,
            fg=self.corBotaoTexto,
            bg=self.corBotaoBg,
            height=self.alturaBotao,
            width=self.comprimentoBotao,
            relief=self.relevo,
            bd=self.espessuraBorda,
            command=lambda:JanelaBase._JanelaBase__nextButton(self.base, self)
        )
        global botao1
        global botao2
        botao2 = self.botao2
        botao1 = self.botao1
##===========================================================================================================================

        # Posicionando os botões considerando um grid
        # com 6 linhas e 4 colunas
        self.botao1           .grid(row=5, column=1, pady=20)
        self.botao2           .grid(row=5, column=1, pady=20)
        self.botao2           .grid_remove()
        
##=====================================================================================================================================
        return None
























































































class FrameCientifica(FramePlay):
    '''Classe referente às configuracoes de
       botoes do modo normal'''

    def __init__(self, base):
        'Construindo a estrutura do frame'
        
        # Agregando os metodos e atributos
        # da classe "FramePlay"
        FramePlay.__init__(self, base)

        # Criando os widgets
        self.__criarWidgets()

        # Habilitando acoes do teclado/mouse
        self.__definirAcoesBotoes()
        
        return None


    # Método Privado
    def __configurarBotao(
        self           : object,
        corTexto       : str,
        corFundo       : str,
        altura         : [int,float],
        comprimento    : [int,float],
        fonte          : str,
        relevo         : [int,float],
        espessuraBorda : [int,float]
        ):
        'Configurando alguns parâmetros dos botoes'

        # Criando atributos privados com os parametros
        self.corBotaoTexto    = corTexto
        self.corBotaoBg       = corFundo
        self.alturaBotao      = altura
        self.comprimentoBotao = comprimento
        self.fonte            = fonte
        self.relevo           = relevo
        self.espessuraBorda   = espessuraBorda

        return None

    def limparDica(
        self : object,
        event: 'Event_object'
        ):
        'Limpar caixa de dica'

        # Escondendo dica
        self.caixaDica.esconderDica()

        return None

    def mostrarDica(
        self    : object,
        elemento: [int,str],
        widget  : 'Widget_object'
        ):
        'Exibindo respectiva dica'

        # Estrutura com as dicas
        respectivaDica = {
            1  : 'Número 1',
            2  : 'Número 2'
##=====================================================================================================            
        }[elemento]


        # Criando uma caixa de dicas para o
        # respectivo widget
        self.caixaDica = ToolTip(widget)

        # Exibindo dica
        self.caixaDica.exibirDica(respectivaDica)

        return None

    def __definirAcoesBotoes(
        self: object
        ):
        'Definindo as ações de teclado/mouse'

        # Habilitando a dica referente ao botao        
        self.botao1.bind       ("<Enter>",lambda event: self.mostrarDica(1,self.botao1))
        self.botao2.bind       ("<Enter>",lambda event: self.mostrarDica(2,self.botao2))

        
##============================================================================================================================
        # Desabilitando dz
        self.botao1.bind       ("<Leave>",self.limparDica)
        self.botao2.bind       ("<Leave>",self.limparDica)

##================================================================================================================================
        return None


    def __criarWidgets(self):
        'Criando os widgets deste frame'
        
"""         # Criando um botão funcional com o texto '1'
        self.botao1 = Button(
            self.frame,                    # Onde será colocado o botão
            text='Play',                     # Texto a ser exibido no botão
            fg=self.corBotaoTexto,         # Cor do texto
            bg=self.corBotaoBg,            # Cor de fundo do botão
            height=self.alturaBotao,       # Altura do botão
            width=self.comprimentoBotao,   # Comprimento do botão
##=====================================================================================================
            relief=self.relevo,            # Estilo de relevo
            font=self.fonte,               # Fonte do texto
            bd=self.espessuraBorda,        # Espessura da boda
            command=lambda:JanelaBase._JanelaBase__ouvirMusicaEChecarResposta(
                self.base, self.botao1, self.botao2
                )                          # Função a ser executada ao clicar no botão
##======================================================================================================          
        )        

        # Criando um botão funcional com o texto '2'
        self.botao2 = Button(
            self.frame,
            text='>',
            font=self.fonte,
            fg=self.corBotaoTexto,
            bg=self.corBotaoBg,
            height=self.alturaBotao,
            width=self.comprimentoBotao,
            relief=self.relevo,
            bd=self.espessuraBorda,
            command=lambda:JanelaBase._JanelaBase__nextButton(self.base, self)
        )
        
        botao2 = self.botao2
        botao1 = self.botao1

##===========================================================================================================================

        # Posicionando os botões considerando um grid
        # com 6 linhas e 4 colunas
        self.botao1           .grid(row=4, columnspan=2)
        self.botao2           .grid(row=4, columnspan=2)
        self.botao2           .grid_remove() """
        
##=====================================================================================================================================
        #return None
       



# ======================================================= #
# FIM DA CLASSE BASE
# ======================================================= #


# Como executar a janela
if __name__ == "__main__":
##======================================================================================================

    # Informando início do programa
    print('\nPrograma iniciado\n')

    # Importando módulos internos
    import subprocess  # Para instalar pacotes externos
    import platform    # Para descobrir o sistema operacional

#========================================================================================================
    # Executando janela
    JanelaBase().rodarJanela()
    
#========================================================================================================
   
    # Informando fim do programa
    print('\n\nPrograma encerrado\n')
