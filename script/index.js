const axios = require('axios')
const cheerio = require('cheerio')

//definieeren van op te halen URL 
const url = 'https://www.snowflake.com/pricing/'

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
                                
            })
                                
        console.log(script)

    }).catch(err => console.log(err))  

//TODO: IF SCRAPER RETURNS ERROR, DO NOT OVERWRITE snowflakeCloudDataScript.js


