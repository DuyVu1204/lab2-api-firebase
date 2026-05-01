from datetime import datetime, timezone
from backend.app.core.firebase_config import get_firestore
from backend.app.schemas.note import NoteCreate, NoteUpdate

db = get_firestore()

def create_note(uid: str, note: NoteCreate):
    doc = {
        "title": note.title,
        "content": note.content,
        "timestamp": datetime.now(timezone.utc)
    }
    ref = db.collection("notes").document(uid).collection("user_notes").add(doc)
    doc_id = ref[1].id
    return {"id": doc_id, **doc}

def get_notes(uid: str):
    notes_ref = db.collection("notes").document(uid).collection("user_notes")
    docs = notes_ref.order_by("timestamp").stream()
    return [
        {"id": d.id, **d.to_dict()} for d in docs
    ]

def update_note(uid: str, note_id: str, note: NoteUpdate):
    note_ref = db.collection("notes").document(uid).collection("user_notes").document(note_id)
    update_data = {k: v for k, v in note.dict().items() if v is not None}
    if not update_data:
        raise ValueError("No data to update")
    note_ref.update(update_data)
    updated = note_ref.get()
    return {"id": note_id, **updated.to_dict()}

def delete_note(uid: str, note_id: str):
    note_ref = db.collection("notes").document(uid).collection("user_notes").document(note_id)
    note_ref.delete()