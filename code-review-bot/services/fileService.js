const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '..\\data\\python-snippets.json');
jsonData = {};
function getCodeSnippet() {
    // "snippets": [
    //    "id"
    //    "snippet"
    //    "language"
    //    "repo_file_name"
    // ]  
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                console.error('Error reading JSON file:', err);
                reject(err);
                return;
            }
            try {
                console.log('Parse JSON data.');
                const jsonData = JSON.parse(data);
                console.log('JSON data parsed.');
                const resultData = jsonData.snippets[6].snippet;
                resolve(resultData);
            } catch (parseErr) {
                console.error('Error parsing JSON:', parseErr);
                reject(parseErr);
            }
        });
    });  
 
    
    // Access and traverse the array
    //count = 0;
    //for (const snippet of jsonData.snippets) {
    //    count++;
    //    if (count >= 10) {
    //      break;
    //    }
    //    console.log(`\n===${count}===\n` + snippet.snippet);
    //  }
      
}

getCodeSnippet()
    .then((resultData) => {
        console.log('Snippet:', resultData);
    })
    .catch((error) => {
        console.error('Error:', error);
    });