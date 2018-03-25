from kivy.app import App
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
import pandas as pd
from selenium import webdriver
import time

#ウィンドウサイズを指定
Config.set('graphics', 'width', '240')
Config.set('graphics', 'height', '340')

# デフォルトに使用するフォントを変更する
resource_add_path('./fonts')
#日本語が使用できるように日本語フォントを指定する
LabelBase.register(DEFAULT_FONT, 'mplus-2c-regular.ttf')
global df
#csvファイル読み込み
df = pd.read_csv('setting.csv', sep=',', quotechar='"', comment="#", encoding='cp932')


class Menu(BoxLayout):
    menu_buttons = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #ファイル内容出力
        #print(df)
        for i in range(len(df)):
            #ボタンを作成(ID、テキスト、比率を設定)
            button = Button(id=str(i), text=df['NAME'][i], \
                    size_hint=(1, 0.1))
            button.bind(on_press=self.select_button)
            self.menu_buttons.add_widget(button)
            
    def select_button(self, button):
        #ボタン押下時の処理
        message = button.text + " を選択しました"
        #ラベルのテキストを更新
        self.ids['menu_label'].text = message

        print('Selected is {0} button'.format(button.id))
        index = int(button.id)
        print(str(df['NAME'][index])+'、'+str(df['URL'][index])+'、'+ \
                str(df['ID'][index])+'、'+str(df['ID_TYPE'][index])+'、'+ \
                str(df['PW'][index])+'、'+str(df['PW_TYPE'][index])+'、'+ \
                str(df['SUBMIT'][index])+'\n')

        #ログイン処理
        #Chromeを起動
        driver = webdriver.Chrome('C:\drivers\chromedriver.exe')
        time.sleep(1)
        driver.refresh()

        #指定のURLにアクセス
        if not str(df['URL'][index]) == '':
            driver.get(str(df['URL'][index]))

            if str(df['NAME'][index]) == "りそな":
                driver.find_element_by_name('param3').click()
                time.sleep(1)

            if not str(df['ID'][index]) == '':
                id_type = driver.find_element_by_name(str(df['ID_TYPE'][index]))
                id_type.send_keys(str(df['ID'][index]))
            if not str(df['PW'][index]) == '':
                pw_type = driver.find_element_by_name(str(df['PW_TYPE'][index]))
                pw_type.send_keys(str(df['PW'][index]))
            if not str(df['SUBMIT'][index]) == '':
                pass
            
        else:
            print('ERROR:01')
        

class MenuApp(App):
    def build(self):
        return Menu()

if __name__ == '__main__':
    MenuApp().run()
