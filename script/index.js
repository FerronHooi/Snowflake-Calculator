const axios = require('axios')
const cheerio = require('cheerio')

//definieeren van op te halen URL 
const url = 'https://www.snowflake.com/pricing/'

const scrapeDataFromSnowflakePricing = async () => {
    axios(url)
        .then(response => {
            const html = response.data
            const $ = cheerio.load(html)

            $('[id=content]', html).each(function () {

                //scraper voor de aanwezige script. de .replace verwijdert de /n en '    
                const data = $(this).find('script').text().replace(/\n/g, '')
                //de text bevat een stuk tekst ervoor en erna die verwijdert moet worden. Dat gebeurd hier
                const script = data.substring(
                    data.indexOf("($)") + 8,
                    data.indexOf("// custom select ")
                );
                
                console.log(script)

                //write string to javascript file
                var fs = require('fs');
                fs.writeFile ("snowflakeCloudDataScript.js", script, function(err) {
                    if (err) throw err;
                    console.log('complete');
                })            
                                
            })

        }
        ).catch(err => console.log(err))
}

scrapeDataFromSnowflakePricing()