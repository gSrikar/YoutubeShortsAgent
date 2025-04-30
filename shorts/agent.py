from google.adk.agents import LlmAgent, LoopAgent, Agent
from google.adk.tools import google_search
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from scripts.util import load_instructions_from_file

# Sub Agent to Write the Script
script_agent = Agent(
    name="script_agent",
    model="gemini-2.0-flash-001",
    description="An expert agent in writing scripts for YouTube Shorts.",
    instruction=load_instructions_from_file("scripts/script_instructions.txt"),
    tools=[google_search],
    output_key="generated_script", # The key where the generated script will be stored
)

# Sub Agent to Create Visuals
visuals_agent = LlmAgent(
    name="visuals_agent",
    model="gemini-2.0-flash-001",
    description="An expert agent in creating visuals for YouTube Shorts.",
    instruction=load_instructions_from_file("scripts/visuals_instructions.txt"),
    output_key="visual_concept", # The key where the generated visuals will be stored
)

# Sub Agent to Format and finalize the script for YouTube Shorts
format_agent = LlmAgent(
    name="format_agent",
    model="gemini-2.0-flash-001",
    description="An expert agent in formatting scripts for YouTube Shorts.",
    instruction="""Combine the script from state['generated_script'] and the visuals from state['visual_concept'] into a final script for YouTube Shorts.""",
    output_key="final_script",
)


# Primary LLM agent for creating YouTube Shorts
youtube_shorts_agent = LoopAgent(
    name="youtube_shorts_agent",
    max_iterations=3,
    sub_agents=[
        script_agent, # Writing the script
        visuals_agent, # Creating visuals
        format_agent, # Formatting the script
        # "thumbnail_agent",
        # "title_agent",
        # "description_agent",
    ],
)

# Set the root agent for the project
root_agent = youtube_shorts_agent

APP_NAME = "YouTube Shorts Creator"
USER_ID = "user_123"
SESSION_ID = "session_123"


session_service = InMemorySessionService()
session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
)
runner = Runner(
    agent=youtube_shorts_agent,
    session_service=session_service,
    app_name=APP_NAME,
)

def call_agent(query):
    # Call the agent with the query
    content = types.Content(
        role='user',
        parts=[types.Part(text=query)],
    )
    events = runner.run(
        new_message=content,
        session_id=SESSION_ID,
        user_id=USER_ID,
    )

    # Process the events
    for event in events:
        if event.is_final_response():
            # Get the final response
            final_response = event.content.parts[0].text
            # Print the final response
            print("Final Response:", final_response)
    
call_agent("Create a YouTube Short about the benefits of meditation.")