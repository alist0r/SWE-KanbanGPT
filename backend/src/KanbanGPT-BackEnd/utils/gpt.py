import openai
from decouple import config

openai.api_key = config("OPENAI_API_KEY")

client = openai.OpenAI(api_key=openai.api_key)

def generate_task_from_prompt(prompt: str) -> dict:
    system_msg = {
        "role": "system",
        "content": ("You are an assistant that writes task titles and descriptions for a kanban project management board."
                    "Do not include the words 'Title' and 'Description' before the title and description."
                    "Do not include other words before the task title or description. just print out the title and description."
                    )
    }
    user_msg = {
        "role": "user",
        "content": f"Create a concise task title and a 1-2 sentence description based on this prompt: {prompt}"
    }

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[system_msg, user_msg],
        temperature=0.7
    )

    content = response.choices[0].message.content.strip()

    lines = content.split("\n", 1)
    title = lines[0].strip()
    description = lines[1].strip() if len(lines) > 1 else ""

    return {"title": title[:40], "description": description}

def generate_guidance_for_task(title: str, description: str) -> str:
    system_msg = {
        "role": "system",
        "content": (
            "You are an assistant helping users break down tasks in a Kanban system."
            "Provide step-by-step guidance, suggestions, and links to resources if appropriate."
        )
    }
    user_msg = {
        "role": "user",
        "content": f"Here is a task:\n\nTitle: {title}\nDescription: {description}\n\nGive advice on how to approach it."
    }

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[system_msg, user_msg],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()