from crewai import Agent
from textwrap import dedent
from langchain.llms import OpenAI, Ollama
from langchain_openai import ChatOpenAI
from tools.search_tools import SearchTools
from tools.calculator import CalculatorTools

"""
Goal - create a 7 day travel itineary with detailed per-day plans
       including,budget ,packing suggestions , and safety tips 
       
Captain/manager/Boss
- Expert Travel agent

Employees/Experts to Hire:
- city selection Expert
- local tour Guide



"""


class TravelAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4 = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        self.ollama = Ollama(model="openhermes")

    def expert_travel_agent(self):
        return Agent(
            role="Expert Travel Agent",
            backstory=dedent(f"""
                              Expert in Travel planning and logistics . I have decades of experience making 
                              travel iteneraries.
                              """),
            goal=dedent(f"""
                          create a 7-day travel itineary with detailed per-day plans,
                          including,budget ,packing suggestions , and safety tips 
                          """),
            tools = [SearchTools.search_internet,CalculatorTools.calculate],
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def city_selection_expert(self):
        return Agent(
            role="City Selection Expert",
            backstory = dedent(
                f""" Expert at analyzing travel data to pick ideal destinations"""
            ),
            goal=dedent(f"""Select the best cities based on weather,season,prices, and traveller interests"""),
            tools=[SearchTools.search_internet],
            verbose=True,
            llm=self.OpenAIGPT35,
        )

    def local_tour_guide(self):
        return Agent(
            role="Local Tour Guide",
            backstory=dedent(f"""Knowledgeable local guide with extensive information about the city , it's
                                attractions and customs."""),
            goal = dedent(f"""provide the BEST insights about the selected city"""),
            tools=[SearchTools.search_internet],
            verbose=True,
            llm=self.OpenAIGPT35,
        )
