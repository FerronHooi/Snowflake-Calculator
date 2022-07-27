const PORT = 8000
const axios = require('axios')
const cheerio = require('cheerio')
const express = require('express')

const app = express()

//definieeren van op te halen URL 
const url = 'https://www.snowflake.com/pricing/'

axios(url)
    .then(response =>{
        const html = response.data
        const $ = cheerio.load(html)
        const price = []
        //PRIJZEN KOMEN NOG NIET OVEREEN MET DE JUISTE REGIO BLIJKBAAR....

                //Microsoft Azure (gebruikt wildcard, hij pakt dus alles met microsoftazure....)
                $('[id^=microsoftazure]', html).each(function(){

                const cloudregion = $(this).attr('id')
                const dataStandard = { tier: $('#standard').attr('id'), priceUSD: $('#standard').find('div.pricing-price').attr('data-price-usd'), priceEUR: $('#standard').find('div.pricing-price').attr('data-price-eur'), priceGBP: $('#standard').find('div.pricing-price').attr('data-price-gbp') }
                const dataEnterprise = { tier: $('#enterprise').attr('id'), priceUSD: $('#enterprise').find('div.pricing-price').attr('data-price-usd'), priceEUR: $('#enterprise').find('div.pricing-price').attr('data-price-eur'), priceGBP: $('#enterprise').find('div.pricing-price').attr('data-price-gbp') }
                const dataBusinessCritical = { tier: $('#business-critical').attr('id'), priceUSD: $('#business-critical').find('div.pricing-price').attr('data-price-usd'), priceEUR: $('#business-critical').find('div.pricing-price').attr('data-price-eur'), priceGBP: $('#business-critical').find('div.pricing-price').attr('data-price-gbp') }

                        
                price.push({
                    
                    cloudregion,
                    dataStandard,
                    dataEnterprise,
                    dataBusinessCritical
                        
                })
                
            })

                //Amazon Web Service AWS
                $('[id^=amazonwebservicesaws]', html).each(function(){

                const cloudregion = $(this).attr('id')
                const dataStandard = { tier: $('#standard').attr('id'), priceUSD: $('#standard').find('div.pricing-price').attr('data-price-usd'), priceEUR: $('#standard').find('div.pricing-price').attr('data-price-eur'), priceGBP: $('#standard').find('div.pricing-price').attr('data-price-gbp') }
                const dataEnterprise = { tier: $('#enterprise').attr('id'), priceUSD: $('#enterprise').find('div.pricing-price').attr('data-price-usd'), priceEUR: $('#enterprise').find('div.pricing-price').attr('data-price-eur'), priceGBP: $('#enterprise').find('div.pricing-price').attr('data-price-gbp') }
                const dataBusinessCritical = { tier: $('#business-critical').attr('id'), priceUSD: $('#business-critical').find('div.pricing-price').attr('data-price-usd'), priceEUR: $('#business-critical').find('div.pricing-price').attr('data-price-eur'), priceGBP: $('#business-critical').find('div.pricing-price').attr('data-price-gbp') }

                        
                price.push({
                    
                    cloudregion,
                    dataStandard,
                    dataEnterprise,
                    dataBusinessCritical
                        
                })
                
            })

                //Google Cloud Platform
                $('[id^=googlecloudplatform]', html).each(function(){

                const cloudregion = $(this).attr('id')
                const dataStandard = { tier: $('#standard').attr('id'), priceUSD: $('#standard').find('div.pricing-price').attr('data-price-usd'), priceEUR: $('#standard').find('div.pricing-price').attr('data-price-eur'), priceGBP: $('#standard').find('div.pricing-price').attr('data-price-gbp') }
                const dataEnterprise = { tier: $('#enterprise').attr('id'), priceUSD: $('#enterprise').find('div.pricing-price').attr('data-price-usd'), priceEUR: $('#enterprise').find('div.pricing-price').attr('data-price-eur'), priceGBP: $('#enterprise').find('div.pricing-price').attr('data-price-gbp') }
                const dataBusinessCritical = { tier: $('#business-critical').attr('id'), priceUSD: $('#business-critical').find('div.pricing-price').attr('data-price-usd'), priceEUR: $('#business-critical').find('div.pricing-price').attr('data-price-eur'), priceGBP: $('#business-critical').find('div.pricing-price').attr('data-price-gbp') }
                
                // onderstaande zouden ook toegevoegd moeten worden eigenlijk alleen deze vallen niet binnen een div.. 
                const onDemandStorageCosts = { priceEuro: $('div.on-demand-price').find('div.addl-pricing-price').toString(), description: $('div.on-demand-price').find('div.pricing-price-desc').text() }
                // const dataCapacityStorage = {}
                // const virtualPrivateSnowflakeVPS = {}
                        
                price.push({
                    
                    cloudregion,
                    dataStandard,
                    dataEnterprise,
                    dataBusinessCritical,
                    onDemandStorageCosts
                    // dataCapacityStorage
                    // virtualPrivateSnowflakeVPS
                        
                })
                
            })
                                
        console.log(price)

        // //schrijft alles naar een json file !!!!VOERT DIT NOG HEEL VAAK ACHTER ELKAAR UIT..MOET OPGELOST WORDEN!!!
        // var fs = require('fs');
        // fs.writeFile ("snowflakeCloudData.json", JSON.stringify(price), function(err) {
        //     if (err) throw err;
        //     console.log('complete');
        //     })

    }).catch(err => console.log(err))

app.listen(PORT, () => console.log('server running on port' + PORT))

