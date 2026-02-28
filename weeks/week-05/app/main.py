from __future__ import annotations

from typing import Optional, List
from uuid import uuid4

import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter


# ---- In-memory "DB" ----
@strawberry.type
class Review:
    id: strawberry.ID
    rating: int


@strawberry.input
class CreateReviewInput:
    rating: int


DB: List[Review] = []


@strawberry.type
class Query:
    @strawberry.field
    def reviews(self) -> list[Review]:
        return DB

    @strawberry.field
    def review(self, id: strawberry.ID) -> Optional[Review]:
        for item in DB:
            if item.id == id:
                return item
        return None


@strawberry.type
class Mutation:
    @strawberry.mutation
    def createReview(self, input: CreateReviewInput) -> Review:
        new_item = Review(
            id=strawberry.ID(str(uuid4())),
            rating=input.rating,
        )
        DB.append(new_item)
        return new_item


schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
