function buildReviewPrompt(code) {
    return `
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
  `;
  }
  
  module.exports = { buildReviewPrompt };
  