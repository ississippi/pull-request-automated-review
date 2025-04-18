const fs = require('fs');
const { reviewCode } = require('./services/codeReviewService');
const { log } = require('./utils/logger');

const codePath = './examples/sampleCode.py'; // change to any code file

async function main() {
  const code = fs.readFileSync(codePath, 'utf-8');
  log('Sending code to OpenAI for review...');
  const review = await reviewCode(code);
  log('\n--- Code Review ---\n');
  console.log(review);
}

main();
