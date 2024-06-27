import pygame
import random
import os
from tkinter import simpledialog

pygame.init()

relogio = pygame.time.Clock()
icone  = pygame.image.load("recursos/icone.png")
bruxa = pygame.image.load("recursos/bruxa.png")
fundo = pygame.image.load("recursos/fundolua.png")
fundoStart = pygame.image.load("recursos/fundoinicio.png")
fundoDead = pygame.image.load("recursos/fundofogo.png")
corvo = pygame.image.load("recursos/corvo.png")

forca = pygame.image.load("recursos/forca.png")
tocha = pygame.image.load("recursos/tocha.png")
tamanho = (800,600)
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Iron Man do Marcão")
pygame.display.set_icon(icone)
arremessosSound = pygame.mixer.Sound("recursos/arremessos.wav")
morteSound = pygame.mixer.Sound("recursos/som_morte.wav")
fonte = pygame.font.SysFont("arial",28)
fonteStart = pygame.font.SysFont("arial",55)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("recursos/som_jogo.wav")

branco = (255,255,255)
preto = (0, 0 ,0 )


def jogar(nome):
    pygame.mixer.Sound.play(arremessosSound)
    pygame.mixer.music.play(-1)
    posicaoXPersona = 400
    posicaoYPersona = 670
    corvo = 50
    corvo = 50
    escalacorvo = 1
    velocidadecorvo = 0.007
    crescendocorvo = True
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXforca = 400
    posicaoYforca = -240
    posicaoXtocha = 100
    posicaoYtocha = -350
    velocidadeforca = 1
    velocidadetocha = 1
    pontos = 0
    larguraPersona = 170
    alturaPersona = 170
    larguaforca  = 100
    alturaforca  = 100
    larguatocha  = 100
    alturatocha  = 100
    dificuldade  = 20

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0

        if crescendocorvo:
            escalacorvo += velocidadecorvo
            if escalacorvo >= 1.5:
                crescendocorvo = False
        
        else:
            escalacorvo -= velocidadecorvo
            if escalacorvo <= 1:
                crescendocorvo = True
        
        posicaoXPersona = posicaoXPersona + movimentoXPersona            
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        
        if posicaoXPersona < 0 :
            posicaoXPersona = 10
        elif posicaoXPersona >550:
            posicaoXPersona = 540
            
        if posicaoYPersona < 0 :
            posicaoYPersona = 10
        elif posicaoYPersona > 473:
            posicaoYPersona = 463
        
            
        tela.fill(branco)
        tela.blit(fundo, (0,0) )
        #pygame.draw.circle(tela, preto, (posicaoXPersona,posicaoYPersona), 40, 0 )
        tela.blit( bruxa, (posicaoXPersona, posicaoYPersona) )
        corvoX = int(corvo.get_width() * escalacorvo)
        corvoY = int(corvo.get_height() * escalacorvo)
        corvoredimencionado = pygame.transform.scale(corvo, (corvoX,corvoY))
        tela.blit(corvoredimencionado, (corvoX, corvoY))
        
        posicaoYforca = posicaoYforca + velocidadeforca
        if posicaoYforca > 600:
            posicaoYforca = -240
            pontos = pontos + 1
            velocidadeforca = velocidadeforca + 1
            posicaoXforca = random.randint(0,800)
            pygame.mixer.Sound.play(arremessosSound)

        posicaoYtocha = posicaoYtocha + velocidadetocha
        if posicaoYtocha > 600:
            posicaoYtocha = -240
            pontos = pontos + 1
            velocidadetocha = velocidadetocha + 1
            posicaoXtocha = random.randint(0,800)
            pygame.mixer.Sound.play(arremessosSound)    
            
            
        tela.blit( forca, (posicaoXforca, posicaoYforca) )
        tela.blit( tocha, (posicaoXtocha, posicaoYtocha) )
        
        texto = fonte.render(nome+"- Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (10,10))
        
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+alturaPersona))
        pixelsforcaX = list(range(posicaoXforca, posicaoXforca + larguaforca))
        pixelsforcaY = list(range(posicaoYforca, posicaoYforca + alturaforca))
        pixelstochaX = list(range(posicaoXtocha, posicaoXtocha + larguatocha))
        pixelstochaY = list(range(posicaoYtocha, posicaoYtocha + alturatocha))
        
        #print( len( list( set(pixelsforcaX).intersection(set(pixelsPersonaX))   ) )   )
        if  len( list( set(pixelsforcaY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsforcaX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                dead(nome, pontos)

        if  len( list( set(pixelstochaY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelstochaX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                dead(nome, pontos)
        
    
        
        pygame.display.update()
        relogio.tick(60)


def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(morteSound)
    
    jogadas  = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt","w",encoding="utf-8")
        arquivo.close()
 
    jogadas[nome] = pontos   
    arquivo = open("historico.txt","w",encoding="utf-8") 
    arquivo.write(str(jogadas))
    arquivo.close()
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogar(nome)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("RESTART", True, branco)
        tela.blit(textoStart, (400,482))
        textoEnter = fonte.render("Press enter to continue...", True, branco)
        tela.blit(textoEnter, (60,482))
        pygame.display.update()
        relogio.tick(60)


def ranking():
    estrelas = {}
    try:
        arquivo = open("historico.txt","r",encoding="utf-8" )
        estrelas = eval(arquivo.read())
        arquivo.close()
    except:
        pass
    
    nomes = sorted(estrelas, key=estrelas.get,reverse=True)
    print(estrelas)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    start()

        tela.fill(preto)
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        textoStart = fonteStart.render("BACK TO START", True, branco)
        tela.blit(textoStart, (330,482))
        
        
        posicaoY = 50
        for key,nome in enumerate(nomes):
            if key == 13:
                break
            textoJogador = fonte.render(nome + " - "+str(estrelas[nome]), True, branco)
            tela.blit(textoJogador, (300,posicaoY))
            posicaoY = posicaoY + 30

            
        
        pygame.display.update()
        relogio.tick(60)


def start():
    nome = simpledialog.askstring("Iron Man","Nome Completo:")
    
    
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
                elif buttonRanking.collidepoint(evento.pos):
                    ranking()

        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        buttonStart = pygame.draw.rect(tela, preto, (35,482,750,100),0)
        buttonRanking = pygame.draw.rect(tela, preto, (35,50,200,50),0,30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (90,50))
        textoStart = fonteStart.render("START", True, branco)
        tela.blit(textoStart, (330,482))

        
        
        pygame.display.update()
        relogio.tick(60)

start()