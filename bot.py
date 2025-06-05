import telebot as tb
import requests, json
from app import recuperar_detalhe_coletivo, Book, del_book
chave = "8119155152:AAGrH0QBrW0WwrM99oN0BaGFY-ckztucqec"

bot = tb.TeleBot(chave)


#╔═══════════════════════════════════════════════╗
#║         ROTA PARA VER OS LIVROS SALVOS        ║
#╚═══════════════════════════════════════════════╝
@bot.message_handler(commands=["livros"])
def buscar_livro(mensagem):
    url = "http://127.0.0.1:5000/api/book"
    livros = requests.get(url)                                        
    livros = livros.json()

    for book in livros:
        titulo = book["titulo"]
        autor = book["autor"]
        bot.send_message(mensagem.chat.id, f"{titulo} --- {autor}")


#╔══════════════════════════════════════════╗
#║         ROTA PARA ADICIONAR LIVRO        ║
#╚══════════════════════════════════════════╝
@bot.message_handler(commands=["add"])
def add_livro(mensagem):
    global titulo_add
    titulo_add = mensagem.text.strip("/add")
    bot.send_message(mensagem.chat.id, "Agora digite o nome do autor(a)")
    bot.send_message(mensagem.chat.id, "/autor")

@bot.message_handler(commands=["autor"])
def add_livro(mensagem):
    global autor_add
    autor_add = mensagem.text.strip("/autor")
    bot.send_message(mensagem.chat.id, "Agora digite o status do livro")
    bot.send_message(mensagem.chat.id, "/status")

@bot.message_handler(commands=["status"])
def add_livro(mensagem):
    global status_add
    url= "http://127.0.0.1:5000/api/book/add"

    status_add = mensagem.text.strip("/status").lstrip()
    
    book = {
        "titulo" : titulo_add,
        "autor" : autor_add,
        "status" : status_add
    }
    requests.post(url, json=book)
    
    bot.send_message(mensagem.chat.id, "Livro adicionado com sucesso!")


#╔══════════════════════════════════════════╗
#║         ROTA PARA DELETAR LIVROS         ║
#╚══════════════════════════════════════════╝
@bot.message_handler(commands=["del"])
def deletar_book(mensagem):
    codigo = (mensagem.text.strip("/del")).split()
    id = codigo[0]
    
    url= f"http://127.0.0.1:5000/api/book/delete/{id}"
    requests.delete(url)
    
    bot.send_message(mensagem.chat.id, "Livro apagado com sucesso!")


#╔══════════════════════════════╗
#║         ROTA INICIAL         ║
#╚══════════════════════════════╝
@bot.message_handler(commands=["start"])
def responder_start(mensagem):                                             
    bot.send_message(mensagem.chat.id, "Ola, seja bem vindo ao chat do Andre Bezer")                                                      
    bot.send_message(mensagem.chat.id, "comandos disponiveis:")
    bot.send_message(mensagem.chat.id,
        """
        /livros
        """)
bot.polling()