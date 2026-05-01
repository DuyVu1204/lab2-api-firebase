from fastapi import APIRouter, Depends, HTTPException
from backend.app.dependencies.auth import get_current_user
from backend.app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from backend.app.services.firestore_service import (
    create_note, get_notes, update_note, delete_note
)

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/", response_model=list[NoteResponse])
def list_notes(user=Depends(get_current_user)):
    return get_notes(user["uid"])

@router.post("/", response_model=NoteResponse)
def add_note(note: NoteCreate, user=Depends(get_current_user)):
    return create_note(user["uid"], note)

@router.put("/{note_id}", response_model=NoteResponse)
def edit_note(note_id: str, note: NoteUpdate, user=Depends(get_current_user)):
    return update_note(user["uid"], note_id, note)

@router.delete("/{note_id}")
def remove_note(note_id: str, user=Depends(get_current_user)):
    delete_note(user["uid"], note_id)
    return {"message": "Note deleted"}