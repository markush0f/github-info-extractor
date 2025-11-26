SUMMARY_PROMPT = """
You will receive metadata and README content extracted from a GitHub project. Your task is to generate a detailed, structured, and comprehensive summary suitable for storing in a vector database for a chatbot system. The output must be in plain text only.

Important rules:
- Do not include code, commands, routes, file paths, configuration examples, or markdown syntax.
- Do not use symbols like *, -, •, #, or any markdown-style formatting.You will receive metadata and README content extracted from a GitHub project. Your task is to generate a detailed, structured, and comprehensive summary suitable for storing in a vector database for a chatbot system. The output must be in plain text only.

Important rules:
- Do not include code, commands, routes, file paths, configuration examples, or markdown syntax.
- Do not use symbols like *, -, •, #, or any markdown-style formatting.
- Do not speculate. Only describe what is present in the provided content.
- Write in a descriptive, neutral, and technical tone.
- The summary must be long, exhaustive, and information-dense.

Output format (plain text, exactly as shown, without markdown or symbols):

PROJECT SUMMARY
Purpose:
Key technologies:
Architecture:
Main features:
Developer skill insights:
Complexity level:
Additional notes:

Now generate a long and detailed summary based strictly on the following project content:

{content}

- Write in a descriptive, neutral, and technical tone.
- The summary must be long, exhaustive, and information-dense.

Output format (plain text, exactly as shown, without markdown or symbols):

PROJECT SUMMARY
Purpose:
Key technologies:
Architecture:
Main features:
Developer skill insights:
Complexity level:
Additional notes:

Now generate a long and detailed summary based strictly on the following project content:

{content}
"""