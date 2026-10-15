var MowerMath = (function () {
  function num(x) { return typeof x === "number" && isFinite(x); }
  function pos(x) { return num(x) && x > 0; }
  function r1(x) { return Math.round(x * 10) / 10; }
  function jsnum(x) { if (typeof x === "number" && isFinite(x) && x === Math.trunc(x)) return String(Math.trunc(x)); return String(x); }
  var VOLT_NORM = 0.9, OVERLAP_NORM = 0.85, LOSS_NORM = 1.15;
  function battPlan(volts, ah, claim, thirst) {
    if (!pos(volts)) return { error: "the sticker volts must be above zero" };
    if (!pos(ah)) return { error: "the amp-hours must be above zero" };
    if (!pos(claim)) return { error: "the claimed square feet must be above zero" };
    if (!pos(thirst)) return { error: "the grass thirst must be above zero" };
    var wh = volts * ah * VOLT_NORM;
    var sqft = wh / thirst * 1000;
    var ratio = sqft / claim;
    var verdict = ratio < 0.7 ? "the box mows the brochure, not your lawn"
      : ratio <= 1.0 ? "in reach on a short, dry day"
      : "the pack outmows the sticker";
    return { wh: r1(wh), sqft: r1(sqft), pct: r1(ratio * 100), verdict: verdict };
  }
  function renderBatt(r, volts, ah, claim, thirst) {
    return "The " + jsnum(volts) + "-volt, " + jsnum(ah) + " amp-hour pack honestly holds " + jsnum(r.wh)
      + " watt-hours - about " + jsnum(r.sqft) + " square feet at the " + jsnum(thirst) + "-watt-hour norm, "
      + jsnum(r.pct) + "% of the " + jsnum(claim) + " on the box: " + r.verdict + ".";
  }
  function pacePlan(deck, mph, lawn) {
    if (!pos(deck)) return { error: "the deck inches must be above zero" };
    if (!pos(mph)) return { error: "the speed must be above zero" };
    if (!pos(lawn)) return { error: "the lawn square feet must be above zero" };
    var raw = deck / 12 * mph * 88;
    var pace = raw * OVERLAP_NORM;
    var minutes = lawn / pace;
    var verdict = minutes < 25 ? "a quick lap"
      : minutes <= 45 ? "a Saturday-morning mow"
      : "a two-session lawn";
    return { pace: r1(pace), minutes: r1(minutes), verdict: verdict };
  }
  function renderPace(r, deck, mph, lawn) {
    var word = r.minutes === 1 ? " minute, " : " minutes, ";
    return "At " + jsnum(mph) + " mph with the " + jsnum(deck) + "-inch deck and the 0.85 overlap norm, the honest pace is "
      + jsnum(r.pace) + " square feet a minute - the " + jsnum(lawn) + "-square-foot lawn takes about "
      + jsnum(r.minutes) + word + r.verdict + ".";
  }
  function chargePlan(wh, watts) {
    if (!pos(wh)) return { error: "the pack watt-hours must be above zero" };
    if (!pos(watts)) return { error: "the charger watts must be above zero" };
    var hours = wh / watts * LOSS_NORM;
    var verdict = hours <= 2 ? "mow again after lunch"
      : hours <= 5 ? "back on the grass tomorrow"
      : "a weekend-only pack without a spare";
    return { hours: r1(hours), verdict: verdict };
  }
  function renderCharge(r, wh, watts) {
    var word = r.hours === 1 ? " hour" : " hours";
    return "The " + jsnum(wh) + "-watt-hour pack on the " + jsnum(watts) + "-watt charger, after the 1.15 loss norm, fills in about "
      + jsnum(r.hours) + word + " - " + r.verdict + ".";
  }
  return { battPlan: battPlan, renderBatt: renderBatt, pacePlan: pacePlan, renderPace: renderPace, chargePlan: chargePlan, renderCharge: renderCharge };
})();
if (typeof module !== "undefined" && module.exports) module.exports = MowerMath;
