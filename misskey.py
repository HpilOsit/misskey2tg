import requests
import json
from dateutil import parser
from datetime import *

class Note:
    def __init__(self):
        self.createdAt = None
        self.text = ""
        self.replyId = ""
        self.cw = ""
        self.files = []

def _get_raw_notes(site: str, user_id: str):
    req_body = {
        "userId": user_id,
        "limit": 10
    }
    req_header = {
        "User-Agent": "MisskeyTelegramForwarder",
        'Content-type':'application/json', 
        'Accept':'*/*'
    }
    res = requests.post(
        url=f"{site}/api/users/notes",
        headers=req_header,
        data=json.dumps(req_body)
    )
    return json.loads(res.content)

def get_notes(site: str, user_id: str) -> list:
    res = _get_raw_notes(site, user_id)
    notes = []
    for n in res:
        note = Note()
        note.replyId = n.get('replyId')
        note.cw = n.get('cw')
        note.createdAt = parser.parse(n["createdAt"])

        if "renote" in n:
            renote = n['renote']
            if note.cw:
                text = (
                    f"<code>❀Title : </code><b>{renote['text']}</b>\n\n"
                    f"<code>❀Artist : </code><b><a href=\"https://t.me/ChuangBian/\">{renote['user']['name']}</a></b>\n\n"
                    f"► <b><a href=\"https://t.me/ChuangBian/5/\">ᴍɪꜱꜱᴋᴇʏ</a></b>"
                )
                lines = text.splitlines()
                lines.insert(1, "\nCW: " + note.cw + "\n\n")
                lines.insert(2, "<tg-spoiler>")
                lines.insert(len(lines) - 1, "</tg-spoiler>")
                note.text = ''.join(lines)
            else:
                note.text = (
                    f"<code>❀Title : </code><b>{renote['text']}</b>\n\n"
                    f"<code>❀Artist : </code><b><a href=\"https://t.me/ChuangBian/\">{renote['user']['name']}</a></b>\n\n"
                    f"► <b><a href=\"https://t.me/ChuangBian/5/\">ᴍɪꜱꜱᴋᴇʏ</a></b>"
                )
            for f in renote["files"]:
                file = {
                    "type": f["type"],
                    "url": f["url"]
                }
                note.files.append(file)
        else:
            if note.cw:
                lines = n["text"].splitlines()
                lines.insert(1, "\nCW: " + note.cw + "\n\n")
                lines.insert(2, "<tg-spoiler>")
                lines.insert(len(lines) - 2, "</tg-spoiler>\n\n")
                note.text = "".join(lines)
            else:
                note.text = n["text"]

            for f in n["files"]:
                file = {
                    "type": f["type"],
                    "url": f["url"]
                }
                note.files.append(file)
        notes.append(note)
    return notes
