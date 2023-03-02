// ████████████████████████████▀████████████████
// █▄─▄─▀███▄─▄█─▄▄─█▄─▄▄▀█─▄▄▄▄█▄─██─▄█▄─▀█▀─▄█
// ██─▄─▀█─▄█─██─██─██─▄─▄█─██▄─██─██─███─█▄█─██
// ▀▄▄▄▄▀▀▄▄▄▀▀▀▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▀▄▄▄▄▀▀▄▄▄▀▄▄▄▀
 
//@version=5

// @description Patterns is a Japanese candlestick pattern recognition Library for developers. Functions here within detect viable setups in a variety of popular patterns. Please note some patterns are without filters such as comparisons to average candle sizing, or trend detection to allow the author more freedom. 

library("BjCandlePatterns", overlay=true)

// ================================== //
// ------> Candle Measurements <----- //
// ================================== //

topWickSize         = math.abs  (math.max( close, open) - high)
bottomWickSize      = math.abs  (math.min( close, open) - low)
bodySize            = math.abs           ( close -open)
bodyHigh            = math.max           ( close, open)
bodyLow             = math.min           ( close, open)
candleSize          = math.abs           ( high  -low)
bodyAvg             = ta.ema             ( bodySize, 14)
tallBody            = bodySize           > bodyAvg
shortBody           = bodySize           < bodyAvg
bodyPcnt            = bodySize           / candleSize * 100
topShadow           = topWickSize        > 5 / 100 * bodySize
bottomShadow        = bottomWickSize     > 5 / 100 * bodySize
middleBody          = bodySize           / 2 + bodyLow
bodyUpGap           = bodyHigh[1]        < bodyLow
bodyDwnGap          = bodyHigh           < bodyLow[1]
upGap               = low    > high[1]
dwnGap              = low[1] > high
bodyIsDoji          = bodyPcnt <= 5
upCandle            = close > open
dwnCandle           = close < open

// ================================== //
// ---> Functional Declarations <---- //
// ================================== //

// @function            Detects "Doji" candle patterns
// @param dojiSize      (float) The relationship of body to candle size (ie. body is 5% of total candle size). Default is 5.0 (5%)
// @param dojiWickSize  (float) Maximum wick size comparative to the opposite wick. (eg. 2 = bottom wick must be less than or equal to 2x the top wick). Default is 2
// @returns             (series bool) True when pattern detected
export doji(float dojiSize = 5.0, float dojiWickSize = 2.0) =>
	calcDoji        = topWickSize <= bottomWickSize * dojiWickSize and bottomWickSize <= topWickSize * dojiWickSize
    result          = bodyPcnt <= dojiSize and calcDoji
 
// @function            Produces "Doji" identifier label 
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export dLab(bool showLabel = false, color labelColor = color.gray, color textColor = color.white) =>
    if showLabel
        var dojiTip = "Doji\nTransitional candle signifying equality or indecision with a small or non-existent real body as the session closes at or near its open"
        label.new(bar_index, na, text="D", yloc = yloc.belowbar, color = labelColor,  style = label.style_label_up, textcolor = textColor, tooltip = dojiTip)

// @function            Detects "Bullish Engulfing" candle patterns
// @param maxRejectWick (float) Maximum rejection wick size. 
//                      The maximum wick size as a percentge of body size allowable for a top wick on the resolution candle of the pattern. 0.0 disables the filter.
//                      eg. 50 allows a top wick half the size of the body. Default is 0% (Disables wick detection).
// @param mustEngulfWick (bool) input to only detect setups that close above the high prior effectively engulfing the candle in its entirety. Default is false
// @returns             (series bool) True when pattern detected 
export bullEngulf(float maxRejectWick = 0.0, bool mustEngulfWick = false) =>
    rejectionRule   = maxRejectWick == 0.0 or topWickSize / bodySize < (maxRejectWick / 100)
    result          = close[1] <= open[1] and close >= open[1] and open <= close[1] and rejectionRule and (not mustEngulfWick or close >= high[1]) and bodySize > 0

// @function            Produces "Bullish Engulfing" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export bewLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var engulfingTip = "Bullish Engulfing\nAn up candle that closes higher than the previous day's opening after opening lower than the previous day's close"
        label.new(bar_index, na, text="BE", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = engulfingTip)
    
// @function            Detects "Bearish Engulfing" candle patterns
// @param maxRejectWick (float) Maximum rejection wick size. 
//                      The maximum wick size as a percentge of body size allowable for a bottom wick on the resolution candle of the pattern.  0.0 disables the filter.
//                      eg. 50 allows a botom wick half the size of the body. Default is 0% (Disables wick detection).
// @param mustEngulfWick (bool) Input to only detect setups that close below the low prior effectively engulfing the candle in its entirety. Default is false
// @returns             (series bool) True when pattern detected 
export bearEngulf(float maxRejectWick = 0.0, bool mustEngulfWick = false) =>
    rejectionRule   = maxRejectWick == 0.0 or bottomWickSize / bodySize < (maxRejectWick / 100)
	result          = close[1] >= open[1] and close <= open[1] and open >= close[1] and rejectionRule and (not mustEngulfWick or close <= low[1]) and bodySize > 0

// @function            Produces "Bearish Engulfing" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export bebLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var EngulfingTip = "Bearish Engulfing\nA down candle that closes lower than the previous day's opening after opening higher than the previous day's close"
        label.new(bar_index, na, text = "BE",  yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = EngulfingTip)
    
// @function            Detects "Hammer" candle patterns
// @param ratio         (float) The relationship of body to candle size (ie. body is 33% of total candle size). Default is 33%.
// @param shadowPercent (float) The maximum allowable top wick size as a percentage of body size. Default is 5%.
// @returns             (series bool) True when pattern detected
export hammer(float ratio = 33, float shadowPercent = 5.0) =>
	bullRatio       = (low - high) * (ratio/100) + high 
	hasShadow       = topWickSize > shadowPercent / 100 * bodySize
	result          = bodySize > 0 and bodyLow >= bullRatio and not hasShadow
    
// @function            Produces "Hammer" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export hLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var HammerTip = "Hammer\nBullish bottoming candle comprised of a long lower wick and small real body typically closing at or near the highs"
        label.new(bar_index, na, text="H",  yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = HammerTip)
    
// @function            Detects "Star" candle patterns
// @param ratio         (float) The relationship of body to candle size (ie. body is 33% of total candle size). Default is 33%.
// @param shadowPercent (float) The maximum allowable bottom wick size as a percentage of body size. Default is 5%.
// @returns             (series bool) True when pattern detected
export star(float ratio = 33, float shadowPercent = 5.0) =>
    bearRatio       = (high - low) * (ratio/100) + low 
    hasShadow       = bottomWickSize > shadowPercent / 100 * bodySize
	result          = bodySize > 0 and bodyHigh <= bearRatio and not hasShadow
	
// @function            Produces "Star" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export ssLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var StarTip = "Shooting Star\nBearish topping candle comprised of a long upper wick and small real body typically closing at or near the lows"
        label.new(bar_index, na, text = "SS", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down,  textcolor = textColor, tooltip = StarTip)

// @function            Detects "Dragonfly Doji" candle patterns
// @returns             (series bool) True when pattern detected 
export dragonflyDoji() =>
    result          = bodyIsDoji  and topWickSize <= bodySize
    
// @function            Produces "Dragonfly Doji" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @returns             (label) A label visible at the chart level intended for the title pattern   
export ddLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var DragonflyDoji = "Dragonfly Doji\nThis bullish doji varietal is defined by an open and a close at or near the highs of the bar"
        label.new(bar_index, na, text="DD", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = DragonflyDoji)

// @function            Detects "Gravestone Doji" candle patterns
// @returns             (series bool) True when pattern detected 
export gravestoneDoji() =>
    result          = bodyIsDoji  and topWickSize <= bodySize
    
// @function            Produces "Gravestone Doji" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export gdLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var GravestoneDoji = "Gravestone Doji\nThis bearish doji varietal is defined by an open and a close at or near the lows of the bar"
        label.new(bar_index, na, text="GD", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = GravestoneDoji)

// @function            Detects "Tweezer Bottom" candle patterns
// @param               closeUpperHalf (bool) input to only detect setups that close above the mid-point of the candle prior increasing its bullish tendancy. Default is false
// @returns             (series bool) True when pattern detected 
export tweezerBottom(bool closeUpperHalf = false) =>
    upperHalf       = close > hl2[1]
    result          = (not bodyIsDoji  or (topShadow and bottomShadow)) and math.abs(low-low[1]) <= bodyAvg*0.05 and dwnCandle[1] and upCandle and tallBody[1] and (not closeUpperHalf or (closeUpperHalf and upperHalf))
    
// @function            Produces "Tweezer Bottom" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export tbLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var TweezerBottom = "Tweezer Bottom\nAn up candle following a down candle in a downtrend who's lows are nearly identical. The defence of the double bottom and a push to close green can show bulls are ready to fight back and can signal reversal"
        label.new(bar_index, na, text="TB", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = TweezerBottom)

// @function            Detects "TweezerTop" candle patterns
// @param closeLowerHalf (bool) input to only detect setups that close below the mid-point of the candle prior increasing its bearish tendancy. Default is false
// @returns             (series bool) True when pattern detected 
export tweezerTop(bool closeLowerHalf = false) =>
    lowerHalf       = close < hl2[1]
    result          = (not bodyIsDoji  or (topShadow and bottomShadow)) and math.abs(high-high[1]) <= bodyAvg*0.05 and upCandle[1] and dwnCandle and tallBody[1] and (not closeLowerHalf or (closeLowerHalf and lowerHalf))
    
// @function            Produces "TweezerTop" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export ttLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var TweezerTop = "TweezerTop\nA down candle following an up candle in a uptrend who's highs are nearly identical. The defence of the double top and a push to close red can show bears are ready to fight back and can signal reversal"
        label.new(bar_index, na, text="TT", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = TweezerTop)

// @function            Detects "Bullish Spinning Top" candle patterns
// @param wickSize      (float) input to adjust detection of the size of the top wick/ bottom wick as a percent of total candle size. Default is 34%, which ensures the wicks are both larger than the body. 
// @returns             (series bool) True when pattern detected 
export spinningTopBull(float wickSize = 34) =>
    result          = bottomWickSize >= candleSize / 100 * wickSize and topWickSize >= candleSize / 100 * wickSize and upCandle and not bodyIsDoji 
    
// @function            Produces "Bullish Spinning Top" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export stwLab(bool showLabel = false, color labelColor = color.gray, color textColor = color.white) =>
    if showLabel
        var SpinningTop = "Bullish Spinning Top\nAn up candle defined by a short body surrounded by long wicks of approximately the same length as one another with each wick greater than the size of the body. Typical sign of indecision and possible reversal when observed at the swing low, or continuation sign if price breaks beyond the swing point"
        label.new(bar_index, na, text="STW", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = SpinningTop)

// @function            Detects "Bearish Spinning Top" candle patterns
// @param wickSize      (float) input to adjust detection of the size of the top wick/ bottom wick as a percent of total candle size. Default is 34%, which ensures the wicks are both larger than the body. 
// @returns             (series bool) True when pattern detected 
export spinningTopBear(float wickSize = 34) =>
    result          = bottomWickSize >= candleSize / 100 * wickSize and topWickSize >= candleSize / 100 * wickSize and dwnCandle and not bodyIsDoji 

// @function            Produces "Bearish Spinning Top" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export stbLab(bool showLabel = false, color labelColor = color.gray, color textColor = color.white) =>
    if showLabel
        var SpinningTop = "Bearish Spinning Top\nA down candle defined by a short body surrounded by long wicks of approximately the same length as one another with each wick greater than the size of the body. Typical sign of indecision and possible reversal when observed at the swing high, or continuation sign if price breaks beyond the swing point"
        label.new(bar_index, na, text="STB", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = SpinningTop)

// @function            Detects "Spinning Top" candle patterns
// @param wickSize      (float) input to adjust detection of the size of the top wick/ bottom wick as a percent of total candle size. Default is 34%, which ensures the wicks are both larger than the body. 
// @returns             (series bool) True when pattern detected 
export spinningTop(float wickSize = 34) =>
    result          = bottomWickSize >= candleSize / 100 * wickSize and topWickSize >= candleSize / 100 * wickSize and not bodyIsDoji 

// @function            Produces "Spinning Top" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export stLab(bool showLabel = false, color labelColor = color.gray, color textColor = color.white) =>
    if showLabel
        var SpinningTop = "Spinning Top\nA candle defined by a short body surrounded by long wicks of approximately the same length as one another with each wick greater than the size of the body. Typical sign of indecision and possible reversal when observed at the swing high/low, or continuation sign if price breaks above/below the candle low"
        label.new(bar_index, na, text="ST", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = SpinningTop)

// @function            Detects "Bullish Morning Star" candle patterns
// @returns             (series bool) True when pattern detected 
export morningStar() =>
    result          = tallBody[2] and shortBody[1] and tallBody and dwnCandle[2] and bodyDwnGap[1] and upCandle and bodyHigh >= middleBody[2] and bodyHigh < bodyHigh[2] and bodyUpGap
    
// @function            Produces "Bullish Morning Star" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export msLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var MorningStar = "Bullish Morning Star\nThe morning star is a 3 bar bullish candlestick pattern that is formed during a downward trend. A small indecsion candle separates a first decisive down move, ending with a strong move in the opposite direction signaling possible reversal"
        label.new(bar_index, na, text="MS", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = MorningStar)

// @function            Detects "Bearish Evening Star" candle patterns
// @returns             (series bool) True when pattern detected 
export eveningStar() =>
    result          = tallBody[2] and shortBody[1] and tallBody and upCandle[2] and bodyUpGap[1] and dwnCandle and bodyLow <= middleBody[2] and bodyLow > bodyLow[2] and bodyDwnGap
    
// @function            Produces "Bearish Evening Star" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export esLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var EveningStar = "Bearish Evening Star\nThe evening star is a 3 bar bullish candlestick pattern that is formed during an upward trend. A small indecsion candle separates a first decisive up move, ending with a strong move in the opposite direction signaling possible reversal"
        label.new(bar_index, na, text="ES", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = EveningStar)

// @function            Detects "Bullish Harami" candle patterns
// @returns             (series bool) True when pattern detected 
export haramiBull() =>
    result          = tallBody[1] and dwnCandle[1] and upCandle and shortBody and high <= bodyHigh[1] and low >= bodyLow[1]
    
// @function            Produces "Bullish Harami" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export hwLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var HaramiBull = "Bullish Harami\nThis 2 bar bullish pattern consists of a small-bodied green candle that is entirely encompassed within the body of what was once a red-bodied candle."
        label.new(bar_index, na, text="HW", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = HaramiBull)
// @function            Detects "Bearish Harami" candle patterns
// @returns             (series bool) True when pattern detected 
export haramiBear() =>
    result          =  tallBody[1] and upCandle[1] and dwnCandle and shortBody and high <= bodyHigh[1] and low >= bodyLow[1]
    
// @function            Produces "Bearish Harami" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export hbLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var HaramiBear = "Bearish Harami\nThis 2 bar bearish pattern consists of a small-bodied red candle that is entirely encompassed within the body of what was once a green-bodied candle."
        label.new(bar_index, na, text="HB", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = HaramiBear)

// @function            Detects "Bullish Harami Cross" candle patterns
// @returns             (series bool) True when pattern detected 
export haramiBullCross() =>
    result          = tallBody[1] and dwnCandle[1] and bodyIsDoji  and high <= bodyHigh[1] and low >= bodyLow[1]

// @function            Produces "Bullish Harami Cross" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export hcwLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var HaramiBullCross = "Bullish Harami Cross\nFound during a downtrend, this Harami variation consists of a Doji candle that is entirely encompassed within the body of what was once a red-bodied candle, signaling possible reversal"
        label.new(bar_index, na, text="HC", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = HaramiBullCross)

// @function            Detects "Bearish Harami Cross" candle patterns
// @returns             (series bool) True when pattern detected 
export haramiBearCross() =>
    result          =  tallBody[1] and upCandle[1] and bodyIsDoji  and high <= bodyHigh[1] and low >= bodyLow[1]
    
// @function            Produces "Bearish Harami Cross" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @returns             (label) A label visible at the chart level intended for the title pattern   
export hcbLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var HaramiBearCross = "Bearish Harami Cross\nFound during an uptrend, this Harami variation consists of a Doji candle that is entirely encompassed within the body of what was once a green-bodied candle, signaling possible reversal"
        label.new(bar_index, na, text="HC", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = HaramiBearCross)

// @function            Detects "Bullish Marubozu" candle patterns
// @returns             (series bool) True when pattern detected 
export marubullzu() =>
    result          = upCandle and tallBody and  5 > topWickSize/ bodySize * 100 and 5 > bottomWickSize/ bodySize * 100 

// @function            Produces "Bullish Marubozu" identifier label
// @param               showLabel (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export mwLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var Marubullzu = "Bullish Marubozu\nA bullish candlestick that does not have a shadow that extends from its candle body at either the open or the close"
        label.new(bar_index, na, text="MW", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = Marubullzu)

// @function            Detects "Bearish Marubozu" candle patterns
// @returns             (series bool) True when pattern detected 
export marubearzu() =>
    result          = dwnCandle and tallBody and  5 > topWickSize/ bodySize * 100 and 5 > bottomWickSize/ bodySize * 100 
    
// @function            Produces "Bearish Marubozu" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export mbLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var Marubearzu = "Bearish Marubozu\nA bearish candlestick that does not have a shadow that extends from its candle body at either the open or the close"
        label.new(bar_index, na, text="MB", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = Marubearzu)

// @function            Detects "Bullish Abandoned Baby" candle patterns
// @returns             (series bool) True when pattern detected 
export abandonedBull() =>
    result          = dwnCandle[2] and bodyIsDoji [1] and dwnGap[1] and upCandle and upGap
    
// @function            Produces "Bullish Abandoned Baby" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export abwLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var AbandonedBull = "Bullish Abandoned Baby\nA bullish reversal pattern where first is a large down candle, followed by a doji candle that gaps below the first candle. The next candle opens higher than the doji and moves aggressively to the upside."
        label.new(bar_index, na, text="AB", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = AbandonedBull)

// @function            Detects "Bearish Abandoned Baby" candle patterns
// @returns             (series bool) True when pattern detected 
export abandonedBear() =>
    result          = upCandle[2] and bodyIsDoji [1] and upGap[1] and dwnCandle and dwnGap 

// @function            Produces "Bearish Abandoned Baby" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export abbLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var AbandonedBear = "Bearish Abandoned Baby\nA bearish reversal pattern where first is a large up candle, followed by a doji candle that gaps above the first candle. The next candle opens lower than the doji and moves aggressively to the downside."
        label.new(bar_index, na, text="AB", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = AbandonedBear)

// @function            Detects "Piercing" candle patterns
// @returns             (series bool) True when pattern detected 
export piercing() =>
    result          = dwnCandle[1] and tallBody[1] and upCandle and open <= low[1] and close > middleBody[1] and close < open[1]

// @function            Produces "Piercing" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export pLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var Piercing = "Piercing\nA two-candle bullish reversal candlestick pattern found in a downtrend. The first candle is red and has a larger than average body. The second candle is green and opens below the low of the prior candle, creating a gap, and then closes above the midpoint of the first candle."
        label.new(bar_index, na, text="P", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = Piercing)

// @function            Detects "Dark Cloud Cover" candle patterns
// @returns             (series bool) True when pattern detected 
export darkCloudCover() =>
    result          = upCandle[1] and tallBody[1] and dwnCandle and open >= high[1] and close < middleBody[1] and close > open[1]

// @function            Produces "Dark Cloud Cover" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export dccLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var DarkCloudCover = "Dark Cloud Cover\nA two-candle bearish reversal candlestick pattern found in an uptrend. The first candle is green and has a larger than average body. The second candle is red and opens above the high of the prior candle, creating a gap, and then closes below the midpoint of the first candle."
        label.new(bar_index, na, text="DCC", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = DarkCloudCover)

// @function            Detects "Upside Tasuki Gap" candle patterns
// @returns             (series bool) True when pattern detected 
export tasukiBull() =>
    result          =  tallBody[2] and shortBody[1] and upCandle[2] and bodyUpGap[1] and upCandle[1] and dwnCandle and bodyLow >= bodyHigh[2] and bodyLow <= bodyLow[1]

// @function            Produces "Upside Tasuki Gap" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export utgLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var TasukiBull = "Upside Tasuki Gap\nA three-candle pattern found in an uptrend that usually hints at the continuation of the uptrend. The first candle is long and green, followed by a smaller green candle with its opening price that gaps above the body of the previous candle. The third candle is red and it closes inside the gap created by the first two candles, unable to close it fully."
        label.new(bar_index, na, text="UTG", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = TasukiBull)

// @function            Detects "Downside Tasuki Gap" candle patterns
// @returns             (series bool) True when pattern detected 
export tasukiBear() =>
    result          = tallBody[2] and shortBody[1] and dwnCandle[2] and bodyDwnGap[1] and dwnCandle[1] and upCandle and bodyHigh <= bodyLow[2] and bodyHigh >= bodyHigh[1]

// @function            Produces "Downside Tasuki Gap" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export dtgLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var TasukiBear = "Downside Tasuki Gap\nA three-candle pattern found in a downtrend that usually hints at the continuation of the downtrend. The first candle is long and red, followed by a smaller red candle with its opening price that gaps below the body of the previous candle. The third candle is green and it closes inside the gap created by the first two candles, unable to close it fully."
        label.new(bar_index, na, text="DTG", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = TasukiBear)

// @function            Detects "Rising Three Methods" candle patterns
// @returns             (series bool) True when pattern detected 
export risingThree() =>
    result          = tallBody[4]       and upCandle[4]      and shortBody[3]           and dwnCandle[3]     and open[3]<high[4] and close[3]>low[4] and 
                      shortBody[2]      and dwnCandle[2]     and open[2]<high[4]        and close[2]>low[4]  and shortBody[1]    and dwnCandle[1]    and 
                      open[1]<high[4]   and close[1]>low[4]  and tallBody and upCandle  and close>close[4]

// @function            Produces "Rising Three Methods" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export rtmLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var RisingThree = "Rising Three Methods\nA five-candle bullish pattern that signifies a continuation of an existing uptrend. The first candle is long and green, followed by three short red candles with bodies inside the range of the first candle. The last candle is also green and long and it closes above the close of the first candle."
        label.new(bar_index, na, text="RTM", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = RisingThree)

// @function            Detects "Falling Three Methods" candle patterns
// @returns             (series bool) True when pattern detected 
export fallingThree() =>
    result          = tallBody[4]       and dwnCandle[4]      and shortBody[3]           and upCandle[3]       and open[3]>low[4] and close[3]<high[4] and 
                      shortBody[2]      and upCandle[2]       and open[2]>low[4]         and close[2]<high[4]  and shortBody[1]   and upCandle[1]      and 
                      open[1]>low[4]    and close[1]<high[4]  and tallBody and dwnCandle and close<close[4]

// @function            Produces "Falling Three Methods" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export ftmLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var FallingThree = "FallingThree\nA five-candle bearish pattern that signifies a continuation of an existing downtrend. The first candle is long and red, followed by three short green candles with bodies inside the range of the first candle. The last candle is also red and long and it closes below the close of the first candle."
        label.new(bar_index, na, text="FTM", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = FallingThree)

// @function            Detects "Rising Window" candle patterns
// @returns             (series bool) True when pattern detected 
export risingWindow() =>
    result          = candleSize !=0 and candleSize[1] != 0 and low > high[1]

// @function            Produces "Rising Window" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export rwLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var RisingWindow =  "Rising Window\nA two-candle bullish continuation pattern that forms during an uptrend. The most important characteristic of the pattern is a price gap between the first candle's high and the second candle's low."
        label.new(bar_index, na, text="RW", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = RisingWindow)

// @function            Detects "Falling Window" candle patterns
// @returns             (series bool) True when pattern detected 
export fallingWindow() =>
    result          = candleSize != 0 and candleSize[1] != 0 and high < low[1]

// @function            Produces "Falling Window" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export fwLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var FallingWindow ="Falling Window\nA two-candle bearish continuation pattern that forms during a downtrend. The most important characteristic of the pattern is a price gap between the first candle's low and the second candle's high."
        label.new(bar_index, na, text="FW", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = FallingWindow)

// @function            Detects "Bullish Kicking" candle patterns
// @returns             (series bool) True when pattern detected 
export kickingBull() =>
    result          = marubearzu()[1] and marubullzu() and upGap

// @function            Produces "Bullish Kicking" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export kwLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var KickingBull =  "Kicking\nThe first day candlestick is a bearish marubozu candlestick with next to no upper or lower shadow and where the price opens at the day’s high and closes at the day’s low. The second day is a bullish marubozu pattern, with next to no upper or lower shadow and where the price opens at the day’s low and closes at the day’s high"
        label.new(bar_index, na, text="K", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = KickingBull)

// @function            Detects "Bearish Kicking" candle patterns
// @returns             (series bool) True when pattern detected 
export kickingBear() =>
    result          = marubullzu()[1] and marubearzu() and dwnGap

// @function            Produces "Bearish Kicking" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export kbLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var KickingBear = "Kicking\nThe first day candlestick is a bullish marubozu candlestick with next to no upper or lower shadow and where the price opens at the day’s low and closes at the day’s high. The second day is a bearish marubozu pattern, with next to no upper or lower shadow and where the price opens at the day’s high and closes at the day’s low"
        label.new(bar_index, na, text="K", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = KickingBear)

// @function            Detects "Long Lower Shadow" candle patterns
// @param ratio         (float) A relationship of the lower wick to the overall candle size expressed as a percent. Default is 75% 
// @returns             (series bool) True when pattern detected 
export lls(float ratio = 75) =>
    result          = bottomWickSize > candleSize/100*ratio

// @function            Produces "Long Lower Shadow" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export llsLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var LLS = "Long Lower Shadow\nTo indicate seller domination of the first part of a session, candlesticks will present with long lower shadows, as well as short upper shadows, which leaves sellers underwater by candles end"
        label.new(bar_index, na, text="LLS", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = LLS)

// @function            Detects "Long Upper Shadow" candle patterns
// @param ratio         (float) A relationship of the upper wick to the overall candle size expressed as a percent. Default is 75% 
// @returns             (series bool) True when pattern detected 
export lus(float ratio = 75) =>
    result          = topWickSize > candleSize/100*ratio

// @function            Produces "Long Upper Shadow" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export lusLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var LUS = "Long Upper Shadow\nTo indicate buyer domination of the first part of a session, candlesticks will present with long upper shadows, as well as short lower shadows, which leaves buyers underwater by candles end"
        label.new(bar_index, na, text="LUS", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = LUS)

// @function            Detects "Bullish On Neck" candle patterns
// @returns             (series bool) True when pattern detected 
export bullNeck() =>
    result          = upCandle[1] and tallBody[1] and dwnCandle and open > close[1] and shortBody and candleSize !=0 and math.abs(close-high[1]) <= bodyAvg*0.05

// @function            Produces "Bullish On Neck" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export nwLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var BullNeck = "On Neck - Bullsih\nOn Neck is a two-line continuation pattern found in a uptrend. The first candle is long and green, the second candle is short and has a red body. The closing price of the second candle is close or equal to the first candle's high price. Hints at continuation of trend"
        label.new(bar_index, na, text="N", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = BullNeck)

// @function            Detects "Bearish On Neck" candle patterns
// @returns             (series bool) True when pattern detected 
export bearNeck() =>
    result          = dwnCandle[1] and tallBody[1] and upCandle and open < close[1] and shortBody and candleSize !=0 and math.abs(close-low[1]) <= bodyAvg*0.05

// @function            Produces "Bearish On Neck" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export nbLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var BearNeck = "On Neck - Bearish\nOn Neck is a two-line continuation pattern found in a downtrend. The first candle is long and red, the second candle is short and has a green body. The closing price of the second candle is close or equal to the first candle's low price. Hints at continuation of trend"
        label.new(bar_index, na, text="N", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = BearNeck)

// @function            Detects "Three White Soldiers" candle patterns
// @param wickSize      (float) Maximum allowable top wick size throughout pattern expressed as a percent of total candle height. Default is 5% 
// @returns             (series bool) True when pattern detected 
export soldiers(float wickSize = 5) =>
    wicks           = candleSize * wickSize / 100 > topWickSize
    result          = tallBody and tallBody[1] and tallBody[2]   and upCandle and upCandle[1] and upCandle[2]    and 
                      close   > close[1] and close[1] > close[2] and open < close[1]          and open > open[1] and 
                      open[1] < close[2] and open[1]  > open[2]  and wicks and wicks[1]       and wicks[2]

// @function            Produces "Three White Soldiers" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export wsLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var Soldiers = "Three White Soldiers\nThis bullish reversal pattern is made up of three long-bodied, green candles in immediate succession. Each one opens within the body before it and the close is near to the high."
        label.new(bar_index, na, text="3WS", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = Soldiers)

// @function            Detects "Three Black Crows" candle patterns
// @param               wickSize (float) Maximum allowable bottom wick size throughout pattern expressed as a percent of total candle height. Default is 5% 
// @returns             (series bool) True when pattern detected 
export crows(float wickSize = 5) =>
    wicks           = candleSize * wickSize / 100 > bottomWickSize
    result          = tallBody and tallBody[1] and tallBody[2]   and dwnCandle and dwnCandle[1] and dwnCandle[2]   and 
                      close   < close[1] and close[1] < close[2] and open > close[1]            and open < open[1] and 
                      open[1] > close[2] and open[1]  < open[2]  and wicks and wicks[1]         and wicks[2]

// @function            Produces "Three Black Crows" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export bcLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var Crows = "Three Black Crows\nThis is a bearish reversal pattern that consists of three long, red-bodied candles in immediate succession. For each of these candles, each day opens within the body of the day before and closes either at or near its low."
        label.new(bar_index, na, text="3BC", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = Crows)

// @function            Detects "Bullish Tri-Star" candle patterns
// @returns             (series bool) True when pattern detected 
export triStarBull() =>
    result          = doji() and doji()[2] and doji()[3] and bodyDwnGap[1] and bodyUpGap

// @function            Produces "Bullish Tri-Star" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export tswLab(bool showLabel = false, color labelColor = #64b5f6, color textColor = color.white) =>
    if showLabel
        var TriStarBull = "Tri-Star Bull\nA bullish TriStar pattern can form when three doji candlesticks materialize in immediate succession at the tail-end of an extended downtrend. The first doji candle marks indecision between bull and bear. The second doji gaps in the direction of the leading trend. The third changes the attitude of the market once the candlestick opens in the direction opposite to the trend."      
        label.new(bar_index, na, text="3S", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = TriStarBull)

// @function            Detects "Bearish Tri-Star" candle patterns
// @returns             (series bool) True when pattern detected 
export triStarBear() =>
    result          = doji() and doji()[2] and doji()[3] and bodyDwnGap and bodyUpGap[1]

// @function            Produces "Bearish Tri-Star" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export tsbLab(bool showLabel = false, color labelColor = #ef5350, color textColor = color.white) =>
    if showLabel
        var TriStarBear = "Tri-Star Bear\nA bearish TriStar pattern can form when three doji candlesticks materialize in immediate succession at the tail-end of an extended uptrend. The first doji candle marks indecision between bull and bear. The second doji gaps in the direction of the leading trend. The third changes the attitude of the market once the candlestick opens in the direction opposite to the trend."
        label.new(bar_index, na, text="3S", yloc = yloc.abovebar, color = labelColor, style = label.style_label_down, textcolor = textColor, tooltip = TriStarBear)

// @function            Detects "Inside Bar" candle patterns
// @returns             (series bool) True when pattern detected 
export insideBar() =>
    result          = high < high[1] and low > low[1]

// @function            Produces "Inside Bar" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export insLab(bool showLabel = false, color labelColor = color.gray, color textColor = color.white) =>
    if showLabel
        var insideBar = 'Inside Bar\nAn “inside bar” pattern is a two-bar price action trading strategy in which the inside bar is smaller and within the high to low range of the prior bar, i.e. the high is lower than the previous bar’s high, and the low is higher than the previous bar’s low.'        
        label.new(bar_index, na, text="IB", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = insideBar)

// @function            Detects "Double Inside Bar" candle patterns
// @returns             (series bool) True when pattern detected 
export doubleInside() =>
    result          = insideBar() and insideBar()[1]

// @function            Produces "Double Inside Bar" identifier label
// @param showLabel     (series bool) Shows label when input is true. Default is false
// @param labelColor    (series color) Color of the label border and arrow
// @param textColor     (series color) Text color
// @returns             (label) A label visible at the chart level intended for the title pattern   
export dinLab(bool showLabel = false, color labelColor = color.gray, color textColor = color.white) =>
    if showLabel
        var dInBar = "Double Inside Bar\nA 'Double Inside' pattern is a 3 bar pattern where 2 inside bars occur in a row. Often seen in consolidation or 'flag' patterns. The pattern typically favors continuation."       
        label.new(bar_index, na, text="DI", yloc = yloc.belowbar, color = labelColor, style = label.style_label_up, textcolor = textColor, tooltip = dInBar)

// @function            Produces a box wrapping the highs and lows over the look back.
// @param cond          (series bool) Condition under which to draw the box.
// @param barsBack      (series int) the number of bars back to begin drawing the box. 
// @param borderColor   (series color) Color of the four borders. Optional. The default is `color.gray` with a 45% transparency.
// @param bgcolor       (series color) Background color of the box. Optional. The default is `color.gray` with a 75% transparency.
// @returns             (box) A box whom's top and bottom are above and below the highest and lowest points over the lookback  
export wrap(bool cond = true, int barsBack = 1, color borderColor = #787B8665, color bgColor = #787B8625) =>
    calc    = ta.atr( 30) * 0.2
    perc    = close* 0.02  
    min     = math.min(calc, perc)
    top     = ta.highest(high, barsBack) + min
    bottom  = ta.lowest (low , barsBack) - min
    left    = bar_index - barsBack
    right   = bar_index + 1
    if cond
        box.new(left, top, right, bottom, border_color = borderColor, xloc = xloc.bar_index, bgcolor = bgColor)

// @function            Returns the top wick size of the current candle
// @returns             (series float) A value equivelent to the distance from the top of the candle body to its high
export topWick() =>
    topWickSize

// @function            Returns the bottom wick size of the current candle
// @returns             (series float) A value equivelent to the distance from the bottom of the candle body to its low
export bottomWick() =>
    bottomWickSize
    
// @function            Returns the body size of the current candle
// @returns             (series float) A value equivelent to the distance between the top and the bottom of the candle body
export body() =>
    bodySize

// @function            Returns the highest body of the current candle
// @returns             (series float) A value equivelent to the highest body, whether it is the open or the close
export highestBody() =>
    bodyHigh

// @function            Returns the lowest body of the current candle
// @returns             (series float) A value equivelent to the highest body, whether it is the open or the close
export lowestBody() =>
    bodyLow

// @function            Returns the height of the current candle
// @returns             (series float) A value equivelent to the distance between the high and the low of the candle
export barRange() =>
    candleSize

// @function            Returns the body size as a percent 
// @returns             (series float) A value equivelent to the percentage of body size to the overall candle size
export bodyPct() =>
    bodySize / candleSize * 100

// @function            Returns the price of the mid-point of the candle body
// @returns             (series float) A value equivelent to the center point of the distance bewteen the body low and the body high
export midBody() =>
    middleBody

// @function            Returns true if there is a gap up between the real body of the current candle in relation to the candle prior 
// @returns             (series bool) True if there is a gap up and no overlap in the real bodies of the current candle and the preceding candle 
export bodyupGap() =>
    bodyUpGap

// @function            Returns true if there is a gap down between the real body of the current candle in relation to the candle prior 
// @returns             (series bool) True if there is a gap down and no overlap in the real bodies of the current candle and the preceding candle 
export bodydwnGap() =>
    bodyDwnGap

// @function            Returns true if there is a gap down between the real body of the current candle in relation to the candle prior 
// @returns             (series bool) True if there is a gap down and no overlap in the real bodies of the current candle and the preceding candle 
export gapUp() =>
    upGap

// @function            Returns true if there is a gap down between the real body of the current candle in relation to the candle prior 
// @returns             (series bool) True if there is a gap down and no overlap in the real bodies of the current candle and the preceding candle 
export gapDwn() =>
    dwnGap

// @function            Returns true if the candle body is a doji
// @returns             (series bool) True if the candle body is a doji. Defined by a body that is 5% of total candle size
export dojiBody() =>
    bodyIsDoji

// ================================== //
// --------> Example Code <---------- //
// ================================== //

trendRule           =   input.string    ("Trend Rule 1", "Detect Trend Based On", options=["Trend Rule 1", "Trend Rule 2", "No detection"])

labels              =   input.bool      (true   ,   "show label"                    ,   group= "Bools")
boxes               =   input.bool      (false  ,   "show box"                      ,   group= "Bools")
ecWick              =   input.bool      (false  ,   "Engulfing Must Engulf Wick"    ,   group= "Bools"                )
closeHalf           =   input.bool      (false  ,   "Tweezer Close Over Half"       ,   group= "Bools"                )

rejectWickMax       =   input.float     (0.0    ,   "[EC] Max Reject Wick Size"     ,   group= "Candle Settings"      ,         minval=0.0,     step= 0.1)  
hammerFib           =   input.float     (33     ,   "[HS] H&S Ratio (%)"            ,   group= "Candle Settings"      ,         minval=0  ,     step= 1) 
hsShadowPerc        =   input.float     (5      ,   "[HS] H&S Max Shadow (%)"       ,   group= "Candle Settings"      ,         minval=0.1,     step= 0.01) 
dojiSize            =   input.float     (5      ,   "[DJ] Doji Size (%)"            ,   group= "Candle Settings"      ,         minval=0.1,     step= 0.1)
dojiWickSize        =   input.float     (5      ,   "[DJ] Max Doji Wick Size"       ,   group= "Candle Settings"      ,         minval=0.1,     step= 0.1)
lsRatio             =   input.float     (100    ,   "[LS] Long Shadow (%)"          ,   group= "Candle Settings"      ,         minval=0.1,     step= 1)
spinWick            =   input.float     (34     ,   "[ST] Spinning Top Wick Size"   ,   group= "Candle Settings"      ,         minval=1  ,     step= 1)
scWick              =   input.float     (5      ,   "[SC] Soldiers and Crows Wick"  ,   group= "Candle Settings"      ,         minval=1  ,     step= 1)

bullColi            =   input.color     (color.green, ""                            ,   group= "Box Color"            ,         inline= "1")
neutColi            =   input.color     (color.gray , ""                            ,   group= "Box Color"            ,         inline= "1")
bearColi            =   input.color     (color.red  , ""                            ,   group= "Box Color"            ,         inline= "1")
borderTransp        =   input.int       (55         , ""                            ,   group= "Box Color"            ,         inline= "1")
bgTransp            =   input.int       (100        , ""                            ,   group= "Box Color"            ,         inline= "1")

alertMode           =   input.string    (alert.freq_once_per_bar_close              ,   "Alerts Mode"                 , group  = "Alert Frequency"  ,   options= [alert.freq_once_per_bar, alert.freq_once_per_bar_close]) 

_alert(_x, _y)      =>
    if _x
        alert   (_y + timeframe.period + ' chart. Price is ' + str.tostring(close), alertMode)

bullBor             =   color.new       (bullColi, borderTransp)
bullBg              =   color.new       (bullColi, bgTransp)
neutBor             =   color.new       (neutColi, borderTransp)
neutBg              =   color.new       (neutColi, bgTransp)
bearBor             =   color.new       (bearColi, borderTransp)
bearBg              =   color.new       (bearColi, bgTransp)

priceAvg            =   ta.sma          (close  ,   50)
sma200              =   ta.sma          (close  ,   200)
sma50               =   ta.sma          (close  ,   50)

utr1                =   close > priceAvg  
utr2                =   close > sma50 and sma50 > sma200

dtr1                =   close < priceAvg
dtr2                =   close < sma50 and sma50 < sma200

upTrend             =   trendRule == "Trend Rule 1" ? utr1 : trendRule == "Trend Rule 2" ? utr2 : true 
downTrend           =   trendRule == "Trend Rule 1" ? dtr1 : trendRule == "Trend Rule 2" ? dtr2 : true
	
d       =   input(false, "doji"             ) and doji              (dojiSize               =   dojiSize                        ,   dojiWickSize                  = dojiWickSize)
bew     =   input(false, "bull Engulf"      ) and bullEngulf        (maxRejectWick          =   rejectWickMax                   ,   mustEngulfWick                = ecWick)             and upTrend
beb     =   input(false, "bear Engulf"      ) and bearEngulf        (maxRejectWick          =   rejectWickMax                   ,   mustEngulfWick                = ecWick)             and downTrend
h       =   input(false, "hammer"           ) and hammer            (ratio                  =   hammerFib                       ,   shadowPercent                 = hsShadowPerc)       and downTrend
ss      =   input(false, "star"             ) and star              (ratio                  =   hammerFib                       ,   shadowPercent                 = hsShadowPerc)       and upTrend
dd      =   input(false, "dragonfly Doji"   ) and dragonflyDoji     ()
gd      =   input(false, "gravestone Doji"  ) and gravestoneDoji    ()
tb      =   input(false, "tweezer Bottom"   ) and tweezerBottom     (closeUpperHalf         =   closeHalf)                      and downTrend[1]
tt      =   input(false, "tweezer Top"      ) and tweezerTop        (closeLowerHalf         =   closeHalf)                      and upTrend  [1]
stw     =   input(false, "spinning Top Bull") and spinningTopBull   (wickSize               =   spinWick)
stb     =   input(false, "spinning Top Bear") and spinningTopBear   (wickSize               =   spinWick)
ms      =   input(false, "morning Star"     ) and morningStar       ()                      and downTrend
es      =   input(false, "evening Star"     ) and eveningStar       ()                      and upTrend
bhw     =   input(false, "harami Bull"      ) and haramiBull        ()                      and downTrend[1]
bhb     =   input(false, "harami Bear"      ) and haramiBear        ()                      and upTrend  [1]
hcw     =   input(false, "harami Bull Cross") and haramiBullCross   ()                      and downTrend[1]
hcb     =   input(false, "harami Bear Cross") and haramiBearCross   ()                      and upTrend  [1]
mw      =   input(false, "marubullzu"       ) and marubullzu        ()
mb      =   input(false, "marubearzu"       ) and marubearzu        ()
abw     =   input(false, "abandoned Bull"   ) and abandonedBull     ()                      and downTrend[1]
abb     =   input(false, "abandoned Bear"   ) and abandonedBear     ()                      and upTrend  [1]
p       =   input(false, "piercing"         ) and piercing          ()                      and downTrend[1]
dcc     =   input(false, "dark Cloud Cover" ) and darkCloudCover    ()                      and upTrend  [1]
utg     =   input(false, "tasuki Bull"      ) and tasukiBull        ()                      and upTrend
dtg     =   input(false, "tasuki Bear"      ) and tasukiBear        ()                      and downTrend
rtm     =   input(false, "rising Three"     ) and risingThree       ()                      and upTrend  [4]          
ftm     =   input(false, "falling Three"    ) and fallingThree      ()                      and downTrend[4]          
rw      =   input(false, "rising Window"    ) and risingWindow      ()                      and upTrend  [1]
fw      =   input(false, "falling Window"   ) and fallingWindow     ()                      and downTrend[1]
kw      =   input(false, "kicking Bull"     ) and kickingBull       ()
kb      =   input(false, "kicking Bear"     ) and kickingBear       ()
ll      =   input(false, "lls"              ) and lls               (ratio                  =   lsRatio)
lu      =   input(false, "lus"              ) and lus               (ratio                  =   lsRatio)
nw      =   input(false, "bull Neck"        ) and bullNeck          ()                      and upTrend
nb      =   input(false, "bear Neck"        ) and bearNeck          ()                      and downTrend
ws      =   input(false, "soldiers"         ) and soldiers          (wickSize               =   scWick)
bc      =   input(false, "crows"            ) and crows             (wickSize               =   scWick)
tsw     =   input(false, "triStar Bull"     ) and triStarBull       ()                      and downTrend[2]
tsb     =   input(false, "triStar Bear"     ) and triStarBear       ()                      and upTrend  [2]
ib      =   input(false, "inside bar"       ) and insideBar         ()                    
dib     =   input(false, "double inside bar") and doubleInside      ()                    

dLab        (d   and labels, labelColor = na, textColor = neutColi)     ,   wrap(d   and boxes, borderColor = neutBor, bgColor = neutBg)
bewLab      (bew and labels, labelColor = na, textColor = bullColi)     ,   wrap(bew and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =2)
bebLab      (beb and labels, labelColor = na, textColor = bearColi)     ,   wrap(beb and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =2)
hLab        (h   and labels, labelColor = na, textColor = bullColi)     ,   wrap(h   and boxes, borderColor = bullBor, bgColor = bullBg)
ssLab       (ss  and labels, labelColor = na, textColor = bearColi)     ,   wrap(ss  and boxes, borderColor = bearBor, bgColor = bearBg)
ddLab       (dd  and labels, labelColor = na, textColor = bullColi)     ,   wrap(dd  and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =2)
gdLab       (gd  and labels, labelColor = na, textColor = bearColi)     ,   wrap(gd  and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =2)
tbLab       (tb  and labels, labelColor = na, textColor = bullColi)     ,   wrap(tb  and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =2)
ttLab       (tt  and labels, labelColor = na, textColor = bearColi)     ,   wrap(tt  and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =2)
stwLab      (stw and labels, labelColor = na, textColor = neutColi)     ,   wrap(stw and boxes, borderColor = neutBor, bgColor = neutBg)
stbLab      (stb and labels, labelColor = na, textColor = neutColi)     ,   wrap(stb and boxes, borderColor = neutBor, bgColor = neutBg)
msLab       (ms  and labels, labelColor = na, textColor = bullColi)     ,   wrap(ms  and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =3)
esLab       (es  and labels, labelColor = na, textColor = bearColi)     ,   wrap(es  and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =3)
hwLab       (bhw and labels, labelColor = na, textColor = bullColi)     ,   wrap(bhw and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =2)
hbLab       (bhb and labels, labelColor = na, textColor = bearColi)     ,   wrap(bhb and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =2)
hcwLab      (hcw and labels, labelColor = na, textColor = bullColi)     ,   wrap(hcw and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =2)
hcbLab      (hcb and labels, labelColor = na, textColor = bearColi)     ,   wrap(hcb and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =2)
mwLab       (mw  and labels, labelColor = na, textColor = bullColi)     ,   wrap(mw  and boxes, borderColor = bullBor, bgColor = bullBg)
mbLab       (mb  and labels, labelColor = na, textColor = bearColi)     ,   wrap(mb  and boxes, borderColor = bearBor, bgColor = bearBg)
abwLab      (abw and labels, labelColor = na, textColor = bullColi)     ,   wrap(abw and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =3)
abbLab      (abb and labels, labelColor = na, textColor = bearColi)     ,   wrap(abb and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =3)
pLab        (p   and labels, labelColor = na, textColor = bullColi)     ,   wrap(p   and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =2)
dccLab      (dcc and labels, labelColor = na, textColor = bearColi)     ,   wrap(dcc and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =2)

utgLab      (utg and labels, labelColor = na, textColor = bullColi)     ,   wrap(utg and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =3)
dtgLab      (dtg and labels, labelColor = na, textColor = bearColi)     ,   wrap(dtg and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =3)
rtmLab      (rtm and labels, labelColor = na, textColor = bullColi)     ,   wrap(rtm and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =5)
ftmLab      (ftm and labels, labelColor = na, textColor = bearColi)     ,   wrap(ftm and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =5)
rwLab       (rw  and labels, labelColor = na, textColor = bullColi)     ,   wrap(rw  and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =2)
fwLab       (fw  and labels, labelColor = na, textColor = bearColi)     ,   wrap(fw  and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =2)
kwLab       (kw  and labels, labelColor = na, textColor = bullColi)     ,   wrap(kw  and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =2)
kbLab       (kb  and labels, labelColor = na, textColor = bearColi)     ,   wrap(kb  and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =2)

llsLab      (ll  and labels, labelColor = na, textColor = bullColi)     ,   wrap(ll  and boxes, borderColor = bullBor, bgColor = bullBg)
lusLab      (lu  and labels, labelColor = na, textColor = bearColi)     ,   wrap(lu  and boxes, borderColor = bearBor, bgColor = bearBg)
nwLab       (nw  and labels, labelColor = na, textColor = bullColi)     ,   wrap(nw  and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =2)
nbLab       (nb  and labels, labelColor = na, textColor = bearColi)     ,   wrap(nb  and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =2)
wsLab       (ws  and labels, labelColor = na, textColor = bullColi)     ,   wrap(ws  and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =3)
bcLab       (bc  and labels, labelColor = na, textColor = bearColi)     ,   wrap(bc  and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =3)
tswLab      (tsw and labels, labelColor = na, textColor = bullColi)     ,   wrap(tsw and boxes, borderColor = bullBor, bgColor = bullBg, barsBack =3)
tsbLab      (tsb and labels, labelColor = na, textColor = bearColi)     ,   wrap(tsb and boxes, borderColor = bearBor, bgColor = bearBg, barsBack =3)
insLab      (ib  and labels, labelColor = na, textColor = neutColi)     ,   wrap(ib  and boxes, borderColor = neutBor, bgColor = neutBg, barsBack =2)
dinLab      (dib and labels, labelColor = na, textColor = neutColi)     ,   wrap(dib and boxes, borderColor = neutBor, bgColor = neutBg, barsBack =3)

_alert      (d      ,   'Doji on '                  )
_alert      (bew    ,   'Bullish Engulfing on '     )
_alert      (beb    ,   'Bearish Engulfing on '     )
_alert      (h      ,   'Hammer candle on '         )
_alert      (ss     ,   'Shooting star on '         )
_alert      (dd     ,   'Dragonfly Doji on '        )
_alert      (gd     ,   'Gravestone Doji on '       )
_alert      (tb     ,   'Tweezer Bottom on '        )
_alert      (tt     ,   'Tweezer Top on '           )
_alert      (stw    ,   'White Spinning Top on '    )
_alert      (stb    ,   'Black Spinning Top on '    )
_alert      (ms     ,   'Morning Star on '          )
_alert      (es     ,   'Evening Star on '          )
_alert      (bhw    ,   'Bullish Harami on '        )
_alert      (bhb    ,   'Bearish Harami on '        )
_alert      (hcw    ,   'Bullish Harami Cross on '  )
_alert      (hcb    ,   'Bearish Harami Cross on '  )
_alert      (mw     ,   'Bullish Marubozu on '      )
_alert      (mb     ,   'Bearish Marubozu on '      )
_alert      (abw    ,   'Bullish Abandoned Baby on ')
_alert      (abb    ,   'Bearish Abandoned Baby on ')
_alert      (p      ,   'Piercing on '              )
_alert      (dcc    ,   'Dark Cloud Cover on '      )
_alert      (utg    ,   'Upside Tasuki Gap on '     )
_alert      (dtg    ,   'Downside Tasuki Gap on '   )
_alert      (rtm    ,   'Rising Three Methods on '  )
_alert      (ftm    ,   'Falling Three Methods on ' )
_alert      (rw     ,   'Rising Window on '         )
_alert      (fw     ,   'Falling Window '           )
_alert      (kw     ,   'Kicking Bull on '          )
_alert      (kb     ,   'Kicking Bear on '          )
_alert      (tsb    ,   'Bearish Tasuki Gap on '    )
_alert      (tsw    ,   'Bullish Tasuki Gap on '    )
_alert      (ib     ,   'Inside Bar on '            )
_alert      (dib    ,   'Double Inside Bar on '     )