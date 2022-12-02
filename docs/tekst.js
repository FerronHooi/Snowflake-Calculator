function makeCalculations() {
  // Als een platform, regio, valuta, aantal tb/s, button of editie wordt geselecteerd dan veranderd de rest mee. Let op: vrijwel alle code hieronder valt hier binnen.

  // Huidige geselecteerde platform
  var currentPlatform = document.getElementById("select-cloudplatform").value;

  // Hudige aantal geselecteerde TBs
  var currentStorageTBs = document.getElementById(
    "input-storage-tb-per-month"
  ).value;
  // Huidige geselecteerde regio
  var currentRegion = document.getElementById("select-region").value;

  // Past de regio aan in de tekst bij de scenario's op basis van de selectie
  document.getElementById("regio-text-scenario-1").innerHTML =
    document.getElementById("select-region").value;

  document.getElementById("regio-text-scenario-2").innerHTML =
    document.getElementById("select-region").value;

  /* CALCULATIONS */

  // Berekeningen die gebruikt worden bij 'schatting opslag & verbruikskosten'

  // Aantal dagen * Aantal uren

  var allActiveWarehouses = document.querySelectorAll(
    "[id^=warehouse-button-]"
  );

  var activeWarehouseNumbers = [];

  allActiveWarehouses.forEach((warehouse) => {
    activeWarehouseNumbers.push(warehouse.id.slice(warehouse.id.length - 1));
  });

  var totalHours = [];
  var totalCredits = [];

  activeWarehouseNumbers.forEach((number) => {
    var hours =
      (document.getElementById("number-of-days-select-" + number).value *
        document.getElementById("number-of-hours-day-select-" + number).value *
        document.getElementById("percentage-bezetting-" + number).value) /
      100;
    totalHours.push(hours);

    var credits = document.getElementById(
      "warehouse-size-number-" + number
    ).innerHTML;

    totalCredits.push(hours * Number(credits.trim()));
  });

  var calculateTotalHours = totalHours.reduce((a, b) => a + b, 0);

  var creditsTotal = totalCredits.reduce((a, b) => a + b, 0);

  // Dit is het gedeelte "X uren p/m". Hier wordt dus alleen aan calculatetotalHours de string " uren p/m" toegevoegd en wordt dan getoond in div met id "total-hours"
  document.getElementById("total-hours-1").innerHTML =
    Math.round(calculateTotalHours * 10) / 10 + " uren p/m";

  // Hierdoor wordt "X credits /uur" getoond
  //var creditsPerHourString = (document.getElementById(
  //  "total-credits-per-hour-1"
  // ).innerHTML = creditsPerHour + " Credit(s)/uur");

  // Totale uren * totale credits

  // Hierdoor wordt "X credits p/m" getoond in de div met id "total-credits"
  var creditsTotalString = (document.getElementById(
    "total-credits-1"
  ).innerHTML = Math.round(creditsTotal * 10) / 10 + " Credits p/m");

  // Hierdoor wordt "X TB p/m" getoond in de div met id "total-storage"
  //var storagetbTotal = (document.getElementById(
  //  "total-storage"
  //).innerHTML =
  //  document.getElementById("input-storage-tb-per-month").value +
  //  " tb opslag p/m");

  // !!!! SCHATTING PER EDITIE !!!!!

  // Hierdoor wordt de huidige geselecteerde cloudplatform + regio weergeven in de header van de div met id "currentregionselection"
  var currentCloudplatformAndRegion = (document.getElementById(
    "currentregionselection"
  ).innerHTML = currentPlatform + " - " + currentRegion);

  // Hierdoor worden de prijzen (per credit) weergeven van de huidige geselecteerde cloudplatform + regio (van standard, enterprise, business critical)

  // editions.forEach(function (edition) {
  //   document.getElementById("inputfield" + edition).value =
  //     platforms[currentPlatform][currentRegion]["tier"][edition][
  //       currentCurrency
  //     ];

  // END REFRESH HERE

  var standardPrice = (document.getElementById("inputfieldstandard").value =
    platforms[currentPlatform][currentRegion]["tier"]["standard"][
      currentCurrency
    ]);
  var enterprisePrice = (document.getElementById("inputfieldenterprise").value =
    platforms[currentPlatform][currentRegion]["tier"]["enterprise"][
      currentCurrency
    ]);

  var businessCritcalPrice = (document.getElementById(
    "inputfieldbusinesscritical"
  ).value =
    platforms[currentPlatform][currentRegion]["tier"]["business-critical"][
      currentCurrency
    ]);

  /* Hieronder worden de totale berekend op basis van de variabelen hierboven. Tevens wordt hier gekeken wat de geselecteerde currency is
                  en op basis daarvan wordt het juiste symbool (euro, usd of gbp) weergeven */
  if (currentCurrency == "eur") {
    var totalCostsStandard = (document.getElementById(
      "standardeditionamount"
    ).innerHTML = (
      Math.round(Number(standardPrice * creditsTotal) * 100) / 100
    ).toFixed(2));
    var totalCostsEnterprise = (document.getElementById(
      "enterpriseeditionamount"
    ).innerHTML = (
      Math.round(Number(enterprisePrice * creditsTotal) * 100) / 100
    ).toFixed(2));
    var totalCostsBusinessCritical = (document.getElementById(
      "businesscriticaleditionamount"
    ).innerHTML = (
      Math.round(Number(businessCritcalPrice * creditsTotal) * 100) / 100
    ).toFixed(2));

    elements.forEach(function (element) {
      document.getElementById("currency-sign-" + element).innerHTML = "€";
    });
  } else if (currentCurrency == "usd") {
    var totalCostsStandard = (document.getElementById(
      "standardeditionamount"
    ).innerHTML = (
      Math.round(Number(standardPrice * creditsTotal) * 100) / 100
    ).toFixed(2));
    var totalCostsEnterprise = (document.getElementById(
      "enterpriseeditionamount"
    ).innerHTML = (
      Math.round(Number(enterprisePrice * creditsTotal) * 100) / 100
    ).toFixed(2));
    var totalCostsBusinessCritical = (document.getElementById(
      "businesscriticaleditionamount"
    ).innerHTML = (
      Math.round(Number(businessCritcalPrice * creditsTotal) * 100) / 100
    ).toFixed(2));

    elements.forEach(function (element) {
      document.getElementById("currency-sign-" + element).innerHTML = "$";
    });
  } else if (currentCurrency == "gbp") {
    var totalCostsStandard = (document.getElementById(
      "standardeditionamount"
    ).innerHTML = (
      Math.round(Number(standardPrice * creditsTotal) * 100) / 100
    ).toFixed(2));
    var totalCostsEnterprise = (document.getElementById(
      "enterpriseeditionamount"
    ).innerHTML = (
      Math.round(Number(enterprisePrice * creditsTotal) * 100) / 100
    ).toFixed(2));
    var totalCostsBusinessCritical = (document.getElementById(
      "businesscriticaleditionamount"
    ).innerHTML = (
      Math.round(Number(businessCritcalPrice * creditsTotal) * 100) / 100
    ).toFixed(2));

    elements.forEach(function (element) {
      document.getElementById("currency-sign-" + element).innerHTML = "£";
    });
  } else {
    var totalCostsStandard = (document.getElementById(
      "standardeditionamount"
    ).innerHTML = (
      Math.round(Number(standardPrice * creditsTotal) * 100) / 100
    ).toFixed(2));
    var totalCostsEnterprise = (document.getElementById(
      "enterpriseeditionamount"
    ).innerHTML = (
      Math.round(Number(enterprisePrice * creditsTotal) * 100) / 100
    ).toFixed(2));
    var totalCostsBusinessCritical = (document.getElementById(
      "businesscriticaleditionamount"
    ).innerHTML = (
      Math.round(Number(businessCritcalPrice * creditsTotal) * 100) / 100
    ).toFixed(2));

    elements.forEach(function (element) {
      document.getElementById("currency-sign-" + element).innerHTML = "";
    });
  }

  // !!!! ON-DEMAND STORAGE EN CAPACITY STORAGE !!!!

  if (currentCurrency == "eur") {
    var totalOnDemandStorageCost = (document.getElementById(
      "on-demand-storage-amount"
    ).innerHTML = (
      Math.round(
        Number(
          platforms[currentPlatform][currentRegion]["on_demand_price"][
            currentCurrency
          ] * currentStorageTBs
        ) * 100
      ) / 100
    ).toFixed(2));
    var totalCapacityStorageCost = (document.getElementById(
      "capacity-storage-amount"
    ).innerHTML = (
      Math.round(
        Number(
          platforms[currentPlatform][currentRegion]["capacity_storage_price"][
            currentCurrency
          ] * currentStorageTBs
        ) * 100
      ) / 100
    ).toFixed(2));

    elements.forEach(function (element) {
      document.getElementById("currency-sign-" + element).innerHTML = "€";
    });
  } else if (currentCurrency == "usd") {
    var totalOnDemandStorageCost = (document.getElementById(
      "on-demand-storage-amount"
    ).innerHTML = (
      Math.round(
        Number(
          platforms[currentPlatform][currentRegion]["on_demand_price"][
            currentCurrency
          ] * currentStorageTBs
        ) * 100
      ) / 100
    ).toFixed(2));
    var totalCapacityStorageCost = (document.getElementById(
      "capacity-storage-amount"
    ).innerHTML = (
      Math.round(
        Number(
          platforms[currentPlatform][currentRegion]["capacity_storage_price"][
            currentCurrency
          ] * currentStorageTBs
        ) * 100
      ) / 100
    ).toFixed(2));

    elements.forEach(function (element) {
      document.getElementById("currency-sign-" + element).innerHTML = "$";
    });
  } else if (currentCurrency == "gbp") {
    var totalOnDemandStorageCost = (document.getElementById(
      "on-demand-storage-amount"
    ).innerHTML = (
      Math.round(
        Number(
          platforms[currentPlatform][currentRegion]["on_demand_price"][
            currentCurrency
          ] * currentStorageTBs
        ) * 100
      ) / 100
    ).toFixed(2));
    var totalCapacityStorageCost = (document.getElementById(
      "capacity-storage-amount"
    ).innerHTML = (
      Math.round(
        Number(
          platforms[currentPlatform][currentRegion]["capacity_storage_price"][
            currentCurrency
          ] * currentStorageTBs
        ) * 100
      ) / 100
    ).toFixed(2));

    elements.forEach(function (element) {
      document.getElementById("currency-sign-" + element).innerHTML = "£";
    });
  } else {
    var totalOnDemandStorageCost = (document.getElementById(
      "on-demand-storage-amount"
    ).innerHTML = (
      Math.round(
        Number(
          platforms[currentPlatform][currentRegion]["on_demand_price"][
            currentCurrency
          ] * currentStorageTBs
        ) * 100
      ) / 100
    ).toFixed(2));
    var totalCapacityStorageCost = (document.getElementById(
      "capacity-storage-amount"
    ).innerHTML = (
      Math.round(
        Number(
          platforms[currentPlatform][currentRegion]["capacity_storage_price"][
            currentCurrency
          ] * currentStorageTBs
        ) * 100
      ) / 100
    ).toFixed(2));

    elements.forEach(function (element) {
      document.getElementById("currency-sign-" + element).innerHTML = "";
    });
  }

  // !!!! TOTALE KOSTEN !!!!!

  // when edition is changed then show the total costs div and contact buttons
  $("#select-edition").on("change", function (e) {
    $("#totale-kosten-div, #contact-button-div").show();
  });

  // Deze hieronder worden gebruikt om "X uren p/m", "X credits p/m" en "X TB p/m" te weergeven.
  document.getElementById("total-hours-edition").innerHTML =
    Math.round(calculateTotalHours * 10) / 10 + " uren p/m";
  document.getElementById("total-credits-edition").innerHTML =
    creditsTotalString;
  document.getElementById("total-storage-edition").innerHTML =
    document.getElementById("input-storage-tb-per-month").value +
    " tb opslag p/m";

  // Hieronder wordt een variabele met daarin de geselecteerde editie gemaakt. Deze wordt vervolgens naar UPPERCASE gedaan omdat dit mooier weergeven is onder het totale bedrag

  var selectedEdition = document.getElementById("select-edition").value;
  var selectedEditionUpper = selectedEdition.toUpperCase();

  // Hieronder worden de berekeningen gedaan voor de totale kosten van de verschillende editie's (de berekening is totale kosten geselecteerde editie + geselecteerde storage type)
  var totalCostStorCreditsStandard =
    Number(document.getElementById("standardeditionamount").innerHTML) +
    Number(document.getElementById(currentSelectedStorageType).innerHTML);
  var totalCostStorCreditsEnterprise =
    Number(document.getElementById("enterpriseeditionamount").innerHTML) +
    Number(document.getElementById(currentSelectedStorageType).innerHTML);
  var totalCostStorCreditsBusinesscritical =
    Number(document.getElementById("businesscriticaleditionamount").innerHTML) +
    Number(document.getElementById(currentSelectedStorageType).innerHTML);

  // Hierdoor worden de totaal bedrag weergeven in de div met id "total-amount-selected-edition"
  if (selectedEdition == "Standard") {
    document.getElementById("total-amount-selected-edition").innerHTML = (
      Math.round(Number(totalCostStorCreditsStandard) * 100) / 100
    ).toFixed(2);
  } else if (selectedEdition == "Enterprise") {
    document.getElementById("total-amount-selected-edition").innerHTML = (
      Math.round(Number(totalCostStorCreditsEnterprise) * 100) / 100
    ).toFixed(2);
  } else if (selectedEdition == "Business Critical") {
    document.getElementById("total-amount-selected-edition").innerHTML = (
      Math.round(Number(totalCostStorCreditsBusinesscritical) * 100) / 100
    ).toFixed(2);
  } else {
  }

  // Maakt een variable aan met daarin het aantal TB's dat de gebruiker heeft ingevuld
  var currentStorageTBs = document.getElementById("input-storage-tb-per-month");

  // When the storage input field is changed calculate the total costs (on-demand and capacity) based on currently selected platform, region and currency
  $("#input-storage-tb-per-month").on("change", function (e) {
    $("#snowflake-calculator-container-storage-cost").show();

    // current input storage tbs, platform, region and currency
    var currentPlatform = document.getElementById("select-cloudplatform").value;
    var currentRegion = document.getElementById("select-region").value;
    var currentCurrency = document
      .getElementById("select-currency")
      .value.toLowerCase();
    var currentStorageTBs = document.getElementById(
      "input-storage-tb-per-month"
    ).value;

    if (currentCurrency == "eur") {
      var totalOnDemandStorageCost = (document.getElementById(
        "on-demand-storage-amount"
      ).innerHTML = (
        Math.round(
          Number(
            platforms[currentPlatform][currentRegion]["on_demand_price"][
              currentCurrency
            ] * currentStorageTBs
          ) * 100
        ) / 100
      ).toFixed(2));
      var totalCapacityStorageCost = (document.getElementById(
        "capacity-storage-amount"
      ).innerHTML = (
        Math.round(
          Number(
            platforms[currentPlatform][currentRegion]["capacity_storage_price"][
              currentCurrency
            ] * currentStorageTBs
          ) * 100
        ) / 100
      ).toFixed(2));
    } else if (currentCurrency == "usd") {
      var totalOnDemandStorageCost = (document.getElementById(
        "on-demand-storage-amount"
      ).innerHTML = (
        Math.round(
          Number(
            platforms[currentPlatform][currentRegion]["on_demand_price"][
              currentCurrency
            ] * currentStorageTBs
          ) * 100
        ) / 100
      ).toFixed(2));
      var totalCapacityStorageCost = (document.getElementById(
        "capacity-storage-amount"
      ).innerHTML = (
        Math.round(
          Number(
            platforms[currentPlatform][currentRegion]["capacity_storage_price"][
              currentCurrency
            ] * currentStorageTBs
          ) * 100
        ) / 100
      ).toFixed(2));
    } else if (currentCurrency == "gbp") {
      var totalOnDemandStorageCost = (document.getElementById(
        "on-demand-storage-amount"
      ).innerHTML = (
        Math.round(
          Number(
            platforms[currentPlatform][currentRegion]["on_demand_price"][
              currentCurrency
            ] * currentStorageTBs
          ) * 100
        ) / 100
      ).toFixed(2));
      var totalCapacityStorageCost = (document.getElementById(
        "capacity-storage-amount"
      ).innerHTML = (
        Math.round(
          Number(
            platforms[currentPlatform][currentRegion]["capacity_storage_price"][
              currentCurrency
            ] * currentStorageTBs
          ) * 100
        ) / 100
      ).toFixed(2));
    } else {
      var totalOnDemandStorageCost = (document.getElementById(
        "on-demand-storage-amount"
      ).innerHTML = (
        Math.round(
          Number(
            platforms[currentPlatform][currentRegion]["on_demand_price"][
              currentCurrency
            ] * currentStorageTBs
          ) * 100
        ) / 100
      ).toFixed(2));
      var totalCapacityStorageCost = (document.getElementById(
        "capacity-storage-amount"
      ).innerHTML = (
        Math.round(
          Number(
            platforms[currentPlatform][currentRegion]["capacity_storage_price"][
              currentCurrency
            ] * currentStorageTBs
          ) * 100
        ) / 100
      ).toFixed(2));
    }
  });

  // Hierdoor wordt "X EDITIE" weergeven in de div met id "selected-edition"
  document.getElementById("selected-edition").innerHTML =
    "(" + selectedEditionUpper + " EDITIE)";
}
