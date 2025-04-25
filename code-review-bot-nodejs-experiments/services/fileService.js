const fs = require('fs');
const path = require('path');

const filePath = path.join(__dirname, '..\\..\\test-data\\python-snippets.json');
jsonData = {};
function getRandomCodeSnippetFromFile(snippet_index_item = -1) {
    // "snippets": [
    //    "id"
    //    "snippet"
    //    "language"
    //    "repo_file_name"
    // ]  
    console.log(`snippet_index_item: ${snippet_index_item}`);
    const max_snippet_count = 200;
    return new Promise((resolve, reject) => {
        if (snippet_index_item > max_snippet_count) {
            snippet_index_item = -1;
        }
        if (snippet_index_item < 0) {
            random_index = Math.floor(Math.random() * max_snippet_count - 1);
        }
        else{
            random_index = snippet_index_item;
        }
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                console.error('Error reading JSON file:', err);
                reject(err);
                return;
            }
            try {
                const jsonData = JSON.parse(data);
                console.log(`Snippet Index: ${random_index}`);
                const resultData = jsonData.snippets[random_index].snippet;
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

getRandomCodeSnippetFromFile()
    .then((resultData) => {
        console.log('Snippet:', resultData);
    })
    .catch((error) => {
        console.error('Error:', error);
    });