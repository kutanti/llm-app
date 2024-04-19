from fastapi import FastAPI
from langchain_openai.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain
from src.config import Config
from pydantic import BaseModel

app = FastAPI()

envConfig = Config()

class CuisineRequest(BaseModel):
    genre: str

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/suggest_movie")
def suggest_resturant(request: CuisineRequest):
    
    model = AzureChatOpenAI(
    api_key=envConfig.openai_api_key,
    api_version=envConfig.openai_api_version,
    azure_endpoint=envConfig.openai_api_base_url,
    azure_deployment="gpt-turbo"
    )

    prompt_movie_name = PromptTemplate(
    input_variables=['Genre'],
    template="I am script writter for Movies, please suggest a nice name for a {Genre} movie."
    )

    chain_movie_name = LLMChain(llm =  model, prompt = prompt_movie_name, output_key="movie_name")


    prompt_movie_story = PromptTemplate(
        input_variables=['movie_name'],
        template="I want to write the story of the movie {movie_name}, please give a story line in about 100 words."
    )

    chain_movie_story = LLMChain(llm =  model, prompt = prompt_movie_story, output_key="movie_story")

    seq_chain = SequentialChain(
        chains=[chain_movie_name, chain_movie_story],
        input_variables=['Genre'],
        output_variables=["movie_name", "movie_story"]

    )

    response = seq_chain.invoke(request.genre)

    return response