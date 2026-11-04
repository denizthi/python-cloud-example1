# interactions.py

import uuid
from dataclasses import dataclass
from database import SessionLocal
from models import PostsX, LikesX, CommentsX, ReactionsX

@dataclass
class CreatePost:
    account_id: uuid.UUID | None = None
    post: str | None = None
    error_message: str | None = None

    def has_error(self) -> bool:
        if self.error_message:
            return True
        return False
    
@dataclass
class CreateLike:
    post_id: int | None = None
    account_id: uuid.UUID | None = None
    synced_from: str | None = None
    error_message: str | None = None

    def has_error(self) -> bool:
        if self.error_message:
            return True
        return False

@dataclass
class CreateComment:
    post_id: int | None = None
    account_id: uuid.UUID | None = None
    text: str | None = None
    synced_from: str | None = None
    error_message: str | None = None

    def has_error(self) -> bool:
        if self.error_message:
            return True
        return False

@dataclass
class CreateRxn:
    post_id: int | None = None
    account_id: uuid.UUID | None = None
    reaction_text: str | None = None
    synced_from: str | None = None
    error_message: str | None = None

    def has_error(self) -> bool:
        if self.error_message:
            return True
        return False

def create_post(account_id: str, post: str) -> CreatePost:
    if not account_id:
        return CreatePost(error_message="Specify account_id")
    if not post:
        return CreatePost(error_message="No post typed")

    db = SessionLocal()

    try:
        new_post = PostsX(account_id=account_id, post=post)
        db.add(new_post)
        db.commit()
    except:
        return CreatePost(error_message="Invalid input")
    
    return CreatePost(account_id=account_id, post=post)

def like_post(post_id: str, account_id: str, synced_from: str | None = None) -> CreateLike:
    if not post_id:
        return CreateLike(error_message="Specify post_id")
    if not account_id:
        return CreateLike(error_message="Specify account_id")
    if not synced_from:
        synced_from = "server_x"

    db = SessionLocal()
    if not db.query(PostsX).filter_by(post_id=post_id).first():
        return CreateLike(error_message="Post does not exist")
    
    try:
        new_like = LikesX(post_id=post_id, account_id=account_id, synced_from=synced_from)
        db.add(new_like)
        db.commit()
    except:
        return CreateLike(error_message="Invalid input")

    return CreateLike(post_id=post_id, account_id=account_id, synced_from=synced_from)

def comment_post(post_id: str, account_id: str, text: str, synced_from: str | None = None) -> CreateComment:
    if not post_id:
        return CreateComment(error_message="Specify post_id")
    if not account_id:
        return CreateComment(error_message="Specify account_id")
    if not text:
        return CreateComment(error_message="No comment typed")
    if not synced_from:
        synced_from = "server_x"

    db = SessionLocal()
    if not db.query(PostsX).filter_by(post_id=post_id).first():
        return CreateLike(error_message="Post does not exist")

    try:
        new_comment = CommentsX(post_id=post_id, account_id=account_id, text=text, synced_from=synced_from)
        db.add(new_comment)
        db.commit()
    except:
        return CreateLike(error_message="Invalid input")
    
    return CreateComment(post_id=post_id, account_id=account_id, text=text, synced_from=synced_from)

def react_post(post_id: str, account_id: str, reaction_text: str, synced_from: str | None = None) -> CreateRxn:
    if not post_id:
        return CreateRxn(error_message="Specify post_id")
    if not account_id:
        return CreateRxn(error_message="Specify account_id")
    if not reaction_text:
        return CreateRxn(error_message="No reaction given")
    if not synced_from:
        synced_from = "server_x"
        
    db = SessionLocal()
    if not db.query(PostsX).filter_by(post_id=post_id).first():
        return CreateRxn(error_message="Post does not exist")

    try:
        new_rxn = ReactionsX(post_id=post_id, account_id=account_id, reaction_text=reaction_text, synced_from=synced_from)
        db.add(new_rxn)
        db.commit()
    except:
        return CreateLike(error_message="Invalid input")
    
    return CreateRxn(post_id=post_id, account_id=account_id, reaction_text=reaction_text, synced_from=synced_from)