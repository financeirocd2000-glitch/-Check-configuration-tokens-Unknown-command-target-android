import os
os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"

import cv2
from pyzbar import pyzbar

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

try:
    from plyer import share
except:
    share = None

coletas = []


class ColetorLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.lista = Label(text="")
        self.add_widget(self.lista)

        botoes = BoxLayout(size_hint_y=0.2)

        btn_manual = Button(text="Incluir Manual")
        btn_manual.bind(on_press=self.incluir_manual)

        btn_export1 = Button(text="Exportar ;")
        btn_export1.bind(on_press=self.exportar_modelo1)

        btn_export2 = Button(text="Exportar /")
        btn_export2.bind(on_press=self.exportar_modelo2)

        botoes.add_widget(btn_manual)
        botoes.add_widget(btn_export1)
        botoes.add_widget(btn_export2)

        self.add_widget(botoes)

        self.atualizar_lista()

        Clock.schedule_once(self.iniciar_camera, 1)

    def atualizar_lista(self):

        texto = ""

        for c in coletas:
            texto += f"{c[0]} | QTD {c[1]}\n"

        self.lista.text = texto


    def iniciar_camera(self, *args):

        self.cap = cv2.VideoCapture(0)
        Clock.schedule_interval(self.ler_camera, 0.3)


    def ler_camera(self, dt):

        ret, frame = self.cap.read()

        if not ret:
            return

        codigos = pyzbar.decode(frame)

        for codigo in codigos:

            codigo_lido = codigo.data.decode("utf-8")

            Clock.unschedule(self.ler_camera)

            self.tratar_codigo(codigo_lido)

            Clock.schedule_once(self.reiniciar_camera, 2)

            break


    def reiniciar_camera(self, dt):

        Clock.schedule_interval(self.ler_camera, 0.3)


    def tratar_codigo(self, codigo):

        for item in coletas:

            if item[0] == codigo:

                box = BoxLayout(orientation="vertical")

                label = Label(text="Código repetido\nSomar quantidade?")
                box.add_widget(label)

                botoes = BoxLayout()

                btn_sim = Button(text="SIM")
                btn_nao = Button(text="NÃO")

                botoes.add_widget(btn_sim)
                botoes.add_widget(btn_nao)

                box.add_widget(botoes)

                popup = Popup(title="Código repetido",
                              content=box,
                              size_hint=(0.7,0.4))

                btn_sim.bind(on_press=lambda x:self.somar(item,popup))
                btn_nao.bind(on_press=popup.dismiss)

                popup.open()
                return

        self.pedir_quantidade(codigo)


    def pedir_quantidade(self, codigo):

        box = BoxLayout(orientation="vertical")

        label = Label(text=f"Código {codigo}\nQuantidade")
        box.add_widget(label)

        qtd = TextInput(multiline=False,input_filter='int')
        box.add_widget(qtd)

        btn = Button(text="Confirmar")
        box.add_widget(btn)

        popup = Popup(title="Quantidade",
                      content=box,
                      size_hint=(0.7,0.5))

        def confirmar(instance):

            coletas.append([codigo,int(qtd.text)])

            popup.dismiss()
            self.atualizar_lista()

        btn.bind(on_press=confirmar)

        popup.open()


    def somar(self,item,popup):

        popup.dismiss()

        box = BoxLayout(orientation="vertical")

        label = Label(text="Quantidade para somar")
        box.add_widget(label)

        qtd = TextInput(multiline=False,input_filter='int')
        box.add_widget(qtd)

        btn = Button(text="Confirmar")
        box.add_widget(btn)

        popup2 = Popup(title="Somar",
                       content=box,
                       size_hint=(0.7,0.5))

        def confirmar(instance):

            item[1] += int(qtd.text)

            popup2.dismiss()
            self.atualizar_lista()

        btn.bind(on_press=confirmar)

        popup2.open()


    def incluir_manual(self,instance):

        box = BoxLayout(orientation="vertical")

        box.add_widget(Label(text="Código"))

        codigo = TextInput(multiline=False)
        box.add_widget(codigo)

        box.add_widget(Label(text="Quantidade"))

        qtd = TextInput(multiline=False,input_filter='int')
        box.add_widget(qtd)

        btn = Button(text="Adicionar")
        box.add_widget(btn)

        popup = Popup(title="Inclusão Manual",
                      content=box,
                      size_hint=(0.7,0.6))

        def confirmar(instance):

            cod = codigo.text
            quantidade = int(qtd.text)

            for item in coletas:

                if item[0] == cod:

                    item[1] += quantidade
                    popup.dismiss()
                    self.atualizar_lista()
                    return

            coletas.append([cod,quantidade])

            popup.dismiss()
            self.atualizar_lista()

        btn.bind(on_press=confirmar)

        popup.open()


    def exportar_modelo1(self,instance):

        caminho="coleta.txt"

        with open(caminho,"w") as f:

            for c in coletas:
                f.write(f"{c[0]};{c[1]}\n")

        if share:
            share.share(filepath=caminho)

        self.perguntar_limpar()


    def exportar_modelo2(self,instance):

        caminho="coleta.txt"

        with open(caminho,"w") as f:

            for c in coletas:
                f.write(f"{c[0]}/{c[1]}\n")

        if share:
            share.share(filepath=caminho)

        self.perguntar_limpar()


    def perguntar_limpar(self):

        box = BoxLayout(orientation="vertical")

        box.add_widget(Label(text="Limpar coleta?"))

        botoes = BoxLayout()

        btn_sim = Button(text="SIM")
        btn_nao = Button(text="NÃO")

        botoes.add_widget(btn_sim)
        botoes.add_widget(btn_nao)

        box.add_widget(botoes)

        popup = Popup(title="Limpar",
                      content=box,
                      size_hint=(0.7,0.4))

        btn_sim.bind(on_press=lambda x:self.limpar(popup))
        btn_nao.bind(on_press=popup.dismiss)

        popup.open()


    def limpar(self,popup):

        global coletas

        coletas=[]

        popup.dismiss()
        self.atualizar_lista()


class ColetorApp(App):

    def build(self):
        return ColetorLayout()


ColetorApp().run()