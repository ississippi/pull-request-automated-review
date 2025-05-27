from langchain.prompts import ChatPromptTemplate

def buildCodeReviewPrompt(code):
    prompt = f"""
        You're a senior software engineer. Review the following code for:
        
        - Bugs
        - Security issues
        - Performance concerns
        - Best practices
        - Readability
        
        Respond with bullet points and helpful suggestions.
        
        \`\`\`
        ${code}
        \`\`\`
            """.strip()
    #print ("==PROMPT==\n", prompt)
    return prompt

def buildDiffReviewPrompt(code):
    prompt = f"""
        You're a senior software engineer. Review the following diff for:
        
        - Bugs
        - Security issues
        - Performance concerns
        - Best practices
        - Readability
        
        Title the review "Pull Request Code Review".
        Respond with bullet points and helpful suggestions.
        List the files in the diff and their status (added, modified, removed).
        State file line numbers for each suggested change.
        Emphasize with a green checkbox the good things and a red cross for the most important issues.
        
        \`\`\`
        ${code}
        \`\`\`
            """.strip()
    #print ("==PROMPT==\n", prompt)
    return prompt

def buildDiffReviewPromptAugmented(code, rag_context):
    prompt = f"""
        You're a senior software engineer. Review the following diff(s) for:
        
        - Bugs
        - Security issues
        - Performance concerns
        - Best practices
        - Readability
        
        Title the review "Pull Request Code Review".
        Respond with bullet points and helpful suggestions.
        List the files in the diff and their status (added, modified, removed).
        Reference the following standards where relevant and list the rules where the code is not in compliance {context}
        
        \`\`\`
        ${code}
        \`\`\`
            """.strip()
    #print ("==PROMPT==\n", prompt)
    return prompt

def buildPythonContextPrompt():
    return "What are the Python naming conventions?"


    # 2. Incorporate the retriever into a question-answering chain.
system_prompt = (
    "You are a financial assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "If the question is not clear ask follow up questions"
    "\n\n"
    "{context}"

)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)


if __name__ == "__main__":
    # Example usage
    example_code = """
    def add(a, b):
        return a + b
    """
    prompt = buildCodeReviewPrompt(example_code)

    example_diff = """
    diff --git a/ts/src/base/Exchange.ts b/ts/src/base/Exchange.ts
    index a4dc8e150b95b..5d76858ab6a11 100644
    --- a/ts/src/base/Exchange.ts
    +++ b/ts/src/base/Exchange.ts
    @@ -7226,7 +7226,12 @@ export default class Exchange {
                if (currentSince >= current) {
                    break;
                }
    -            tasks.push (this.safeDeterministicCall (method, symbol, currentSince, maxEntriesPerRequest, timeframe, params));
    +            const checkEntry = await this.safeDeterministicCall (method, symbol, currentSince, maxEntriesPerRequest, timeframe, params);
    +            if ((checkEntry.length) === (maxEntriesPerRequest - 1)) {
    +                tasks.push (this.safeDeterministicCall (method, symbol, currentSince, maxEntriesPerRequest + 1, timeframe, params));
    +            } else {
    +                tasks.push (checkEntry);
    +            }
                currentSince = this.sum (currentSince, step) - 1;
            }
            const results = await Promise.all (tasks);
    """

    prompt = buildDiffReviewPrompt(example_diff)
    #print(prompt)   
  
  