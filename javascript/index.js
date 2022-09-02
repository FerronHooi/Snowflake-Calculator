// const axios = require('axios')
// const cheerio = require('cheerio')

// //definieeren van op te halen URL
// const url = 'https://www.snowflake.com/pricing/'

// const scrapeDataFromSnowflakePricing = async () => {
//     axios(url)
//         .then(response => {
//             const html = response.data
//             const $ = cheerio.load(html)

//             $('[id=content]', html).each(function () {

//                 //ON DEMAND STORAGE EN CAPACITY STORAGE
//                 //scraper voor de aanwezige script. de .replace verwijdert de /n en '
//                 const data = $(this).find('script').text().replace(/\n/g, '')
//                 //de text bevat een stuk tekst ervoor en erna die verwijdert moet worden. Dat gebeurd hier
//                 const script = data.substring(
//                     data.indexOf("($)") + 8,
//                     data.indexOf("// custom select ")
//                 );
                
//                 console.log(script)

//                 // //write to javascript file
//                 // var fs = require('fs');
//                 // fs.writeFile ("snowflakeCloudDataScript.js", script, function(err) {
//                 //     if (err) throw err;
//                 //     console.log('complete');
//                 // })
             
//             //PRIJZEN PER REGIO IN EUR, GBP OF USD
//             const price = [];
//             //TODO: PRIJZEN KOMEN NOG NIET OVEREEN MET DE JUISTE REGIO BLIJKBAAR....
//             //TODO: Scrape moet ook in een loopje kunnen.. die standard door enterprise of

//             //Microsoft Azure (gebruikt wildcard, hij pakt dus alles met microsoftazure....)
//             $('[id^=microsoftazure]', html).each(function () {
//             const platform = $(this).attr('id').toString().split('-')[0];
//             const cloudregion = $(this).attr('id').toString().split('-')[1];
//             const dataStandard = {
//                 tier: $('#standard').attr('id'),
//                 price_usd: $('#standard')
//                 .find('div.pricing-price')
//                 .attr('data-price-usd'),
//                 price_eur: $('#standard')
//                 .find('div.pricing-price')
//                 .attr('data-price-eur'),
//                 price_gbp: $('#standard')
//                 .find('div.pricing-price')
//                 .attr('data-price-gbp'),
//             };
//             const dataEnterprise = {
//                 tier: $('#enterprise').attr('id'),
//                 price_usd: $('#enterprise')
//                 .find('div.pricing-price')
//                 .attr('data-price-usd'),
//                 price_eur: $('#enterprise')
//                 .find('div.pricing-price')
//                 .attr('data-price-eur'),
//                 price_gbp: $('#enterprise')
//                 .find('div.pricing-price')
//                 .attr('data-price-gbp'),
//             };
//             const dataBusinessCritical = {
//                 tier: $('#business-critical').attr('id'),
//                 price_usd: $('#business-critical')
//                 .find('div.pricing-price')
//                 .attr('data-price-usd'),
//                 price_eur: $('#business-critical')
//                 .find('div.pricing-price')
//                 .attr('data-price-eur'),
//                 price_gbp: $('#business-critical')
//                 .find('div.pricing-price')
//                 .attr('data-price-gbp'),
//             };

//                 price.push({
//                 platform,
//                 cloudregion,
//                 dataStandard,
//                 dataEnterprise,
//                 dataBusinessCritical,
//             });
//             });

//             //Amazon Web Service AWS
//             $('[id^=amazonwebservicesaws]', html).each(function () {
//             const platform = $(this).attr('id').toString().split('-')[0];
//             const cloudregion = $(this).attr('id').toString().split('-')[1];
//             const dataStandard = {
//                 tier: $('#standard').attr('id'),
//                 price_usd: $('#standard')
//                 .find('div.pricing-price')
//                 .attr('data-price-usd'),
//                 price_eur: $('#standard')
//                 .find('div.pricing-price')
//                 .attr('data-price-eur'),
//                 price_gbp: $('#standard')
//                 .find('div.pricing-price')
//                 .attr('data-price-gbp'),
//             };
//             const dataEnterprise = {
//                 tier: $('#enterprise').attr('id'),
//                 price_usd: $('#enterprise')
//                 .find('div.pricing-price')
//                 .attr('data-price-usd'),
//                 price_eur: $('#enterprise')
//                 .find('div.pricing-price')
//                 .attr('data-price-eur'),
//                 price_gbp: $('#enterprise')
//                 .find('div.pricing-price')
//                 .attr('data-price-gbp'),
//             };
//             const dataBusinessCritical = {
//                 tier: $('#business-critical').attr('id'),
//                 price_usd: $('#business-critical')
//                 .find('div.pricing-price')
//                 .attr('data-price-usd'),
//                 price_eur: $('#business-critical')
//                 .find('div.pricing-price')
//                 .attr('data-price-eur'),
//                 price_gbp: $('#business-critical')
//                 .find('div.pricing-price')
//                 .attr('data-price-gbp'),
//             };

//                 price.push({
//                 platform,
//                 cloudregion,
//                 dataStandard,
//                 dataEnterprise,
//                 dataBusinessCritical,
//             });
//             });

//             //Google Cloud Platform
//             $('[id^=googlecloudplatform]', html).each(function () {
//             const platform = $(this).attr('id').toString().split('-')[0];
//             const cloudregion = $(this).attr('id').toString().split('-')[1];
//             const dataStandard = {
//                 tier: $('#standard').attr('id'),
//                 price_usd: $('#standard')
//                 .find('div.pricing-price')
//                 .attr('data-price-usd'),
//                 price_eur: $('#standard')
//                 .find('div.pricing-price')
//                 .attr('data-price-eur'),
//                 price_gbp: $('#standard')
//                 .find('div.pricing-price')
//                 .attr('data-price-gbp'),
//             };
//             const dataEnterprise = {
//                 tier: $('#enterprise').attr('id'),
//                 price_usd: $('#enterprise')
//                 .find('div.pricing-price')
//                 .attr('data-price-usd'),
//                 price_eur: $('#enterprise')
//                 .find('div.pricing-price')
//                 .attr('data-price-eur'),
//                 price_gbp: $('#enterprise')
//                 .find('div.pricing-price')
//                 .attr('data-price-gbp'),
//             };
//             const dataBusinessCritical = {
//                 tier: $('#business-critical').attr('id'),
//                 price_usd: $('#business-critical')
//                 .find('div.pricing-price')
//                 .attr('data-price-usd'),
//                 price_eur: $('#business-critical')
//                 .find('div.pricing-price')
//                 .attr('data-price-eur'),
//                 price_gbp: $('#business-critical')
//                 .find('div.pricing-price')
//                 .attr('data-price-gbp'),
//             };

//                 price.push({
//                 platform,
//                 cloudregion,
//                 dataStandard,
//                 dataEnterprise,
//                 dataBusinessCritical,
//             });
//             });
            
//             console.log(price)
//             const jsonPricesTiers = JSON.stringify(price)
//             console.log(jsonPricesTiers)
                                
//             })

//         }
//         ).catch(err => console.log(err))
// }

// scrapeDataFromSnowflakePricing()

import myJson from '../Datafiles/example.json' assert {type: 'json'};

// 👇️ {
//   name: 'Alice',
//   country: 'Austria',
//   tasks: [ 'develop', 'design', 'test' ],
//   age: 30
// }
console.log(myJson.platform)