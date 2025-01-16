from netmiko import ConnectHandler
from ntc_templates.parse import parse_output
import sqlite3
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
import json

from dotenv import load_dotenv
load_dotenv()


def get_platform_credentials(device_type):

    plat_creds_dict = {
        "cisco_ios": {
        "host": "localhost",
        "username": "admin",
        "password": "admin",
        "port": 6000,
        "device_type": "cisco_ios"
    },
    "arista_eos": {
        "host": "localhost",
        "username": "admin",
        "password": "admin",
        "port": 6001,
        "device_type": "arista_eos"
    },
    "juniper_junos": {
        "host": "localhost",
        "username": "admin",
        "password": "admin",
        "port": 6002,
        "device_type": "juniper_junos"
    }
    }

    return plat_creds_dict[device_type]


def get_device_type(device_name):
    # Create/connect to the SQLite database
    conn = sqlite3.connect('/Users/ashwjosh/AgentUniverse/ReActAgent/NetworkAutomationAgent/FakeNetwork/networkdb/devices.db')
    cursor = conn.cursor()

    # Execute the query to get device_platform based on device_name
    cursor.execute('''
    SELECT device_platform FROM device_metadata WHERE device_name = ?
    ''', (device_name,))

    # Fetch the result
    result = cursor.fetchone()

    # Check if a result is found and return it
    if result:
        return result[0]
    else:
        return None

    # Close the connection
    conn.close()

def get_command_out(user_intent=None, device_name=None):
    """Get LLDP information for cisco , juniper, arista

    Args:
        device_name (str): device_name_string
    """
    device_type = get_device_type(device_name)
    print(device_type)
    credentials = get_platform_credentials(device_type)
    print(credentials)
    command = get_commands_from_llm(user_intent, device_type)
    print(command)
    command_out = run_command(credentials, command)
    return command_out

def run_command(credentials, command):
    with ConnectHandler(**credentials) as conn:
        output = conn.send_command(command)
        print(output)
        if output in ["Unknown command", "% Invalid input detected at '^' marker.", "% Invalid input"]:
            return f"This command [{command}] is not implemented in FakeNOS. Please try running it yourself"
        return output

def get_commands_from_llm(command_description, device_type):
    # Let's ask LLM for commands rather than hard coding them:


    q = """Question: what is command to {command_description} for device type {device_type}." 
            Answer:< relevant command based on device type>"""
    prompt_template = ChatPromptTemplate([
        ("system", """
        Role:You are a helpful network assistant with 15+ years of experience in Network Automation for Cisco, Arista and Juniper devices.
        Prompt: Given the command in regular english language you need to get the actual network device command based on device type.
                Answer only should be the command , nothing else.
        Example:
        Question:what is command to get lldp neighbors for device type juniper_junos
        Answer: show lldp neighbors
        Rules: Only give me command as output, nothing else
        Example: 
        Question: what is command to get version for  device type juniper_junos
        Answer: show version
        Clarification: return the closed command from {{junos_commands}}"""
         ),
        ("user", q)
    ])
    
    model = ChatOpenAI(model="gpt-4o-mini")
    out = prompt_template | model | StrOutputParser()
    command = out.invoke({"command_description": command_description, 
                          "device_type": device_type})
    return command


def get_device_information(question):
    prompt_template = ChatPromptTemplate([
        ("system", """
        Role: You are an expert network automation assistant with 15+ years of experience in handling Cisco, Arista, and Juniper devices. 
        Prompt: For each user question, extract two key pieces of information: 
        1. The user's intent (what they are trying to accomplish).
        2. The device name referenced in the query.
        
        Output the extracted information as a JSON object with the following keys:
        - 'user_intent': The user's main request or command.
        - 'device_name': The device mentioned in the question.

        Example 1:
        Question: What command retrieves LLDP neighbors for device sea3_cor_agg.iad34?
        Answer: 
        {{
            "user_intent": "retrieve LLDP neighbors",
            "device_name": "sea3_cor_agg.iad34"
        }}

        Example 2: 
        Question: Show me the version information for device sea3_core01.iad34.
        Answer:
        {{
            "user_intent": "show version information",
            "device_name": "sea3_core01.iad34"
        }} 
        """),
        ("user", "Question:{question}. Answer:")
    ])
    model = ChatOpenAI(model="gpt-4o-mini")
    out = prompt_template | model | StrOutputParser()
    user_intent_and_device = json.loads(out.invoke({"question": question}))
    print(user_intent_and_device)
    return get_command_out(user_intent=user_intent_and_device['user_intent'], device_name=user_intent_and_device['device_name'])
    # device_name = 'cisco_ce_sea3.agg'
    # device_name = 'jun_border_sea3.bor'
    # device_name = 'arista_core_sea3.agg'


