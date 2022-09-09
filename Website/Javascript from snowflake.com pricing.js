<script></script>   
jQuery(document).ready(function ($) {
      var platforms = {};
      var currentPlatform = "";
      var currentRegion = "";
        var currentCurrency = "usd";
        
    platforms.amazonwebservicesaws = {};

    platforms.amazonwebservicesaws.useastnorthernvirginia = {};
    platforms.amazonwebservicesaws.useastnorthernvirginia.display_name =
      "US East (Northern Virginia)";

    platforms.amazonwebservicesaws.useastnorthernvirginia.on_demand_price_usd =
      "$40";
    platforms.amazonwebservicesaws.useastnorthernvirginia.on_demand_price_eur =
      "€33.33";
    platforms.amazonwebservicesaws.useastnorthernvirginia.on_demand_price_gbp =
      "£";
    platforms.amazonwebservicesaws.useastnorthernvirginia.on_demand_under_price =
      "per TB / per month";
    platforms.amazonwebservicesaws.useastnorthernvirginia.on_demand_cta_text =
      "Learn More";
    platforms.amazonwebservicesaws.useastnorthernvirginia.on_demand_cta_url =
      "https://www.snowflake.com/pricing-page-registration-page/?utm_cta=website-pricing-on-demand-storage-cta-pricing-guide";


      // custom select
      $("select").each(function () {
        var $this = $(this),
          numberOfOptions = $(this).children("option").length;
        $this.addClass("select-hidden");
        $this.wrap('<div class="select white"></div>');
        $this.after('<div class="select-styled white"></div>');
        var $styledSelect = $this.next("div.select-styled");
        $styledSelect.text($this.children("option").eq(0).text());
        var $list = $("<ul />", {
          class: "select-options white",
          id: $this.attr("id") + "-styled",
        }).insertAfter($styledSelect);
        for (var i = 0; i < numberOfOptions; i++) {
          $("<li />", {
            text: $this.children("option").eq(i).data("pretty"),
            "data-filter": $this.children("option").eq(i).data("filter"),
            "data-pretty": $this.children("option").eq(i).data("pretty"),
            rel: $this.children("option").eq(i).data("filter"),
          }).appendTo($list);
        }
        var $listItems = $list.children("li");
        $styledSelect.click(function (e) {
          e.stopPropagation();
          if (!$(this).parents(".filter-container").hasClass("disabled")) {
            $("div.select-styled.active")
              .not(this)
              .each(function () {
                $(this).removeClass("active").next("ul.select-options").hide();
              });
            $(this).toggleClass("active").next("ul.select-options").toggle();
          }
        });
        $listItems.click(function (e) {
          $styledSelect.text($(this).text()).removeClass("active");
          $this.val($(this).attr("rel"));
          $list.hide();
        });
        $(document).click(function () {
          $styledSelect.removeClass("active");
          $list.hide();
        });
      });
      // reset filters
      $(document).on("click", ".reset-selections", function (e) {
        currentPlatform = "";
        currentRegion = "";
        currentCurrency = "usd";

        $(".platform-filter-container .select-styled").html("Platform");
        $("#region-filter-styled").html("");
        $(".region-filter-container .select-styled").html("Region");
        $(".currency-filter-container .select-styled").html("Currency");
        $(".capacity-storage-price").fadeTo(250, 0);
        $(".on-demand-price").fadeTo(250, 0);
        $(".pricing-column").hide();
        $("#default-pricing-column").show();
        $(".region-filter-container").addClass("disabled");
        $(".currency-filter-container").addClass("disabled");
        $(".addl-pricing-box").show();
        $("#default-pricing-column .pricing-header h3").matchHeight();
        $("#default-pricing-column .pricing-details").matchHeight();
        $(".pricing-col-match").matchHeight();
      });
      // Platform filter
      $(document).on("click", "#platform-filter-styled li", function (e) {
        currentPlatform = $(this).data("filter");
        var currentPlatformPretty = $(this).data("pretty");
        // reset region dropdown
        $(".region-filter-container .select-styled").html("Region");
        $("#region-filter-styled").html("");
        $("#region-filter").html("");
        // populate region dropdown with this platform's regions
        $.each(platforms[currentPlatform], function (k, v) {
          displayRegion = v.display_name;
          $("#region-filter-styled").append(
            '<li rel="' +
              k +
              '" data-filter="' +
              k +
              '" data-platform="' +
              currentPlatform +
              '" data-pretty="' +
              displayRegion +
              '">' +
              displayRegion +
              "</li>"
          );
          $("#region-filter").append(
            '<option data-filter="' +
              k +
              '" data-platform="' +
              currentPlatform +
              '" data-pretty="' +
              displayRegion +
              '">' +
              displayRegion +
              "</option>"
          );
        });
        $(".region-filter-container").removeClass("disabled");
        // update message
        $(".filter-note").html("Please select region");
        $(".addl-pricing-box").show();
      });
      // Region filter
      $(document).on("click", "#region-filter-styled li", function (e) {
        $styledSelect = $(this).parent().siblings(".select-styled");
        $list = $(this).parent();
        e.stopPropagation();
        $styledSelect.text($(this).data("pretty"));
        $(this).val($(this).attr("rel"));
        $list.hide();
        currentPlatform = $(this).data("platform");
        currentRegion = $(this).data("filter");
        $(".pricing-column").hide();
        $("#" + currentPlatform + "-" + currentRegion).show();
        $("#" + currentPlatform + "-" + currentRegion)
          .find(".pricing-price")
          .each(function () {
            $(this).html($(this).data("price-" + currentCurrency));
          });
        $(".pricing-header h3").matchHeight();
        $(".pricing-details").matchHeight();
        $(".pricing-col-match").matchHeight();
        $(".capacity-storage-price .addl-pricing-price").html(
          platforms[currentPlatform][currentRegion][
            "capacity_storage_price_" + currentCurrency
          ]
        );
        $(".capacity-storage-price .pricing-price-desc").html(
          platforms[currentPlatform][currentRegion].capacity_storage_under_price
        );
        $(".capacity-storage-cta").html(
          platforms[currentPlatform][currentRegion].capacity_storage_cta_text
        );
        $(".capacity-storage-cta").attr(
          "href",
          platforms[currentPlatform][currentRegion].capacity_storage_cta_url
        );
        $(".capacity-storage-price").fadeTo(250, 1);
        $(".on-demand-price .addl-pricing-price").html(
          platforms[currentPlatform][currentRegion][
            "on_demand_price_" + currentCurrency
          ]
        );
        $(".on-demand-price .pricing-price-desc").html(
          platforms[currentPlatform][currentRegion].on_demand_under_price
        );
        $(".on-demand-cta").html(
          platforms[currentPlatform][currentRegion].on_demand_cta_text
        );
        $(".on-demand-cta").attr(
          "href",
          platforms[currentPlatform][currentRegion].on_demand_cta_url
        );
        $(".on-demand-price").fadeTo(250, 1);
        // update message
        $(".filter-note").html(
          '<a class="reset-selections">reset selections</a>'
        );
        $(".currency-filter-container").removeClass("disabled");
        $(".currency-filter-container .select-styled").text(
          $(
            '#currency-filter-styled li[data-filter="' + currentCurrency + '"]'
          ).data("pretty")
        );
      });
      // Currency filter
      $(document).on("click", "#currency-filter-styled li", function (e) {
        currentCurrency = $(this).data("filter");
        $("#" + currentPlatform + "-" + currentRegion)
          .find(".pricing-price")
          .each(function () {
            $(this).html($(this).data("price-" + currentCurrency));
          });
        $(".capacity-storage-price .addl-pricing-price").html(
          platforms[currentPlatform][currentRegion][
            "capacity_storage_price_" + currentCurrency
          ]
        );
        $(".on-demand-price .addl-pricing-price").html(
          platforms[currentPlatform][currentRegion][
            "on_demand_price_" + currentCurrency
          ]
        );
      });
    });
    </script>