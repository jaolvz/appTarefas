from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
import sqlite3
import os



class VizualizarLista(Screen):
    def on_pre_enter(self):
        conn = sqlite3.connect('appListas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        consulta_tabelas = cursor.fetchall()

        tabelas = []
        for tupla in consulta_tabelas:
            elemento = tupla[0]
            tabelas.append(elemento)
        menu_items = [
            {
                "text": f"{i}",
            } for i in tabelas
        ]

        self.menu = MDDropdownMenu(
            caller=self.ids.dropdown_tabelas,
            items=menu_items,
            position="center",
        )
        self.menu.bind()
        conn.close()

    def pegar_todaslinhas(self):
        # Conectar ao banco de dados
        conn = sqlite3.connect('testeApp.db')

        # Criar um cursor para executar comandos SQL
        cursor = conn.cursor()

        # Executar uma consulta SELECT para recuperar todos os registros da tabela
        cursor.execute("SELECT * FROM ola")

        # Recuperar os resultados da consulta
        rows = cursor.fetchall()

        # Exibir os resultados
        for row in rows:
            print(row)

        # Fechar a conexão
        conn.close()

class TelaCarregamento(Screen):
    def on_enter(self):
        Clock.schedule_once(self.change_screen, 3)

    def change_screen(self, dt):
        self.manager.current = "tela_inicial"

    pass

class TelaInicial(Screen):
   pass


class CriarLista(Screen):
    lista_itens = []
    lista_quantidade = []

    def btn_AdicionarItens(self):
        # pegando os campos pelo id
        text_fieldItem = self.ids.text_field_Item
        text_fieldQuantidade = self.ids.text_field_Quantidade

        # pegando os textos dos refenrentes id's
        quantidade = text_fieldQuantidade.text
        item = text_fieldItem.text

        # função nativa do py para retirar espaços do começo e fim da string
        quantidade = quantidade.strip()
        item = item.strip()

        item = item.lower()  # função nativa para passar o texto inteiro para minusculo
        item = item.capitalize()  # função nativa para a primeira letra ser maiuscula
        # Assim, evita-se que o mesmo item seja colocado. Exemplo: Manga e manga

        for item_lista in self.lista_itens:
            if item == item_lista:
                text_fieldItem.text = "Você já adicionou esse item."
                return 0

        self.lista_itens.append(item)
        self.lista_quantidade.append(quantidade)

        # Exibir o vetor
        print(self.lista_itens)
        print(self.lista_quantidade)


    def criar_tabela(self):
        texField_nomeTabela = self.ids.nome_lista
        nome_Tabela = texField_nomeTabela.text

        conn = sqlite3.connect('appListas.db')
        cursor = conn.cursor()

        # Criar tabelas ou executar outras operações necessárias
        cursor.execute(f'''CREATE TABLE {nome_Tabela} (id INTEGER PRIMARY KEY AUTOINCREMENT,name_item TEXT NOT NULL,quantidade_item INTEGER NOT NULL)''')

        for item , quantidade in  zip(self.lista_itens, self.lista_quantidade):
            cursor.execute(f"INSERT INTO {nome_Tabela} (name_item,quantidade_item) VALUES (?, ?)", (item,quantidade))


        # Salvar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        print("Tabela criada com sucesso")




class gerenciador_Tela(ScreenManager):
    pass


class appCompras(MDApp):
    def create_database(self):
        # Verificar se o arquivo do banco de dados já existe
        if not os.path.exists('appListas.db'):
            # Conectar ao banco de dados
            conn = sqlite3.connect('appListas.db')
            conn.commit()
            conn.close()

            print("Banco de dados criado com sucesso!")
        else:
            print("Banco de dados já existe.")

    def build(self):
        self.create_database()
        Window.size = (360, 640)
        return Builder.load_file("telas.kv")





appCompras().run()