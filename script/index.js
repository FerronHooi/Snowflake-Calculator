const PORT = 8000
const axios = require('axios')
const cheerio = require('cheerio')
const express = require('express')
const app = express()
const cors = require('cors')
app.use(cors())

//definieeren van op te halen URL 
const url = 'https://www.snowflake.com/pricing/'

//app.METHOD(PATH, HANDLER)

app.get('/', function (req, res) {
    res.json('test')
})

app.get('/results', (req, res) => {

    axios(url)
    .then(response =>{
        const html = response.data
        const $ = cheerio.load(html)
        const script = []

                $('[id=content]', html).each(function(){

                //scraper voor de aanwezige script. de .replace verwijdert de /n en '    
                const data = $(this).find('script').text().replace(/\n/g,'')
                //de text bevat een stuk tekst ervoor en erna die verwijdert moet worden. Dat gebeurd hier
                const subStringData = data.substring(
                    data.indexOf("($)") + 8, 
                    data.indexOf("// custom select ")
                );

                //write string to javascript file
                /*var fs = require('fs');
                fs.writeFile ("snowflakeCloudDataScript.js", subStringData, function(err) {
                    if (err) throw err;
                    console.log('complete');
                    })*/
 
                script.push({
                    
                    subStringData
                        
                })
                
                JSON.stringify(script)
                
            })
                                
        //console.log(script)
        res.json(script)

    }).catch(err => console.log(err))

})



app.listen(PORT, () => console.log('server running on port' + PORT));   


