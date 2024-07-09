import requests
import json
from dateutil import parser
from datetime import datetime
from typing import List, Dict

class Note:
    def __init__(self, createdAt: datetime, text: str, replyId: str, cw: str, files: List[Dict[str, str]]):
        self.createdAt = createdAt
        self.text = text
        self.replyId = replyId
        self.cw = cw
        self.files = files

def _get_raw_notes(site: str, user_id: str) -> List[Dict]:
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

def get_notes(site: str, user_id: str) -> List[Note]:
    raw_notes = _get_raw_notes(site, user_id)
    notes = []
    for n in raw_notes:
        note = Note(
            createdAt=parser.parse(n["createdAt"]),
            text=n.get("text", ""),
            replyId=n.get("replyId", ""),
            cw=n.get("cw", ""),
            files=[{"type": f["type"], "url": f["url"]} for f in n.get("files", [])]
        )

        if "renote" in n:
            renote = n["renote"]
            note.text = (
                    f"<code>❀Title : </code><b>{renote['text']}</b>\n\n"
                    f"<code>❀Artist : </code><b><a href=\"https://t.me/ChuangBian/\">{renote['user']['name']}</a></b>\n\n"
                    f"► <b><a href=\"https://t.me/ChuangBian/5/\">ᴍɪꜱꜱᴋᴇʏ</a></b>"
                )
            if note.cw:
                note.text = f"<tg-spoiler>{note.text}</tg-spoiler>"
            note.files = [{"type": f["type"], "url": f["url"]} for f in renote.get("files", [])]
        else:
            if note.cw:
                note.text = f"<tg-spoiler>{note.text}</tg-spoiler>"

        notes.append(note)
    return notes
