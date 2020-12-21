import requests
import json
import urllib.request as req
from bs4 import BeautifulSoup
from transitions.extensions import GraphMachine

from utils import send_text_message, send_sticker_message, send_flex_message


class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    def is_going_to_state1(self, event):
        text = event.message.text
        return text.lower() == "go to state1"

    def is_going_to_state2(self, event):
        text = event.message.text
        return text.lower() == "go to state2"

    def is_going_to_state3(self, event):
        text = event.message.text
        return text.lower() == "state3"

    def on_enter_state1(self, event):
        print("I'm entering state1")

        reply_token = event.reply_token
        send_sticker_message(reply_token, "1", "2")
        self.go_back()

    def on_exit_state1(self):
        print("Leaving state1")

    def on_enter_state2(self, event):
        print("I'm entering state2")

        reply_token = event.reply_token
        url = "https://www.vscinemas.com.tw/vsweb/film/index.aspx"
        request = req.Request(url, headers={
                              "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"})
        #r = requests.get('https://www.vscinemas.com.tw/vsweb/film/index.aspx')
        #r.encoding = 'utf-8'
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        soup = BeautifulSoup(data, 'lxml')
        content = []
        column = []
        name = []
        english = []
        introduction = []
        for i, data in enumerate(soup.select('ul.movieList figure a')):
            if i > 4:
                break
            introduction.append(
                "https://www.vscinemas.com.tw/vsweb/film/"+data['href'])
        for i, data in enumerate(soup.select('ul.movieList figure a img')):
            if i > 4:
                break
            content.append(
                "https://www.vscinemas.com.tw/vsweb" + data['src'][2:])
        for i, data in enumerate(soup.select('section.infoArea a')):
            if i > 4:
                break
            name.append(data.text)
        for i, data in enumerate(soup.select('section.infoArea h3')):
            if i > 4:
                break
            english.append(data.text)

        bubble_string = {
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "image",
                                "size": "full",
                                "aspectMode": "cover",
                                "aspectRatio": "2:3",
                                "gravity": "top",
                                "url": content[0]
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "text": name[0],
                                                "size": "xl",
                                                "color": "#000000",
                                                "weight": "bold"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "box",
                                        "layout": "baseline",
                                        "contents": [
                                            {
                                                "type": "text",
                                                "color": "#000000",
                                                "size": "sm",
                                                "flex": 0,
                                                "text": english[0]
                                            }
                                        ],
                                        "spacing": "lg"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "uri",
                                                    "uri": "http://linecorp.com/",
                                                    "label": "簡介"
                                                },
                                                "margin": "xs",
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#ff1493"
                                            },
                                            {
                                                "type": "button",
                                                "action": {
                                                    "type": "uri",
                                                    "label": "時刻表",
                                                    "uri": "http://linecorp.com/"
                                                },
                                                "height": "sm",
                                                "style": "primary",
                                                "color": "#1e90ff"
                                            }
                                        ],
                                        "borderWidth": "none",
                                        "cornerRadius": "4px",
                                        "spacing": "lg",
                                        "borderColor": "#000000",
                                        "margin": "md"
                                    }
                                ],
                                "position": "absolute",
                                "offsetBottom": "0px",
                                "offsetStart": "0px",
                                "offsetEnd": "0px",
                                "backgroundColor": "#ffffffcc",
                                "paddingAll": "20px",
                                "paddingTop": "18px",
                                "height": "130px"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "熱映中",
                                        "color": "#ffffff",
                                        "align": "center",
                                        "size": "xs",
                                        "offsetTop": "3px"
                                    }
                                ],
                                "position": "absolute",
                                "cornerRadius": "20px",
                                "offsetTop": "18px",
                                "backgroundColor": "#ff334b",
                                "offsetStart": "18px",
                                "height": "25px",
                                "width": "53px"
                            }
                        ],
                        "paddingAll": "0px"
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": content[1],
                        "size": "full",
                        "aspectRatio": "21:30",
                        "aspectMode": "fit"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "電影簡介",
                                    "uri": introduction[1]
                                },
                                "color": "#ff005e",
                                "style": "link"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "電影時刻表",
                                    "text": name[1]+"時刻表",
                                    "data": introduction[1]
                                },
                                "style": "link"
                            }
                        ],
                        "backgroundColor": "#ffffffe0",
                        "borderColor": "#ffffffe0"
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": content[2],
                        "size": "full",
                        "aspectRatio": "21:30",
                        "aspectMode": "fit"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "電影簡介",
                                    "uri": introduction[2]
                                },
                                "color": "#ff005e",
                                "style": "link"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "電影時刻表",
                                    "text": name[2]+"時刻表",
                                    "data": introduction[2]
                                },
                                "style": "link"
                            }
                        ],
                        "backgroundColor": "#ffffffe0",
                        "borderColor": "#ffffffe0"
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": content[3],
                        "size": "full",
                        "aspectRatio": "21:30",
                        "aspectMode": "fit"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "電影簡介",
                                    "uri": introduction[3]
                                },
                                "color": "#ff005e",
                                "style": "link"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "電影時刻表",
                                    "text": name[3]+"時刻表",
                                    "data": introduction[3]
                                },
                                "style": "link"
                            }
                        ],
                        "backgroundColor": "#ffffffe0",
                        "borderColor": "#ffffffe0"
                    }
                },
                {
                    "type": "bubble",
                    "hero": {
                        "type": "image",
                        "url": content[4],
                        "size": "full",
                        "aspectRatio": "21:30",
                        "aspectMode": "fit"
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "uri",
                                    "label": "電影簡介",
                                    "uri": introduction[4]
                                },
                                "color": "#ff005e",
                                "style": "link"
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "postback",
                                    "label": "電影時刻表",
                                    "text": name[4]+"時刻表",
                                    "data": introduction[4]
                                },
                                "style": "link"
                            }
                        ],
                        "backgroundColor": "#ffffffe0",
                        "borderColor": "#ffffffe0"
                    }
                }
            ]
        }
        s1 = json.dumps(bubble_string)
        s2 = json.loads(s1)

        send_flex_message(reply_token, "hello", s2)
        self.go_back()

    def on_exit_state2(self):
        print("Leaving state2")

    def on_enter_state3(self, event):
        print("I'm entering state3")

        reply_token = event.reply_token
        send_text_message(reply_token, "goto state3")
        self.go_back()

    def on_exit_state3(self):
        print("Leaving state3")
