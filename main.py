from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import  Builder
from kivy.core.window import Window


class VizualizarLista(Screen):
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

class gerenciador_Tela(ScreenManager):
    pass


class appCompras(MDApp):

    def build(self):
        Window.size = (360, 640)
        return Builder.load_file("telas.kv")





appCompras().run()