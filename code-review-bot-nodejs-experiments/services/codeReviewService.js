const openai = require('../openai/client');
const { buildReviewPrompt } = require('../prompts/reviewPromptBuilder');

async function reviewCode(code) {
  const prompt = buildReviewPrompt(code);

  const response = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      { role: 'system', content: 'You are a helpful code reviewer.' },
      { role: 'user', content: prompt }
    ],
    temperature: 0.2
  });

  return response.choices[0].message.content;
}

module.exports = { reviewCode };
