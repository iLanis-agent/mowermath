import json, math

def num(x): return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)
def pos(x): return num(x) and x>0
def jround(x): return math.floor(x+0.5)
def r1(x): return jround(x*10)/10
def jsnum(x):
    if isinstance(x,float) and x==int(x): return str(int(x))
    return str(x)

VOLT_NORM=0.9; OVERLAP_NORM=0.85; LOSS_NORM=1.15

def batt_plan(volts,ah,claim,thirst):
    if not pos(volts): return {"error":"the sticker volts must be above zero"}
    if not pos(ah): return {"error":"the amp-hours must be above zero"}
    if not pos(claim): return {"error":"the claimed square feet must be above zero"}
    if not pos(thirst): return {"error":"the grass thirst must be above zero"}
    wh=volts*ah*VOLT_NORM
    sqft=wh/thirst*1000
    ratio=sqft/claim
    if ratio<0.7: verdict="the box mows the brochure, not your lawn"
    elif ratio<=1.0: verdict="in reach on a short, dry day"
    else: verdict="the pack outmows the sticker"
    return {"wh":r1(wh),"sqft":r1(sqft),"pct":r1(ratio*100),"verdict":verdict}

def render_batt(r,volts,ah,claim,thirst):
    return ("The "+jsnum(volts)+"-volt, "+jsnum(ah)+" amp-hour pack honestly holds "+jsnum(r["wh"])
            +" watt-hours - about "+jsnum(r["sqft"])+" square feet at the "+jsnum(thirst)+"-watt-hour norm, "
            +jsnum(r["pct"])+"% of the "+jsnum(claim)+" on the box: "+r["verdict"]+".")

def pace_plan(deck,mph,lawn):
    if not pos(deck): return {"error":"the deck inches must be above zero"}
    if not pos(mph): return {"error":"the speed must be above zero"}
    if not pos(lawn): return {"error":"the lawn square feet must be above zero"}
    raw=deck/12*mph*88
    pace=raw*OVERLAP_NORM
    minutes=lawn/pace
    if minutes<25: verdict="a quick lap"
    elif minutes<=45: verdict="a Saturday-morning mow"
    else: verdict="a two-session lawn"
    return {"pace":r1(pace),"minutes":r1(minutes),"verdict":verdict}

def render_pace(r,deck,mph,lawn):
    word=" minute, " if r["minutes"]==1 else " minutes, "
    return ("At "+jsnum(mph)+" mph with the "+jsnum(deck)+"-inch deck and the 0.85 overlap norm, the honest pace is "
            +jsnum(r["pace"])+" square feet a minute - the "+jsnum(lawn)+"-square-foot lawn takes about "
            +jsnum(r["minutes"])+word+r["verdict"]+".")

def charge_plan(wh,watts):
    if not pos(wh): return {"error":"the pack watt-hours must be above zero"}
    if not pos(watts): return {"error":"the charger watts must be above zero"}
    hours=wh/watts*LOSS_NORM
    if hours<=2: verdict="mow again after lunch"
    elif hours<=5: verdict="back on the grass tomorrow"
    else: verdict="a weekend-only pack without a spare"
    return {"hours":r1(hours),"verdict":verdict}

def render_charge(r,wh,watts):
    word=" hour" if r["hours"]==1 else " hours"
    return ("The "+jsnum(wh)+"-watt-hour pack on the "+jsnum(watts)+"-watt charger, after the 1.15 loss norm, fills in about "
            +jsnum(r["hours"])+word+" - "+r["verdict"]+".")

cases=[]
def add(tool,args):
    if tool=="batt": r=batt_plan(*args); fn=render_batt
    elif tool=="pace": r=pace_plan(*args); fn=render_pace
    else: r=charge_plan(*args); fn=render_charge
    case={"tool":tool,"args":args,"result":r}
    if "error" not in r: case["render"]=fn(r,*args)
    cases.append(case)

for a in [(40,4,5000,30),(56,7.5,9000,30),(40,5,5000,20),(40,4,5000,45),(80,6,12000,30),(36,3,3000,30)]:
    add("batt",a)
for a in [(21,3,6000),(20,2.5,8000),(30,4,20000),(21,3,12000),(14,2,2000),(18,2,30000)]:
    add("pace",a)
for a in [(160,60),(300,90),(120,80),(400,50),(200,100),(720,150)]:
    add("charge",a)
add("batt",[0,4,5000,30]); add("batt",[40,0,5000,30]); add("batt",[40,4,0,30]); add("batt",[40,4,5000,0])
add("pace",[0,3,6000]); add("pace",[21,0,6000]); add("pace",[21,3,0])
add("charge",[0,60]); add("charge",[160,0])

json.dump(cases,open("expected.json","w"),separators=(",",":"))
print(len(cases),"cases")
