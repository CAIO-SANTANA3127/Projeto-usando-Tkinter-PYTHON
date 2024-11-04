from tkinter import *
from tkcalendar import DateEntry
import pyodbc
import tkinter.messagebox as Messagebox

# Configurações de conexão
conexao = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;"
    "Database=TKPY;"
    "Trusted_Connection=yes;"
)

try:
    x = pyodbc.connect(conexao)
    cursor = x.cursor()  # Cria o cursor para realizar operações no banco de dados
    print('Conexão bem-sucedida')
except pyodbc.Error as e:
    print("Erro ao conectar:", e)

# Função de inserção
def inserir():
    id_novo = e_id.get()
    nome = e_nome.get()
    data_nascimento = e_data.get_date()
    uf = e_uf.get()
    
    if id_novo == '' or nome == '' or uf == '' or data_nascimento == '':
        Messagebox.showinfo('Status inserido!', 'Todos os campos são obrigatórios')
        return
    
    # Verifica se o ID já está cadastrado
    cursor.execute("SELECT * FROM pessoa WHERE id = ?", (id_novo,))
    resultado = cursor.fetchall()

    if resultado:
        Messagebox.showwarning("Aviso", "ID já cadastrado! Por favor, insira um novo ID.")
        return

    try:
        a = "INSERT INTO pessoa (id, nome, uf, data_nascimento) VALUES (?, ?, ?, ?)"
        b = (int(id_novo), nome, uf, data_nascimento)
        
        cursor.execute(a, b)
        x.commit()
        
        Messagebox.showinfo('Status inserido!', 'Inserido com sucesso!')
        
        e_id.delete(0, END)
        e_nome.delete(0, END)
        e_uf.delete(0, END)
        e_data.set_date('1900-01-01')

    except Exception as e:
        Messagebox.showerror("Erro", f"Ocorreu um erro ao inserir os dados: {e}")

# Função de exclusão
def excluir():
    cod = e_id.get()

    if cod == '':
        Messagebox.showinfo('Status inserido!', 'Campo são obrigatório')
    else:
        try:
            cursor.execute('DELETE FROM pessoa WHERE id = ?', (int(cod),))
            x.commit()
            Messagebox.showinfo('Status deletado!', 'Deletado com sucesso!')
            
            e_id.delete(0, END)
            e_nome.delete(0, END)
            e_uf.delete(0, END)
            e_data.set_date('1900-01-01')

        except Exception as e:
            Messagebox.showerror("Erro", f"Ocorreu um erro ao excluir os dados: {e}")

# Função de seleção
def selecionar():
    if e_id.get() == '':
        Messagebox.showinfo('Status selecionado!', 'Campo são obrigatório')
    else:
        try:
            cursor.execute('SELECT * FROM pessoa WHERE id = ?', (int(e_id.get()),))
            r = cursor.fetchall()

            e_id.delete(0, END)
            e_nome.delete(0, END)
            e_uf.delete(0, END)
            e_data.set_date('1900-01-01')

            for row in r:
                e_nome.insert(0, row[1])
                e_id.insert(0, row[0])
                e_uf.insert(0, row[2])
                e_data.set_date(row[3])

            print(r)
            Messagebox.showinfo('selecionar', 'Registro carregado com sucesso!')

        except Exception as e:
            Messagebox.showerror("Erro", f"Ocorreu um erro ao selecionar os dados: {e}")

# Configuração da interface gráfica
i = Tk()
i.title('Assesando um Banco de dados')
i.geometry('500x400')

nome = Label(i, text='Nome:')
nome.place(x=80, y=30)

id = Label(i, text='Id:')
id.place(x=80, y=60)

uf = Label(i, text='UF:')
uf.place(x=80, y=90)

data_nascimento = Label(i, text='Nascimento:')
data_nascimento.place(x=80, y=120)

e_nome = Entry(i)
e_nome.place(x=150, y=30)

e_id = Entry(i)
e_id.place(x=150, y=60)

e_uf = Entry(i)
e_uf.place(x=150, y=90)

e_data = DateEntry(i, date_pattern="yyyy-mm-dd")
e_data.place(x=150, y=120)

inserir = Button(i, text='Inserir', bg='white', command=inserir)
inserir.place(x=120, y=160)

excluir = Button(i, text='Excluir', bg='white', command=excluir)
excluir.place(x=170, y=160)

selecionar = Button(i, text='Consultar', bg='white', command=selecionar)
selecionar.place(x=220, y=160)

i.mainloop()
