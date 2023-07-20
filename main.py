from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.list import OneLineRightIconListItem
from kivymd.uix.button import MDIconButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.label import  MDLabel
from kivy.metrics import dp
from kivy.clock import Clock
import sqlite3
import os



class VizualizarLista(Screen):
    def on_enter(self):
        tabelas = self.buscar_todasListas()
        for tabela in tabelas:
            self.item = OneLineRightIconListItem(text=f"{tabela}")
            btn_Direito = MDIconButton(icon="eye-outline", pos_hint={"center_x": .9, "center_y": .5})
            btn_Direito.bind(on_release=lambda x, tabela=tabela: self.abrirLista(tabela))
            self.item.add_widget(btn_Direito)
            self.ids.container.add_widget(self.item)
    def on_leave(self):
        container = self.ids.container
        for child in container.children[:]:
            container.remove_widget(child)

    def abrirLista(self,nomeLista):
        telaLista = self.manager.get_screen('lista')
        telaLista.update_label(nomeLista)
        self.manager.current = 'lista'


    def buscar_todasListas(self):
        conn = sqlite3.connect('appListas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        consulta_tabelas = cursor.fetchall()
        conn.close()
        tabelas = []
        for tupla in consulta_tabelas:
            elemento = tupla[0]
            tabelas.append(elemento)
        return tabelas

class TelaCarregamento(Screen):
    def on_enter(self):
        Clock.schedule_once(self.change_screen,3)

    def change_screen(self,e):
        self.manager.current = "tela_inicial"


class Lista(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def update_label(self, name):
        self.ids.nomeLista.text = name
        self.dados_tabela(name)

    def dados_tabela(self,nome_tabela):
        conn = sqlite3.connect('appListas.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {nome_tabela}")
        consultaLista = cursor.fetchall()
        conn.close()
        consultaTratada = [(item[1],item[2]) for item in consultaLista]
        self.tabelaLista = MDDataTable(
            size_hint=(0.9, 0.6),
            use_pagination=True,
            pos_hint=( {"center_x": .5, "center_y": .5}),
            column_data=[
                ("Item",dp(25)),
                ("Quantidade",dp(30))
            ]
        )
        self.tabelaLista.row_data=consultaTratada
        self.add_widget(self.tabelaLista)

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
        text_fieldQuantidade.text=''
        text_fieldItem.text=f"{item} foi adicionado"

        # Exibir o vetor
        print(self.lista_itens)
        print(self.lista_quantidade)


    def criar_tabela(self):
        text_field_nomeTabela = self.ids.nome_lista
        nome_Tabela = text_field_nomeTabela.text

        if self.verificando_Existencia_Tabela(nome_Tabela) is False:
            conn = sqlite3.connect('appListas.db')
            cursor = conn.cursor()
            cursor.execute(f'''CREATE TABLE {nome_Tabela} (id INTEGER PRIMARY KEY AUTOINCREMENT,name_item TEXT NOT NULL,quantidade_item INTEGER NOT NULL)''')
            for item , quantidade in zip(self.lista_itens, self.lista_quantidade):
                cursor.execute(f"INSERT INTO {nome_Tabela} (name_item,quantidade_item) VALUES (?, ?)", (item,quantidade))
            conn.commit()
            conn.close()
            text_fieldItem = self.ids.text_field_Item
            text_fieldQuantidade = self.ids.text_field_Quantidade
            text_fieldItem.text=''
            text_fieldQuantidade.text = ''
            text_field_nomeTabela.text=''
            aviso = Snackbar(text=f"A lista {nome_Tabela} criada com sucesso.")
            aviso.open()
        else:
            aviso = Snackbar(text=f"A lista {nome_Tabela} já existe.")
            aviso.open()

    def verificando_Existencia_Tabela(self,table_name):
        conn = sqlite3.connect('appListas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()
        return resultado is not None
class gerenciador_Tela(ScreenManager):
    pass


class appListas(MDApp):
    def create_database(self):
        if not os.path.exists('appListas.db'):
            conn = sqlite3.connect('appListas.db')
            conn.commit()
            conn.close()
            print("Banco de dados criado com sucesso!")
        else:
            print("Banco de dados já existe.")

    def build(self):
        self.create_database()
        self.icon ='imagens/logo_carregamento.png'
        self.title = 'Listas'
        Window.size = (360, 640)

        return Builder.load_file("telas.kv")





appListas().run()