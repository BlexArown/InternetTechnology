from typing import List
import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Review:
    id: int
    rating: int

REVIEWS: List[Review] = [
    Review(id=1, rating=4),
    Review(id=2, rating=5),
]

@strawberry.type
class Query:
    @strawberry.field
    def reviews(self) -> List[Review]:
        return REVIEWS

@strawberry.type
class Mutation:
    @strawberry.mutation
    def createReview(self, rating: int) -> Review:
        new_id = len(REVIEWS) + 1
        r = Review(id=new_id, rating=rating)
        REVIEWS.append(r)
        return r

schema = strawberry.Schema(query=Query, mutation=Mutation)

app = FastAPI()
app.include_router(GraphQLRouter(schema), prefix="/graphql")
