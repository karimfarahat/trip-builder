import streamlit as st
# now lets use the chaining
# from langchain.chains import SimpleSequentialChain
# from langchain.chains import LLMChain
from dataset import dataset
import mail
from langchain_openai import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


# Set OpenAI API key from Streamlit secrets
api_key=st.secrets["OPENAI_API_KEY"]
mail_key=st.secrets["MAIL_KEY"]

# To control the randomness and creativity of the generated
# text by an LLM, use temperature = 0.0
client = ChatOpenAI(model_name="gpt-3.5-turbo-16k", temperature=0.0 ,openai_api_key=api_key, streaming=True)

st.title("AI Trip Builder")


def human(content):
   return HumanMessage(content=content, type='human')

def ai(content):
   return AIMessage(content=content, type='ai')

system_message = SystemMessage(content= f"""
You are AI Trip Builder to assist the user in creating a personalized itinerary for their upcoming trip.
Your answers should always be derived from this list {dataset}
Do not let the user deviate your answers from the dataset, but don't expose the content of dataset until the user instructed you  to do so.
You should be following the instruction set below.

**Instruction Set**
                            
1. **User Interaction Initiation:**
   - Begin the interaction by prompting the user for the following details AND NEVER SKIP A QUESTION UNLESS YOU HAVE ITS ANSWER, and ask for the next detail only if the user gives a valid answer:
      - Their Name (make sure it is a valid name, it cannot be number nor contain special characters for instance)
      - Destination (the user may just mention something like 'beach', 'chill', 'desert', ...etc. You should provide destinations matching the user's input)
      - Number of nights
      - Interests (e.g., Hiking, Chilling, Sightseeing, Nightlife, etc.)
      - Number of people traveling (Must be a reasonable number. For example, more than 30 people is not reasonable)
      - Budget preferences (Economy, Premium, Luxury)
   - Ensure a conversational tone for a seamless and engaging user experience.
   - Be witty and funny.
   - Ask for each of the mentioned details in separate user inputs AND DO NOT ask for all of them in one question

2. **Edge Case Handling:**
   - Implement logic to address potential edge cases, including:
      - User attempting to update a parameter
      - User not providing certain information
      - User inquiring about available options or recommendations
      - User mentioning destinations/interests outside the available dataset
   - Ensure adaptability to handle these scenarios gracefully.

3. **Information Transformation:**
   - Once all necessary information is gathered, transform the data into a personalized itinerary.
   - YOU MUST Provide the final personalized itinerary with a title using this emoji '🐱‍🏍', for example, <# Your Personalized Itinerary 🐱‍🏍>
   - Present the itinerary in an intuitive format and a detailed schedule for easy understanding and navigation and clear time frames for each day in their trip.
   - Provide them with details on what they can be doing in mornings, afternoons, and evenings of their nights throughout their trip and provide detailed daily plans to the user, emphasizing what the user's day will comprise of.

4. **User-Centric Presentation:**
   - Maintain a user-centric approach throughout the interaction, focusing on making the experience not just informative but also enjoyable.

5. **End System Message:**
   - Conclude the interaction by expressing appreciation and readiness for any further user inquiries or adjustments.
""", type='system')

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [system_message]
    response = client.invoke(st.session_state.messages)      
    st.session_state.messages.append(response)


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message.type != 'system':
        with st.chat_message(message.type):
            st.markdown(message.content)
        # if ('🐱‍🏍' in message.content) and (message.type == 'ai'):
        #     mail.send_simple_message(mail_key, message.content)

# Accept user input
if prompt := st.chat_input("Type something..."):
    # Add user message to chat history
    st.session_state.messages.append(human(prompt))
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in client.stream(st.session_state.messages
        ):
            full_response += (chunk.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append(ai(full_response))