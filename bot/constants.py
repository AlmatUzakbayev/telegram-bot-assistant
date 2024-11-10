TEXT_PROMPT = """
Provide a detailed response about [topic or question]. 
Include key information, recent updates, and any relevant 
resources for further reading."""

VOICE_PROMPT = """
Listen to the provided audio. 
1. If it contains a question, provide a detailed and thorough answer, 
explaining all relevant aspects.
2. If it contains an example or problem, provide the solution or answer in a concise manner, 
focusing only on the resolution.
3. If the audio contains general information or mentions a specific topic, provide detailed and relevant information about that topic. 
Explain its significance, background, and any important facts related to it,
without just repeating the name of the topic. 
"""

IMAGE_PROMPT = """
Analyze the provided image. 
1. If it contains a question or a problem, provide a clear, step-by-step solution leading to the answer.
2. If it is a passage from a book or general content (not a question or task),
 give a brief explanation of what it is and its context or purpose.
3. If it is purely informational or contains visual elements, provide a concise summary of the main points.

Your response should adjust to the type of content detected, delivering either a solution, 
an explanation, or a summary as appropriate.
"""