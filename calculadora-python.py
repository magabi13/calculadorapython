import flet as ft
from flet import Colors

def main(page: ft.Page):
    # 1. CONFIGURAÇÕES DA JANELA
    page.window.width = 250
    page.window.height = 480 
    page.window.resizable = False #Trava o tamanho da janela para que o design não quebre
    page.window.always_on_top = True #Faz com que a calculadora flutue sobre qualquer outra janela aberta
    page.bgcolor = '#000'
    page.window.title_bar_hidden = True #Remove a barra de título padrão do windows
    page.window.title_bar_buttons_hidden = True

    formula = ""
    
    # 2. LÓGICA DE CÁLCULO
    def calculate(): #substitui o x e dividir   por */
        nonlocal formula
        try:
            expressao = formula.replace("x", "*").replace("÷", "/")
            return str(eval(expressao))
        except:
            return "Erro"

    def on_click(e): #Ela verifica qual texto está dentro do botão clicado
        nonlocal formula
        botao = e.control.content.value
        if botao == "AC":
            formula = ""
            result.value = "0"
        elif botao == "=":
            resultado = calculate()
            result.value = resultado
            formula = resultado 
        elif botao == "+/-":
            if result.value != "0":
                result.value = str(float(result.value) * -1)
                formula = result.value
        elif botao == "%":
            result.value = str(float(result.value) / 100)
            formula = result.value
        else:
            if result.value == "0" and botao not in "+-x÷":
                result.value = botao
                formula = botao
            else:
                result.value += botao
                formula += botao
        page.update()

    # 3. FUNÇÃO DE BOTÃO COM HOVER (coloquei bem suave)
    def btn(texto, cor_fundo, cor_texto=Colors.WHITE, largura=50):
        cor_hover = Colors.WHITE24 if cor_fundo == Colors.GREY_900 else Colors.BLACK12

        def mudar_cor(e):
            # e.data é "true" ou "false"
            e.control.bgcolor = cor_hover if e.data == "true" else cor_fundo
            e.control.update()

        return ft.Container(
            content=ft.Text(texto, color=cor_texto, size=18, weight="bold"),
            alignment=ft.Alignment(0, 0),
            width=largura,
            height=50,
            bgcolor=cor_fundo,
            border_radius=25,
            on_click=on_click,
            on_hover=mudar_cor,
            # Correção: Use um número simples ou ft.Animation (A maiúsculo)
            animate=300 
        )

    # 4. DESIGN DA BARRA SUPERIOR
    controls_buttons = ft.Row(
        controls=[
            ft.Container(width=12, height=12, bgcolor=Colors.RED_400, border_radius=6),
            ft.Container(width=12, height=12, bgcolor=Colors.AMBER_300, border_radius=6),
            ft.Container(width=12, height=12, bgcolor=Colors.GREEN_400, border_radius=6),
        ],
        spacing=8
    )

    drag_area = ft.WindowDragArea(
        content=ft.Container(
            bgcolor=Colors.WHITE, 
            padding=ft.Padding(10, 5, 10, 5),
            content=ft.Row(
                controls=[
                    controls_buttons,
                    ft.Text("Calculadora", color=Colors.BLACK, size=12, weight="bold"),
                    ft.Container(width=40) 
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        )
    )

    # 5. DISPLAY E FILEIRAS
    result = ft.Text(value='0', color=Colors.WHITE, size=40)
    display = ft.Container(
        content=ft.Row(controls=[result], alignment=ft.MainAxisAlignment.END),
        padding=ft.Padding(0, 0, 20, 0)
    )

    rows = [
        ft.Row(controls=[btn("AC", Colors.GREY_400, Colors.BLACK), btn("+/-", Colors.GREY_400, Colors.BLACK), btn("%", Colors.GREY_400, Colors.BLACK), btn("÷", Colors.ORANGE)], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        ft.Row(controls=[btn("7", Colors.GREY_900), btn("8", Colors.GREY_900), btn("9", Colors.GREY_900), btn("x", Colors.ORANGE)], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        ft.Row(controls=[btn("4", Colors.GREY_900), btn("5", Colors.GREY_900), btn("6", Colors.GREY_900), btn("-", Colors.ORANGE)], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        ft.Row(controls=[btn("1", Colors.GREY_900), btn("2", Colors.GREY_900), btn("3", Colors.GREY_900), btn("+", Colors.ORANGE)], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        ft.Row(controls=[btn("0", Colors.GREY_900, largura=110), btn(".", Colors.GREY_900), btn("=", Colors.ORANGE)], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
    ]

    page.add(drag_area, ft.Column(controls=[ft.Container(height=20), display, *rows], spacing=10))
    page.update()

ft.app(target=main)