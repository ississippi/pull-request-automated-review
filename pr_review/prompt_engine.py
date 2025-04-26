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
  
  