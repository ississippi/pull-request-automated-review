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

if __name__ == "__main__":
    # Example usage
    example_code = """
    def add(a, b):
        return a + b
    """
    prompt = buildCodeReviewPrompt(example_code)
    #print(prompt)   
  
  