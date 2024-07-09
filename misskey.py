import requests
import json
from dateutil import parser
from datetime import datetime


class Note:
    createdAt: datetime
    text: str
    replyId: str
    cw: str
    files: list


def _get_raw_notes(site: str, user_id: str):
    req_body = {
        "userId": user_id,
        "limit": 10
    }
    req_header = {
        "User-Agent": "MisskeyTelegramForwarder",
        'Content-type': 'application/json',
        'Accept': '*/*'
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
        if "renote" in n:
            note = Note()
            note.replyId = n['replyId']
            note.cw = n['cw']
            renote = n['renote']
            note.createdAt = parser.parse(n["createdAt"])

 
            text = (
                f"<code>❀Title : </code><b>{renote['text']}</b>\n\n"
                f"<code>❀Artist : </code><b><a href=\"https://t.me/ChuangBian/\">{renote['user']['name']}</a></b>"
                f"► <b><a href=\"https://t.me/ChuangBian/5/\">ᴍɪꜱꜱᴋᴇʏ</a></b>"
            )
            note.text = text

            note.files = [{"type": f["type"], "url": f["url"]} for f in renote["files"]]
            notes.append(note)
        else:
            note = Note()
            note.replyId = n['replyId']
            note.cw = n['cw']
            note.createdAt = parser.parse(n["createdAt"])

            note.text = n["text"]

            note.files = [{"type": f["type"], "url": f["url"]} for f in n["files"]]
            notes.append(note)
    return notes
