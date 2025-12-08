import string
import tkinter as tk #importando a tela
from tkinter import messagebox, LabelFrame, PhotoImage,ttk#são as funções que estou puxando da biblioteca do tkinter
from PIL import Image, ImageTk
import mysql.connector
"""
Login: usuario senha: 1234
quando for usar comandos de insert,update e delet
query = "insert into log (nome,senha)values(%s,%s)"
cursor.execute(query,(nome.get(),senha.get()))
conexao.commit()

query = "update log set nome=%s,senha=%s where id = 43"
cursor.execute(query,(nome.get(),senha.get())
conexao.commit()

cursor.execute("delete from log where id=15")    
conexao.commit()
"""
conexao = mysql.connector.connect(host='localhost',database='login',user='root',password='')#conector do python com o mysql


cursor = conexao.cursor()#o objeto que usamos para mexer no mysql pelo pyhon

janela = tk.Tk() #definindo o nome da tela


janela.title("Login Parcates")#nome da janela
janela.resizable(0,0)#desabilita a função de maximizar a tela de login
janela.geometry("450x300") #definido o tamanho da tela 
janela.config(bg="#E9E3D7")

tk.Label(janela, text="Usuário", bg="#E9E3D7").place(x=20,y=20) #Onde ira aparecer uma mensagem
nome = tk.Entry(janela)
nome.place(height=20,width=150,x=70,y=20)# campo de texto onde iremos digitar o nome

tk.Label(janela, text="Senha", bg="#E9E3D7").place(x=25,y=70)#Onde ira aparecer uma mensagem
senha = tk.Entry(janela, show="*")# campo de texto onde iremos digitar a senha
senha.place(height=20,width=150,y=70,x=65)
img = Image.open("Logo_Restaurante.png")
aspect_ratio = img.height / img.width
new_width = 200
new_height = int(new_width * aspect_ratio)
img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
img = ImageTk.PhotoImage(img)
lb = tk.Label(janela, image=img, command=None)
lb.place(height=180, width=200, x=220, y=20)
    
def cardapio():#tabela do cliente
    janela.destroy()
    jlistaa = tk.Tk()
    jlistaa.title("Lista")
    jlistaa.geometry("400x300")
    jlistaa.config(bg="#E9E3D7")
    cursor.execute('select nome, preco from cardapio')
    card = cursor.fetchall()
    select = ttk.Treeview(jlistaa, columns=("Nome", "Preco"), show="headings")
    select.column("Nome", width=200, minwidth=50)
    select.column("Preco", width=200, minwidth=50)
    select.heading("Nome",text="Nome:")
    select.heading("Preco",text="Preço:")
    select.pack()
    for (n, p) in card:
        select.insert("", "end", values=(n, p))
    

def delete(nome2):
    try:
        cursor.execute("delete from cardapio where nome = '"+nome2.get()+"'")
        conexao.commit()
    except:
        print('erro ao apagar produto')
    else:
        print('produto apagado com sucesso')
def insert(nome2, preco):
    try:
        cursor.execute("insert into cardapio (nome, preco) values ('"+nome2.get()+"', "+preco.get()+")")
        conexao.commit()
    except:
        print('Erro ao cadastrar produto')
    else:
        print('Produto cadastrado com sucesso')
def select():
    jLista = tk.Toplevel()#uma segunda tela
    jLista.title("Cardapio Parcates")#nome da tela
    jLista.geometry("400x250")#tamanho
    jLista.config(bg="#E9E3D7")
    cursor.execute("select id,nome,preco from cardapio")#Cogido do sql 
    card = cursor.fetchall()#puxando dos os dados fornecidos pelo mysql
    selec = ttk.Treeview(jLista,columns=("id","Nome","Preco"),show="headings")#criando uma treeview e definindo o nome das colunas
    selec.column("id",width=10,minwidth=50)#definindo o tamanho da coluna
    selec.column("Nome",width=100,minwidth=50)#definindo o tamanho da coluna
    selec.column("Preco",width=100,minwidth=50)#definindo o tamanho da coluna
    selec.heading("id",text="ID:")#definindo qual o texto que ira aparecer na coluna
    selec.heading("Nome",text="Nome:")#definindo qual o texto que ira aparecer na coluna
    selec.heading("Preco",text="Preço:")#definindo qual o texto que ira aparecer na coluna
    selec.pack()#terminando a treeview
    for(i,n,p) in card:
        selec.insert("","end",values=(i,n,p))
def prato(nome2, preco,id):
        nome2.delete(0, tk.END) #resetando nome2
        preco.delete(0, tk.END) #resetando preco
        seleco ="select nome,preco from cardapio where id = "+id.get()+""
        cursor.execute(seleco,id.get())
        Produto = str(cursor.fetchall()).replace("(", "", 1).replace("]", "").replace("[", "").replace("'", "")#ele subistitui os caracteres por caracteres vazios e o str trasforma o cursor.fetchone() em string pois ele vem como truple
        Produto, Preco = Produto.split(",", 2) #aqui to pedindo pro python separar produto em 2 variaveis a partir da ","
        Preco = Preco.replace(" ", "").replace(")", "", 1) #aqui so to dando uns replace pq fica um espaço e um parenteses q eu n quero q fiquem la
        nome2.insert(0, Produto) #inserindo Produto em nome2
        preco.insert(0, Preco) #inserindo Preco em preco

def upd(nome2,preco,id):
    upd =  cursor.execute("update cardapio set nome='"+nome2.get()+"',preco='"+preco.get()+"'where id = "+id.get()+"")
    cursor.execute(upd,nome2.get(),preco.get())
    conexao.commit()
    querry = "select id from cardapio where id ="+id.get()
    cursor.execute(querry)
    idb = cursor.fetchone()
    if  idb == None:
        messagebox.showerror("Erro", 'Id inexistente no banco de dados, sugiro que de um insert')#messagebox importado par quando os dados estiverm em branco

def log():
    e1 = nome.get()#passando o valor do label para uma varialvel par dar print no nome
    e2 =senha.get()#passando o valor do label para uma varialvel par dar print na senha 
     
    query = "select nome from log where nome = '"+e1+"'"#funções sendo passadas para o mysql e sendo definidas dentro de uma variavel
    query2 = "select senha from log where nome = '"+e1+"'"#funções sendo passadas para o mysql e sendo definidas dentro de uma variavel
    
    cursor.execute(query, e1)#usa o cursor para executar o comando e a variavel mais o e1 que e == nome.get()
    userNome = str(cursor.fetchone()).replace("(", "").replace(")", "").replace("]", "").replace("[", "").replace("'", "").replace(",", "")#ele subistitui os caracteres por caracteres vazios e o str trasforma o cursor.fetchone() em string pois ele vem como truple
    cursor.execute(query2, e1)#usa o cursor para executar o comando e a variavel mais o e2 que e == senha.get()
    userSenha = str(cursor.fetchone()).replace("(", "").replace("(", "").replace(")", "").replace("]", "").replace("[", "").replace("'", "").replace(",", "")#ele subistitui os caracteres por caracteres vazios e o str trasforma o cursor.fetchone() em string pois ele vem como truple 
    
    cursor.execute("select nome,senha from cliente")
    Nomecl = str(cursor.fetchall()).replace("(", "", 1).replace("]", "").replace("[", "").replace("'", "")#ele subistitui os caracteres por caracteres vazios e o str trasforma o cursor.fetchone() em string pois ele vem como truple
    Nomecl, senhacl = Nomecl.split(",", 2) #aqui to pedindo pro python separar produto em 2 variaveis a partir da ","
    senhacl = senhacl.replace(" ", "").replace(")", "", 1) #aqui so to dando uns replace pq fica um espaço e um parenteses q eu n quero q fiquem la
    if(e2 == senhacl and e1 == Nomecl):
        cardapio()
    if e1 == ""and e2 == "":
     messagebox.showerror("Erro",'Digite os valores')#messagebox importado par quando os dados estiverm em branco
    if(e1 == userNome and e2 == userSenha):
        tk.Label(janela,text="Login efetuado com sucesso").place(x=100,y=200)
        janela.destroy()#fecha a janela principal 
        jsecundaria = tk.Tk()#definindo a janela 
        jsecundaria.title("Principal")#Nome da janela 
        jsecundaria.config(bg="#E9E3D7")
        jsecundaria.geometry("400x250")#tamanho da janela
        jsecundaria.resizable(0,0)#não permite que a janela seja maximizada
        tk.Label(jsecundaria,text='Nome:',bg="#E9E3D7").place(x=9,y=41)#X e de um lado pro outro e y cima e baixo
        tk.Label(jsecundaria,text='Preço:',bg="#E9E3D7").place(x=9,y=80)#X e de um lado pro outro e y cima e baixo
        tk.Label(jsecundaria,text='ID:',bg="#E9E3D7").place(x=9,y=13)
        id = tk.Entry(jsecundaria)
        nome2=tk.Entry(jsecundaria)
        preco=tk.Entry(jsecundaria)
        id.place(width=50,x=50,y=13)
        preco.place(width=150,x=50,y=80)
        nome2.place(width=150,x=50,y=41)
        tk.Button(jsecundaria,text="Procurar produto",command=lambda:prato(nome2,preco,id)).place(x=250,y=10)
        tk.Button(jsecundaria,text='select',command=lambda:select()).place(x=10,y=130)#botao de select
        tk.Button(jsecundaria,text='update', command=lambda: upd(nome2, preco,id)).place(x=60,y=130)#botao de update 
        tk.Button(jsecundaria,text='insert', command=lambda: insert(nome2, preco)).place(x=120,y=130)#botao de insert
        tk.Button(jsecundaria,text='delete',command=lambda: delete(nome2)).place(x=170,y=130)#botao de delet
    else:
        tk.Label(janela,text="nome/senha estao incorretos", bg="#E9E3D7").place(x=100,y=200)#mostra quando os dados do usuarios estão incorretos
botao = tk.Button(janela, text="Entrar",command=log).place(height=50,width=100,y=100,x=50)#botao que executa a ação

janela.bind('<Return>',lambda event:log())#Return e no nome do enter no teclado lambda event manda a função pedida

janela.mainloop()
