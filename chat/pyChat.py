import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
import socket_client
import sys
import os

kivy.require("1.10.1")


class ConnectPage(GridLayout):
    def __init__(self, **kwargs):
        # run init method from GridLayout
        super().__init__(**kwargs)
        self.cols = 2

        # fill with previously entered connection and user info
        if os.path.isfile("prev_details.txt"):
            with open("prev_details.txt", "r") as f:
                d = f.read().split(",")
                prev_ip = d[0]
                prev_port = d[1]
                prev_username = d[2]
        else:
            prev_ip = ""
            prev_port = ""
            prev_username = ""

        # IP
        self.add_widget(Label(text="IP:"))
        self.ip = TextInput(text=prev_ip, multiline=False)
        self.add_widget(self.ip)

        # Port
        self.add_widget(Label(text="Port:"))
        self.port = TextInput(text=prev_port, multiline=False)
        self.add_widget(self.port)

        # Username
        self.add_widget(Label(text="Username:"))
        self.username = TextInput(text=prev_username, multiline=False)
        self.add_widget(self.username)

        # Connect button
        self.connectButton = Button(text="Connect")
        self.connectButton.bind(on_press=self.connect_button)
        self.add_widget(Label())
        self.add_widget(self.connectButton)

    def connect_button(self, instance):
        port = self.port.text
        ip = self.ip.text
        username = self.username.text

        # create file with connection and user info
        with open("prev_details.txt", "w") as f:
            f.write(f"{ip},{port},{username}")

        info = f"Attempting to join {ip}:{port} as {username}"
        chat_app.info_page.update_info(info)

        # update screen manager when pressing connect
        chat_app.screen_manager.current = "Info"

        Clock.schedule_once(self.connect, 1)

    def connect(self, _):
        port = int(self.port.text)
        ip = self.ip.text
        username = self.username.text

        if not socket_client.connect(ip, port, username, show_error):
            return

        chat_app.create_chat_page()
        chat_app.screen_manager.current = "Chat"


class ChatApp(App):
    def build(self):
        # screen manager for multiple screens
        self.screen_manager = ScreenManager()
        # initial connection screen
        # create a pagee, then a screen. add page to screen and screen to screen manager
        self.connect_page = ConnectPage()
        screen = Screen(name="Connect")
        screen.add_widget(self.connect_page)
        self.screen_manager.add_widget(screen)

        # info page
        self.info_page = InfoPage()
        screen = Screen(name="Info")
        screen.add_widget(self.info_page)
        self.screen_manager.add_widget(screen)

        return self.screen_manager

    def create_chat_page(self):
        self.chat_page = ChatPage()
        screen = Screen(name="Chat")
        screen.add_widget(self.chat_page)
        self.screen_manager.add_widget(screen)


class ChatPage(GridLayout):
    def __init__(self, **kwargs):
        # run init method from GridLayout
        super().__init__(**kwargs)

        self.cols = 1
        self.rows = 2

        self.history = ScrollableLabel(height=Window.size[1] * 0.9, size_hint_y=None)
        self.add_widget(self.history)

        self.new_message = TextInput(width=Window.size[0] * 0.8, size_hint_x=None, multiline=False)
        self.send = Button(text="Send")
        self.send.bind(on_press=self.send_message)

        # add grid with two columns containing message and send button
        bottom_line = GridLayout(cols=2)
        bottom_line.add_widget(self.new_message)
        bottom_line.add_widget(self.send)
        # add this to the widget
        self.add_widget(bottom_line)

        # bind function to use enter key to be able to send a message
        Window.bind(on_key_down=self.on_key_down)

        Clock.schedule_once(self.focus_text_input, 1)
        socket_client.start_listening(self.incoming_message, show_error)
        self.bind(size=self.adjust_fields)

    # Updates page layout
    def adjust_fields(self, *_):
        # Chat history height - 90%, but at least 50px for bottom new message/send button part
        if Window.size[1] * 0.1 < 50:
            new_height = Window.size[1] - 50
        else:
            new_height = Window.size[1] * 0.9
        self.history.height = new_height

        # New message input width - 80%, but at least 160px for send button
        if Window.size[0] * 0.2 < 160:
            new_width = Window.size[0] - 160
        else:
            new_width = Window.size[0] * 0.8
        self.new_message.width = new_width

        # Update chat history layout
        # self.history.update_chat_history_layout()
        Clock.schedule_once(self.history.update_chat_history_layout, 0.01)

    def on_key_down(self, instance, keyboard, keycode, text, modifiers):
        # enter key
        if keycode == 40:
            self.send_message(None)

    def send_message(self, _):
        message = self.new_message.text
        self.new_message.text = ""
        if message:
            # own user's message + color
            self.history.update_chat_history(f"[color=dd2020]{chat_app.connect_page.username.text}[/color] > {message}")
            socket_client.send(message)

        Clock.schedule_once(self.focus_text_input, 0.1)

    def focus_text_input(self, _):
        self.new_message.focus = True

    def incoming_message(self, username, message):
        self.history.update_chat_history(f"[color=20dd20]{username}[/color] > {message}")


class InfoPage(GridLayout):
    def __init__(self, **kwargs):
        # run init method from GridLayout
        super().__init__(**kwargs)
        self.cols = 1
        self.message = Label(halign="center", valign="middle", font_size=30)
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)

    def update_info(self, message):
        self.message.text = message

    def update_text_width(self, *_):
        self.message.text_size = (self.message.width*0.9, None)


# kivy doesnt provide a scrollable label, so we need to create one
class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        # run init method from GridLayout
        super().__init__(**kwargs)

        self.layout = GridLayout(cols=1, size_hint_y=None)
        self.add_widget(self.layout)

        self.chat_history = Label(size_hint_y=None, markup=True)
        self.scroll_to_point = Label()

        self.layout.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll_to_point)

    # add new message to the chat history
    def update_chat_history(self, message):
        # add new line and message
        self.chat_history.text += '\n' + message

        # set layout height to height of chat history text + 15 pixels
        self.layout.height = self.chat_history.texture_size[1] + 15
        # set chat history label to height of chat history text
        self.chat_history.height = self.chat_history.texture_size[1]
        # set width of chat history text to 98% of label width
        self.chat_history.text_size = (self.chat_history.width*.98, None)

        # scroll to bottom of layout
        self.scroll_to(self.scroll_to_point)

    def update_chat_history_layout(self, _=None):
        # Set layout height to height of chat history + 15 pixels
        self.layout.height = self.chat_history.texture_size[1] + 15
        # set chat history label to height of chat history text
        self.chat_history.height = self.chat_history.texture_size[1]
        # set width of chat history text to 98% of the label width
        self.chat_history.text_size = (self.chat_history.width * 0.98, None)


def show_error(message):
    chat_app.info_page.update_info(message)
    chat_app.screen_manager.current = "Info"
    Clock.schedule_once(sys.exit, 3)


if __name__ == "__main__":
    chat_app = ChatApp()
    chat_app.run()
