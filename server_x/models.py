# app/models.py

from sqlalchemy import Column, BigInteger, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from database import Base

class PostsX(Base):
    __tablename__ = "posts_x"

    post_id = Column(BigInteger, primary_key=True, index=True)
    account_id = Column(UUID(as_uuid=True), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    post = Column(Text, nullable=False)

    comments = relationship("CommentsX", back_populates="post")
    likes = relationship("LikesX", back_populates="post")
    reactions = relationship("ReactionsX", back_populates="post")

    def to_dict(self):
        return {"post_id": self.post_id, "account_id": self.account_id,  "time_created": self.time_created, "post": self.post}

class CommentsX(Base):
    __tablename__ = "comments_x"

    comment_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    post_id = Column(BigInteger, ForeignKey("posts_x.post_id", name="post_id_c2"), nullable=False)
    account_id = Column(UUID(as_uuid=True), nullable=False)
    time_commented = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    text = Column(Text, nullable=False)

    post = relationship("PostsX", back_populates="comments")

class LikesX(Base):
    __tablename__ = "likes_x"

    like_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    post_id = Column(BigInteger, ForeignKey("posts_x.post_id", name="post_id_c"), nullable=False)
    account_id = Column(UUID(as_uuid=True), nullable=False)
    time_liked = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    post = relationship("PostsX", back_populates="likes")

class ReactionsX(Base):
    __tablename__ = "reactions_x"

    reaction_id = Column(BigInteger, primary_key=True, index=True, nullable=False)
    post_id = Column(BigInteger, ForeignKey("posts_x.post_id", name="post_id_c3"), nullable=False)
    account_id = Column(UUID(as_uuid=True), nullable=False)
    time_reaction = Column(DateTime(timezone=True),server_default=func.now(), nullable=False)
    reaction_text = Column(Text, nullable=False)

    post = relationship("PostsX", back_populates="reactions")

