import flet as ft

def main(pagina: ft.Page):
    pagina.title = "Meu HashZap"

    pagina.theme_mode = ft.ThemeMode.DARK

    # texto = ft.Text("HashZap")
    # pagina.add(texto)

    pagina.vertical_alignment = ft.MainAxisAlignment.CENTER
    pagina.horizontal_alignment= ft.CrossAxisAlignment.CENTER

    img = ft.Image(
        src=f"/imgs/Logo HashZap.png",
        width=250,
        height=250,
        fit=ft.ImageFit.CONTAIN,
    )
    pagina.add(img)
    pagina.update()

    #chat = ft.Column()

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    nome_usuario = ft.TextField(label="Escreva seu Nome")
    
    def enviar_mensagem_tunel(mensagem):

        tipo_mensagem = mensagem["tipo"]

        if tipo_mensagem == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]

            # # add mensagem no chat
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}"),)

        else:
            usuario_mensagem = mensagem["usuario"]
            # add mensagem no chat
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat!", size=12, italic=True, color=ft.colors.DEEP_ORANGE_900))

        pagina.update()

    # PubSub
    pagina.pubsub.subscribe(enviar_mensagem_tunel)

    def enviar_mensagem(evento):
        pagina.pubsub.send_all({
            "texto": campo_mensagem.value, 
            "usuario": nome_usuario.value, 
            "tipo": "mensagem"
            })
        # limpar o campo de mensagem
        campo_mensagem.value = ""
        pagina.update()

    campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem, autofocus=True, shift_enter=True, min_lines=1, max_lines=5, filled=True, expand=True)
    botao_enviar = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)
    
    def entrar_chat(evento):
        if not nome_usuario.value:
            nome_usuario.error_text = "Name cannot be blank!"
            nome_usuario.update()

            pagina.pubsub.send_all({
                "usuario":"SemNome", 
                "tipo": "entrada"
            })
        else:
            pagina.session.set("nome_usuario", nome_usuario.value)
            pagina.dialog.open = False
            pagina.pubsub.send_all({
                "usuario":nome_usuario.value, 
                "tipo": "entrada"
            })
        
        # Add chat
        #pagina.add(chat)
        pagina.add(ft.Container(
            content=chat,
            border=ft.border.all(1, ft.colors.OUTLINE),
            border_radius=5,
            padding=10,
            expand=True,
            ),
            ft.Row(
                [
                    campo_mensagem,
                    ft.IconButton(
                        icon=ft.icons.SEND_ROUNDED,
                        tooltip="Send message",
                        on_click=enviar_mensagem,
                    ),
                ]
            ),
        )

        #fechar o popup
        popup.open = False

        #remover o botao iniciar chat
        pagina.remove(botao_iniciar)
        #pagina.remove(texto)

        #criar o campo de mensagem do user
        """ pagina.add(ft.Row([
            campo_mensagem,
            botao_enviar
            ])) """
        
        # Atualizar Pag
        pagina.update()

    popup = ft.AlertDialog(
        open=False,
        modal=True,
        title=ft.Text("Bem Vindo ao HashZap!"),
        content=nome_usuario, 
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_chat)],
    )

    def entrar_popup(evento):
        pagina.dialog = popup
        popup.open = True
        pagina.update()

    botao_iniciar = ft.ElevatedButton("Iniciar Chat", on_click=entrar_popup)
    pagina.add(botao_iniciar)


#ft.app(target=main, assets_dir="assets") # PAra rodar num APP
ft.app(target=main, view=ft.WEB_BROWSER, port=8000) # Para rodar na Web