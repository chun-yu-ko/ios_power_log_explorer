# iOS Power Log Explorer 🚀🔋

### URL to access the app:
Check it out here: [iOS Power Log Explorer](https://ios-power-log-explorer.streamlit.app/)

![](https://github.com/chun-yu-ko/ios_power_log_explorer/blob/main/demo.png?raw=true)
---

## 🚀 How to Use This App (Yes, It’s That Easy!)

So, you've got yourself a `.plsql` file brimming with iOS device power logs? Fantastic! Here’s what you need to do:

1. **Upload the .plsql File** - Click the “Upload” button, select your `.plsql` file, and you’re off to the races. We support **only** `.plsql` files—because we believe in being exclusive and picky like that.
2. **Select a Node** - We’ll display a list of “Nodes.” You pick one (yes, just one—think of it like choosing your favorite dessert).
3. **Watch the Magic Happen** - Sit back and enjoy as we whip up beautiful visualizations of your data faster than you can say “low battery warning.”

**That’s it. No complex commands. No rocket science degree required. Just plug, upload, and explore!**

---

## 💻 Tech Stack (A Fancy Way of Saying “Things We Used to Make This Cool”)

- **Streamlit** - Making boring web apps a thing of the past with our interactive and user-friendly UI.
- **Pandas & Numpy** - Because data manipulation deserves only the finest and most performant tools.
- **Plotly** - Interactive charts and visualizations so sleek you might mistake them for a high-end sports car.
- **SQLite** - We open your `.plsql` file, treat it as a database, and dive into its depths like professional data divers (except without getting wet).

---

## 📚 Data Sources (Because Knowledge is Power...Log)

We harness the power of data straight from Apple’s iOS device logs, specifically:

- `PLBatteryAgent_EventBackward_BatteryUI`: Your battery data, sorted, transformed, and visualized.
- `PLAppTimeService_Aggregate_AppRunTime`: Tracks app usage for precise runtime analytics.
- `PLAccountingOperator_EventNone_Nodes` & `PLAccountingOperator_Aggregate_RootNodeEnergy`: Providing critical insights into node-based energy consumption.

---

## 🔍 What’s This Really About?

Ever wondered why your iPhone’s battery suddenly decides to nap halfway through the day? Or what’s *really* going on under the hood with app usage and power consumption? Fear not, fellow detective! This app peeks under the covers, letting you explore battery life, app run times, and energy usage down to the tiniest node-level details.

### References & Knowledge Dump

- [Apple Developer Forum Discussion](https://forums.developer.apple.com/forums/thread/4654)
- [iOS 功耗分析指南 by PunMy](https://punmy.cn/2018/06/12/iOS%20%E6%9C%80%E5%85%A8%E9%9D%A2%E7%9A%84%E5%8A%9F%E8%80%97%E5%88%86%E6%9E%90%E4%B9%8B%E2%80%94%E2%80%94Power%20Log.html)
- [ThinkDFIR’s Powerlog Analysis Guide](https://thinkdfir.com/2018/09/15/playing-with-the-ios-powerlog/)


### Contributer

 - [Woody](https://github.com/woodycatliu)

---

**Happy Exploring! May your logs always be insightful and your battery never die at 3 PM.**