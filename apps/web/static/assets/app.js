/* SHC — Sovereign Hedge Console terminal */

const I18N = {
  ar: {
    brand: "SHC",
    tagline: "منصة التحليل والتداول السيادية",
    login: "دخول",
    register: "إنشاء حساب",
    email: "البريد الإلكتروني",
    password: "كلمة المرور",
    name: "الاسم",
    markets: "الأسواق",
    agents: "وكلاء SHC",
    runAnalysis: "تشغيل التحليل السربي",
    analyzing: "جارٍ التحليل…",
    plans: "العضوية",
    logout: "خروج",
    balance: "الرصيد",
    plan: "الخطة",
    success: "احتمال النجاح",
    entry: "دخول",
    stop: "وقف",
    live: "بث مباشر",
    timeframe: "الإطار",
    subscribe: "تفعيل الخطة",
    needAuth: "سجّل الدخول لاستخدام الوكلاء والاشتراكات.",
    oracle: "قرار الأوراكل",
    noResult: "شغّل السرب لاستخراج الفرصة ونسبة النجاح.",
    terminal: "مكتب التحليل",
    indicators: "المؤشرات",
    chart: "الرسم البياني",
    panels: "اللوحات",
    vrcs: "VRCS بصمة الاحتقان الصامت",
    compression: "احتقان صامت / تجميع صانع السوق",
    spring_bullish: "انطلاق الزنبرك صعوداً",
    spring_bearish: "انطلاق الزنبرك هبوطاً",
    bullish: "صعود",
    bearish: "هبوط",
    neutral: "محايد",
    normal: "حركة طبيعية",
    confidence: "الثقة",
    streak: "شموع الاحتقان",
    alerts: "تنبيهات VRCS",
    settings: "إعدادات VRCS",
    period: "فترة الاحتقان",
    threshold: "معامل الانضغاط",
    volFactor: "معامل الحجم الهادئ",
    lookback: "مراقبة الانفجار",
    dashboard: "لوحة القياس",
    search: "بحث عن رمز…",
    crypto: "سوق العملات الرقمية",
    tadawul: "السوق السعودي",
    us: "السوق الأمريكي",
    europe: "السوق الأوروبي",
    asia: "السوق الآسيوي",
    commodities: "سوق السلع والطاقة",
    gainers: "الأعلى ربحاً",
    losers: "الأقل ربحاً",
    mcap: "الأكبر قيمة",
    draw: "الرسم",
    cursor: "تحديد",
    hline: "خط أفقي",
    trend: "خط اتجاه",
    rect: "مستطيل",
    fib: "فيبوناتشي",
    erase: "مسح الرسوم",
    coil: "قوة الاحتقان",
    body: "جسم الشمعة",
    vol: "الحجم",
    brain: "العقل",
    hunter: "الصياد",
    history: "السجل",
    analytics: "التحليلات",
    journal: "المفكرة",
    mtf: "توافق الفريمات",
    aligned: "فريمات متوافقة",
    coiled: "فريمات محتقنة",
    scanning: "جارٍ المسح…",
    scanNow: "مسح السوق",
    elite: "فرص نخبة (90%+)",
    quietSurge: "تدفق حجمي في شموع هادئة",
    winRate: "نسبة النجاح",
    trades: "الفرص",
    closed: "مغلقة",
    avgPnl: "متوسط الحركة",
    export: "تصدير CSV",
    correlation: "ارتباط السيولة",
    heatmap: "أوقات الاحتقان",
    peakHours: "أعلى الساعات",
    hour: "الساعة",
    springs: "انفجارات",
    rr: "حاسبة المستهدفات",
    risk: "المخاطرة",
    target: "الهدف",
    ratio: "العائد/المخاطرة",
    invalidation: "إبطال التحليل",
    addNote: "إضافة ملاحظة",
    notePlaceholder: "ملاحظتك التحليلية…",
    noNotes: "لا ملاحظات بعد.",
    sound: "الصوت",
    stealth: "الوضع الهادئ",
    split: "تقسيم",
    live_ws: "بث Binance",
    connecting: "جارٍ الاتصال…",
    alertFired: "إشارة نخبة",
    delete: "حذف",
    refresh: "تحديث",
    pageHistory: "الأرشيف",
    pageReports: "التقارير",
    pageAgents: "وكلاء SHC",
    pageAnalytics: "التحليلات",
    analyticsHint: "ابحث عن عملة أو سهم محدد فقط عندما تريد تحليله يدوياً. كل وكيل يظهر على حدة.",
    noConsensus: "لا يوجد إجماع كافٍ بعد. هذه قراءة كل وكيل على حدة.",
    pageSettings: "الإعدادات",
    assistant: "المساعد",
    ask: "اسأل",
    asking: "جارٍ التحليل…",
    members: "الأعضاء",
    verifyEmail: "إعادة إرسال التفعيل",
    health: "صحة المنصة",
    calibrate: "معايرة الثقة",
    applyCal: "اعتماد المعايرة",
    searchInd: "ابحث في المؤشرات…",
    venueHint: "السعودي · الأمريكي · الأوروبي · الآسيوي · السلع · العملات الرقمية",
    openSource: "مفتوحة المصدر",
    membership: "العضوية",
    entitlements: "الصلاحيات",
    leak: "تسريب ذاكرة محتمل",
    stable: "مستقر",
    welcomeSent: "أُرسلت رسالة الترحيب إلى بريدك.",
    upgrade: "ترقية",
    locked: "مقفل",
    paywallTitle: "هذه الميزة ضمن باقة أعلى",
    delayedData: "بيانات متأخرة — رقِّ الباقة للبث الحي",
    explorer: "الأساسية",
    pro_hunter: "الصياد",
    elite_brain: "العقل",
    compare: "مقارنة الميزات",
    watchlist: "قائمة المراقبة",
    addWatch: "أضف للمراقبة",
    delayedHunter: "الصياد المتأخر (Explorer)",
    webhook: "Webhook",
    telegram: "Telegram",
    dismiss: "إغلاق",
    split2: "تقسيم إلى شارتين",
    split4: "تقسيم إلى أربع شارتات",
    live_equities: "الأسواق العالمية اللحظية",
    watchlists: "قوائم المراقبة الذكية",
    pageMarkets: "الأسواق والأخبار",
    marketsNewsHint: "الشريط الحي والقطاعات والأخبار في صفحة واحدة.",
    pageChart: "الرسم البياني",
    indDockHint: "كل المؤشرات — فعّل ما تحتاجه على الشارت",
    tape: "شريط المؤشرات",
    tasi: "تاسي",
    spx: "S&P 500",
    ixic: "ناسداك",
    btcDom: "استحواذ BTC",
    totalCap: "القيمة السوقية",
    totalVol: "سيولة 24س",
    activeVol: "الأعلى سيولة",
    sectors: "القطاعات",
    removeWatch: "إزالة",
    hunterNear: "فرصة قريبة من الصياد",
    huntingMarket: "جارٍ مسح السوق النشط",
    openSetup: "افتح على التحليل",
    liveDesk: "بث حي للأسواق",
    crossWatch: "قائمة عابرة للأسواق",
    openChart: "افتح الشارت",
    long: "شراء",
    short: "بيع",
    wallet: "المحفظة",
    riskPct: "نسبة المخاطرة",
    position: "حجم الصفقة",
    applyLevels: "ارسم SL / TP",
    autoRisk: "تطبيق تلقائي مع إشارة الصياد",
    autoDir: "الاتجاه من التحليل",
    manualDir: "تعديل يدوي",
    fromHunter: "من الصياد / VRCS",
    fromBrain: "من توافق الفريمات",
    fromTape: "من حركة السعر",
    resetAuto: "أعد التلقائي",
    shareChart: "تصدير",
    shared: "تم تجهيز الصورة",
    fundamentals: "الأساسيات",
    pe: "مكرر الربحية",
    mcap: "القيمة السوقية",
    industry: "القطاع",
    sentiment: "مشاعر السوق",
    profileTitle: "بطاقة الأصل",
    lastPrice: "آخر سعر",
    change24h: "التغير",
    supply: "المعروض المتداول",
    outstanding: "الأسهم القائمة",
    sharesFloat: "الأسهم الحرة",
    liquidity: "السيولة",
    momentum: "الزخم",
    quoteVolume: "حجم التداول",
    avgVolume: "متوسط الحجم",
    volume24: "الحجم",
    momOverbought: "تشبع شرائي",
    momOversold: "تشبع بيعي",
    momBullish: "زخم صاعد",
    momBearish: "زخم هابط",
    momNeutral: "زخم محايد",
    agentsOpinions: "آراء الوكلاء",
    risk_on: "سيولة شرائية",
    risk_off: "سيولة بيعية",
    commandCenter: "مركز القيادة",
    opsRoom: "غرفة العمليات",
    opsGate: "دخول المشغّل",
    opsLogin: "دخول المسؤول",
    opsBack: "العودة إلى البرنامج",
    opsUnlock: "فتح الغرفة",
    opsWrong: "تعذّر الدخول",
    opsLock: "إغلاق الغرفة",
    opsAgents: "مراقبة الوكلاء",
    opsExec: "الوكيل التنفيذي",
    opsAudit: "الوكيل المراقب",
    opsLive: "يعمل الآن",
    opsIdle: "في الانتظار",
    opsFills: "صفقات وهمية منفذة",
    opsWinRate: "نسبة النجاح اللحظية",
    opsThreshold: "عتبة الثقة",
    opsAuditLog: "سجل التدقيق والتصحيح",
    opsHist: "النجاح التاريخي",
    opsCorrected: "تصحيح العتبة",
    opsPaperFleet: "المحفظة الافتراضية الموحدة",
    opsBank: "رأس المال الافتراضي",
    opsPnl: "ربح / خسارة محقق",
    opsFeeds: "مركز البث والأسواق",
    opsFilter: "فلتر المستقرات",
    opsBlocked: "مستبعد",
    opsTradeable: "قابل للرصد",
    opsHooks: "سجل الويب هوك والبوتات",
    opsDelivered: "وُصل",
    opsFailed: "فشل",
    opsNoAudit: "لا مراجعات بعد.",
    opsNoHooks: "لا إرسالات بعد.",
    opsBotDay: "تقرير البوت اليومي",
    opsBotReset: "يتجدد يومياً الساعة 12:00 (الرياض) ويعيد المحفظة إلى 100,000$",
    opsBotOpened: "عدد الصفقات",
    opsBotProfit: "الربح",
    opsBotLoss: "الخسارة",
    opsBotWallet: "المحفظة شاملة الأرباح والخسائر",
    opsBotLastReset: "آخر تجديد",
    opsBotNextReset: "التجديد القادم",
    opsBotHistory: "سجل الأيام",
    opsNoBotDay: "لا تقرير يومي بعد.",
    membersActive: "مشتركون نشطون",
    paidActive: "باقات مدفوعة",
    wsHealth: "استجابة البث",
    backtest: "الاختبار العكسي",
    webhooks: "تصدير Webhooks",
    checkout: "إتمام الدفع",
    paySuccess: "تم تفعيل الباقة بعد الدفع",
    payCancel: "أُلغي الدفع — الباقة لم تتغير",
    testPayHint: "وضع تجريبي: الدفع محلي ويفعّل الباقة بعد التأكيد",
    stripeHint: "الدفع عبر Stripe — التفعيل بعد نجاح العملية فقط",
    testAlert: "إرسال تنبيه تجريبي",
    alertSent: "أُرسل التنبيه إلى القنوات المربوطة",
    saveFirst: "احفظ الرابط أو معرف تيليجرام أولاً",
    paper: "التداول الافتراضي",
    openPaper: "افتح صفقة ورقية",
    closePaper: "إغلاق",
    paperCash: "السيولة الافتراضية",
    paperEquity: "قيمة الحساب",
    realized: "ربح محقق",
    noPaper: "لا صفقات مفتوحة.",
    paperOpened: "فُتحت الصفقة في التداول الافتراضي",
    paperClosed: "أُغلقت الصفقة",
    resetPaper: "إعادة تعيين الدفتر",
    paperHint: "محفظتك اليدوية 100,000$. صفقات الوكيل تظهر في غرفة المسؤول فقط.",
    agentsSilent: "هذه الصفحة تعرض تلقائياً الفرص المجازة: فريم الصفقة، نوعها فوري أو عقود شراء/بيع، الدخول والوقف وثلاثة أهداف، مع نطاق الدخول ووقت الصفقة.",
    execBot: "الوكيل التنفيذي الآلي",
    execBotHint: "يختار من صفقات وكلاء التحليل المجازة فقط، يحدد الحجم لوحده، ويمرّر كل صفقة للمراقب.",
    auditor: "الوكيل المراقب الذكي",
    auditorHint: "يراقب صفقات التنفيذي بعد التنفيذ، ويعدّ أخطاء الصياد ووكلاء التحليل والتنفيذي حسب النتيجة.",
    swarmApproved: "صفقات مؤكدة",
    swarmRejected: "مرفوضة من التحليل",
    swarmVotes: "تصويت الوكلاء",
    swarmNeed: "يُعرض المقبول فقط: إجماع 75% من ثمانية وكلاء وثقة 70% على الأقل",
    analysisSetups: "صفقات التحليل",
    swarmWaiting: "لا توجد فرص مستوفية حالياً. السرب يعمل في الخلفية ويعرض هنا ما يُجاز تلقائياً.",
    agentsLive: "تحديث تلقائي",
    swarmAlert: "فرصة الوكلاء",
    tradeFrame: "فريم الصفقة",
    tradeType: "نوع الصفقة",
    target1: "الهدف الأول",
    target2: "الهدف الثاني",
    target3: "الهدف الثالث",
    futuresBuy: "عقود شراء",
    futuresSell: "عقود بيع",
    spotBuy: "فوري شراء",
    spotSell: "فوري بيع",
    entryWindow: "نطاق الدخول",
    tradeTime: "وقت الصفقة",
    agentErrors: "تصنيف أخطاء الوكلاء",
    radar_agent: "الرادار",
    quant_agent: "الكمّي",
    pattern_agent: "الأنماط",
    liquidity_agent: "السيولة",
    news_sentiment_agent: "أخبار السوق",
    risk_management_agent: "إدارة المخاطر",
    market_sentiment_agent: "مشاعر السوق",
    on_chain_agent: "السلسلة",
    Radar: "الرادار",
    Quant: "الكمّي",
    Patterns: "الأنماط",
    Liquidity: "السيولة",
    News_Sentiment: "أخبار السوق",
    Risk_Management: "إدارة المخاطر",
    Market_Sentiment: "مشاعر السوق",
    On_Chain: "السلسلة",
    BUY: "شراء",
    SELL: "بيع",
    WAIT: "انتظار",
    execution: "التنفيذي",
    hunter_false_signal: "فرصة خاطئة",
    false_confirm: "تأكيد خاطئ",
    wrong_direction: "اتجاه معاكس",
    execution_losing_fill: "تنفيذ خاسر",
    masterSupervisor: "المراقب الرئيسي",
    botOn: "التفيذ الآلي يعمل",
    botOff: "التفيذ الآلي متوقف",
    botTick: "تشغيل دورة تنفيذ",
    runAudit: "مراجعة المراقب",
    lastAudit: "آخر مراجعة",
    winRateLive: "نسبة النجاح الحية",
    correctedParams: "المعايير بعد التصحيح",
    autoExec: "تنفيذ تلقائي من الصياد",
    virtualBank: "المحفظة الافتراضية",
    execReport: "تقرير تنفيذي",
    auditReport: "تقرير المراقب",
    botTrade: "صفقة الوكيل",
    noBotTrades: "لا صفقات آلية بعد.",
    openedNow: "صفقات نُفذت الآن",
    supervisorNotes: "ملاحظات التصحيح",
    qtyHint: "حدد مبلغ الصفقة من الرصيد الافتراضي 100,000$",
    tradeAmount: "مبلغ الصفقة",
    ofBank: "من 100,000$",
    amountHint: "هذا المبلغ لصفقاتك اليدوية فقط. البوت يحدد مبلغه لوحده من الرصيد الافتراضي ويرسل الصفقة للمراقب.",
    paperCashShort: "السيولة الافتراضية لا تكفي — خفّض مبلغ الصفقة",
    openTrades: "صفقات مفتوحة",
    forgot: "نسيت كلمة المرور؟",
    sendReset: "أرسل رابط الاستعادة",
    resetSent: "إن كان البريد مسجّلاً وصلك رابط الاستعادة",
    resetTitle: "تعيين كلمة مرور جديدة",
    newPassword: "كلمة المرور الجديدة",
    confirmPassword: "تأكيد كلمة المرور",
    savePassword: "حفظ كلمة المرور",
    resetDone: "تم تغيير كلمة المرور — سجّل الدخول",
    resetMismatch: "كلمتا المرور غير متطابقتين",
    twoFactor: "التأكيد الثنائي",
    twoFactorHint: "تطبيق المصادقة (Google Authenticator أو ما يشابهه)",
    twoFactorCode: "رمز المصادقة",
    enable2fa: "تفعيل التأكيد الثنائي",
    disable2fa: "إيقاف التأكيد الثنائي",
    twoFactorOn: "التأكيد الثنائي مفعّل",
    twoFactorOff: "التأكيد الثنائي غير مفعّل",
    copySecret: "نسخ المفتاح",
    backupCodes: "رموز احتياطية — احفظها مرة واحدة",
    confirm2fa: "أكّد الرمز",
    continue2fa: "متابعة",
    zoomIn: "تكبير",
    zoomOut: "تصغير",
    drawBasic: "الأدوات الأساسية",
    drawShapes: "الأشكال الهندسية",
    drawMeasure: "التنبؤ والقياس",
    brush: "فرشاة",
    arrow: "سهم",
    arrowUp: "سهم لأعلى",
    arrowDown: "سهم لأسفل",
    arrowMark: "علامة سهم",
    rectTilt: "مستطيل مائل",
    circle: "دائرة",
    ellipse: "بيضاوي",
    triangle: "مثلث",
    arc: "قوس",
    path: "مسار",
    curve: "منحنى",
    polyline: "متعدد الخطوط",
    doubleCurve: "منحنى مزدوج",
    highlighter: "لون مُميز",
    longPos: "صفقة شراء",
    shortPos: "مركز بيع",
    forecastPos: "توقع المركز",
    barPattern: "نمط الأعمدة",
    ghostPath: "مسار تخيلي",
    pitchfork: "قطاع",
    anchoredVwap: "VWAP مُثبَّت",
    vrFixed: "بروفايل الحجم بنطاق ثابت",
    vrAnchored: "بروفايل الحجم المُثبَّت",
    priceRange: "المدى السعري",
    timeRange: "المدى الزمني",
    datePriceRange: "نطاق التاريخ والسعر",
    pageWatchlist: "المراقبة",
    pagePaper: "التداول الافتراضي",
    pageNews: "الأخبار",
    simpleMode: "الوضع البسيط",
    proMode: "الوضع الاحترافي",
    modeHint: "البسيط للشارت والتنفيذ. الاحترافي يفتح التحليل الكامل لأعضاء الصياد والعقل.",
    execLong: "شراء الآن",
    execShort: "بيع الآن",
    newsEmpty: "لا أخبار مطابقة حالياً.",
    newsFilter: "تصفية حسب الرمز",
    allNews: "كل أخبار السوق",
    relatedNews: "أخبار الرمز",
    newsSearch: "ابحث عن عملة أو سهم لأخباره…",
    latestNews: "آخر العناوين",
    hideSide: "إخفاء اللوحة",
    showSide: "إظهار اللوحة",
    spotMkt: "فوري",
    futuresMkt: "عقود",
    binance: "باينانس",
    noHits: "لا نتائج مطابقة",
    kindSymbol: "رمز",
    kindIndicator: "مؤشر",
    uiMode: "نمط الواجهة",
    language: "اللغة",
    theme: "المظهر",
    darkTheme: "داكن",
    lightTheme: "فاتح",
    lang_ar: "العربية",
    lang_en: "الإنجليزية",
    lang_fr: "الفرنسية",
    lang_zh: "الصينية",
    lang_ja: "اليابانية",
    lang_es: "الإسبانية",
    lang_de: "الألمانية",
    lang_ko: "الكورية",
    lang_ru: "الروسية",
  },
  en: {
    brand: "SHC",
    tagline: "Sovereign Hedge Console",
    login: "Sign in",
    register: "Create account",
    email: "Email",
    password: "Password",
    name: "Name",
    markets: "Markets",
    agents: "SHC Agents",
    runAnalysis: "Run swarm analysis",
    analyzing: "Analyzing…",
    plans: "Membership",
    logout: "Log out",
    balance: "Balance",
    plan: "Plan",
    success: "Success probability",
    entry: "Entry",
    stop: "Stop",
    live: "Live",
    timeframe: "Timeframe",
    subscribe: "Activate plan",
    needAuth: "Sign in to use agents and subscriptions.",
    oracle: "Oracle decision",
    noResult: "Run the swarm to extract the setup and hit-rate.",
    terminal: "Analysis Desk",
    indicators: "Indicators",
    chart: "Chart",
    panels: "Panels",
    vrcs: "VRCS silent-congestion fingerprint",
    compression: "Silent compression / smart-money coil",
    spring_bullish: "Bullish spring",
    spring_bearish: "Bearish spring",
    bullish: "Bullish",
    bearish: "Bearish",
    neutral: "Neutral",
    normal: "Normal flow",
    confidence: "Confidence",
    streak: "Compression bars",
    alerts: "VRCS alerts",
    settings: "VRCS settings",
    period: "Compression period",
    threshold: "Threshold multiplier",
    volFactor: "Quiet volume factor",
    lookback: "Breakout lookback",
    dashboard: "Dashboard",
    search: "Search symbol…",
    crypto: "Crypto market",
    tadawul: "Saudi market",
    us: "US market",
    europe: "European market",
    asia: "Asian market",
    commodities: "Commodities & energy",
    gainers: "Gainers",
    losers: "Losers",
    mcap: "Largest",
    draw: "Draw",
    cursor: "Select",
    hline: "Horizontal",
    trend: "Trend line",
    rect: "Rectangle",
    fib: "Fibonacci",
    erase: "Clear drawings",
    coil: "Coil strength",
    body: "Candle body",
    vol: "Volume",
    brain: "Brain",
    hunter: "Hunter",
    history: "History",
    analytics: "Analytics",
    journal: "Journal",
    mtf: "Timeframe confluence",
    aligned: "Aligned frames",
    coiled: "Coiled frames",
    scanning: "Scanning…",
    scanNow: "Scan market",
    elite: "Elite setups (90%+)",
    quietSurge: "Quiet-candle volume surge",
    winRate: "Win rate",
    trades: "Setups",
    closed: "Closed",
    avgPnl: "Avg move",
    export: "Export CSV",
    correlation: "Liquidity correlation",
    heatmap: "Compression hours",
    peakHours: "Peak hours",
    hour: "Hour",
    springs: "Springs",
    rr: "Target calculator",
    risk: "Risk",
    target: "Target",
    ratio: "Reward/Risk",
    invalidation: "Invalidation",
    addNote: "Add note",
    notePlaceholder: "Your analytical note…",
    noNotes: "No notes yet.",
    sound: "Sound",
    stealth: "Stealth",
    split: "Split",
    live_ws: "Binance feed",
    connecting: "Connecting…",
    alertFired: "Elite signal",
    delete: "Delete",
    refresh: "Refresh",
    pageHistory: "Archive",
    pageReports: "Reports",
    pageAgents: "SHC Agents",
    pageAnalytics: "Analytics",
    analyticsHint: "Search a specific coin or stock only when you want a manual agent-by-agent read.",
    noConsensus: "No full consensus yet. Each agent is shown on its own.",
    pageSettings: "Settings",
    assistant: "Assistant",
    ask: "Ask",
    asking: "Thinking…",
    members: "Members",
    verifyEmail: "Resend activation",
    health: "Platform health",
    calibrate: "Calibrate confidence",
    applyCal: "Apply calibration",
    searchInd: "Search indicators…",
    venueHint: "Saudi · US · Europe · Asia · Commodities · Crypto",
    openSource: "Open source",
    membership: "Membership",
    entitlements: "Entitlements",
    leak: "Possible memory leak",
    stable: "Stable",
    welcomeSent: "A welcome email was sent to your inbox.",
    upgrade: "Upgrade",
    locked: "Locked",
    paywallTitle: "This feature needs a higher plan",
    delayedData: "Delayed data — upgrade for the live feed",
    explorer: "Explorer",
    pro_hunter: "Pro Hunter",
    elite_brain: "Elite Brain",
    compare: "Compare features",
    watchlist: "Watchlist",
    addWatch: "Watch",
    delayedHunter: "Delayed Hunter (Explorer)",
    webhook: "Webhook",
    telegram: "Telegram",
    dismiss: "Close",
    split2: "Split into 2 charts",
    split4: "Split into 4 charts",
    live_equities: "Live global markets",
    watchlists: "Smart watchlists",
    pageMarkets: "Markets & News",
    marketsNewsHint: "Live tape, sectors, and headlines in one desk.",
    pageChart: "Chart",
    indDockHint: "Full catalog — toggle any indicator onto the chart",
    tape: "Global tape",
    tasi: "TASI",
    spx: "S&P 500",
    ixic: "NASDAQ",
    btcDom: "BTC dominance",
    totalCap: "Market cap",
    totalVol: "24h volume",
    activeVol: "Most active",
    sectors: "Sectors",
    removeWatch: "Remove",
    hunterNear: "Hunter setup nearby",
    huntingMarket: "Scanning the active market",
    openSetup: "Open on analysis",
    liveDesk: "Live market feed",
    crossWatch: "Cross-market watchlist",
    openChart: "Open chart",
    long: "Long",
    short: "Short",
    wallet: "Portfolio",
    riskPct: "Risk %",
    position: "Position size",
    applyLevels: "Draw SL / TP",
    autoRisk: "Auto-apply on Hunter signal",
    autoDir: "Direction from analysis",
    manualDir: "Manual override",
    fromHunter: "From Hunter / VRCS",
    fromBrain: "From timeframe confluence",
    fromTape: "From price action",
    resetAuto: "Back to auto",
    shareChart: "Export",
    shared: "Image ready",
    fundamentals: "Fundamentals",
    pe: "P/E",
    mcap: "Market cap",
    industry: "Industry",
    sentiment: "Sentiment",
    profileTitle: "Asset profile",
    lastPrice: "Last price",
    change24h: "Change",
    supply: "Circulating supply",
    outstanding: "Shares outstanding",
    sharesFloat: "Float",
    liquidity: "Liquidity",
    momentum: "Momentum",
    quoteVolume: "Turnover",
    avgVolume: "Average volume",
    volume24: "Volume",
    momOverbought: "Overbought",
    momOversold: "Oversold",
    momBullish: "Bullish momentum",
    momBearish: "Bearish momentum",
    momNeutral: "Neutral momentum",
    agentsOpinions: "Agent views",
    risk_on: "Buy-side liquidity",
    risk_off: "Sell-side liquidity",
    commandCenter: "Command center",
    opsRoom: "Operations room",
    opsGate: "Operator access",
    opsLogin: "Admin login",
    opsBack: "Back to the desk",
    opsUnlock: "Unlock room",
    opsWrong: "Access denied",
    opsLock: "Lock room",
    opsAgents: "Live agents",
    opsExec: "Execution bot",
    opsAudit: "Auditor",
    opsLive: "Live",
    opsIdle: "Idle",
    opsFills: "Paper fills",
    opsWinRate: "Live win rate",
    opsThreshold: "Confidence threshold",
    opsAuditLog: "Audit and self-correction",
    opsHist: "Historical win rate",
    opsCorrected: "Threshold correction",
    opsPaperFleet: "Unified virtual book",
    opsBank: "Virtual bankroll",
    opsPnl: "Realized P&L",
    opsFeeds: "Market feeds",
    opsFilter: "Stablecoin filter",
    opsBlocked: "Excluded",
    opsTradeable: "Tradable",
    opsHooks: "Webhook and bot log",
    opsDelivered: "Delivered",
    opsFailed: "Failed",
    opsNoAudit: "No reviews yet.",
    opsNoHooks: "No deliveries yet.",
    opsBotDay: "Daily bot report",
    opsBotReset: "Resets every day at 12:00 (Riyadh) and restores the $100,000 bank",
    opsBotOpened: "Trades opened",
    opsBotProfit: "Profit",
    opsBotLoss: "Loss",
    opsBotWallet: "Wallet including P&L",
    opsBotLastReset: "Last reset",
    opsBotNextReset: "Next reset",
    opsBotHistory: "Daily history",
    opsNoBotDay: "No daily report yet.",
    membersActive: "Active members",
    paidActive: "Paid plans",
    wsHealth: "Feed latency",
    backtest: "Instant backtesting",
    webhooks: "Live webhook export",
    checkout: "Complete payment",
    paySuccess: "Plan activated after payment",
    payCancel: "Payment canceled — plan unchanged",
    testPayHint: "Test desk: local checkout activates the plan after confirm",
    stripeHint: "Stripe checkout — plan activates only after a successful charge",
    testAlert: "Send test alert",
    alertSent: "Alert dispatched to connected channels",
    saveFirst: "Save the webhook or Telegram chat id first",
    paper: "Virtual trading",
    openPaper: "Open paper trade",
    closePaper: "Close",
    paperCash: "Paper cash",
    paperEquity: "Equity",
    realized: "Realized",
    noPaper: "No open paper trades.",
    paperOpened: "Paper trade opened",
    paperClosed: "Paper trade closed",
    resetPaper: "Reset paper book",
    paperHint: "Your manual $100,000 book. Agent fills appear only in the operations room.",
    agentsSilent: "This page lists approved setups: timeframe, spot or futures buy/sell, entry, stop, three targets, plus the entry window and trade time.",
    execBot: "Execution Bot",
    execBotHint: "Picks only analysis-approved setups, sizes fills autonomously, and hands each fill to the auditor.",
    auditor: "Master AI Supervisor",
    auditorHint: "Watches execution fills and scores errors for Hunter, the four analysis agents, and execution.",
    swarmApproved: "Confirmed setups",
    swarmRejected: "Rejected by analysis",
    swarmVotes: "Agent votes",
    swarmNeed: "Approved only: 75% of eight agents and 70% average confidence",
    analysisSetups: "Analysis setups",
    swarmWaiting: "No qualifying setups right now. The swarm keeps scanning and posts approvals here automatically.",
    agentsLive: "Live auto-refresh",
    swarmAlert: "Agents opportunity",
    tradeFrame: "Trade timeframe",
    tradeType: "Trade type",
    target1: "Target 1",
    target2: "Target 2",
    target3: "Target 3",
    futuresBuy: "Futures buy",
    futuresSell: "Futures sell",
    spotBuy: "Spot buy",
    spotSell: "Spot sell",
    entryWindow: "Entry window",
    tradeTime: "Trade time",
    agentErrors: "Agent error scores",
    radar_agent: "Radar",
    quant_agent: "Quant",
    pattern_agent: "Pattern",
    liquidity_agent: "Liquidity",
    news_sentiment_agent: "News",
    risk_management_agent: "Risk",
    market_sentiment_agent: "Market sentiment",
    on_chain_agent: "On-chain",
    Radar: "Radar",
    Quant: "Quant",
    Patterns: "Patterns",
    Liquidity: "Liquidity",
    News_Sentiment: "News",
    Risk_Management: "Risk",
    Market_Sentiment: "Market sentiment",
    On_Chain: "On-chain",
    BUY: "BUY",
    SELL: "SELL",
    WAIT: "WAIT",
    execution: "Execution",
    hunter_false_signal: "False setup",
    false_confirm: "False confirm",
    wrong_direction: "Wrong direction",
    execution_losing_fill: "Losing fill",
    masterSupervisor: "Master supervisor",
    botOn: "Auto-execution is on",
    botOff: "Auto-execution is off",
    botTick: "Run execution cycle",
    runAudit: "Run supervisor review",
    lastAudit: "Last review",
    winRateLive: "Live win rate",
    correctedParams: "Corrected parameters",
    autoExec: "Auto-execute Hunter setups",
    virtualBank: "Virtual bankroll",
    execReport: "Execution report",
    auditReport: "Supervisor report",
    botTrade: "Bot trade",
    noBotTrades: "No automated trades yet.",
    openedNow: "Trades opened now",
    supervisorNotes: "Correction notes",
    qtyHint: "Set a trade amount from the $100,000 virtual bank",
    tradeAmount: "Trade amount",
    ofBank: "of $100,000",
    amountHint: "This amount is for your manual trades only. The bot sizes its own fills and sends them to the supervisor.",
    paperCashShort: "Not enough paper cash — lower the trade amount",
    openTrades: "Open trades",
    forgot: "Forgot password?",
    sendReset: "Send reset link",
    resetSent: "If that email is registered, a reset link is on its way",
    resetTitle: "Set a new password",
    newPassword: "New password",
    confirmPassword: "Confirm password",
    savePassword: "Save password",
    resetDone: "Password updated — sign in",
    resetMismatch: "Passwords do not match",
    twoFactor: "Two-factor authentication",
    twoFactorHint: "Authenticator app (Google Authenticator or similar)",
    twoFactorCode: "Authenticator code",
    enable2fa: "Enable 2FA",
    disable2fa: "Disable 2FA",
    twoFactorOn: "Two-factor is on",
    twoFactorOff: "Two-factor is off",
    copySecret: "Copy secret",
    backupCodes: "Backup codes — save them once",
    confirm2fa: "Confirm code",
    continue2fa: "Continue",
    zoomIn: "Zoom in",
    zoomOut: "Zoom out",
    drawBasic: "Basic tools",
    drawShapes: "Geometric shapes",
    drawMeasure: "Forecast and measure",
    brush: "Brush",
    arrow: "Arrow",
    arrowUp: "Arrow up",
    arrowDown: "Arrow down",
    arrowMark: "Arrow marker",
    rectTilt: "Rotated rectangle",
    circle: "Circle",
    ellipse: "Ellipse",
    triangle: "Triangle",
    arc: "Arc",
    path: "Path",
    curve: "Curve",
    polyline: "Polyline",
    doubleCurve: "Double curve",
    highlighter: "Highlighter",
    longPos: "Long position",
    shortPos: "Short position",
    forecastPos: "Forecast position",
    barPattern: "Bars pattern",
    ghostPath: "Ghost path",
    pitchfork: "Pitchfork",
    anchoredVwap: "Anchored VWAP",
    vrFixed: "Fixed range volume profile",
    vrAnchored: "Anchored volume profile",
    priceRange: "Price range",
    timeRange: "Time range",
    datePriceRange: "Date and price range",
    pageWatchlist: "Watchlist",
    pagePaper: "Virtual trading",
    pageNews: "News",
    simpleMode: "Simple mode",
    proMode: "Pro / Elite mode",
    modeHint: "Simple keeps the chart and execution. Pro unlocks the full desk for Hunter and Elite members.",
    execLong: "Buy now",
    execShort: "Sell now",
    newsEmpty: "No matching headlines right now.",
    newsFilter: "Filter by symbol",
    allNews: "All market news",
    relatedNews: "Symbol news",
    newsSearch: "Search a coin or stock for its news…",
    latestNews: "Latest headlines",
    hideSide: "Hide panel",
    showSide: "Show panel",
    spotMkt: "Spot",
    futuresMkt: "Futures",
    binance: "Binance",
    noHits: "No matching results",
    kindSymbol: "Symbol",
    kindIndicator: "Indicator",
    uiMode: "Interface mode",
    language: "Language",
    theme: "Theme",
    darkTheme: "Dark",
    lightTheme: "Light",
    lang_ar: "Arabic",
    lang_en: "English",
    lang_fr: "French",
    lang_zh: "Chinese",
    lang_ja: "Japanese",
    lang_es: "Spanish",
    lang_de: "German",
    lang_ko: "Korean",
    lang_ru: "Russian",
  },
};
if (window.SHC_I18N) Object.assign(I18N, window.SHC_I18N);

const LOCALES = [
  { id: "ar", short: "ع", dir: "rtl" },
  { id: "en", short: "EN", dir: "ltr" },
  { id: "fr", short: "FR", dir: "ltr" },
  { id: "zh", short: "中", dir: "ltr" },
  { id: "ja", short: "日", dir: "ltr" },
  { id: "es", short: "ES", dir: "ltr" },
  { id: "de", short: "DE", dir: "ltr" },
  { id: "ko", short: "한", dir: "ltr" },
  { id: "ru", short: "RU", dir: "ltr" },
];

function localeMeta(id) {
  return LOCALES.find((item) => item.id === id) || LOCALES[0];
}

const ICO = {
  terminal: '<rect x="3" y="4" width="18" height="13" rx="1.5"/><path d="M8 20h8M12 17v3"/>',
  chart: '<path d="M4 18V9M9 18V6M14 18v-8M19 18V8"/><path d="M3 19h18"/>',
  indicators: '<path d="M4 6h16M4 12h10M4 18h13"/><circle cx="16" cy="12" r="1.6"/><circle cx="19" cy="18" r="1.6"/>',
  markets: '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
  history: '<circle cx="12" cy="12" r="8"/><path d="M12 8v5l3 2"/>',
  reports: '<path d="M7 3h8l4 4v14H7z"/><path d="M15 3v5h5M9 13h6M9 17h4"/>',
  settings: '<circle cx="12" cy="12" r="3"/><path d="M12 3v2.2M12 18.8V21M4.9 6.5l1.6 1.6M17.5 16l1.6 1.6M3 12h2.2M18.8 12H21M4.9 17.5l1.6-1.6M17.5 8l1.6-1.6"/>',
  plans: '<path d="M12 3l2.2 6.6H21l-5.4 4 2.1 6.5L12 16.6 6.3 20.1 8.4 13.6 3 9.6h6.8z"/>',
  admin: '<path d="M12 3l8 3v6c0 5-3.4 8.4-8 9.7C7.4 20.4 4 17 4 12V6z"/>',
  cursor: '<path d="M5 4l5 16 2.2-6.2L19 12z"/>',
  hline: '<path d="M3 12h18"/><path d="M7 9v6M17 9v6"/>',
  trend: '<path d="M4 17l6-7 4 3 6-8"/><path d="M16 5h4v4"/>',
  rect: '<rect x="5" y="6" width="14" height="12" rx="1"/>',
  fib: '<path d="M4 6h16M4 10h16M4 13.5h16M4 16.5h16M4 19h16"/>',
  erase: '<path d="M5 8l5-5 10 10-5 5H8L5 15z"/><path d="M8 20h11"/>',
  share: '<path d="M12 3v11"/><path d="M8 7l4-4 4 4"/><path d="M5 13v7h14v-7"/>',
  draw: '<path d="M4 20l4.2-1.2L19 8l-3-3L5.2 15.8z"/><path d="M14.5 6.5l3 3"/>',
  zoomIn: '<circle cx="11" cy="11" r="6.5"/><path d="M11 8v6M8 11h6M16.5 16.5L21 21"/>',
  zoomOut: '<circle cx="11" cy="11" r="6.5"/><path d="M8 11h6M16.5 16.5L21 21"/>',
  brush: '<path d="M5 20c2 0 3-1 4-3l9-9-3-3-9 9c-2 1-3 2-3 4z"/><path d="M14 6l3 3"/>',
  arrow: '<path d="M5 19L19 5"/><path d="M11 5h8v8"/>',
  arrowUp: '<path d="M12 19V6"/><path d="M7 11l5-5 5 5"/>',
  arrowDown: '<path d="M12 5v13"/><path d="M7 13l5 5 5-5"/>',
  arrowMark: '<path d="M6 18l6-14 2.5 6.5L20 12z"/>',
  rectTilt: '<path d="M7 8l12 3-2 9-12-3z"/>',
  circle: '<circle cx="12" cy="12" r="8"/>',
  ellipse: '<ellipse cx="12" cy="12" rx="9" ry="6"/>',
  triangle: '<path d="M12 4l8 16H4z"/>',
  arc: '<path d="M5 16a8 8 0 0 1 14-2"/>',
  path: '<path d="M4 16c3-8 5 2 8-4s5 1 8-5"/>',
  curve: '<path d="M4 17c4-12 12 8 16-10"/>',
  polyline: '<path d="M4 16l5-8 5 6 6-10"/>',
  doubleCurve: '<path d="M4 16c3-10 5 6 8-2s5 8 8-6"/>',
  highlighter: '<path d="M6 16l4-10 8 3-4 10z"/><path d="M5 20h14"/>',
  longPos: '<rect x="4" y="4" width="16" height="7" rx="1"/><rect x="4" y="13" width="16" height="7" rx="1"/>',
  shortPos: '<rect x="4" y="4" width="16" height="7" rx="1"/><path d="M4 17h16"/>',
  forecastPos: '<path d="M4 16l5-6 4 3 7-8"/><path d="M16 5h4v4"/>',
  barPattern: '<path d="M6 18V8M10 18V5M14 18v-7M18 18V9"/>',
  ghostPath: '<path d="M4 16c3-7 5 1 8-3s4 0 8-6"/>',
  pitchfork: '<path d="M5 19L12 5M5 19l7-6M5 19l7 2"/><path d="M12 13h8M12 21h8"/>',
  anchoredVwap: '<path d="M4 16c3-1 5-8 8-8s5 6 8 4"/><circle cx="6" cy="16" r="1.4"/>',
  vrFixed: '<path d="M5 6h8M5 10h12M5 14h6M5 18h10"/><path d="M4 4v16"/>',
  vrAnchored: '<path d="M6 5v14M6 8h10M6 12h14M6 16h8"/>',
  priceRange: '<path d="M12 4v16"/><path d="M8 6l4-3 4 3M8 18l4 3 4-3"/>',
  timeRange: '<path d="M4 12h16"/><path d="M6 8l-3 4 3 4M18 8l3 4-3 4"/>',
  datePriceRange: '<rect x="5" y="6" width="14" height="12" rx="1"/><path d="M5 12h14M12 6v12"/>',
  watchlist: '<path d="M5 6h14M5 12h10M5 18h12"/><path d="M17 10l3 3-3 3"/>',
  star: '<path d="M12 3l2.4 6.6H21l-5.3 3.9 2 6.5L12 16.6 6.3 20l2-6.5L3 9.6h6.6z"/>',
  paper: '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M8 8h8M8 12h8M8 16h5"/>',
  news: '<path d="M4 5h16v14H4z"/><path d="M7 9h10M7 13h7"/>',
  agents: '<circle cx="8" cy="8" r="2.4"/><circle cx="16" cy="8" r="2.4"/><circle cx="12" cy="15" r="2.4"/><path d="M4 19c.5-2 2-3 4-3s3.5 1 4 3M12 19c.5-2 2-3 4-3s3.5 1 4 3"/>',
  analytics: '<path d="M4 18V9M9 18V6M14 18v-8M19 18V8"/><path d="M3 19h18"/>',
  panelHide: '<path d="M14 5l-7 7 7 7"/><path d="M20 5v14"/>',
  panelShow: '<path d="M10 5l7 7-7 7"/><path d="M4 5v14"/>',
};

function ico(name) {
  const inner = ICO[name];
  if (!inner) return "";
  return `<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${inner}</svg>`;
}

const DRAW_GOLD = "#c8a45a";
const DRAW_INK = "#05070a";
const DRAW_SECTIONS = [
  { id: "drawBasic", tools: ["cursor", "hline", "trend", "fib", "erase"] },
  {
    id: "drawShapes",
    tools: [
      "brush", "arrow", "arrowUp", "arrowDown", "arrowMark", "rect", "rectTilt",
      "circle", "ellipse", "triangle", "arc", "path", "curve", "polyline", "doubleCurve", "highlighter",
    ],
  },
  {
    id: "drawMeasure",
    tools: [
      "longPos", "shortPos", "forecastPos", "barPattern", "ghostPath", "pitchfork",
      "anchoredVwap", "vrFixed", "vrAnchored", "priceRange", "timeRange", "datePriceRange",
    ],
  },
];
const DRAW_CLICK = new Set(["hline", "arrowUp", "arrowDown", "arrowMark"]);
const DRAW_FREEHAND = new Set(["brush"]);
const DRAW_MULTI = { path: 0, polyline: 0, ghostPath: 0, curve: 3, doubleCurve: 4, pitchfork: 3 };

function allDrawTools() {
  return DRAW_SECTIONS.flatMap((sec) => sec.tools);
}

function multiNeed(type) {
  return Object.prototype.hasOwnProperty.call(DRAW_MULTI, type) ? DRAW_MULTI[type] : null;
}

function drawMenu() {
  const current = allDrawTools().includes(state.drawTool) ? state.drawTool : "cursor";
  return `<div class="draw-wrap">
    <button type="button" class="ghost tiny ico-btn ${current !== "cursor" ? "active" : ""}" id="draw-btn" title="${t("draw")}">${ico(current)}<span>${t("draw")}</span><span class="caret">▾</span></button>
    <div class="draw-menu hidden" id="draw-menu">
      ${DRAW_SECTIONS.map(
        (sec) => `<div class="draw-sec">
          <div class="draw-sec-title">${t(sec.id)}</div>
          ${sec.tools
            .map(
              (tool) => `<button type="button" class="draw-item ${current === tool ? "active" : ""}" data-tool="${tool}">${ico(tool)}<span>${t(tool)}</span></button>`,
            )
            .join("")}
        </div>`,
      ).join("")}
    </div>
  </div>`;
}

function applyDrawTool(tool) {
  if (tool === "erase") {
    const cell = activeCell();
    if (cell) {
      delete state.drawings[drawKey(cell.symbol)];
      saveDrawings();
      scheduleRedraw(cell);
    }
    state.drawDraft = null;
    return;
  }
  state.drawDraft = null;
  state.drawTool = tool;
  state.cells.forEach((cell) => cell.canvas && cell.canvas.classList.toggle("active", tool !== "cursor"));
}

function paintDrawTrigger() {
  const btn = document.getElementById("draw-btn");
  const menu = document.getElementById("draw-menu");
  if (!btn) return;
  const current = allDrawTools().includes(state.drawTool) ? state.drawTool : "cursor";
  btn.innerHTML = `${ico(current)}<span>${t("draw")}</span><span class="caret">▾</span>`;
  btn.classList.toggle("active", current !== "cursor");
  if (menu)
    menu.querySelectorAll("[data-tool]").forEach((el) => el.classList.toggle("active", el.dataset.tool === current));
}

function bindDrawMenu() {
  const btn = document.getElementById("draw-btn");
  const menu = document.getElementById("draw-menu");
  if (!btn || !menu) return;
  if (menu.parentElement !== document.body) document.body.appendChild(menu);
  const place = () => {
    if (menu.classList.contains("hidden")) return;
    const box = btn.getBoundingClientRect();
    const rtl = document.documentElement.dir === "rtl";
    const width = Math.min(300, window.innerWidth - 16);
    let left = rtl ? box.right - width : box.left;
    left = Math.max(8, Math.min(left, window.innerWidth - width - 8));
    menu.style.width = `${Math.round(width)}px`;
    menu.style.left = `${Math.round(left)}px`;
    menu.style.right = "auto";
    menu.style.top = `${Math.round(box.bottom + 6)}px`;
  };
  btn.onclick = (e) => {
    e.stopPropagation();
    const langMenu = document.getElementById("lang-menu");
    if (langMenu) langMenu.classList.add("hidden");
    menu.classList.toggle("hidden");
    place();
  };
  if (state.drawMenuCloser) document.removeEventListener("click", state.drawMenuCloser);
  state.drawMenuCloser = (e) => {
    if (!menu.contains(e.target) && !btn.contains(e.target)) menu.classList.add("hidden");
  };
  document.addEventListener("click", state.drawMenuCloser);
  menu.querySelectorAll("[data-tool]").forEach((item) => {
    item.onclick = (e) => {
      e.stopPropagation();
      applyDrawTool(item.dataset.tool);
      paintDrawTrigger();
      menu.classList.add("hidden");
    };
  });
}

const TIMEFRAMES = ["1s", "1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "12h", "1d", "3d", "1w", "1M", "1Y"];
const BINANCE_TF = {
  "1s": "1s", "1m": "1m", "3m": "3m", "5m": "5m", "15m": "15m", "30m": "30m",
  "1h": "1h", "2h": "2h", "4h": "4h", "6h": "6h", "12h": "12h",
  "1d": "1d", "3d": "3d", "1w": "1w", "1M": "1M", "1Y": "1M",
};
const OVERLAY_STYLES = {
  sma20: { color: "#c8a45a", width: 2 },
  sma50: { color: "#8a6b2c", width: 2 },
  sma200: { color: "#8b98a8", width: 2 },
  ema12: { color: "#f2d98a", width: 2 },
  ema26: { color: "#c8a45a", width: 2 },
  bb_mid: { color: "#8b98a8", width: 1 },
  bb_upper: { color: "#e8c36a", width: 1 },
  bb_lower: { color: "#e8c36a", width: 1 },
  vwap: { color: "#f2d98a", width: 2 },
  supertrend: { color: "#c8a45a", width: 2 },
  ichi_tenkan: { color: "#e8c36a", width: 1 },
  ichi_kijun: { color: "#8b98a8", width: 1 },
  ichi_span_a: { color: "#c8a45a", width: 1 },
  ichi_span_b: { color: "#8a6b2c", width: 1 },
  don_upper: { color: "#8b98a8", width: 1 },
  don_lower: { color: "#8b98a8", width: 1 },
  kel_upper: { color: "#e8c36a", width: 1 },
  kel_mid: { color: "#8b98a8", width: 1 },
  kel_lower: { color: "#e8c36a", width: 1 },
  wma: { color: "#e8c36a", width: 2 },
  hma: { color: "#f2d98a", width: 2 },
  dema: { color: "#c8a45a", width: 2 },
  tema: { color: "#8a6b2c", width: 2 },
  zlema: { color: "#d4b36a", width: 2 },
  vwma: { color: "#c8a45a", width: 2 },
  psar: { color: "#e8c36a", width: 1 },
  pivot: { color: "#c8a45a", width: 1 },
  pivot_r1: { color: "#26a69a", width: 1 },
  pivot_s1: { color: "#ef5350", width: 1 },
  pivot_r2: { color: "#26a69a88", width: 1 },
  pivot_s2: { color: "#ef535088", width: 1 },
  chandelier_long: { color: "#26a69a", width: 1 },
  chandelier_short: { color: "#ef5350", width: 1 },
};
const OSC_IDS = [
  "rsi", "macd", "atr", "stoch", "willr", "cci", "obv",
  "adx", "aroon", "vortex", "roc", "momentum", "trix", "ppo", "ao", "uo",
  "coppock", "kst", "fisher", "wavetrend", "squeeze", "bbextras", "elder",
  "mfi", "cmf", "adline", "chaikin", "fi", "eom",
];
const OSC_PAINT = {
  rsi: [["rsi", "#c8a45a"]],
  atr: [["atr", "#ff9f43"]],
  stoch: [["stoch_k", "#c8a45a"], ["stoch_d", "#8b98a8"]],
  willr: [["willr", "#c27aff"]],
  cci: [["cci", "#5b8def"]],
  obv: [["obv", "#8b98a8"]],
  adx: [["adx", "#c8a45a"], ["plus_di", "#26a69a"], ["minus_di", "#ef5350"]],
  aroon: [["aroon_up", "#26a69a"], ["aroon_down", "#ef5350"]],
  vortex: [["vi_plus", "#26a69a"], ["vi_minus", "#ef5350"]],
  roc: [["roc", "#c8a45a"]],
  momentum: [["momentum", "#f2d98a"]],
  trix: [["trix", "#c27aff"]],
  ppo: [["ppo", "#5b8def"], ["ppo_signal", "#c8a45a"]],
  ao: [["ao", "#c8a45a"]],
  uo: [["uo", "#ff9f43"]],
  coppock: [["coppock", "#c8a45a"]],
  kst: [["kst", "#5b8def"], ["kst_signal", "#c8a45a"]],
  fisher: [["fisher", "#c27aff"]],
  wavetrend: [["wt1", "#c8a45a"], ["wt2", "#5b8def"]],
  squeeze: [["squeeze_momentum", "#c8a45a"]],
  bbextras: [["bb_percent_b", "#c8a45a"], ["bb_bandwidth", "#5b8def"]],
  elder: [["bull_power", "#26a69a"], ["bear_power", "#ef5350"]],
  mfi: [["mfi", "#c8a45a"]],
  cmf: [["cmf", "#5b8def"]],
  adline: [["adline", "#8b98a8"]],
  chaikin: [["chaikin", "#c8a45a"]],
  fi: [["fi", "#ff9f43"]],
  eom: [["eom", "#c27aff"]],
};

/* ------------------------------------------------------------------ state */

function readJSON(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

const state = {
  locale: localeMeta(localStorage.getItem("shc_locale") || "ar").id,
  token: localStorage.getItem("shc_token") || "",
  user: null,
  access: { subscription_tier: "explorer", entitlements: ["chart", "classic_indicators", "live_equities", "delayed_equities", "watchlists", "split2", "hunter_delayed"], max_charts: 1 },
  watchlist: readJSON("shc_watch", ["BTC/USDT", "ETH/USDT"]),
  timeframe: localStorage.getItem("shc_tf") || "15m",
  view: "terminal",
  panel: "brain",
  panelOpen: localStorage.getItem("shc_panel_open") !== "0",
  venue: localStorage.getItem("shc_venue") || "crypto",
  scanTab: "gainers",
  split: Number(localStorage.getItem("shc_split") || 1),
  symbols: readJSON("shc_symbols", ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT"]),
  activeCell: 0,
  cells: [],
  catalog: [],
  active: new Set(readJSON("shc_inds", ["vrcs", "volume"])),
  alerts: localStorage.getItem("shc_alerts") !== "0",
  sound: localStorage.getItem("shc_sound") === "1",
  stealth: localStorage.getItem("shc_stealth") === "1",
  theme: localStorage.getItem("shc_theme") === "light" ? "light" : "dark",
  drawTool: "cursor",
  drawings: readJSON("shc_draw", {}),
  drawDraft: null,
  journal: readJSON("shc_journal", []),
  firedAlerts: new Set(),
  poll: null,
  huntTimer: null,
  cryptoPulse: null,
  mkWs: null,
  mkFutWs: null,
  mkPoll: null,
  mkVenue: localStorage.getItem("shc_mk_venue") || localStorage.getItem("shc_venue") || "crypto",
  mkHunter: {},
  lastHunt: null,
  pendingHunt: null,
  huntFlight: null,
  deskWs: null,
  futWs: null,
  futWsRetry: 0,
  quotePulse: null,
  resizeObserver: null,
  resizeBound: false,
  indMenuCloser: null,
  langMenuCloser: null,
  ws: null,
  wsRetry: 0,
  vrcs: readJSON("shc_vrcs", {
    compression_period: 20,
    threshold_multiplier: 0.6,
    volume_factor: 0.7,
    lookback_breakout: 3,
    show_dashboard: true,
  }),
  mobile: "chart",
  risk: (() => {
    const pack = readJSON("shc_risk", { wallet: 100000, pct: 1, auto: true, side: "bullish", override: {} });
    pack.wallet = 100000;
    if (!Number.isFinite(Number(pack.amount)) || Number(pack.amount) <= 0) {
      pack.amount = Number.isFinite(Number(pack.pct)) ? 100000 * (Number(pack.pct) / 100) : 1000;
    }
    pack.amount = Math.max(10, Math.min(100000, Number(pack.amount)));
    if (!Number.isFinite(Number(pack.wallet)) || Number(pack.wallet) < 50000) {
      pack.wallet = 100000;
      try {
        localStorage.setItem("shc_risk", JSON.stringify(pack));
      } catch {
        /* ignore quota */
      }
    }
    return pack;
  })(),
  paperBook: null,
  desk: null,
  execution: localStorage.getItem("shc_exec") !== "0",
  execTimer: null,
  opsToken: sessionStorage.getItem("shc_ops") || "",
  opsTimer: null,
  uiMode: localStorage.getItem("shc_ui_mode") || "",
  newsTimer: null,
  agentsTimer: null,
  newsFilter: localStorage.getItem("shc_news_filter") || "all",
  searchRemote: [],
  searchCloser: null,
  swarmTimer: null,
  swarmSeen: new Set(),
  swarmPrimed: false,
};

function t(key) {
  const pack = I18N[state.locale] || {};
  return pack[key] || (I18N.en && I18N.en[key]) || (I18N.ar && I18N.ar[key]) || key;
}

function applyDir() {
  const meta = localeMeta(state.locale);
  state.locale = meta.id;
  const root = document.documentElement;
  root.lang = meta.id;
  root.dir = meta.dir;
  root.classList.toggle("is-rtl", meta.dir === "rtl");
  root.classList.toggle("is-ltr", meta.dir !== "rtl");
  document.body.dataset.locale = meta.id;
  localStorage.setItem("shc_locale", meta.id);
  document.title = `SHC · ${t("tagline")}`;
}

function applyStealth() {
  document.body.classList.toggle("stealth", state.stealth);
}

function applyTheme() {
  const light = state.theme === "light";
  const root = document.documentElement;
  root.classList.toggle("theme-light", light);
  root.classList.toggle("theme-dark", !light);
  document.body.classList.toggle("theme-light", light);
  document.body.classList.toggle("theme-dark", !light);
  persist("shc_theme", light ? "light" : "dark");
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.setAttribute("content", light ? "#f4f6f8" : "#05070a");
}

function themeBtnLabel() {
  return state.theme === "light" ? `☀ ${t("lightTheme")}` : `🌙 ${t("darkTheme")}`;
}

function toggleTheme() {
  state.theme = state.theme === "light" ? "dark" : "light";
  applyTheme();
  const btn = document.getElementById("theme-btn");
  if (btn) {
    btn.textContent = themeBtnLabel();
    btn.title = t("theme");
    btn.setAttribute("aria-pressed", state.theme === "light" ? "true" : "false");
  }
  state.cells.forEach((cell) => cell.chart && cell.chart.applyOptions(chartTheme()));
}

function canProMode() {
  return can("hunter") || can("brain") || can("vrcs") || can("analytics");
}

function isSimple() {
  return state.uiMode !== "pro";
}

function applyUiMode() {
  const saved = localStorage.getItem("shc_ui_mode");
  if (saved === "simple" || saved === "pro") state.uiMode = saved;
  else state.uiMode = canProMode() ? "pro" : "simple";
  if (state.uiMode === "pro" && !canProMode()) state.uiMode = "simple";
  document.body.classList.toggle("ui-simple", state.uiMode === "simple");
  document.body.classList.toggle("ui-pro", state.uiMode === "pro");
  persist("shc_ui_mode", state.uiMode);
}

function toggleUiMode() {
  if (state.uiMode !== "pro") {
    if (!canProMode()) {
      paywall("elite_brain");
      return;
    }
    state.uiMode = "pro";
  } else {
    state.uiMode = "simple";
  }
  persist("shc_ui_mode", state.uiMode);
  applyUiMode();
  void route();
}

function persist(key, value) {
  localStorage.setItem(key, typeof value === "string" ? value : JSON.stringify(value));
}

function can(feature) {
  if (state.user && state.user.is_admin) return true;
  const list = (state.access && state.access.entitlements) || [];
  return list.includes(feature);
}

function vrcsLocked() {
  return !can("vrcs");
}

function maxCharts() {
  return Number((state.access && state.access.max_charts) || 1);
}

function paywall(feature) {
  const host = document.getElementById("paywall");
  const box = host || (() => {
    const el = document.createElement("div");
    el.id = "paywall";
    el.className = "paywall hidden";
    document.body.appendChild(el);
    return el;
  })();
  box.classList.remove("hidden");
  box.innerHTML = `<div class="paywall-card">
    <strong>${t("paywallTitle")}</strong>
    <p class="muted">${(state.access.features_catalog && state.access.features_catalog[feature]) || t(feature) || feature}</p>
    <button class="primary wide" id="pw-go">${t("upgrade")}</button>
    <button class="ghost wide" id="pw-close">${t("dismiss")}</button>
  </div>`;
  document.getElementById("pw-go").onclick = () => {
    box.classList.add("hidden");
    go("plans");
  };
  document.getElementById("pw-close").onclick = () => box.classList.add("hidden");
}

async function loadAccess() {
  try {
    state.access = await api("/api/subscriptions/entitlements");
    if (state.split > maxCharts()) {
      state.split = maxCharts();
      persist("shc_split", String(state.split));
    }
    if (!can("vrcs")) {
      state.active.delete("vrcs");
      persist("shc_inds", [...state.active]);
    }
  } catch {
    state.access = { subscription_tier: "explorer", entitlements: ["chart", "classic_indicators", "live_equities", "delayed_equities", "watchlists", "split2", "hunter_delayed"], max_charts: 1 };
  }
}

/* ------------------------------------------------------- smart data cache */

const cache = new Map();
const CACHE_MAX = 160;

function cacheGet(key, ttlMs) {
  const hit = cache.get(key);
  if (!hit) return null;
  if (Date.now() - hit.at > ttlMs) {
    cache.delete(key);
    return null;
  }
  cache.delete(key);
  cache.set(key, hit);
  return hit.value;
}

function cacheSet(key, value) {
  cache.set(key, { at: Date.now(), value });
  while (cache.size > CACHE_MAX) cache.delete(cache.keys().next().value);
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  if (state.opsToken) headers["X-Admin-Ops"] = state.opsToken;
  const res = await fetch(path, { ...options, headers });
  const body = await res.json().catch(() => ({}));
  if (!res.ok) {
    const raw = body.detail;
    if (raw && raw.code === "upgrade_required") {
      const err = new Error(t("paywallTitle"));
      err.upgrade = raw.feature;
      throw err;
    }
    const detail = Array.isArray(raw) ? JSON.stringify(raw) : raw || res.statusText;
    throw new Error(typeof detail === "object" ? JSON.stringify(detail) : detail);
  }
  return body;
}

async function apiCached(path, ttlMs = 20000) {
  const hit = cacheGet(path, ttlMs);
  if (hit) return hit;
  const value = await api(path);
  cacheSet(path, value);
  return value;
}

function setToken(token) {
  state.token = token || "";
  if (token) localStorage.setItem("shc_token", token);
  else localStorage.removeItem("shc_token");
}

/* ---------------------------------------------------- alerts: audio/visual */

let audioCtx = null;

function enableSound() {
  if (!audioCtx) {
    const Ctor = window.AudioContext || window.webkitAudioContext;
    if (Ctor) audioCtx = new Ctor();
  }
  if (audioCtx && audioCtx.state === "suspended") void audioCtx.resume();
}

function beep(side) {
  if (!state.sound || !audioCtx) return;
  const now = audioCtx.currentTime;
  [0, 0.18].forEach((offset, i) => {
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.type = "sine";
    osc.frequency.value = side === "bearish" ? 420 - i * 80 : 720 + i * 180;
    gain.gain.setValueAtTime(0.0001, now + offset);
    gain.gain.exponentialRampToValueAtTime(0.22, now + offset + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + offset + 0.16);
    osc.connect(gain).connect(audioCtx.destination);
    osc.start(now + offset);
    osc.stop(now + offset + 0.18);
  });
}

function toast(message, side = "bullish") {
  const host = document.getElementById("toasts");
  if (!host) return;
  const el = document.createElement("div");
  el.className = `toast ${side === "bearish" ? "down" : "up"}`;
  el.innerHTML = message;
  host.appendChild(el);
  setTimeout(() => el.classList.add("show"), 20);
  setTimeout(() => {
    el.classList.remove("show");
    setTimeout(() => el.remove(), 320);
  }, 6500);
}

function fireEliteAlert(symbol, timeframe, signal) {
  const key = `${symbol}|${timeframe}|${signal.time}|${signal.confidence}`;
  if (state.firedAlerts.has(key)) return;
  state.firedAlerts.add(key);
  if (!state.alerts || !can("alerts")) return;
  const label = `<strong>${t("alertFired")} · ${signal.label}</strong><br>${symbol} · ${timeframe} · ${
    signal.side === "bullish" ? "▲" : "▼"
  }`;
  toast(label, signal.side);
  beep(signal.side);
  const stage = document.querySelector(`.cell[data-symbol="${symbol}"]`);
  if (stage) {
    stage.classList.add(signal.side === "bullish" ? "flash-up" : "flash-down");
    setTimeout(() => stage.classList.remove("flash-up", "flash-down"), 1400);
  }
  if (window.Notification && Notification.permission === "granted") {
    new Notification(`SHC ${signal.side} ${signal.label}`, { body: `${symbol} ${timeframe}` });
  }
  const cell = state.cells.find((item) => item.symbol === symbol);
  if (cell && state.risk.auto && !(state.risk.override && state.risk.override[cell.symbol])) {
    applyRiskFromSignal(cell, signal);
  }
  if (can("alerts") || can("webhooks") || can("telegram")) {
    void api("/api/alerts/emit", {
      method: "POST",
      body: JSON.stringify({
        symbol,
        timeframe,
        side: signal.side,
        label: signal.label,
        confidence: signal.confidence,
        time: signal.time,
        last_price: cell && cell.lastBar ? cell.lastBar.close : null,
        state: signal.side,
      }),
    }).catch(() => {});
  }
}

/* --------------------------------------------------------------- charting */

function chartTheme() {
  if (state.theme === "light") {
    return {
      layout: {
        background: { color: "#ffffff" },
        textColor: "#5c6573",
        fontFamily: "IBM Plex Sans",
      },
      grid: {
        vertLines: { color: "#e8eaee" },
        horzLines: { color: "#e8eaee" },
      },
      rightPriceScale: { borderColor: "#d5d8de", visible: true, entireTextOnly: false },
      timeScale: { borderColor: "#d5d8de", timeVisible: true, secondsVisible: state.timeframe === "1s" },
      crosshair: { mode: 0 },
      handleScale: { axisPressedMouseMove: true },
    };
  }
  const dim = state.stealth;
  return {
    layout: {
      background: { color: dim ? "#05070a" : "#07090d" },
      textColor: dim ? "#6c7889" : "#8b98a8",
      fontFamily: "IBM Plex Sans",
    },
    grid: {
      vertLines: { color: dim ? "#0f141a" : "#151b22" },
      horzLines: { color: dim ? "#0f141a" : "#151b22" },
    },
    rightPriceScale: { borderColor: "#1e2630", visible: true, entireTextOnly: false },
    timeScale: { borderColor: "#1e2630", timeVisible: true, secondsVisible: state.timeframe === "1s" },
    crosshair: { mode: 0 },
    handleScale: { axisPressedMouseMove: true },
  };
}

function drawKey(symbol) {
  return `${symbol}|${state.timeframe}`;
}

function zoomControls() {
  return `<div class="zoom-cluster" role="group" aria-label="${t("zoomIn")} / ${t("zoomOut")}">
    <button type="button" class="ghost tiny zoom-btn" id="zoom-out" title="${t("zoomOut")} (−)">${ico("zoomOut")}<span>−</span></button>
    <button type="button" class="ghost tiny zoom-btn" id="zoom-in" title="${t("zoomIn")} (+)">${ico("zoomIn")}<span>+</span></button>
  </div>`;
}

let zoomKeysBound = false;

function zoomActiveChart(factor) {
  const cell = activeCell();
  if (!cell || !cell.chart) return;
  const scale = cell.chart.timeScale();
  const range = scale.getVisibleLogicalRange();
  if (!range || !Number.isFinite(range.from) || !Number.isFinite(range.to)) return;
  const span0 = Math.max(2, range.to - range.from);
  const span1 = Math.max(12, Math.min(span0 * factor, 8000));
  const from0 = range.from;
  const to0 = range.to;
  const to1 = to0;
  const from1 = to1 - span1;
  let price0 = null;
  let price1 = null;
  try {
    const priceScale = cell.series && cell.series.priceScale();
    const visible = priceScale && priceScale.getVisibleRange && priceScale.getVisibleRange();
    if (visible && Number.isFinite(visible.from) && Number.isFinite(visible.to) && visible.to > visible.from) {
      const mid = (visible.from + visible.to) / 2;
      const half = ((visible.to - visible.from) / 2) * factor;
      price0 = { from: visible.from, to: visible.to };
      price1 = { from: mid - half, to: mid + half };
      priceScale.applyOptions({ autoScale: false });
    }
  } catch {
    price0 = null;
  }
  if (cell.zoomAnim) cancelAnimationFrame(cell.zoomAnim);
  const started = performance.now();
  const duration = 170;
  const tick = (now) => {
    const t = Math.min(1, (now - started) / duration);
    const ease = 1 - (1 - t) ** 3;
    scale.setVisibleLogicalRange({
      from: from0 + (from1 - from0) * ease,
      to: to0 + (to1 - to0) * ease,
    });
    if (price0 && price1 && cell.series) {
      try {
        cell.series.priceScale().setVisibleRange({
          from: price0.from + (price1.from - price0.from) * ease,
          to: price0.to + (price1.to - price0.to) * ease,
        });
      } catch {
        /* keep last price window */
      }
    }
    if (t < 1) {
      cell.zoomAnim = requestAnimationFrame(tick);
      return;
    }
    cell.zoomAnim = 0;
    scheduleRedraw(cell);
  };
  cell.userZoom = true;
  cell.fitted = true;
  cell.zoomAnim = requestAnimationFrame(tick);
}

function bindZoomControls() {
  const inn = document.getElementById("zoom-in");
  const out = document.getElementById("zoom-out");
  if (inn) inn.onclick = (e) => {
    e.preventDefault();
    zoomActiveChart(0.7);
  };
  if (out) out.onclick = (e) => {
    e.preventDefault();
    zoomActiveChart(1.42);
  };
  if (zoomKeysBound) return;
  zoomKeysBound = true;
  document.addEventListener("keydown", (e) => {
    if (e.target && /^(INPUT|TEXTAREA|SELECT)$/.test(e.target.tagName)) return;
    if (e.key === "+" || e.key === "=") {
      e.preventDefault();
      zoomActiveChart(0.7);
    } else if (e.key === "-" || e.key === "_") {
      e.preventDefault();
      zoomActiveChart(1.42);
    } else if (e.key === "Escape" && state.drawDraft) {
      e.preventDefault();
      state.drawDraft = null;
      scheduleRedraw(activeCell());
    } else if ((e.key === "Enter" || e.key === " ") && state.drawDraft) {
      const draft = state.drawDraft;
      const cell = state.cells[draft.cell];
      if (cell && multiNeed(draft.shape.type) !== null && (draft.shape.points || []).length >= 2) {
        e.preventDefault();
        finishDraft(cell);
      }
    }
  });
}

function createCell(index, symbol) {
  const root = document.querySelector(`.cell[data-index="${index}"]`);
  if (!root || !window.LightweightCharts) return null;
  const holder = root.querySelector(".cell-chart");
  const chart = LightweightCharts.createChart(holder, {
    ...chartTheme(),
    width: holder.clientWidth,
    height: holder.clientHeight || 320,
  });
  const series = chart.addCandlestickSeries({
    upColor: "#26a69a",
    downColor: "#ef5350",
    borderVisible: false,
    wickUpColor: "#26a69a",
    wickDownColor: "#ef5350",
    lastValueVisible: true,
    priceLineVisible: true,
    priceLineWidth: 1,
    priceLineColor: "#26a69a",
  });
  const volume = chart.addHistogramSeries({ priceFormat: { type: "volume" }, priceScaleId: "vol" });
  chart.priceScale("vol").applyOptions({ scaleMargins: { top: 0.8, bottom: 0 } });

  const cell = {
    index,
    symbol,
    chart,
    series,
    volume,
    lines: {},
    osc: null,
    oscSeries: {},
    pack: null,
    fitted: false,
    lastBar: null,
    canvas: root.querySelector(".draw-layer"),
  };
  chart.timeScale().subscribeVisibleLogicalRangeChange(() => scheduleRedraw(cell));
  bindCellDrawing(cell);
  return cell;
}

function destroyCells() {
  state.cells.forEach((cell) => {
    try {
      cell.chart.remove();
    } catch {
      /* already gone */
    }
    if (cell.osc) {
      try {
        cell.osc.remove();
      } catch {
        /* ignore */
      }
    }
  });
  state.cells = [];
}

function teardown() {
  destroyCells();
  if (state.poll) clearInterval(state.poll);
  state.poll = null;
  if (state.cryptoPulse) clearInterval(state.cryptoPulse);
  state.cryptoPulse = null;
  if (state.huntTimer) clearInterval(state.huntTimer);
  state.huntTimer = null;
  if (state.resizeObserver) state.resizeObserver.disconnect();
  if (state.indMenuCloser) {
    document.removeEventListener("click", state.indMenuCloser);
    state.indMenuCloser = null;
  }
  if (state.drawMenuCloser) {
    document.removeEventListener("click", state.drawMenuCloser);
    state.drawMenuCloser = null;
  }
  if (state.langMenuCloser) {
    document.removeEventListener("click", state.langMenuCloser);
    state.langMenuCloser = null;
  }
  const floatingMenu = document.getElementById("ind-menu");
  if (floatingMenu && floatingMenu.parentElement === document.body) floatingMenu.remove();
  const drawMenuEl = document.getElementById("draw-menu");
  if (drawMenuEl && drawMenuEl.parentElement === document.body) drawMenuEl.remove();
  const wall = document.getElementById("paywall");
  if (wall) wall.classList.add("hidden");
  if (state.ws) {
    state.ws.shcClosed = true;
    state.ws.close();
    state.ws = null;
  }
  if (state.futWs) {
    state.futWs.shcClosed = true;
    state.futWs.close();
    state.futWs = null;
  }
  if (state.mkWs) {
    state.mkWs.shcClosed = true;
    state.mkWs.close();
    state.mkWs = null;
  }
  if (state.mkFutWs) {
    state.mkFutWs.shcClosed = true;
    state.mkFutWs.close();
    state.mkFutWs = null;
  }
  if (state.deskWs) {
    state.deskWs.shcClosed = true;
    state.deskWs.close();
    state.deskWs = null;
  }
  if (state.mkPoll) clearInterval(state.mkPoll);
  state.mkPoll = null;
  if (state.quotePulse) clearInterval(state.quotePulse);
  state.quotePulse = null;
  if (state.execTimer) clearInterval(state.execTimer);
  state.execTimer = null;
  if (state.newsTimer) clearInterval(state.newsTimer);
  state.newsTimer = null;
  if (state.agentsTimer) clearInterval(state.agentsTimer);
  state.agentsTimer = null;
  if (state.opsTimer) clearInterval(state.opsTimer);
  state.opsTimer = null;
  if (state.searchCloser) {
    document.removeEventListener("click", state.searchCloser);
    state.searchCloser = null;
  }
}

function layoutCells() {
  state.cells.forEach((cell) => {
    const root = document.querySelector(`.cell[data-index="${cell.index}"]`);
    if (!root) return;
    const holder = root.querySelector(".cell-chart");
    cell.chart.applyOptions({ width: holder.clientWidth, height: holder.clientHeight || 300 });
    const oscHolder = root.querySelector(".cell-osc");
    if (cell.osc && oscHolder && !oscHolder.classList.contains("hidden")) {
      cell.osc.applyOptions({ width: oscHolder.clientWidth, height: 118 });
    }
    scheduleRedraw(cell);
    paintLivePrice(cell);
  });
}

function overlaySeries(cell, key) {
  if (!cell.lines[key]) {
    const style = OVERLAY_STYLES[key] || { color: "#8b98a8", width: 1 };
    cell.lines[key] = cell.chart.addLineSeries({
      color: style.color,
      lineWidth: style.width,
      priceLineVisible: false,
      lastValueVisible: false,
    });
  }
  return cell.lines[key];
}

function ensureOsc(cell) {
  const root = document.querySelector(`.cell[data-index="${cell.index}"]`);
  if (!root) return;
  const holder = root.querySelector(".cell-osc");
  if (isSimple()) {
    if (holder) holder.classList.add("hidden");
    return;
  }
  const need = OSC_IDS.some((id) => state.active.has(id)) && cell.index === state.activeCell;
  holder.classList.toggle("hidden", !need);
  if (!need) {
    if (cell.osc) {
      cell.osc.remove();
      cell.osc = null;
      cell.oscSeries = {};
    }
    return;
  }
  if (!cell.osc) {
    cell.osc = LightweightCharts.createChart(holder, {
      ...chartTheme(),
      width: holder.clientWidth,
      height: 118,
    });
  }
}

function paintOscillators(cell, osc) {
  if (!cell.osc) return;
  const keep = new Set();
  const line = (key, color) => {
    keep.add(key);
    if (!cell.oscSeries[key]) cell.oscSeries[key] = cell.osc.addLineSeries({ color, lineWidth: 2, lastValueVisible: false });
    return cell.oscSeries[key];
  };
  if (state.active.has("macd") && osc.macd) {
    line("macd", "#8b98a8").setData(osc.macd);
    line("signal", "#c8a45a").setData(osc.macd_signal || []);
    keep.add("hist");
    if (!cell.oscSeries.hist) cell.oscSeries.hist = cell.osc.addHistogramSeries({ priceScaleId: "hist" });
    cell.oscSeries.hist.setData(
      (osc.macd_hist || []).map((p) => ({ ...p, color: p.value >= 0 ? "#c8a45a" : "#8a6b2c" })),
    );
  }
  Object.entries(OSC_PAINT).forEach(([id, series]) => {
    if (!state.active.has(id)) return;
    series.forEach(([key, color]) => {
      if (osc[key]) line(key, color).setData(osc[key]);
    });
  });
  Object.keys(cell.oscSeries).forEach((key) => {
    if (keep.has(key)) return;
    try {
      cell.osc.removeSeries(cell.oscSeries[key]);
    } catch {
      /* already detached */
    }
    delete cell.oscSeries[key];
  });
}

function idsQuery() {
  const ids = new Set(state.active);
  ids.add("volume");
  ids.add("atr");
  return [...ids].join(",");
}

function packUrl(symbol) {
  const params = new URLSearchParams({
    symbol,
    timeframe: state.timeframe,
    ids: idsQuery(),
    compression_period: String(state.vrcs.compression_period),
    threshold_multiplier: String(state.vrcs.threshold_multiplier),
    volume_factor: String(state.vrcs.volume_factor),
    lookback_breakout: String(state.vrcs.lookback_breakout),
    limit: state.timeframe === "1s" ? "500" : "400",
  });
  return `/api/indicators/compute?${params}`;
}

function markersFor(cell, pack) {
  const markers = [];
  if (state.active.has("vrcs") && pack.vrcs) {
    pack.vrcs.signals.forEach((s) => {
      markers.push({
        time: s.time,
        position: s.side === "bullish" ? "belowBar" : "aboveBar",
        color: s.confidence >= 90 ? "#ffd479" : s.side === "bullish" ? "#26a69a" : "#ef5350",
        shape: s.side === "bullish" ? "arrowUp" : "arrowDown",
        text: s.label,
      });
    });
  }
  state.journal
    .filter((n) => n.symbol === cell.symbol && n.timeframe === state.timeframe)
    .forEach((n) => {
      markers.push({
        time: Math.floor(n.ts / 1000),
        position: "aboveBar",
        color: "#5b8def",
        shape: "circle",
        text: "📝",
      });
    });
  markers.sort((a, b) => a.time - b.time);
  return markers;
}

async function loadCell(cell, { silent = false } = {}) {
  const url = packUrl(cell.symbol);
  let pack;
  try {
    pack = await apiCached(url, state.timeframe === "1s" ? 2000 : 6000);
  } catch (err) {
    if (!silent) setCellStatus(cell, `<span class="down">${err.message}</span>`);
    return;
  }
  cell.pack = pack;
  const compressed = (pack.vrcs && pack.vrcs.compressed) || [];
  const candles = pack.candles.map((c, i) => {
    const bar = { time: c.time, open: c.open, high: c.high, low: c.low, close: c.close };
    if (state.active.has("vrcs") && compressed[i]) {
      bar.color = c.close >= c.open ? "#1e4f4a" : "#4a2424";
      bar.wickColor = "#c8a45a";
      bar.borderColor = "#c8a45a";
    }
    return bar;
  });
  cell.series.setData(candles);
  cell.lastBar = candles[candles.length - 1] || null;
  cell.series.setMarkers(markersFor(cell, pack));
  cell.volume.setData(pack.volume || []);

  const wanted = new Set(Object.keys(pack.overlays || {}));
  wanted.forEach((key) => overlaySeries(cell, key).setData(pack.overlays[key]));
  Object.keys(cell.lines).forEach((key) => {
    if (!wanted.has(key)) {
      cell.chart.removeSeries(cell.lines[key]);
      delete cell.lines[key];
    }
  });

  ensureOsc(cell);
  paintOscillators(cell, pack.oscillators || {});
  if (!cell.fitted) {
    cell.chart.timeScale().fitContent();
    cell.fitted = true;
  } else if (cell.userZoom && cell.series) {
    try {
      cell.series.priceScale().applyOptions({ autoScale: false });
    } catch {
      /* keep the user's zoom window */
    }
  }
  paintCellHeader(cell);
  paintMarketTypeTabs();
  paintVrcsDashboard(cell);
  if (cell.index === state.activeCell) paintRR(cell);
  if (state.pendingHunt && state.pendingHunt.symbol === cell.symbol) consumePendingHunt(cell);
  void syncPaperMarks(cell);
  /* Alerts and auto-fills come only from the Hunter scan, never from the open chart. */
  scheduleRedraw(cell);
}

function setCellStatus(cell, html) {
  const el = document.querySelector(`.cell[data-index="${cell.index}"] .cell-status`);
  if (el) el.innerHTML = html;
}

function paintCellHeader(cell) {
  const dash = (cell.pack && cell.pack.vrcs && cell.pack.vrcs.dashboard) || null;
  const price = cell.lastBar ? cell.lastBar.close : null;
  const conf = dash ? Number(dash.confidence || 0) : 0;
  const regime = dash ? dash.regime : "normal";
  const badge = conf >= 90 ? "elite" : regime === "compression" ? "coil" : regime.startsWith("spring") ? "spring" : "";
  const el = document.querySelector(`.cell[data-index="${cell.index}"] .cell-meta`);
  if (!el) return;
  el.innerHTML = `<span class="cell-price">${price != null ? price : "—"}</span>
    <span class="badge ${badge}">${t(regime) || regime} · ${conf.toFixed(1)}%</span>
    ${cell.pack && cell.pack.delayed ? `<span class="muted">${t("delayedData")}</span>` : ""}`;
  paintLivePrice(cell);
}

function fmtAxisPrice(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return "—";
  const abs = Math.abs(n);
  if (abs >= 1000) return n.toFixed(2);
  if (abs >= 1) return n.toFixed(4);
  return n.toFixed(6);
}

function paintLivePrice(cell) {
  if (!cell || !cell.series) return;
  const bar = cell.lastBar;
  const badge = document.querySelector(`[data-price-badge="${cell.index}"]`);
  if (!bar) {
    if (badge) badge.classList.add("hidden");
    return;
  }
  const close = Number(bar.close);
  const open = Number(bar.open != null ? bar.open : close);
  const up = close >= open;
  const color = up ? "#26a69a" : "#ef5350";
  try {
    cell.series.applyOptions({
      lastValueVisible: true,
      priceLineVisible: true,
      priceLineColor: color,
      priceLineWidth: 1,
    });
  } catch {
    /* series may be mid-rebuild */
  }
  if (!badge) return;
  const y = cell.series.priceToCoordinate(close);
  if (y == null || !Number.isFinite(y)) {
    badge.classList.add("hidden");
    return;
  }
  badge.textContent = fmtAxisPrice(close);
  badge.classList.toggle("up", up);
  badge.classList.toggle("down", !up);
  badge.classList.remove("hidden");
  badge.style.top = `${Math.round(y)}px`;
}

function paintVrcsDashboard(cell) {
  const box = document.querySelector(`.vrcs-dash[data-dash="${cell.index}"]`);
  if (!box) return;
  const dash = cell.pack && cell.pack.vrcs ? cell.pack.vrcs.dashboard : null;
  const show = !isSimple() && state.active.has("vrcs") && state.vrcs.show_dashboard && dash;
  box.classList.toggle("hidden", !show);
  if (!show) return;
  const parts = dash.parts;
  box.innerHTML = `<strong>SHC VRCS · ${Number(dash.confidence || 0).toFixed(1)}%</strong>
    <div>${cell.symbol} · ${state.timeframe}</div>
    <div>${t(dash.regime) || dash.regime}</div>
    <div>${t("streak")}: ${dash.streak || 0}</div>
    ${parts ? `<div class="muted">${t("coil")} ${parts.streak_pts} · ${t("body")} ${parts.body_pts} · ${t("vol")} ${parts.volume_pts}</div>` : ""}
    ${dash.last_signal && dash.last_signal.calibrated_confidence != null ? `<div class="muted">${t("calibrate")}: ${dash.last_signal.calibrated_confidence}%</div>` : ""}
    <div class="conf-bar"><span style="width:${Math.min(100, Number(dash.confidence || 0))}%"></span></div>
    ${dash.last_signal ? `<div class="${dash.last_signal.side === "bullish" ? "up" : "down"}">${dash.last_signal.label} · ${dash.last_signal.side}</div>` : ""}`;
}

/* ------------------------------------------------------- live Binance feed */

function binanceStreamHost(futures) {
  return futures ? "wss://fstream.binance.com/stream" : "wss://data-stream.binance.vision/stream";
}

function binanceStreamId(symbol) {
  return parseMarketSymbol(symbol).display.replace("/", "").toLowerCase();
}

function binanceSymbol(symbol) {
  return binanceStreamId(symbol);
}

function isCrypto(symbol) {
  return parseMarketSymbol(symbol).crypto || String(symbol || "").includes("/");
}

function chartLiveOn() {
  return state.view === "chart" || state.view === "terminal";
}

function socketLive(socket) {
  if (!socket || socket.readyState !== 1) return false;
  const now = Date.now();
  const opened = socket.shcOpened || 0;
  if (now - opened < 3500) return true;
  return now - (socket.shcLastMsg || 0) < 4000;
}

function paintFeedStatus() {
  const cryptoOn = socketLive(state.ws) || socketLive(state.futWs);
  const deskOn = state.deskWs && state.deskWs.readyState === 1;
  if (cryptoOn || deskOn) {
    setFeedStatus(`${t("live")} ● ${state.timeframe}`, "up");
    return;
  }
  setFeedStatus(t("connecting"), "");
}

function closeLiveSocket(key) {
  const socket = state[key];
  if (!socket) return;
  socket.shcClosed = true;
  socket.close();
  state[key] = null;
}

function applyBinancePayload(cell, payload) {
  if (!cell || !cell.series || !payload) return;
  if (payload.e === "kline" && payload.k) {
    const k = payload.k;
    const bar = {
      time: Math.floor(k.t / 1000),
      open: Number(k.o),
      high: Number(k.h),
      low: Number(k.l),
      close: Number(k.c),
    };
    try {
      cell.series.update(bar);
      cell.volume.update({
        time: bar.time,
        value: Number(k.v),
        color: bar.close >= bar.open ? "#26a69a88" : "#ef535088",
      });
    } catch {
      return;
    }
    cell.lastBar = bar;
    paintCellHeader(cell);
    paintLivePrice(cell);
    void syncPaperMarks(cell);
    const pct = bar.open ? ((bar.close - bar.open) / bar.open) * 100 : 0;
    applyLiveQuote(cell, bar.close, pct);
    if (k.x) {
      cache.delete(packUrl(cell.symbol));
      void loadCell(cell, { silent: true });
    }
    return;
  }
  if (payload.e === "aggTrade" || payload.e === "trade") {
    applyLiveQuote(cell, Number(payload.p), null);
    return;
  }
  if (payload.e === "24hrMiniTicker" || (payload.c != null && payload.s && !payload.k)) {
    const close = Number(payload.c);
    const open = Number(payload.o);
    const pct = open ? ((close - open) / open) * 100 : 0;
    applyLiveQuote(cell, close, pct);
  }
}

function openBinanceSocket(key, cells, futures) {
  closeLiveSocket(key);
  if (!cells.length || !chartLiveOn()) return;
  const interval = BINANCE_TF[state.timeframe] || "15m";
  const tf = futures && interval === "1s" ? "1m" : interval;
  const streams = [];
  cells.forEach((cell) => {
    const id = binanceStreamId(cell.symbol);
    streams.push(`${id}@aggTrade`);
    streams.push(`${id}@kline_${tf}`);
    streams.push(`${id}@miniTicker`);
  });
  const host = binanceStreamHost(futures);
  const socket = new WebSocket(`${host}?streams=${[...new Set(streams)].join("/")}`);
  socket.shcClosed = false;
  socket.shcOpened = Date.now();
  socket.shcLastMsg = 0;
  state[key] = socket;
  const retryKey = key === "futWs" ? "futWsRetry" : "wsRetry";
  socket.onopen = () => {
    if (state[key] !== socket) return;
    socket.shcOpened = Date.now();
    state[retryKey] = 0;
    paintFeedStatus();
  };
  socket.onmessage = (evt) => {
    if (state[key] !== socket) return;
    socket.shcLastMsg = Date.now();
    let msg;
    try {
      msg = JSON.parse(evt.data);
    } catch {
      return;
    }
    const payload = msg.data || msg;
    const streamId = String(msg.stream || payload.s || "").split("@")[0].toLowerCase();
    const cell = state.cells.find((item) => {
      const spec = parseMarketSymbol(item.symbol);
      if (!spec.crypto) return false;
      if ((spec.marketType === "futures") !== futures) return false;
      return binanceStreamId(item.symbol) === streamId;
    });
    if (cell) applyBinancePayload(cell, payload);
  };
  socket.onclose = () => {
    if (socket.shcClosed || state[key] !== socket || !chartLiveOn()) return;
    setFeedStatus(t("connecting"), "down");
    state[retryKey] = Math.min((state[retryKey] || 0) + 1, 6);
    setTimeout(() => {
      if (!chartLiveOn() || state[key] !== socket) return;
      const again = state.cells.filter((item) => {
        const spec = parseMarketSymbol(item.symbol);
        return spec.crypto && (spec.marketType === "futures") === futures;
      });
      openBinanceSocket(key, again, futures);
    }, 1000 * state[retryKey]);
  };
  socket.onerror = () => {
    if (state[key] === socket) setFeedStatus(t("connecting"), "down");
  };
}

function applyLiveQuote(cell, price, pct) {
  const close = Number(price);
  if (!cell || !cell.series || !Number.isFinite(close)) return;
  if (pct == null && cell.lastBar && Number(cell.lastBar.open)) {
    pct = ((close - Number(cell.lastBar.open)) / Number(cell.lastBar.open)) * 100;
  }
  const last = cell.lastBar;
  const bar = last
    ? {
        time: last.time,
        open: last.open,
        high: Math.max(Number(last.high), close),
        low: Math.min(Number(last.low), close),
        close,
      }
    : { time: Math.floor(Date.now() / 1000), open: close, high: close, low: close, close };
  try {
    cell.series.update(bar);
  } catch {
    return;
  }
  cell.lastBar = bar;
  paintCellHeader(cell);
  paintLivePrice(cell);
  void syncPaperMarks(cell);
  const el = document.querySelector(`.cell[data-index="${cell.index}"] .cell-price`);
  if (el) {
    const up = Number(pct) >= 0;
    el.textContent = fmtAxisPrice(close);
    el.className = `cell-price ${up ? "up" : "down"}`;
  }
  if (cell.index === state.activeCell) {
    const tick = document.getElementById("tick");
    if (tick) {
      const change = Number(pct);
      tick.innerHTML = `${t("live")}: <span class="${change >= 0 ? "up" : "down"}">${fmtAxisPrice(close)}</span>
        ${Number.isFinite(change) ? `<span class="${change >= 0 ? "up" : "down"}">(${change.toFixed(2)}%)</span>` : ""}`;
    }
  }
}

function connectDeskFeed() {
  if (state.deskWs) {
    state.deskWs.shcClosed = true;
    state.deskWs.close();
    state.deskWs = null;
  }
  const desk = state.cells.filter((cell) => cell && cell.symbol);
  if (!desk.length || !chartLiveOn()) return;
  const proto = location.protocol === "https:" ? "wss" : "ws";
  const symbols = desk.map((cell) => cell.symbol).slice(0, 8).join(",");
  const socket = new WebSocket(`${proto}://${location.host}/api/ws/market?symbols=${encodeURIComponent(symbols)}`);
  socket.shcClosed = false;
  state.deskWs = socket;
  socket.onopen = () => {
    if (state.deskWs === socket) paintFeedStatus();
  };
  socket.onmessage = (evt) => {
    if (state.deskWs !== socket) return;
    let msg;
    try {
      msg = JSON.parse(evt.data);
    } catch {
      return;
    }
    const rows = Array.isArray(msg.quotes) ? msg.quotes : [msg];
    rows.forEach((row) => {
      if (!row || row.error || row.price == null) return;
      const cell = state.cells.find((item) => item.symbol === row.symbol);
      if (cell) applyLiveQuote(cell, row.price, row.percentage);
    });
  };
  socket.onclose = () => {
    if (socket.shcClosed || state.deskWs !== socket || !chartLiveOn()) return;
    setTimeout(() => {
      if (chartLiveOn() && state.deskWs === socket) connectDeskFeed();
    }, 2000);
  };
}

function connectLiveFeed() {
  const cryptoCells = state.cells.filter((cell) => parseMarketSymbol(cell.symbol).crypto);
  const spot = cryptoCells.filter((cell) => !isFuturesSymbol(cell.symbol));
  const fut = cryptoCells.filter((cell) => isFuturesSymbol(cell.symbol));
  if (spot.length || fut.length) setFeedStatus(t("connecting"), "");
  openBinanceSocket("ws", spot, false);
  openBinanceSocket("futWs", fut, true);
  connectDeskFeed();
  startPoll();
  startLiveQuoteGuard();
}

function huntUrl({ top = 40, min = 70, spike = 1.5 } = {}) {
  const tf = state.timeframe === "1s" ? "1m" : state.timeframe;
  const venue = state.venue || "crypto";
  return `/api/hunter/scan?venue=${encodeURIComponent(venue)}&timeframe=${tf}&top=${top}&min_confidence=${min}&volume_spike=${spike}`;
}

function huntSide(hit) {
  if (!hit) return "bullish";
  if (hit.side === "bearish" || hit.side === "bullish") return hit.side;
  return String(hit.state || "").includes("bear") ? "bearish" : "bullish";
}

function consumePendingHunt(cell) {
  const hit = state.pendingHunt;
  if (!hit || !cell || hit.symbol !== cell.symbol) return;
  const side = huntSide(hit);
  state.risk.side = side;
  persist("shc_risk", state.risk);
  const entry = Number(hit.entry || (hit.signal && hit.signal.price) || (cell.lastBar && cell.lastBar.close));
  const stop = Number(hit.stop);
  const target = Number(hit.target);
  const levels =
    Number.isFinite(entry) && Number.isFinite(stop) && Number.isFinite(target)
      ? { entry, stop, target, side }
      : { ...riskLevels(cell, side), ...(Number.isFinite(entry) ? { entry } : {}) };
  applyRiskLines(cell, levels);
  const paintBox = () => {
    const box = document.getElementById("rr-box");
    if (!box) return;
    box.dataset.symbol = cell.symbol;
    fillRiskInputs(levels);
    paintRiskSides(box, side, cell);
    updateRiskMath();
  };
  if (!isSimple()) {
    state.panel = "brain";
    void renderPanel().then(paintBox);
  } else {
    paintBox();
  }
  state.pendingHunt = null;
}

function applyHuntToChart(hit) {
  if (!hit || !hit.symbol) return;
  state.pendingHunt = hit;
  if (!state.mkHunter) state.mkHunter = {};
  state.mkHunter[hit.symbol] = hit;
  state.venue = hit.venue || venueOf(hit.symbol);
  persist("shc_venue", state.venue);
  const cell = activeCell();
  if (state.view === "chart" && cell && cell.symbol === hit.symbol && cell.pack) {
    consumePendingHunt(cell);
    return;
  }
  if (state.view === "chart") {
    setCellSymbol(state.activeCell, hit.symbol);
    return;
  }
  openOnChart(hit.symbol);
}

function paintDeskHunt(data) {
  const strip = document.getElementById("desk-hunt");
  if (!strip) return;
  const hits = filterHuntHits((data && data.hits) || []);
  if (!hits.length) {
    strip.hidden = false;
    strip.innerHTML = `<span class="muted small">${t("huntingMarket")} · ${t(state.venue)} · ${data && data.scanned ? data.scanned : 0} · —</span>`;
    return;
  }
  strip.hidden = false;
  strip.innerHTML = hits
    .slice(0, 12)
    .map((hit) => {
      const dir = huntSide(hit) === "bearish" ? "down" : "up";
      return `<button type="button" class="desk-hit ${hit.confidence >= 90 ? "elite" : ""}" data-hunt-sym="${escapeHtml(hit.symbol)}">
        ${assetLogo(hit.symbol, { size: "sm" })}
        <span>${escapeHtml(hit.symbol)}<small class="muted"> ${t(hit.state) || hit.state}</small></span>
        <span class="${dir}">${Number(hit.confidence || 0).toFixed(0)}%</span>
      </button>`;
    })
    .join("");
  strip.querySelectorAll("[data-hunt-sym]").forEach((btn) => {
    btn.onclick = () => {
      const hit = hits.find((item) => item.symbol === btn.dataset.huntSym);
      applyHuntToChart(hit || { symbol: btn.dataset.huntSym });
    };
  });
}

async function runDeskHunter({ auto = false } = {}) {
  const url = huntUrl({ top: 40, min: 70, spike: 1.5 });
  if (state.huntFlight && state.huntFlight.url === url) return state.huntFlight.promise;
  const strip = document.getElementById("desk-hunt");
  if (strip) {
    strip.hidden = false;
    strip.innerHTML = `<span class="muted small">${t("huntingMarket")} · ${t(state.venue)}</span>`;
  }
  const promise = (async () => {
    try {
      const data = await apiCached(url, 40000);
      state.lastHunt = data;
      state.mkHunter = {};
      data.hits = filterHuntHits(data.hits);
      data.elite = filterHuntHits(data.elite);
      data.quiet_surges = filterHuntHits(data.quiet_surges);
      [...(data.hits || []), ...(data.elite || [])].forEach((hit) => {
        if (hit && hit.symbol) state.mkHunter[hit.symbol] = hit;
      });
      paintDeskHunt(data);
      (data.elite || []).forEach((hit) => {
        if (hit.signal) fireEliteAlert(hit.symbol, data.timeframe, hit.signal);
      });
      return data;
    } catch (err) {
      if (strip) strip.innerHTML = `<span class="down small">${err.message}</span>`;
      throw err;
    } finally {
      if (state.huntFlight && state.huntFlight.url === url) state.huntFlight = null;
    }
  })();
  state.huntFlight = { url, promise };
  return promise;
}

function setVenue(venue, { rescan = true } = {}) {
  const next = MARKET_VENUES.includes(venue) ? venue : "crypto";
  state.venue = next;
  state.mkVenue = next;
  persist("shc_venue", next);
  persist("shc_mk_venue", next);
  document.querySelectorAll("[data-desk-venue], [data-mk-venue], [data-venue]").forEach((el) => {
    const value = el.dataset.deskVenue || el.dataset.mkVenue || el.dataset.venue;
    el.classList.toggle("active", value === next);
  });
  if (rescan) {
    cache.delete(huntUrl({ top: 40, min: 70, spike: 1.5 }));
    if (!isSimple() && state.view === "chart" && (state.panel === "agents" || state.panel === "analytics")) {
      state.panel = "brain";
    }
    void runDeskHunter({ auto: true })
      .then(() => {
        if (!isSimple() && state.view === "chart") void renderPanel();
      })
      .catch(() => {});
  }
}

function bindDeskVenues() {
  document.querySelectorAll("[data-desk-venue]").forEach((btn) => {
    btn.onclick = () => {
      if (btn.dataset.deskVenue !== "crypto" && !can("live_equities") && !can("delayed_equities")) {
        paywall("live_equities");
        return;
      }
      setVenue(btn.dataset.deskVenue);
      paintMarketTypeTabs();
    };
  });
}

function paintMarketTypeTabs() {
  const tabs = document.getElementById("mkt-type-tabs");
  if (!tabs) return;
  const cell = activeCell();
  const crypto = !!(cell && venueOf(cell.symbol) === "crypto");
  tabs.classList.toggle("hidden", !crypto);
  const kind = cell ? parseMarketSymbol(cell.symbol).marketType || "spot" : "spot";
  tabs.querySelectorAll("[data-mkt]").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.mkt === kind);
  });
}

function bindMarketTypeTabs() {
  const tabs = document.getElementById("mkt-type-tabs");
  if (!tabs) return;
  tabs.querySelectorAll("[data-mkt]").forEach((btn) => {
    btn.onclick = () => {
      const cell = activeCell();
      if (!cell || venueOf(cell.symbol) !== "crypto") return;
      const spec = parseMarketSymbol(cell.symbol);
      const next = btn.dataset.mkt === "futures" ? `${spec.display}:FUT` : spec.display;
      setCellSymbol(state.activeCell, next);
    };
  });
  paintMarketTypeTabs();
}

function watchHunter() {
  if (state.huntTimer) clearInterval(state.huntTimer);
  state.huntTimer = setInterval(() => {
    void runDeskHunter({ auto: true }).catch(() => {});
  }, 90000);
  void runDeskHunter({ auto: true }).catch(() => {});
}

function setFeedStatus(text, cls) {
  const el = document.getElementById("feed-status");
  if (el) el.innerHTML = `<span class="${cls}">${text}</span>`;
}

function startPoll() {
  if (state.poll) clearInterval(state.poll);
  const hasStock = state.cells.some((c) => !isCrypto(c.symbol));
  const ms = hasStock ? 4000 : state.timeframe === "1s" ? 4000 : 20000;
  state.poll = setInterval(() => {
    state.cells.forEach((cell) => {
      if (!isCrypto(cell.symbol) || state.timeframe === "1s") {
        cache.delete(packUrl(cell.symbol));
      }
      void loadCell(cell, { silent: true });
    });
  }, ms);
}

function startLiveQuoteGuard() {
  if (state.cryptoPulse) clearInterval(state.cryptoPulse);
  const tick = async () => {
    if (!chartLiveOn()) return;
    const cells = state.cells.filter((cell) => parseMarketSymbol(cell.symbol).crypto);
    if (!cells.length) return;
    const spotLive = socketLive(state.ws);
    const futLive = socketLive(state.futWs);
    const need = cells.filter((cell) => (isFuturesSymbol(cell.symbol) ? !futLive : !spotLive));
    if (!need.length) return;
    try {
      const data = await api(`/api/market/quotes?symbols=${encodeURIComponent(need.map((cell) => cell.symbol).join(","))}`);
      (data.quotes || []).forEach((row) => {
        const cell = state.cells.find(
          (item) => item.symbol === row.symbol || normalizeDeskSymbol(item.symbol) === normalizeDeskSymbol(row.symbol),
        );
        if (cell && (row.last != null || row.price != null)) {
          applyLiveQuote(cell, row.last != null ? row.last : row.price, row.percentage);
        }
      });
    } catch {
      /* keep last tick */
    }
  };
  state.cryptoPulse = setInterval(tick, 2500);
  void tick();
}

function startQuotePulse(symbols, view) {
  if (state.quotePulse) {
    clearInterval(state.quotePulse);
    state.quotePulse = null;
  }
  const desk = [...new Set((symbols || []).filter((item) => item && !isCrypto(item)))].slice(0, 24);
  if (!desk.length) return;
  const tick = async () => {
    if (state.view !== view) return;
    try {
      const data = await api(`/api/market/quotes?symbols=${encodeURIComponent(desk.join(","))}`);
      (data.quotes || []).forEach((row) => applyQuotePatch(row.symbol, row.last, row.percentage));
    } catch {
      /* keep last painted ticks */
    }
  };
  void tick();
  state.quotePulse = setInterval(tick, 4000);
}

/* ------------------------------------------------------------- drawings */

let redrawHandle = null;

function scheduleRedraw(cell) {
  if (redrawHandle) cancelAnimationFrame(redrawHandle);
  redrawHandle = requestAnimationFrame(() => {
    redrawHandle = null;
    state.cells.forEach((c) => redrawCell(c));
  });
}

function toXY(cell, point) {
  return {
    x: cell.chart.timeScale().timeToCoordinate(point.time),
    y: cell.series.priceToCoordinate(point.price),
  };
}

function validXY(p) {
  return p && p.x != null && p.y != null && Number.isFinite(p.x) && Number.isFinite(p.y);
}

function mappedPoints(cell, item) {
  const raw = item.points && item.points.length ? item.points.slice() : [];
  if (item.a) raw.unshift(item.a);
  if (item.b && (!raw.length || raw[raw.length - 1] !== item.b)) raw.push(item.b);
  if (state.drawDraft && state.drawDraft.shape === item && item.b) {
    const last = raw[raw.length - 1];
    if (!last || last.time !== item.b.time || last.price !== item.b.price) raw.push(item.b);
  }
  const seen = new Set();
  const uniq = [];
  raw.forEach((pt) => {
    if (!pt) return;
    const key = `${pt.time}:${pt.price}`;
    if (seen.has(key)) return;
    seen.add(key);
    uniq.push(pt);
  });
  return uniq.map((pt) => toXY(cell, pt)).filter(validXY);
}

function strokePoints(ctx, pts, smooth) {
  if (pts.length < 2) return;
  ctx.beginPath();
  if (!smooth || pts.length === 2) {
    ctx.moveTo(pts[0].x, pts[0].y);
    pts.slice(1).forEach((p) => ctx.lineTo(p.x, p.y));
  } else {
    ctx.moveTo(pts[0].x, pts[0].y);
    for (let i = 1; i < pts.length - 1; i += 1) {
      ctx.quadraticCurveTo(pts[i].x, pts[i].y, (pts[i].x + pts[i + 1].x) / 2, (pts[i].y + pts[i + 1].y) / 2);
    }
    const last = pts[pts.length - 1];
    ctx.quadraticCurveTo(last.x, last.y, last.x, last.y);
  }
  ctx.stroke();
}

function arrowHead(ctx, x1, y1, x2, y2, size = 11) {
  const ang = Math.atan2(y2 - y1, x2 - x1);
  ctx.beginPath();
  ctx.moveTo(x2, y2);
  ctx.lineTo(x2 - size * Math.cos(ang - 0.46), y2 - size * Math.sin(ang - 0.46));
  ctx.lineTo(x2 - size * Math.cos(ang + 0.46), y2 - size * Math.sin(ang + 0.46));
  ctx.closePath();
  ctx.fill();
}

function barsInRange(cell, t0, t1) {
  const candles = (cell.pack && cell.pack.candles) || [];
  const vols = (cell.pack && cell.pack.volume) || [];
  const volMap = {};
  vols.forEach((v) => {
    volMap[v.time] = v.value;
  });
  const lo = Math.min(t0, t1);
  const hi = Math.max(t0, t1);
  return candles.filter((c) => c.time >= lo && c.time <= hi).map((c) => ({ ...c, volume: volMap[c.time] || 0 }));
}

function volumeBins(bars, bins = 28) {
  if (!bars.length) return [];
  let lo = Math.min(...bars.map((b) => b.low));
  let hi = Math.max(...bars.map((b) => b.high));
  const span = hi - lo || 1;
  const counts = Array(bins).fill(0);
  bars.forEach((b) => {
    const mid = (b.high + b.low) / 2;
    const i = Math.min(bins - 1, Math.max(0, Math.floor(((mid - lo) / span) * bins)));
    counts[i] += b.volume || 1;
  });
  const max = Math.max(...counts, 1);
  return counts.map((v, i) => ({
    price0: lo + (span * i) / bins,
    price1: lo + (span * (i + 1)) / bins,
    ratio: v / max,
  }));
}

function anchoredVwapPoints(cell, fromTime) {
  const candles = (cell.pack && cell.pack.candles) || [];
  const vols = (cell.pack && cell.pack.volume) || [];
  const volMap = {};
  vols.forEach((v) => {
    volMap[v.time] = v.value;
  });
  let pv = 0;
  let vv = 0;
  const out = [];
  candles.forEach((c) => {
    if (c.time < fromTime) return;
    const typical = (c.high + c.low + c.close) / 3;
    const vol = volMap[c.time] || 1;
    pv += typical * vol;
    vv += vol;
    out.push({ time: c.time, price: pv / (vv || 1) });
  });
  return out;
}

function fmtDur(t0, t1) {
  const s = Math.abs(Number(t1) - Number(t0));
  if (s < 120) return `${Math.round(s)}s`;
  if (s < 7200) return `${Math.round(s / 60)}m`;
  if (s < 172800) return `${(s / 3600).toFixed(1)}h`;
  return `${Math.round(s / 86400)}d`;
}

function paintVolumeProfile(ctx, cell, item, anchored) {
  const t0 = item.a.time;
  const t1 = anchored && cell.lastBar ? cell.lastBar.time : item.b.time;
  const x0 = cell.chart.timeScale().timeToCoordinate(Math.min(t0, t1));
  const x1 = cell.chart.timeScale().timeToCoordinate(Math.max(t0, t1));
  if (x0 == null || x1 == null) return;
  const left = Math.min(x0, x1);
  const width = Math.max(36, Math.abs(x1 - x0));
  const bins = volumeBins(barsInRange(cell, t0, t1));
  bins.forEach((bin) => {
    const y0 = cell.series.priceToCoordinate(bin.price0);
    const y1 = cell.series.priceToCoordinate(bin.price1);
    if (y0 == null || y1 == null) return;
    ctx.fillStyle = "rgba(200,164,90,0.28)";
    ctx.fillRect(left, Math.min(y0, y1), width * bin.ratio, Math.max(1, Math.abs(y1 - y0)));
  });
  ctx.strokeStyle = DRAW_GOLD;
  const ya = cell.series.priceToCoordinate(item.a.price);
  const yb = cell.series.priceToCoordinate(item.b.price);
  if (ya != null && yb != null) ctx.strokeRect(left, Math.min(ya, yb), width, Math.abs(yb - ya));
}

function paintPosition(ctx, cell, item, side) {
  const a = toXY(cell, item.a);
  const b = toXY(cell, item.b);
  if (!validXY(a) || !validXY(b)) return;
  const entry = item.a.price;
  const other = item.b.price;
  let tp;
  let sl;
  if (side === "long") {
    if (other >= entry) {
      tp = other;
      sl = entry - (tp - entry) / 2;
    } else {
      sl = other;
      tp = entry + (entry - sl) * 2;
    }
  } else if (other <= entry) {
    tp = other;
    sl = entry + (entry - tp) / 2;
  } else {
    sl = other;
    tp = entry - (sl - entry) * 2;
  }
  const yEntry = cell.series.priceToCoordinate(entry);
  const yTp = cell.series.priceToCoordinate(tp);
  const ySl = cell.series.priceToCoordinate(sl);
  if (yEntry == null || yTp == null || ySl == null) return;
  const x0 = Math.min(a.x, b.x);
  const x1 = Math.max(a.x, b.x);
  const w = Math.max(24, x1 - x0);
  ctx.fillStyle = side === "long" ? "rgba(38,166,154,0.18)" : "rgba(239,83,80,0.18)";
  ctx.fillRect(x0, Math.min(yEntry, yTp), w, Math.abs(yTp - yEntry));
  ctx.fillStyle = side === "long" ? "rgba(239,83,80,0.16)" : "rgba(38,166,154,0.16)";
  ctx.fillRect(x0, Math.min(yEntry, ySl), w, Math.abs(ySl - yEntry));
  ctx.strokeStyle = DRAW_GOLD;
  ctx.strokeRect(x0, Math.min(yTp, ySl), w, Math.abs(yTp - ySl));
  ctx.beginPath();
  ctx.moveTo(x0, yEntry);
  ctx.lineTo(x0 + w, yEntry);
  ctx.stroke();
  ctx.fillStyle = DRAW_GOLD;
  ctx.font = "11px IBM Plex Sans";
  const rr = Math.abs(tp - entry) / (Math.abs(entry - sl) || 1);
  ctx.fillText(`${t(side === "long" ? "longPos" : "shortPos")}  ${rr.toFixed(2)}R`, x0 + 6, Math.min(yTp, ySl) + 14);
  ctx.fillText(`${entry.toFixed(4)} → ${tp.toFixed(4)}`, x0 + 6, yEntry - 4);
}

function paintShape(ctx, cell, item, w) {
  const gold = item.color || DRAW_GOLD;
  ctx.strokeStyle = gold;
  ctx.fillStyle = gold;
  ctx.lineWidth = item.type === "brush" || item.type === "highlighter" ? 8 : 1.5;
  ctx.lineCap = "round";
  ctx.lineJoin = "round";
  ctx.setLineDash([]);
  ctx.font = "11px IBM Plex Sans";

  if (item.type === "hline") {
    const y = cell.series.priceToCoordinate(item.price != null ? item.price : item.a && item.a.price);
    if (y == null) return;
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(w, y);
    ctx.stroke();
    const px = item.price != null ? item.price : item.a.price;
    ctx.fillText(`${item.label ? `${item.label} ` : ""}${Number(px).toFixed(4)}`, 4, y - 4);
    return;
  }

  if (item.type === "arrowUp" || item.type === "arrowDown" || item.type === "arrowMark") {
    const p = toXY(cell, item.a || { time: item.time, price: item.price });
    if (!validXY(p)) return;
    ctx.beginPath();
    if (item.type === "arrowUp") {
      ctx.moveTo(p.x, p.y - 14);
      ctx.lineTo(p.x - 8, p.y + 6);
      ctx.lineTo(p.x + 8, p.y + 6);
    } else if (item.type === "arrowDown") {
      ctx.moveTo(p.x, p.y + 14);
      ctx.lineTo(p.x - 8, p.y - 6);
      ctx.lineTo(p.x + 8, p.y - 6);
    } else {
      ctx.moveTo(p.x, p.y - 16);
      ctx.lineTo(p.x + 12, p.y + 4);
      ctx.lineTo(p.x + 3, p.y + 4);
      ctx.lineTo(p.x + 3, p.y + 14);
      ctx.lineTo(p.x - 3, p.y + 14);
      ctx.lineTo(p.x - 3, p.y + 4);
      ctx.lineTo(p.x - 12, p.y + 4);
    }
    ctx.closePath();
    ctx.fillStyle = gold;
    ctx.fill();
    ctx.strokeStyle = DRAW_INK;
    ctx.lineWidth = 1;
    ctx.stroke();
    return;
  }

  if (item.type === "anchoredVwap") {
    const pts = anchoredVwapPoints(cell, item.a.time).map((pt) => toXY(cell, pt)).filter(validXY);
    ctx.lineWidth = 2;
    strokePoints(ctx, pts, true);
    return;
  }
  if (item.type === "vrFixed" || item.type === "vrAnchored") {
    paintVolumeProfile(ctx, cell, item, item.type === "vrAnchored");
    return;
  }
  if (item.type === "longPos" || item.type === "shortPos") {
    paintPosition(ctx, cell, item, item.type === "longPos" ? "long" : "short");
    return;
  }

  const a = item.a ? toXY(cell, item.a) : null;
  const b = item.b ? toXY(cell, item.b) : null;
  const pts = mappedPoints(cell, item);

  if (item.type === "brush") {
    ctx.strokeStyle = "rgba(200,164,90,0.72)";
    strokePoints(ctx, pts, true);
    return;
  }
  if (item.type === "path" || item.type === "curve") {
    strokePoints(ctx, pts, true);
    return;
  }
  if (item.type === "polyline") {
    strokePoints(ctx, pts, false);
    return;
  }
  if (item.type === "ghostPath") {
    ctx.setLineDash([5, 4]);
    strokePoints(ctx, pts, true);
    ctx.setLineDash([]);
    return;
  }
  if (item.type === "doubleCurve" && pts.length >= 3) {
    ctx.beginPath();
    ctx.moveTo(pts[0].x, pts[0].y);
    ctx.quadraticCurveTo(pts[1].x, pts[1].y, (pts[1].x + (pts[2] || pts[1]).x) / 2, (pts[1].y + (pts[2] || pts[1]).y) / 2);
    if (pts[2] && pts[3]) ctx.quadraticCurveTo(pts[2].x, pts[2].y, pts[3].x, pts[3].y);
    else if (pts[2]) ctx.quadraticCurveTo(pts[2].x, pts[2].y, pts[2].x, pts[2].y);
    ctx.stroke();
    return;
  }
  if (item.type === "pitchfork" && pts.length >= 3) {
    const [p0, p1, p2] = pts;
    const mid = { x: (p1.x + p2.x) / 2, y: (p1.y + p2.y) / 2 };
    const dx = mid.x - p0.x;
    const dy = mid.y - p0.y;
    const extend = 2.4;
    const end = { x: p0.x + dx * extend, y: p0.y + dy * extend };
    const o1 = { x: p1.x + dx * (extend - 1), y: p1.y + dy * (extend - 1) };
    const o2 = { x: p2.x + dx * (extend - 1), y: p2.y + dy * (extend - 1) };
    ctx.beginPath();
    ctx.moveTo(p0.x, p0.y);
    ctx.lineTo(end.x, end.y);
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(o1.x, o1.y);
    ctx.moveTo(p2.x, p2.y);
    ctx.lineTo(o2.x, o2.y);
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.stroke();
    return;
  }

  if (!validXY(a) || !validXY(b)) return;
  const x = Math.min(a.x, b.x);
  const y = Math.min(a.y, b.y);
  const rw = Math.abs(b.x - a.x);
  const rh = Math.abs(b.y - a.y);

  if (item.type === "trend" || item.type === "arrow") {
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.stroke();
    if (item.type === "arrow") {
      ctx.fillStyle = gold;
      arrowHead(ctx, a.x, a.y, b.x, b.y);
    }
    return;
  }
  if (item.type === "rect" || item.type === "highlighter" || item.type === "datePriceRange") {
    ctx.fillStyle = item.type === "highlighter" ? "rgba(242,217,138,0.22)" : "rgba(200,164,90,0.12)";
    ctx.fillRect(x, y, rw, rh);
    if (item.type !== "highlighter") ctx.strokeRect(x, y, rw, rh);
    if (item.type === "datePriceRange") {
      ctx.fillStyle = gold;
      const chg = ((item.b.price - item.a.price) / (item.a.price || 1)) * 100;
      ctx.fillText(`${fmtDur(item.a.time, item.b.time)} · ${chg.toFixed(2)}%`, x + 6, y + 14);
    }
    return;
  }
  if (item.type === "rectTilt") {
    const cx = (a.x + b.x) / 2;
    const cy = (a.y + b.y) / 2;
    ctx.save();
    ctx.translate(cx, cy);
    ctx.rotate(Math.PI / 7);
    ctx.fillStyle = "rgba(200,164,90,0.12)";
    ctx.fillRect(-rw / 2, -rh / 2, rw, rh);
    ctx.strokeRect(-rw / 2, -rh / 2, rw, rh);
    ctx.restore();
    return;
  }
  if (item.type === "circle" || item.type === "ellipse") {
    const rx = item.type === "circle" ? Math.hypot(b.x - a.x, b.y - a.y) : rw / 2;
    const ry = item.type === "circle" ? rx : rh / 2;
    const cx = item.type === "circle" ? a.x : (a.x + b.x) / 2;
    const cy = item.type === "circle" ? a.y : (a.y + b.y) / 2;
    ctx.beginPath();
    ctx.ellipse(cx, cy, Math.max(2, rx), Math.max(2, ry), 0, 0, Math.PI * 2);
    ctx.fillStyle = "rgba(200,164,90,0.10)";
    ctx.fill();
    ctx.stroke();
    return;
  }
  if (item.type === "triangle") {
    ctx.beginPath();
    ctx.moveTo((a.x + b.x) / 2, Math.min(a.y, b.y));
    ctx.lineTo(Math.min(a.x, b.x), Math.max(a.y, b.y));
    ctx.lineTo(Math.max(a.x, b.x), Math.max(a.y, b.y));
    ctx.closePath();
    ctx.fillStyle = "rgba(200,164,90,0.10)";
    ctx.fill();
    ctx.stroke();
    return;
  }
  if (item.type === "arc") {
    const r = Math.hypot(b.x - a.x, b.y - a.y);
    ctx.beginPath();
    ctx.arc(a.x, a.y, Math.max(4, r), Math.atan2(b.y - a.y, b.x - a.x) - Math.PI / 2, Math.atan2(b.y - a.y, b.x - a.x) + Math.PI / 2);
    ctx.stroke();
    return;
  }
  if (item.type === "fib") {
    const levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1];
    ctx.font = "10px IBM Plex Sans";
    levels.forEach((lv) => {
      const yy = a.y + (b.y - a.y) * lv;
      const price = item.a.price + (item.b.price - item.a.price) * lv;
      ctx.setLineDash(lv === 0 || lv === 1 ? [] : [4, 4]);
      ctx.beginPath();
      ctx.moveTo(Math.min(a.x, b.x), yy);
      ctx.lineTo(Math.max(a.x, b.x), yy);
      ctx.stroke();
      ctx.fillStyle = "#8b98a8";
      ctx.fillText(`${(lv * 100).toFixed(1)}% ${price.toFixed(4)}`, Math.min(a.x, b.x) + 4, yy - 3);
    });
    ctx.setLineDash([]);
    return;
  }
  if (item.type === "forecastPos") {
    ctx.setLineDash([6, 4]);
    ctx.beginPath();
    ctx.moveTo(a.x, a.y);
    ctx.lineTo(b.x, b.y);
    ctx.lineTo(b.x + (b.x - a.x) * 0.45, b.y + (b.y - a.y) * 0.45);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.fillStyle = "rgba(200,164,90,0.14)";
    ctx.fillRect(x, y, rw, rh);
    ctx.strokeRect(x, y, rw, rh);
    ctx.fillStyle = gold;
    ctx.fillText(t("forecastPos"), x + 6, y + 14);
    return;
  }
  if (item.type === "barPattern") {
    const n = 6;
    for (let i = 0; i < n; i += 1) {
      const cx = x + (rw / n) * (i + 0.5);
      const wave = Math.sin(i * 1.1) * rh * 0.28;
      const body = rh * 0.22;
      ctx.strokeStyle = gold;
      ctx.beginPath();
      ctx.moveTo(cx, y + rh * 0.15);
      ctx.lineTo(cx, y + rh * 0.85);
      ctx.stroke();
      ctx.fillStyle = i % 2 ? "rgba(38,166,154,0.55)" : "rgba(239,83,80,0.55)";
      ctx.fillRect(cx - 4, y + rh * 0.4 + wave, 8, body);
    }
    ctx.strokeStyle = gold;
    ctx.strokeRect(x, y, rw, rh);
    return;
  }
  if (item.type === "priceRange") {
    const midX = (a.x + b.x) / 2;
    ctx.beginPath();
    ctx.moveTo(midX, a.y);
    ctx.lineTo(midX, b.y);
    ctx.stroke();
    arrowHead(ctx, midX, b.y, midX, a.y, 8);
    arrowHead(ctx, midX, a.y, midX, b.y, 8);
    const chg = item.b.price - item.a.price;
    const pct = (chg / (item.a.price || 1)) * 100;
    ctx.fillText(`${chg.toFixed(4)} (${pct.toFixed(2)}%)`, midX + 8, (a.y + b.y) / 2);
    return;
  }
  if (item.type === "timeRange") {
    const midY = (a.y + b.y) / 2;
    ctx.beginPath();
    ctx.moveTo(a.x, midY);
    ctx.lineTo(b.x, midY);
    ctx.stroke();
    arrowHead(ctx, b.x, midY, a.x, midY, 8);
    arrowHead(ctx, a.x, midY, b.x, midY, 8);
    ctx.fillText(fmtDur(item.a.time, item.b.time), (a.x + b.x) / 2 - 12, midY - 6);
  }
}

function redrawCell(cell) {
  const canvas = cell.canvas;
  if (!canvas) return;
  const holder = canvas.parentElement;
  const dpr = window.devicePixelRatio || 1;
  const w = holder.clientWidth;
  const h = holder.clientHeight || 320;
  if (canvas.width !== w * dpr || canvas.height !== h * dpr) {
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width = `${w}px`;
    canvas.style.height = `${h}px`;
  }
  const ctx = canvas.getContext("2d");
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  ctx.clearRect(0, 0, w, h);
  const items = (state.drawings[drawKey(cell.symbol)] || []).slice();
  if (state.drawDraft && state.drawDraft.cell === cell.index) items.push(state.drawDraft.shape);
  items.forEach((item) => paintShape(ctx, cell, item, w));
  paintLivePrice(cell);
}

function cellPoint(cell, evt) {
  const rect = cell.canvas.getBoundingClientRect();
  const x = evt.clientX - rect.left;
  const y = evt.clientY - rect.top;
  const time = cell.chart.timeScale().coordinateToTime(x);
  const price = cell.series.coordinateToPrice(y);
  if (time == null || price == null) return null;
  return { time, price };
}

function saveDrawings() {
  persist("shc_draw", state.drawings);
}

function finishDraft(cell) {
  if (!state.drawDraft || state.drawDraft.cell !== cell.index) return;
  const shape = { ...state.drawDraft.shape, color: state.drawDraft.shape.color || DRAW_GOLD };
  if (shape.points && shape.points.length) {
    shape.a = shape.points[0];
    shape.b = shape.points[shape.points.length - 1];
    if (shape.points.length < 2 && multiNeed(shape.type) !== null) {
      state.drawDraft = null;
      scheduleRedraw(cell);
      return;
    }
  }
  const key = drawKey(cell.symbol);
  state.drawings[key] = state.drawings[key] || [];
  state.drawings[key].push(shape);
  state.drawDraft = null;
  saveDrawings();
  scheduleRedraw(cell);
}

function commitShape(cell, shape) {
  const key = drawKey(cell.symbol);
  state.drawings[key] = state.drawings[key] || [];
  state.drawings[key].push({ color: DRAW_GOLD, ...shape });
  saveDrawings();
  scheduleRedraw(cell);
}

function bindCellDrawing(cell) {
  const canvas = cell.canvas;
  if (!canvas) return;
  canvas.classList.toggle("active", state.drawTool !== "cursor");
  canvas.oncontextmenu = (evt) => evt.preventDefault();
  canvas.onmousedown = (evt) => {
    if (state.drawTool === "cursor") return;
    evt.preventDefault();
    const pt = cellPoint(cell, evt);
    if (!pt) return;
    const tool = state.drawTool;
    if (DRAW_CLICK.has(tool)) {
      if (tool === "hline") commitShape(cell, { type: "hline", price: pt.price });
      else commitShape(cell, { type: tool, a: pt, b: pt, price: pt.price });
      return;
    }
    if (DRAW_FREEHAND.has(tool)) {
      state.drawDraft = { cell: cell.index, shape: { type: tool, points: [pt], a: pt, b: pt, color: DRAW_GOLD } };
      return;
    }
    const need = multiNeed(tool);
    if (need !== null) {
      if (state.drawDraft && state.drawDraft.cell === cell.index && state.drawDraft.shape.type === tool) {
        state.drawDraft.shape.points.push(pt);
        state.drawDraft.shape.b = pt;
        if (need && state.drawDraft.shape.points.length >= need) finishDraft(cell);
        else scheduleRedraw(cell);
      } else {
        state.drawDraft = { cell: cell.index, shape: { type: tool, points: [pt], a: pt, b: pt, color: DRAW_GOLD } };
      }
      return;
    }
    state.drawDraft = { cell: cell.index, shape: { type: tool, a: pt, b: pt, color: DRAW_GOLD } };
  };
  canvas.onmousemove = (evt) => {
    if (!state.drawDraft || state.drawDraft.cell !== cell.index) return;
    const pt = cellPoint(cell, evt);
    if (!pt) return;
    const shape = state.drawDraft.shape;
    shape.b = pt;
    if (DRAW_FREEHAND.has(shape.type)) shape.points.push(pt);
    scheduleRedraw(cell);
  };
  canvas.onmouseup = (evt) => {
    if (!state.drawDraft || state.drawDraft.cell !== cell.index) return;
    const type = state.drawDraft.shape.type;
    if (multiNeed(type) !== null) return;
    const pt = cellPoint(cell, evt) || state.drawDraft.shape.b;
    if (DRAW_FREEHAND.has(type)) {
      if (pt) state.drawDraft.shape.points.push(pt);
      finishDraft(cell);
      return;
    }
    state.drawDraft.shape.b = pt;
    if (pt && state.drawDraft.shape.a && pt.time === state.drawDraft.shape.a.time && pt.price === state.drawDraft.shape.a.price) {
      state.drawDraft = null;
      scheduleRedraw(cell);
      return;
    }
    finishDraft(cell);
  };
  canvas.ondblclick = (evt) => {
    evt.preventDefault();
    if (!state.drawDraft || state.drawDraft.cell !== cell.index) return;
    if (multiNeed(state.drawDraft.shape.type) === null) return;
    if ((state.drawDraft.shape.points || []).length >= 2) finishDraft(cell);
  };
}

/* ----------------------------------------------------------- right panels */

function activeCell() {
  return state.cells[state.activeCell] || state.cells[0] || null;
}

function isPanelOpen() {
  return !isSimple() && state.panelOpen !== false;
}

function applyPanelOpen() {
  const desk = document.querySelector(".chart-desk");
  if (desk) desk.classList.toggle("panel-collapsed", !isPanelOpen());
  const btn = document.getElementById("panel-toggle");
  if (btn) {
    const open = isPanelOpen();
    btn.setAttribute("aria-pressed", open ? "true" : "false");
    btn.title = open ? t("hideSide") : t("showSide");
    btn.setAttribute("aria-label", open ? t("hideSide") : t("showSide"));
    btn.innerHTML = `${ico(open ? "panelHide" : "panelShow")}<span>${open ? t("hideSide") : t("showSide")}</span>`;
  }
  requestAnimationFrame(() => requestAnimationFrame(layoutCells));
}

function toggleSidePanel() {
  if (isSimple()) return;
  state.panelOpen = !isPanelOpen();
  persist("shc_panel_open", state.panelOpen ? "1" : "0");
  applyPanelOpen();
  if (state.panelOpen) void renderPanel();
}

function panelTabs() {
  const tabs = isSimple() ? [] : ["brain", "history", "journal", "paper"];
  if (!tabs.length) return "";
  if (state.panel === "hunter" || state.panel === "agents" || state.panel === "analytics") state.panel = "brain";
  if (!tabs.includes(state.panel)) state.panel = "brain";
  return `<div class="panel-tabs">
    ${tabs
      .map((id) => `<button data-panel="${id}" class="${state.panel === id ? "active" : ""}">${t(id)}</button>`)
      .join("")}
    <button type="button" class="ghost tiny panel-close" id="panel-close" title="${t("hideSide")}">×</button>
  </div>`;
}

let panelToken = 0;

function stale(token) {
  return token !== panelToken;
}

async function renderPanel() {
  const host = document.getElementById("panel-body");
  if (!host) return;
  document.querySelectorAll("[data-panel]").forEach((b) => b.classList.toggle("active", b.dataset.panel === state.panel));
  const cell = activeCell();
  if (!cell) return;
  const token = ++panelToken;
  if (state.panel === "brain") return renderBrain(host, cell, token);
  if (state.panel === "history") return renderHistory(host, cell, token);
  if (state.panel === "journal") return renderJournal(host, cell);
  if (state.panel === "paper") return renderPaperPanel(host, cell);
}

async function renderBrain(host, cell, token) {
  host.innerHTML = `<div class="card"><strong>${t("mtf")}</strong><p class="muted">${t("scanning")}</p></div>
    <div id="rr-box"></div>
    <div class="card">
      <strong>${t("settings")}</strong>
      <div>${t("period")}: <span id="p-val">${state.vrcs.compression_period}</span></div>
      <input type="range" id="p-period" min="8" max="60" value="${state.vrcs.compression_period}">
      <div>${t("threshold")}: <span id="t-val">${state.vrcs.threshold_multiplier}</span></div>
      <input type="range" id="p-th" min="30" max="90" value="${Math.round(state.vrcs.threshold_multiplier * 100)}">
      <div>${t("volFactor")}: <span id="v-val">${state.vrcs.volume_factor}</span></div>
      <input type="range" id="p-vol" min="30" max="90" value="${Math.round(state.vrcs.volume_factor * 100)}">
      <div>${t("lookback")}: <span id="l-val">${state.vrcs.lookback_breakout}</span></div>
      <input type="range" id="p-lb" min="2" max="8" value="${state.vrcs.lookback_breakout}">
      <label class="check"><input type="checkbox" id="p-dash" ${state.vrcs.show_dashboard ? "checked" : ""}> ${t("dashboard")}</label>
    </div>`;
  bindVrcsSettings();
  paintRR(cell);
  host.insertAdjacentHTML("beforeend", `<div id="fund-box" class="card"><strong>${t("fundamentals")}</strong><p class="muted">${t("scanning")}</p></div>`);
  void loadFundamentals(cell);
  try {
    const data = await apiCached(`/api/hunter/confluence?symbol=${encodeURIComponent(cell.symbol)}&timeframes=15m,1h,4h`, 45000);
    if (stale(token)) return;
    cell._confluence = data;
    syncRiskDesk(cell);
    const dirClass = data.direction === "bullish" ? "up" : data.direction === "bearish" ? "down" : "";
    host.querySelector(".card").innerHTML = `<strong>${t("mtf")}</strong>
      <div class="big ${dirClass}">${String(data.direction).toUpperCase()} · ${data.confluence_confidence}%</div>
      <div>${t("aligned")}: ${(data.aligned_frames || []).join(", ") || "—"}</div>
      <div>${t("coiled")}: ${(data.coiled_frames || []).join(", ") || "—"}</div>
      <table class="mini">${(data.frames || [])
        .map(
          (f) => `<tr><td>${f.timeframe}</td><td class="${f.side === "bullish" ? "up" : f.side === "bearish" ? "down" : "muted"}">${
            t(f.regime) || f.regime
          }</td><td>${Number(f.confidence).toFixed(1)}%</td></tr>`,
        )
        .join("")}</table>`;
  } catch (err) {
    if (stale(token)) return;
    if (err.upgrade) {
      host.querySelector(".card").innerHTML = `<strong>${t("mtf")}</strong><p>${t("paywallTitle")}</p><button class="primary wide" id="brain-up">${t("upgrade")}</button>`;
      const up = document.getElementById("brain-up");
      if (up) up.onclick = () => go("plans");
      return;
    }
    host.querySelector(".card").innerHTML = `<strong>${t("mtf")}</strong><p class="down">${err.message}</p>`;
  }
}

function lastVrcsSignal(cell) {
  const pack = cell && cell.pack && cell.pack.vrcs;
  const dash = pack && pack.dashboard;
  if (dash && dash.last_signal && dash.last_signal.side) return dash.last_signal;
  const signals = (pack && pack.signals) || [];
  return signals.length ? signals[signals.length - 1] : null;
}

function tapeBias(cell) {
  const candles = (cell && cell.pack && cell.pack.candles) || [];
  const last = candles[candles.length - 1] || (cell && cell.lastBar);
  if (!last) return "";
  const prev = candles[candles.length - 2];
  let score = 0;
  if (last.close > last.open) score += 1;
  else if (last.close < last.open) score -= 1;
  if (prev) {
    if (last.close > prev.close) score += 1;
    else if (last.close < prev.close) score -= 1;
  }
  if (score > 0) return "bullish";
  if (score < 0) return "bearish";
  return "";
}

function riskOverride(symbol) {
  if (!state.risk.override || typeof state.risk.override !== "object") state.risk.override = {};
  return symbol ? state.risk.override[symbol] : "";
}

function detectRiskSide(cell) {
  const locked = cell && riskOverride(cell.symbol);
  if (locked === "bullish" || locked === "bearish") return locked;
  const signal = lastVrcsSignal(cell);
  if (signal && (signal.side === "bullish" || signal.side === "bearish")) return signal.side;
  const regime = cell && cell.pack && cell.pack.vrcs && cell.pack.vrcs.dashboard && cell.pack.vrcs.dashboard.regime;
  if (regime === "spring_bullish") return "bullish";
  if (regime === "spring_bearish") return "bearish";
  const hunt = cell && state.mkHunter && state.mkHunter[cell.symbol];
  if (hunt && (hunt.side === "bullish" || hunt.side === "bearish")) return hunt.side;
  const conf = cell && cell._confluence;
  if (conf && (conf.direction === "bullish" || conf.direction === "bearish")) return conf.direction;
  return tapeBias(cell) || "bullish";
}

function riskBiasSource(cell) {
  if (cell && riskOverride(cell.symbol)) return "manual";
  if (lastVrcsSignal(cell)) return "hunter";
  const hunt = cell && state.mkHunter && state.mkHunter[cell.symbol];
  if (hunt && hunt.side) return "hunter";
  const regime = cell && cell.pack && cell.pack.vrcs && cell.pack.vrcs.dashboard && cell.pack.vrcs.dashboard.regime;
  if (regime === "spring_bullish" || regime === "spring_bearish") return "hunter";
  const conf = cell && cell._confluence;
  if (conf && (conf.direction === "bullish" || conf.direction === "bearish")) return "brain";
  return "tape";
}

function paintRiskSides(box, side, cell) {
  if (!box) return;
  box.querySelectorAll("[data-side]").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.side === side);
  });
  const hint = box.querySelector("#rr-dir");
  if (hint) {
    const src = riskBiasSource(cell);
    const label = src === "manual" ? t("manualDir") : src === "brain" ? t("fromBrain") : src === "tape" ? t("fromTape") : t("fromHunter");
    hint.textContent = `${t("autoDir")} · ${label}`;
    hint.className = `muted small rr-dir ${side === "bearish" ? "down" : "up"}`;
  }
  const reset = box.querySelector("#rr-auto-side");
  if (reset) reset.classList.toggle("hidden", !(cell && riskOverride(cell.symbol)));
}

function fillRiskInputs(levels) {
  const fmt = (v) => (Math.abs(v) > 100 ? Number(v).toFixed(2) : Number(v).toFixed(5));
  const entry = document.getElementById("rr-entry");
  const stop = document.getElementById("rr-stop");
  const target = document.getElementById("rr-target");
  if (entry) {
    entry.value = fmt(levels.entry);
    entry.dataset.dirty = "";
  }
  if (stop) {
    stop.value = fmt(levels.stop);
    stop.dataset.dirty = "";
  }
  if (target) {
    target.value = fmt(levels.target);
    target.dataset.dirty = "";
  }
}

function riskLevels(cell, side) {
  const pack = cell && cell.pack;
  const price = cell && cell.lastBar ? cell.lastBar.close : 0;
  const atrList = (pack && pack.oscillators && pack.oscillators.atr) || [];
  const atrNow = atrList.length ? atrList[atrList.length - 1].value : price * 0.01;
  const signal = lastVrcsSignal(cell);
  const dir = side || detectRiskSide(cell);
  const entry = signal && signal.price ? signal.price : price;
  const risk = atrNow * 1.5 || Math.abs(entry) * 0.01;
  const stop = dir === "bearish" ? entry + risk : entry - risk;
  const target = dir === "bearish" ? entry - risk * 2 : entry + risk * 2;
  return { entry, stop, target, atr: atrNow, side: dir };
}

function syncRiskDesk(cell) {
  const box = document.getElementById("rr-box");
  if (!box || !cell || box.dataset.symbol !== cell.symbol) return;
  if (box.querySelector('input[data-dirty="1"]')) {
    paintRiskSides(box, detectRiskSide(cell), cell);
    return;
  }
  if (riskOverride(cell.symbol)) {
    paintRiskSides(box, riskOverride(cell.symbol), cell);
    return;
  }
  const levels = riskLevels(cell);
  fillRiskInputs(levels);
  paintRiskSides(box, levels.side, cell);
  updateRiskMath();
}

function applySmartRisk(cell) {
  if (!cell) return;
  const box = document.getElementById("rr-box");
  const dirty = box && [...box.querySelectorAll("#rr-entry, #rr-stop, #rr-target")].some((el) => el.dataset.dirty === "1");
  const side = detectRiskSide(cell);
  state.risk.side = side;
  persist("shc_risk", state.risk);
  paintRiskSides(box, side, cell);
  let levels;
  if (dirty) {
    levels = {
      entry: Number(document.getElementById("rr-entry").value),
      stop: Number(document.getElementById("rr-stop").value),
      target: Number(document.getElementById("rr-target").value),
      side,
    };
  } else {
    levels = riskLevels(cell, side);
    fillRiskInputs(levels);
    updateRiskMath();
  }
  applyRiskLines(cell, levels);
}

const PAPER_BANK = 100000;

function fmtBank(value) {
  const n = Number(value);
  const amount = Number.isFinite(n) ? n : PAPER_BANK;
  return amount.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function tradeAmount() {
  const cash = Number((state.paperBook && state.paperBook.cash) || PAPER_BANK);
  const raw = Number(state.risk.amount);
  const fallback = PAPER_BANK * ((Number(state.risk.pct) || 1) / 100);
  const amount = Number.isFinite(raw) && raw > 0 ? raw : fallback;
  return Math.max(10, Math.min(PAPER_BANK, cash > 0 ? cash : PAPER_BANK, amount));
}

function positionSize(entry) {
  const notional = tradeAmount();
  const qty = entry > 0 ? notional / entry : 0;
  return { riskAmt: notional, qty, notional: qty * entry };
}

function applyRiskLines(cell, levels) {
  if (!cell || !levels) return;
  const key = drawKey(cell.symbol);
  const kept = (state.drawings[key] || []).filter((item) => item.source !== "risk");
  kept.push(
    { type: "hline", price: levels.entry, color: "#c8a45a", label: "IN", source: "risk" },
    { type: "hline", price: levels.stop, color: "#ef5350", label: "SL", source: "risk" },
    { type: "hline", price: levels.target, color: "#26a69a", label: "TP", source: "risk" },
  );
  state.drawings[key] = kept;
  saveDrawings();
  scheduleRedraw(cell);
}

function applyRiskFromSignal(cell, signal) {
  if (!cell || !signal) return;
  if (riskOverride(cell.symbol)) return;
  const side = signal.side === "bearish" ? "bearish" : "bullish";
  state.risk.side = side;
  persist("shc_risk", state.risk);
  const levels = riskLevels(cell, side);
  if (signal.price) levels.entry = signal.price;
  const risk = Math.abs(levels.entry - levels.stop) || Math.abs(levels.entry) * 0.01;
  levels.stop = side === "bearish" ? levels.entry + risk : levels.entry - risk;
  levels.target = side === "bearish" ? levels.entry - risk * 2 : levels.entry + risk * 2;
  applyRiskLines(cell, levels);
  const box = document.getElementById("rr-box");
  if (box && box.dataset.symbol === cell.symbol) {
    fillRiskInputs(levels);
    paintRiskSides(box, side, cell);
    updateRiskMath();
  }
}

function updateRiskMath() {
  const entry = Number((document.getElementById("rr-entry") || {}).value);
  const stop = Number((document.getElementById("rr-stop") || {}).value);
  const target = Number((document.getElementById("rr-target") || {}).value);
  if (!entry) return;
  const dist = Math.abs(entry - stop);
  const size = positionSize(entry, stop);
  const fmt = (v) => (Math.abs(v) > 100 ? v.toFixed(2) : v.toFixed(5));
  const riskEl = document.getElementById("rr-risk");
  const pctEl = document.getElementById("rr-riskpct");
  const ratioEl = document.getElementById("rr-ratio");
  const qtyEl = document.getElementById("rr-qty");
  if (riskEl) riskEl.textContent = fmt(dist);
  if (pctEl) pctEl.textContent = `${((dist / entry) * 100).toFixed(2)}%`;
  if (ratioEl) ratioEl.textContent = dist ? `1 : ${(Math.abs(target - entry) / dist).toFixed(2)}` : "—";
  if (qtyEl) qtyEl.textContent = `${fmt(size.qty)} · $${fmtBank(size.notional)}`;
}

function paintRR(cell) {
  const box = document.getElementById("rr-box");
  if (!box || !cell) return;
  const existing = box.querySelector("#rr-entry");
  if (box.dataset.symbol === cell.symbol && existing && Number(existing.value)) {
    if (!box.querySelector('input[data-dirty="1"]')) {
      paintRiskSides(box, detectRiskSide(cell), cell);
      updateRiskMath();
    }
    return;
  }
  const levels = riskLevels(cell);
  const fmt = (v) => (Math.abs(v) > 100 ? v.toFixed(2) : v.toFixed(5));
  box.dataset.symbol = cell.symbol;
  box.innerHTML = `<div class="card risk-desk">
    <strong>${t("rr")}</strong>
    <div class="rr-sides">
      <button class="ghost tiny ${levels.side !== "bearish" ? "active" : ""}" data-side="bullish">${t("long")}</button>
      <button class="ghost tiny ${levels.side === "bearish" ? "active" : ""}" data-side="bearish">${t("short")}</button>
      <button type="button" class="ghost tiny ${riskOverride(cell.symbol) ? "" : "hidden"}" id="rr-auto-side">${t("resetAuto")}</button>
    </div>
    <div id="rr-dir" class="muted small rr-dir ${levels.side === "bearish" ? "down" : "up"}">${t("autoDir")}</div>
    <div class="rr-grid">
      <label>${t("virtualBank")}<strong id="rr-wallet" class="bank-fixed">$${fmtBank(PAPER_BANK)}</strong></label>
      <label>${t("tradeAmount")}<input id="rr-amount" type="number" min="10" max="${PAPER_BANK}" step="100" value="${tradeAmount()}"></label>
      <label>${t("entry")}<input id="rr-entry" type="number" step="any" value="${levels.entry}"></label>
      <label>${t("stop")}<input id="rr-stop" type="number" step="any" value="${levels.stop}"></label>
      <label>${t("target")}<input id="rr-target" type="number" step="any" value="${levels.target}"></label>
    </div>
    <div>${t("risk")}: <span id="rr-risk">${fmt(Math.abs(levels.entry - levels.stop))}</span>
      (<span id="rr-riskpct">${((Math.abs(levels.entry - levels.stop) / (levels.entry || 1)) * 100).toFixed(2)}%</span>)</div>
    <div class="amount-chips">${[500, 1000, 2500, 5000, 10000, 25000]
      .map((n) => `<button type="button" class="ghost tiny" data-amt="${n}">$${n.toLocaleString("en-US")}</button>`)
      .join("")}</div>
    <p class="muted small">${t("amountHint")}</p>
    <div>${t("position")}: <span id="rr-qty">—</span></div>
    <div>${t("ratio")}: <span id="rr-ratio">1 : 2.00</span></div>
    <label class="check"><input type="checkbox" id="rr-auto" ${state.risk.auto ? "checked" : ""}/> ${t("autoRisk")}</label>
    <div class="rr-actions">
      <button class="primary wide" id="rr-apply">${t("applyLevels")}</button>
      <button class="ghost wide" id="rr-paper">${t("openPaper")}</button>
    </div>
    <div id="paper-book" class="paper-mini"></div>
  </div>`;
  const persistRisk = () => {
    state.risk.wallet = PAPER_BANK;
    const amountEl = document.getElementById("rr-amount");
    const next = Number(amountEl && amountEl.value);
    if (Number.isFinite(next) && next > 0) {
      state.risk.amount = Math.max(10, Math.min(PAPER_BANK, next));
      state.risk.pct = (state.risk.amount / PAPER_BANK) * 100;
    }
    persist("shc_risk", state.risk);
    updateRiskMath();
  };
  const amountEl = document.getElementById("rr-amount");
  if (amountEl) amountEl.oninput = persistRisk;
  box.querySelectorAll("[data-amt]").forEach((btn) => {
    btn.onclick = () => {
      state.risk.amount = Number(btn.dataset.amt);
      state.risk.pct = (state.risk.amount / PAPER_BANK) * 100;
      if (amountEl) amountEl.value = String(state.risk.amount);
      persist("shc_risk", state.risk);
      updateRiskMath();
    };
  });
  ["rr-entry", "rr-stop", "rr-target"].forEach((id) => {
    const el = document.getElementById(id);
    if (el)
      el.oninput = () => {
        el.dataset.dirty = "1";
        updateRiskMath();
      };
  });
  box.querySelectorAll("[data-side]").forEach((btn) => {
    btn.onclick = () => {
      state.risk.override = state.risk.override || {};
      state.risk.override[cell.symbol] = btn.dataset.side;
      state.risk.side = btn.dataset.side;
      persist("shc_risk", state.risk);
      const next = riskLevels(cell, btn.dataset.side);
      fillRiskInputs(next);
      paintRiskSides(box, next.side, cell);
      updateRiskMath();
      applyRiskLines(cell, next);
    };
  });
  const resetDir = document.getElementById("rr-auto-side");
  if (resetDir)
    resetDir.onclick = () => {
      if (state.risk.override) delete state.risk.override[cell.symbol];
      persist("shc_risk", state.risk);
      const next = riskLevels(cell);
      fillRiskInputs(next);
      paintRiskSides(box, next.side, cell);
      updateRiskMath();
      applyRiskLines(cell, next);
    };
  const auto = document.getElementById("rr-auto");
  if (auto)
    auto.onchange = () => {
      state.risk.auto = auto.checked;
      persist("shc_risk", state.risk);
    };
  const apply = document.getElementById("rr-apply");
  if (apply) apply.onclick = () => applySmartRisk(cell);
  paintRiskSides(box, levels.side, cell);
  const paperBtn = document.getElementById("rr-paper");
  if (paperBtn)
    paperBtn.onclick = () => {
      const levels = {
        entry: Number(document.getElementById("rr-entry").value),
        stop: Number(document.getElementById("rr-stop").value),
        target: Number(document.getElementById("rr-target").value),
      };
      applyRiskLines(cell, levels);
      void openPaperFromRisk(cell, levels);
    };
  updateRiskMath();
  void paintPaperBook(cell);
}

function defaultPaperBook() {
  return { cash: PAPER_BANK, starting_cash: PAPER_BANK, equity: PAPER_BANK, realized_pnl: 0, open: [], closed: [] };
}

function localPaperBook() {
  const book = readJSON("shc_paper", defaultPaperBook());
  const start = Number(book.starting_cash);
  if (!Number.isFinite(start) || Math.abs(start - PAPER_BANK) > 0.5) {
    const delta = PAPER_BANK - (Number.isFinite(start) ? start : 0);
    book.cash = Number(book.cash || 0) + delta;
    book.starting_cash = PAPER_BANK;
    persist("shc_paper", recountPaper(book));
  }
  return book;
}

function executionOn() {
  return true;
}

function persistExecution(on) {
  state.execution = !!on;
  localStorage.setItem("shc_exec", on ? "1" : "0");
}

function saveLocalPaper(book) {
  persist("shc_paper", book);
  state.paperBook = book;
}

function paperPnl(pos, last) {
  const px = Number(last);
  if (!px) return Number(pos.pnl || 0);
  return pos.side === "short" ? (pos.entry - px) * pos.qty : (px - pos.entry) * pos.qty;
}

function paperHit(pos, last) {
  if (pos.side === "short") {
    if (pos.stop && last >= pos.stop) return "sl";
    if (pos.target && last <= pos.target) return "tp";
    return "";
  }
  if (pos.stop && last <= pos.stop) return "sl";
  if (pos.target && last >= pos.target) return "tp";
  return "";
}

function recountPaper(book) {
  const open = book.open || [];
  book.realized_pnl = (book.closed || []).reduce((sum, row) => sum + Number(row.pnl || 0), 0);
  book.equity =
    Number(book.cash || 0) +
    open.reduce((sum, row) => sum + Number(row.qty) * Number(row.entry) + Number(row.pnl || 0), 0);
  return book;
}

function localMarkPaper(symbol, last) {
  const book = localPaperBook();
  const keep = [];
  let closed = 0;
  (book.open || []).forEach((pos) => {
    if (pos.symbol !== symbol) {
      keep.push(pos);
      return;
    }
    const hit = paperHit(pos, last);
    pos.pnl = paperPnl(pos, last);
    if (!hit) {
      keep.push(pos);
      return;
    }
    pos.status = "closed";
    pos.exit = last;
    pos.reason = hit;
    pos.closed_at = new Date().toISOString();
    book.cash = Number(book.cash) + pos.qty * pos.entry + pos.pnl;
    book.closed = [pos, ...(book.closed || [])].slice(0, 40);
    closed += 1;
  });
  book.open = keep;
  saveLocalPaper(recountPaper(book));
  return { book: state.paperBook, closed };
}

async function ensurePaperBook() {
  if (!state.user) {
    state.paperBook = localPaperBook();
    return state.paperBook;
  }
  if (state.paperBook && Date.now() - (state.paperBook._at || 0) < 3500) return state.paperBook;
  try {
    const book = await api("/api/paper/book");
    book._at = Date.now();
    state.paperBook = book;
  } catch {
    state.paperBook = state.paperBook || defaultPaperBook();
  }
  return state.paperBook;
}

async function openPaperFromRisk(cell, levels) {
  const size = positionSize(levels.entry, levels.stop);
  if (!size.qty) {
    toast(t("qtyHint"), "bearish");
    return;
  }
  const body = {
    symbol: cell.symbol,
    side: levels.side || (detectRiskSide(cell) === "bearish" ? "short" : "long"),
    qty: size.qty,
    entry: levels.entry,
    stop: levels.stop,
    target: levels.target,
    wallet: PAPER_BANK,
  };
  try {
    if (state.user) {
      const book = await api("/api/paper/open", { method: "POST", body: JSON.stringify(body) });
      book._at = Date.now();
      state.paperBook = book;
    } else {
      const book = localPaperBook();
      const notional = size.qty * levels.entry;
      if (book.cash < notional) throw new Error("insufficient paper cash");
      book.cash -= notional;
      book.open = [
        {
          id: Date.now(),
          symbol: cell.symbol,
          side: body.side,
          qty: size.qty,
          entry: levels.entry,
          stop: levels.stop,
          target: levels.target,
          status: "open",
          pnl: 0,
        },
        ...(book.open || []),
      ];
      saveLocalPaper(recountPaper(book));
    }
    toast(t("paperOpened"));
    paintPaperBook(cell);
    if (state.panel === "paper") void renderPanel();
  } catch (err) {
    const msg = String(err.message || "");
    toast(/insufficient/i.test(msg) ? t("paperCashShort") : msg || t("noResult"), "bearish");
  }
}

async function closePaperTrade(id, last, cell) {
  try {
    if (state.user) {
      const book = await api(`/api/paper/close/${id}`, {
        method: "POST",
        body: JSON.stringify({ exit: last || undefined }),
      });
      book._at = Date.now();
      state.paperBook = book;
    } else {
      const book = localPaperBook();
      const pos = (book.open || []).find((row) => String(row.id) === String(id));
      if (!pos) return;
      const px = last || pos.entry;
      pos.status = "closed";
      pos.exit = px;
      pos.reason = "manual";
      pos.pnl = paperPnl(pos, px);
      pos.closed_at = new Date().toISOString();
      book.cash = Number(book.cash) + pos.qty * pos.entry + pos.pnl;
      book.open = (book.open || []).filter((row) => String(row.id) !== String(id));
      book.closed = [pos, ...(book.closed || [])].slice(0, 40);
      saveLocalPaper(recountPaper(book));
    }
    toast(t("paperClosed"));
    paintPaperBook(cell);
    if (state.panel === "paper") void renderPanel();
  } catch (err) {
    toast(err.message || t("noResult"), "bearish");
  }
}

async function syncPaperMarks(cell) {
  if (!cell || !cell.lastBar) return;
  const last = Number(cell.lastBar.close);
  if (!last) return;
  const symbol = cell.symbol;
  const open = subscriberPaperRows(((state.paperBook && state.paperBook.open) || (!state.user ? localPaperBook().open : [])) || []);
  if (!open.some((row) => row.symbol === symbol && row.status !== "closed")) {
    if (cell.index === state.activeCell) paintPaperBook(cell);
    return;
  }
  try {
    if (state.user) {
      const book = await api("/api/paper/mark", {
        method: "POST",
        body: JSON.stringify({ symbol, last }),
      });
      book._at = Date.now();
      state.paperBook = book;
    } else {
      localMarkPaper(symbol, last);
    }
  } catch {
    /* keep the last known book */
  }
  paintPaperBook(cell);
}

function subscriberPaperRows(rows) {
  return (rows || []).filter((row) => row.source !== "execution_bot");
}

function paperRowsHtml(rows, cell, last) {
  rows = subscriberPaperRows(rows);
  if (!rows || !rows.length) return `<p class="muted">${t("noPaper")}</p>`;
  return rows
    .map((row) => {
      const pnl = row.status === "open" ? paperPnl(row, last) : Number(row.pnl || 0);
      const cls = pnl >= 0 ? "up" : "down";
      return `<div class="paper-row">
        <div><strong>${row.symbol}</strong> · ${row.side === "short" ? t("short") : t("long")}${
          row.source === "execution_bot" ? ` · <span class="muted">${t("botTrade")}</span>` : ""
        }
          <div class="muted">${Number(row.qty).toFixed(4)} @ ${Number(row.entry).toFixed(4)}</div></div>
        <div class="${cls}">${pnl >= 0 ? "+" : ""}${pnl.toFixed(2)}</div>
        ${
          row.status === "open"
            ? `<button class="ghost tiny" data-paper-close="${row.id}">${t("closePaper")}</button>`
            : `<span class="muted">${row.reason || t("closed")}</span>`
        }
      </div>`;
    })
    .join("");
}

async function paintPaperBook(cell) {
  const host = document.getElementById("paper-book");
  if (!host) return;
  await ensurePaperBook();
  const book = state.paperBook || defaultPaperBook();
  const last = cell && cell.lastBar ? cell.lastBar.close : 0;
  const open = subscriberPaperRows(book.open || []).filter((row) => !cell || row.symbol === cell.symbol);
  host.innerHTML = `<div class="paper-meta">
      <span>${t("virtualBank")}: $${fmtBank(book.starting_cash || PAPER_BANK)}</span>
      <span>${t("paperCash")}: $${fmtBank(book.cash)}</span>
      <span>${t("paperEquity")}: $${fmtBank(book.equity)}</span>
    </div>
    ${paperRowsHtml(open, cell, last)}`;
  host.querySelectorAll("[data-paper-close]").forEach((btn) => {
    btn.onclick = () => void closePaperTrade(btn.dataset.paperClose, last, cell);
  });
}

async function renderPaperPanel(host, cell) {
  host.innerHTML = `<div class="card"><strong>${t("paper")}</strong><p class="muted">${t("paperHint")}</p></div>`;
  await ensurePaperBook();
  const book = state.paperBook || defaultPaperBook();
  const last = cell && cell.lastBar ? cell.lastBar.close : 0;
  host.innerHTML = `<div class="card">
      <strong>${t("paper")}</strong>
      <p class="muted">${t("paperHint")}</p>
      <div class="paper-meta">
        <span>${t("virtualBank")}: $${fmtBank(book.starting_cash || PAPER_BANK)}</span>
        <span>${t("paperCash")}: $${fmtBank(book.cash)}</span>
        <span>${t("paperEquity")}: $${fmtBank(book.equity)}</span>
      </div>
      <div>${t("realized")}: <span class="${Number(book.realized_pnl) >= 0 ? "up" : "down"}">${fmtNum(book.realized_pnl)}</span></div>
      <button class="ghost wide" id="paper-reset">${t("resetPaper")}</button>
    </div>
    <div class="card"><strong>${t("openTrades")}</strong>${paperRowsHtml(book.open, cell, last)}</div>
    <div class="card"><strong>${t("closed")}</strong>${
      book.closed && book.closed.length
        ? paperRowsHtml(book.closed, cell, last)
        : `<p class="muted">${t("noPaper")}</p>`
    }</div>`;
  host.querySelectorAll("[data-paper-close]").forEach((btn) => {
    btn.onclick = () => void closePaperTrade(btn.dataset.paperClose, last, cell);
  });
  const reset = document.getElementById("paper-reset");
  if (reset)
    reset.onclick = async () => {
      try {
        if (state.user) {
          const next = await api("/api/paper/reset", {
            method: "POST",
            body: JSON.stringify({ cash: PAPER_BANK }),
          });
          next._at = Date.now();
          state.paperBook = next;
        } else {
          saveLocalPaper(defaultPaperBook());
        }
        void renderPaperPanel(host, cell);
      } catch (err) {
        toast(err.message || t("noResult"), "bearish");
      }
    };
}

async function renderHistory(host, cell, token) {
  const tf = state.timeframe === "1s" ? "1m" : state.timeframe;
  host.innerHTML = `<div class="card"><strong>${t("history")} · ${cell.symbol}</strong><p class="muted">${t("scanning")}</p></div>`;
  try {
    const data = await apiCached(
      `/api/hunter/backtest?symbol=${encodeURIComponent(cell.symbol)}&timeframe=${tf}&horizon=24&reward_multiple=2`,
      60000,
    );
    if (stale(token)) return;
    const buckets = Object.entries(data.buckets || {})
      .map(([range, v]) => `<tr><td>${range}%</td><td>${v.trades}</td><td>${v.win_rate}%</td></tr>`)
      .join("");
    host.innerHTML = `<div class="card">
        <strong>${t("history")} · ${cell.symbol} ${tf}</strong>
        <div class="big ${data.win_rate >= 50 ? "up" : "down"}">${t("winRate")}: ${data.win_rate}%</div>
        <div>${t("trades")}: ${data.total_signals} · ${t("closed")}: ${data.closed}</div>
        <div>${t("avgPnl")}: ${data.avg_pnl_pct}% · 90%+: ${data.high_confidence_win_rate}%</div>
        <table class="mini"><tr><th>${t("confidence")}</th><th>${t("trades")}</th><th>${t("winRate")}</th></tr>${buckets}</table>
        <a class="ghost wide center" href="/api/hunter/export.csv?symbol=${encodeURIComponent(cell.symbol)}&timeframe=${tf}" download>${t("export")}</a>
      </div>
      <div class="card"><table class="mini wide-table">
        <tr><th>#</th><th>${t("confidence")}</th><th>PnL</th><th></th></tr>
        ${(data.trades || [])
          .slice()
          .reverse()
          .slice(0, 40)
          .map(
            (tr) => `<tr>
              <td>${new Date(tr.time * 1000).toISOString().slice(5, 16).replace("T", " ")}</td>
              <td class="${tr.side === "bullish" ? "up" : "down"}">${tr.confidence}%</td>
              <td class="${tr.pnl_pct >= 0 ? "up" : "down"}">${tr.pnl_pct}%</td>
              <td>${tr.outcome === "win" ? "✔" : tr.outcome === "loss" ? "✘" : "…"}</td>
            </tr>`,
          )
          .join("")}
      </table></div>`;
  } catch (err) {
    if (stale(token)) return;
    host.innerHTML = `<div class="card"><p class="down">${err.message}</p></div>`;
  }
}

function swarmRowKey(row) {
  return row && (row.signal_key || `${row.symbol}|${row.timeframe}|${row.entry}|${row.status}`);
}

function notifySwarmOpportunity(row) {
  if (!row || !row.symbol) return;
  const vote = swarmVoteOf(row);
  const side = vote === "SELL" ? "bearish" : "bullish";
  const title = `${t("swarmAlert")} · ${t(vote)}`;
  const body = `${row.symbol} · ${row.timeframe || ""} · ${swarmTradeKind(row)} · ${t("entry")} ${fmtNum(row.entry)}`;
  toast(`<strong>${title}</strong><br>${escapeHtml(body)}`, side);
  if (state.sound) {
    enableSound();
    beep(side);
  }
  if (window.Notification && Notification.permission === "granted") {
    new Notification(`SHC ${title}`, { body });
  } else if (window.Notification && Notification.permission === "default") {
    void Notification.requestPermission();
  }
}

function ingestSwarmApproved(rows) {
  const approved = (rows || []).filter((row) => row && row.status === "approved" && row.symbol);
  if (!state.swarmPrimed) {
    approved.forEach((row) => state.swarmSeen.add(swarmRowKey(row)));
    state.swarmPrimed = true;
    return;
  }
  approved.forEach((row) => {
    const key = swarmRowKey(row);
    if (!key || state.swarmSeen.has(key)) return;
    state.swarmSeen.add(key);
    notifySwarmOpportunity(row);
  });
}

function paintSwarmHost(approved) {
  const host = document.getElementById("swarm-approved");
  if (!host || state.view !== "agents") return;
  host.innerHTML = `<strong>${t("swarmApproved")}</strong>
      <p class="muted small">${t("agentsLive")}</p>
      ${approved.length ? approved.map(swarmHitCard).join("") : `<p class="muted">${t("swarmWaiting")}</p>`}`;
  bindSwarmHits(host, approved);
}

async function paintLiveSetups() {
  const host = document.getElementById("swarm-approved");
  if (!state.user) {
    if (host && state.view === "agents") {
      host.innerHTML = `<strong>${t("swarmApproved")}</strong><p class="down">${t("needAuth")}</p>`;
    }
    return;
  }
  try {
    const data = await api("/api/agents/swarm");
    const approved = data.approved || [];
    ingestSwarmApproved(approved);
    paintSwarmHost(approved);
  } catch (err) {
    if (host && state.view === "agents") {
      host.innerHTML = `<strong>${t("swarmApproved")}</strong><p class="down">${err.message}</p>`;
    }
  }
}

function watchSwarm() {
  if (!can("agents")) return;
  if (state.swarmTimer) return;
  state.swarmTimer = setInterval(() => void paintLiveSetups(), 15000);
  void paintLiveSetups();
}

async function renderAgentsPage() {
  state.view = "agents";
  teardown();
  if (!can("agents")) {
    document.getElementById("app").innerHTML = pageShell(
      t("pageAgents"),
      t("locked"),
      `<div class="card"><p>${t("paywallTitle")}</p><p class="muted">${t("elite_brain")}</p><button class="primary wide" id="up">${t("upgrade")}</button></div>`,
    );
    bindChrome();
    const up = document.getElementById("up");
    if (up) up.onclick = () => go("plans");
    return;
  }
  document.getElementById("app").innerHTML = pageShell(
    t("pageAgents"),
    t("agentsSilent"),
    `<div class="card" id="swarm-approved"><strong>${t("swarmApproved")}</strong><p class="muted">${t("scanning")}</p></div>`,
  );
  bindChrome();
  applyStealth();
  await paintLiveSetups();
  watchSwarm();
}

function paintManualAgents(result) {
  const setup = result.setup || {};
  const vote = String(result.vote || setup.vote || "").toUpperCase();
  const status = result.status || "";
  const dir = vote === "SELL" ? "down" : vote === "BUY" ? "up" : "muted";
  const setupHtml =
    status === "approved" && setup.entry
      ? `<div class="big ${dir}">${t(vote)}</div>
         <div>${t("entry")}: ${fmtNum(setup.entry)} · ${t("stop")}: ${fmtNum(setup.stop)}</div>
         <div>${t("target1")}: ${fmtNum((setup.targets && setup.targets[0]) || setup.target)} · ${t("target2")}: ${fmtNum((setup.targets && setup.targets[1]) || setup.target)} · ${t("target3")}: ${fmtNum((setup.targets && setup.targets[2]) || setup.target)}</div>`
      : `<p class="muted">${t("noConsensus")}</p>`;
  const agents = (result.agents || [])
    .map((agent) => {
      const side = String(agent.vote || "").toUpperCase() || (agent.direction === "bullish" ? "BUY" : agent.direction === "bearish" ? "SELL" : "WAIT");
      const cls = side === "BUY" ? "up" : side === "SELL" ? "down" : "muted";
      return `<article class="card agent-card">
        <strong>${t(agent.agent_name || agent.name)}</strong>
        <div class="big ${cls}">${t(side)}</div>
        <div>${t("confidence")}: ${Math.round(Number(agent.confidence || 0) * 100)}%</div>
        <p>${escapeHtml(agent.reasoning || "")}</p>
      </article>`;
    })
    .join("");
  return `${result.profile ? paintAssetProfile(result.profile) : ""}
    <div class="card"><strong>${t("agentsOpinions")}</strong>${setupHtml}<p class="muted small">${escapeHtml(result.reasoning || "")}</p></div>
    <div class="agent-grid">${agents || `<p class="muted">${t("noResult")}</p>`}</div>`;
}

function paintAssetProfile(data) {
  if (!data || !data.symbol) return "";
  const mood = data.sentiment || {};
  const liq = data.liquidity || {};
  const mom = data.momentum || {};
  const venue = data.venue || "crypto";
  const supplyLabel = venue === "crypto" ? t("supply") : t("outstanding");
  const supplyValue = venue === "crypto" ? data.supply : data.shares_outstanding;
  const momLabel = t(mom.label || "momNeutral");
  const momCls = mom.label === "momOverbought" || mom.label === "momBearish" ? "down" : mom.label === "momOversold" || mom.label === "momBullish" ? "up" : "muted";
  const liqBias = liq.bias || mood.bias || "neutral";
  const liqCls = liqBias === "risk_on" ? "up" : liqBias === "risk_off" ? "down" : "muted";
  const stats = [
    [t("lastPrice"), fmtNum(data.last, data.last > 100 ? 2 : 5)],
    [t("change24h"), pctText(data.percentage), pctClass(data.percentage)],
    [t("mcap"), fmtNum(data.market_cap, 0)],
    [supplyLabel, fmtNum(supplyValue, 0)],
    venue !== "crypto" && data.shares_float ? [t("sharesFloat"), fmtNum(data.shares_float, 0)] : null,
    [t("volume24"), fmtNum(data.volume || data.quote_volume, 0)],
    [t("quoteVolume"), fmtNum(data.quote_volume || liq.quote_volume, 0)],
    data.avg_volume ? [t("avgVolume"), fmtNum(data.avg_volume, 0)] : null,
    [t("liquidity"), `${liqBias === "risk_on" || liqBias === "risk_off" ? t(liqBias) : t("sentiment")}${liq.score != null ? ` · ${liq.score}` : ""}`, liqCls],
    [t("momentum"), `${momLabel}${mom.rsi != null ? ` · RSI ${mom.rsi}` : ""}`, momCls],
    venue !== "crypto" && data.pe != null ? [t("pe"), Number(data.pe).toFixed(2)] : null,
    data.industry || data.sector ? [t("industry"), data.industry || data.sector] : null,
  ].filter(Boolean);
  return `<div class="card asset-profile">
    <div class="profile-head">
      ${assetLogo(data.symbol, { eager: true, size: "lg" })}
      <div>
        <strong>${t("profileTitle")}</strong>
        <div class="big">${escapeHtml(data.name || data.symbol)}</div>
        <div class="muted">${escapeHtml(data.symbol)} · ${t(venue) || venue}</div>
      </div>
    </div>
    <div class="stat-grid">${stats
      .map((row) => `<div class="stat"><small>${row[0]}</small><b class="${row[2] || ""}">${row[1]}</b></div>`)
      .join("")}</div>
  </div>`;
}

async function loadAnalyticsProfile(symbol) {
  const host = document.getElementById("an-result");
  if (!host || !symbol) return;
  const frame = (document.getElementById("an-tf") && document.getElementById("an-tf").value) || "1h";
  host.innerHTML = `<div class="card"><p class="muted">${t("scanning")}</p></div><div id="an-agents"><p class="muted">${t("analyticsHint")}</p></div>`;
  try {
    const data = await api(`/api/market/fundamentals?symbol=${encodeURIComponent(symbol)}&timeframe=${encodeURIComponent(frame)}`);
    if (state.view !== "analytics") return;
    const input = document.getElementById("an-symbol");
    if (input && (input.value || "").trim().toUpperCase() !== symbol.toUpperCase()) return;
    host.innerHTML = `${paintAssetProfile(data)}<div id="an-agents"><p class="muted">${t("analyticsHint")}</p></div>`;
  } catch (err) {
    if (state.view !== "analytics") return;
    host.innerHTML = `<div class="card"><p class="down">${err.message}</p></div>`;
  }
}

async function renderAnalyticsPage() {
  state.view = "analytics";
  teardown();
  if (!can("analytics")) {
    document.getElementById("app").innerHTML = pageShell(
      t("pageAnalytics"),
      t("locked"),
      `<div class="card"><p>${t("paywallTitle")}</p><p class="muted">${t("elite_brain")}</p><button class="primary wide" id="up">${t("upgrade")}</button></div>`,
    );
    bindChrome();
    const up = document.getElementById("up");
    if (up) up.onclick = () => go("plans");
    return;
  }
  const frames = TIMEFRAMES.filter((id) => id !== "1s");
  const tf = frames.includes(state.timeframe) ? state.timeframe : "1h";
  document.getElementById("app").innerHTML = pageShell(
    t("pageAnalytics"),
    t("analyticsHint"),
    `<div class="card">
      <div class="rr-grid">
        <label>${t("search")}<div class="chart-sym-search">
          <input id="an-symbol" value="" placeholder="${t("search")}" autocomplete="off" />
          <div id="an-hits"></div>
        </div></label>
        <label>${t("timeframe")}
          <select id="an-tf">${frames
            .map((id) => `<option value="${id}" ${id === tf ? "selected" : ""}>${id}</option>`)
            .join("")}</select>
        </label>
      </div>
      <button class="primary wide" id="an-run">${t("runAnalysis")}</button>
    </div>
    <div id="an-result"><p class="muted">${t("analyticsHint")}</p></div>`,
  );
  bindChrome();
  applyStealth();
  bindLiveSearch(document.getElementById("an-symbol"), document.getElementById("an-hits"));
  const run = document.getElementById("an-run");
  run.onclick = async () => {
    const sym = (document.getElementById("an-symbol").value || "").trim().toUpperCase();
    const frame = document.getElementById("an-tf").value || "1h";
    if (!sym) return;
    if (!state.user) {
      document.getElementById("an-result").innerHTML = `<div class="card"><p class="down">${t("needAuth")}</p></div>`;
      return;
    }
    run.disabled = true;
    run.textContent = t("analyzing");
    const prev = document.getElementById("an-result").querySelector(".asset-profile");
    document.getElementById("an-result").innerHTML = `${prev ? prev.outerHTML : ""}<div class="card"><p class="muted">${t("analyzing")}</p></div>`;
    try {
      const result = await api("/api/agents/analyze", {
        method: "POST",
        body: JSON.stringify({ symbol: sym, timeframe: frame, locale: state.locale }),
      });
      document.getElementById("an-result").innerHTML = paintManualAgents(result);
    } catch (err) {
      document.getElementById("an-result").innerHTML = `<div class="card"><p class="down">${err.message}</p></div>`;
    } finally {
      run.disabled = false;
      run.textContent = t("runAnalysis");
    }
  };
}

function renderJournal(host, cell) {
  const dash = cell.pack && cell.pack.vrcs ? cell.pack.vrcs.dashboard : null;
  const conf = dash ? Number(dash.confidence || 0).toFixed(1) : "0.0";
  const price = cell.lastBar ? cell.lastBar.close : 0;
  host.innerHTML = `<div class="card">
      <strong>${t("journal")}</strong>
      <div class="muted">${cell.symbol} · ${state.timeframe} · ${price} · ${conf}%</div>
      <textarea id="note-text" rows="3" placeholder="${t("notePlaceholder")}"></textarea>
      <button class="primary wide" id="note-add">${t("addNote")}</button>
    </div>
    <div id="note-list">${
      state.journal.length
        ? state.journal
            .slice()
            .reverse()
            .map(
              (n, i) => `<div class="card note">
                <div class="muted">${new Date(n.ts).toLocaleString()} · ${n.symbol} ${n.timeframe}</div>
                <div>${n.price} · <span class="${n.side === "bearish" ? "down" : "up"}">${n.confidence}%</span> · ${
                  t(n.regime) || n.regime
                }</div>
                <p>${n.text}</p>
                <button class="ghost tiny del" data-idx="${state.journal.length - 1 - i}">${t("delete")}</button>
              </div>`,
            )
            .join("")
        : `<p class="muted pad">${t("noNotes")}</p>`
    }</div>`;
  document.getElementById("note-add").onclick = () => {
    const text = document.getElementById("note-text").value.trim();
    if (!text) return;
    state.journal.push({
      ts: Date.now(),
      symbol: cell.symbol,
      timeframe: state.timeframe,
      price,
      confidence: conf,
      regime: dash ? dash.regime : "normal",
      side: dash && dash.last_signal ? dash.last_signal.side : "bullish",
      text,
    });
    persist("shc_journal", state.journal);
    cell.series.setMarkers(markersFor(cell, cell.pack || { vrcs: null }));
    renderJournal(host, cell);
  };
  host.querySelectorAll(".del").forEach((btn) => {
    btn.onclick = () => {
      state.journal.splice(Number(btn.dataset.idx), 1);
      persist("shc_journal", state.journal);
      renderJournal(host, cell);
    };
  });
}

function swarmVoteOf(row) {
  const raw = String((row && row.vote) || "").toUpperCase();
  if (raw === "BUY" || raw === "SELL") return raw;
  return row && (row.side === "bearish" || row.direction === "bearish") ? "SELL" : "BUY";
}

function swarmTargets(row) {
  const listed = Array.isArray(row && row.targets) ? row.targets.map(Number).filter(Number.isFinite) : [];
  if (listed.length >= 3) return listed.slice(0, 3);
  const t1 = Number(row && row.target1);
  const t2 = Number(row && (row.target2 != null ? row.target2 : row.target));
  const t3 = Number(row && row.target3);
  if ([t1, t2, t3].every(Number.isFinite)) return [t1, t2, t3];
  const entry = Number(row && row.entry);
  const stop = Number(row && row.stop);
  const target = Number(row && row.target);
  const risk = Math.abs(entry - stop);
  const sell = swarmVoteOf(row) === "SELL";
  if (!Number.isFinite(entry) || !risk) return [target, target, target];
  return sell
    ? [listed[0] || entry - risk, listed[1] || target || entry - risk * 2, listed[2] || entry - risk * 3]
    : [listed[0] || entry + risk, listed[1] || target || entry + risk * 2, listed[2] || entry + risk * 3];
}

function swarmTradeKind(row) {
  if (row && row.trade_kind) return t(row.trade_kind);
  const fut = (row && row.market_type === "futures") || isFuturesSymbol(row && row.symbol);
  return fut
    ? swarmVoteOf(row) === "SELL" ? t("futuresSell") : t("futuresBuy")
    : swarmVoteOf(row) === "SELL" ? t("spotSell") : t("spotBuy");
}

function tradeDateLocale() {
  const base = state.locale === "ar" ? "ar" : state.locale || "en";
  return `${base}-u-ca-gregory`;
}

function fmtTradeStamp(iso, timeOnly) {
  if (!iso) return "—";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "—";
  const loc = tradeDateLocale();
  return timeOnly
    ? date.toLocaleTimeString(loc, { hour: "2-digit", minute: "2-digit" })
    : date.toLocaleString(loc, { calendar: "gregory", year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
}

function fmtEntryWindow(row) {
  const start = row && (row.entry_from || row.trade_at || row.reviewed_at);
  const end = row && row.entry_until;
  if (!start && !end) return "—";
  const a = start ? new Date(start) : null;
  const b = end ? new Date(end) : null;
  const sameDay = a && b && !Number.isNaN(a.getTime()) && !Number.isNaN(b.getTime()) && a.toDateString() === b.toDateString();
  if (sameDay) return `${fmtTradeStamp(start, true)} — ${fmtTradeStamp(end, true)}`;
  return `${fmtTradeStamp(start)} — ${fmtTradeStamp(end)}`;
}

function swarmHitCard(row) {
  const vote = swarmVoteOf(row);
  const dir = vote === "SELL" ? "down" : "up";
  const kind = swarmTradeKind(row);
  const tps = swarmTargets(row);
  const votes = (row.agents || [])
    .map((agent) => {
      const side = String(agent.vote || "").toUpperCase() || (agent.direction === "bullish" ? "BUY" : agent.direction === "bearish" ? "SELL" : "WAIT");
      const cls = side === "BUY" ? "up" : side === "SELL" ? "down" : "muted";
      return `<span class="vote ${cls}">${t(agent.agent_name || agent.name)} · ${t(side)}</span>`;
    })
    .join("");
  const ratio = row.coordinator && row.coordinator.consensus_ratio != null
    ? `${Math.round(Number(row.coordinator.consensus_ratio) * 100)}%`
    : `${row.votes_for || 0}/8`;
  return `<button type="button" class="hit swarm-hit ${row.status === "approved" ? "elite" : ""}" data-swarm="${escapeHtml(row.signal_key || "")}">
      <span class="hit-main">${assetLogo(row.symbol, { size: "sm" })}<span>${escapeHtml(formatSymbolLabel(row.symbol))}
        <br><small class="${dir}">${escapeHtml(kind)} · ${ratio}</small></span></span>
      <span class="swarm-facts">
        <span>${t("tradeFrame")} <b>${escapeHtml(row.timeframe || "—")}</b></span>
        <span>${t("tradeType")} <b class="${dir}">${escapeHtml(kind)}</b></span>
        <span>${t("entry")} <b>${fmtNum(row.entry)}</b></span>
        <span>${t("stop")} <b>${fmtNum(row.stop)}</b></span>
        <span>${t("target1")} <b>${fmtNum(tps[0])}</b></span>
        <span>${t("target2")} <b>${fmtNum(tps[1])}</b></span>
        <span>${t("target3")} <b>${fmtNum(tps[2])}</b></span>
        <span>${t("entryWindow")} <b>${escapeHtml(fmtEntryWindow(row))}</b></span>
        <span>${t("tradeTime")} <b>${escapeHtml(fmtTradeStamp(row.trade_at || row.reviewed_at || row.created_at))}</b></span>
      </span>
      <span class="vote-row">${votes}</span>
    </button>`;
}

function bindSwarmHits(host, rows) {
  host.querySelectorAll("[data-swarm]").forEach((btn) => {
    btn.onclick = () => {
      const row = rows.find((item) => item.signal_key === btn.dataset.swarm);
      if (!row) return;
      applyHuntToChart({
        symbol: row.symbol,
        timeframe: row.timeframe,
        venue: row.venue,
        side: swarmVoteOf(row) === "SELL" ? "bearish" : "bullish",
        confidence: row.hunter_confidence,
        entry: row.entry,
        stop: row.stop,
        target: (row.targets && row.targets[1]) || row.target2 || row.target,
        state: row.status,
      });
    };
  });
}

function bindVrcsSettings() {
  const save = () => persist("shc_vrcs", state.vrcs);
  const reload = () => {
    state.cells.forEach((cell) => {
      cache.delete(packUrl(cell.symbol));
      void loadCell(cell, { silent: true });
    });
  };
  const bind = (id, apply) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.oninput = (e) => {
      apply(e.target);
      save();
      reload();
    };
  };
  bind("p-period", (el) => {
    state.vrcs.compression_period = Number(el.value);
    document.getElementById("p-val").textContent = el.value;
  });
  bind("p-th", (el) => {
    state.vrcs.threshold_multiplier = Number(el.value) / 100;
    document.getElementById("t-val").textContent = state.vrcs.threshold_multiplier;
  });
  bind("p-vol", (el) => {
    state.vrcs.volume_factor = Number(el.value) / 100;
    document.getElementById("v-val").textContent = state.vrcs.volume_factor;
  });
  bind("p-lb", (el) => {
    state.vrcs.lookback_breakout = Number(el.value);
    document.getElementById("l-val").textContent = el.value;
  });
  const dash = document.getElementById("p-dash");
  if (dash) {
    dash.onchange = (e) => {
      state.vrcs.show_dashboard = e.target.checked;
      persist("shc_vrcs", state.vrcs);
      const cell = activeCell();
      if (cell) paintVrcsDashboard(cell);
    };
  }
}

/* --------------------------------------------------------------- markets */

function renderScanRows(rows) {
  const box = document.getElementById("symbols");
  if (!box) return;
  box.innerHTML = (rows || [])
    .map((s) => {
      const pct = Number(s.percentage || 0);
      return `<button class="symbol-row" data-sym="${s.symbol}" data-venue="${s.venue || state.venue}">
        <span class="sym-line">${assetLogo(s.symbol)}<span>${s.symbol}<br><small class="muted">${s.name || ""}</small></span></span>
        <span class="pct ${pct >= 0 ? "up" : "down"}">${Number.isFinite(pct) ? pct.toFixed(2) : "—"}%</span></button>`;
    })
    .join("") || `<p class="muted pad">${t("scanning")}</p>`;
  box.querySelectorAll(".symbol-row").forEach((btn) => {
    btn.onclick = () => {
      if (btn.dataset.venue) state.venue = btn.dataset.venue;
      setCellSymbol(state.activeCell, btn.dataset.sym);
    };
  });
}

async function loadScan() {
  try {
    const data = await apiCached(`/api/market/scan?venue=${state.venue}`, 30000);
    const box = document.getElementById("symbols");
    if (data.warning && box) {
      box.innerHTML = `<p class="down pad">${data.warning}</p>`;
    }
    renderScanRows(data[state.scanTab] || data.gainers || []);
    if (data.delayed && box) {
      box.insertAdjacentHTML("afterbegin", `<p class="muted pad">${t("delayedData")}</p>`);
    }
  } catch (err) {
    const box = document.getElementById("symbols");
    if (box) box.innerHTML = `<p class="down pad">${err.message}</p>`;
  }
}

const SEARCH_SEED = [
  ["BTC/USDT", "Bitcoin", "crypto"], ["ETH/USDT", "Ethereum", "crypto"], ["SOL/USDT", "Solana", "crypto"],
  ["XRP/USDT", "XRP", "crypto"], ["BNB/USDT", "BNB", "crypto"], ["ADA/USDT", "Cardano", "crypto"],
  ["DOGE/USDT", "Dogecoin", "crypto"], ["AVAX/USDT", "Avalanche", "crypto"], ["DOT/USDT", "Polkadot", "crypto"],
  ["LINK/USDT", "Chainlink", "crypto"], ["TON/USDT", "Toncoin", "crypto"], ["NEAR/USDT", "NEAR", "crypto"],
  ["APT/USDT", "Aptos", "crypto"], ["SUI/USDT", "Sui", "crypto"], ["LTC/USDT", "Litecoin", "crypto"],
  ["UNI/USDT", "Uniswap", "crypto"], ["ARB/USDT", "Arbitrum", "crypto"], ["OP/USDT", "Optimism", "crypto"],
  ["PEPE/USDT", "Pepe", "crypto"], ["SHIB/USDT", "Shiba", "crypto"], ["MATIC/USDT", "Polygon", "crypto"],
  ["2222.SR", "أرامكو", "tadawul"], ["1120.SR", "الراجحي", "tadawul"], ["2010.SR", "سابك", "tadawul"],
  ["1180.SR", "الأهلي", "tadawul"], ["7010.SR", "اس تي سي", "tadawul"], ["1211.SR", "معادن", "tadawul"],
  ["1150.SR", "الإنماء", "tadawul"], ["2280.SR", "المراعي", "tadawul"], ["5110.SR", "كهرباء السعودية", "tadawul"],
  ["AAPL", "Apple", "us"], ["MSFT", "Microsoft", "us"], ["NVDA", "NVIDIA", "us"], ["TSLA", "Tesla", "us"],
  ["AMZN", "Amazon", "us"], ["GOOGL", "Alphabet", "us"], ["META", "Meta", "us"], ["SPY", "S&P 500 ETF", "us"],
  ["QQQ", "Nasdaq 100 ETF", "us"], ["AMD", "AMD", "us"],
  ["GC=F", "Gold", "commodities"], ["SI=F", "Silver", "commodities"], ["CL=F", "WTI Crude", "commodities"],
  ["BZ=F", "Brent Crude", "commodities"], ["NG=F", "Natural Gas", "commodities"],
  ["ASML.AS", "ASML", "europe"], ["MC.PA", "LVMH", "europe"], ["SAP.DE", "SAP", "europe"],
  ["NESN.SW", "Nestlé", "europe"], ["SHEL.L", "Shell", "europe"], ["AZN.L", "AstraZeneca", "europe"],
  ["7203.T", "Toyota", "asia"], ["6758.T", "Sony", "asia"], ["0700.HK", "Tencent", "asia"],
  ["005930.KS", "Samsung", "asia"], ["2330.TW", "TSMC", "asia"],
];

function escapeHtml(value) {
  return String(value || "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function markMatch(text, q) {
  const raw = String(text || "");
  const needle = String(q || "").toLowerCase();
  const i = raw.toLowerCase().indexOf(needle);
  if (!needle || i < 0) return escapeHtml(raw);
  return `${escapeHtml(raw.slice(0, i))}<mark>${escapeHtml(raw.slice(i, i + needle.length))}</mark>${escapeHtml(raw.slice(i + needle.length))}`;
}

function searchIndex() {
  const seen = new Set();
  const rows = [];
  const push = (symbol, name, venue, extra) => {
    if (!symbol || seen.has(symbol)) return;
    seen.add(symbol);
    const spec = parseMarketSymbol(symbol);
    const desk = spec.crypto ? spec.desk : symbol;
    rows.push({
      kind: "symbol",
      symbol: desk,
      name: name || "",
      venue: venue || venueOf(symbol),
      exchange: spec.exchange,
      market_type: (extra && extra.market_type) || spec.marketType,
    });
    if (spec.crypto && spec.marketType === "spot") {
      const fut = `${spec.display}:FUT`;
      if (!seen.has(fut)) {
        seen.add(fut);
        rows.push({
          kind: "symbol",
          symbol: fut,
          name: name || spec.display.split("/")[0],
          venue: "crypto",
          exchange: "binance",
          market_type: "futures",
        });
      }
    }
  };
  SEARCH_SEED.forEach(([symbol, name, venue]) => push(symbol, name, venue));
  (state.watchlist || []).forEach((symbol) => push(symbol, "", venueOf(symbol)));
  (state.symbols || []).forEach((symbol) => push(symbol, "", venueOf(symbol)));
  (state.searchRemote || []).forEach((row) => push(row.symbol, row.name, row.venue, row));
  return rows;
}

function scoreHit(row, q) {
  const query = q.toLowerCase();
  const symbol = String(row.symbol || row.id || "").toLowerCase();
  const name = String(row.name || "").toLowerCase();
  if (symbol.startsWith(query)) return 0;
  if (name.startsWith(query)) return 1;
  if (symbol.includes(query)) return 2;
  if (name.includes(query)) return 3;
  return 9;
}

function matchesQuery(row, q) {
  const query = q.toLowerCase();
  return String(row.symbol || row.id || "").toLowerCase().includes(query) || String(row.name || "").toLowerCase().includes(query);
}

function liveSearchRows(q) {
  const query = q.trim();
  if (!query) return [];
  const guessed = [];
  const spec = parseMarketSymbol(query);
  const compact = query.toUpperCase().replace(/\s+/g, "");
  if (spec.crypto) {
    guessed.push({ kind: "symbol", symbol: spec.display, name: spec.display.split("/")[0], venue: "crypto", exchange: "binance", market_type: "spot" });
    guessed.push({ kind: "symbol", symbol: `${spec.display}:FUT`, name: spec.display.split("/")[0], venue: "crypto", exchange: "binance", market_type: "futures" });
  } else if (/^[A-Z0-9]{2,12}$/.test(compact) && !/[.=]/.test(compact) && !/^\d+$/.test(compact)) {
    const pair = `${compact}/USDT`;
    guessed.push({ kind: "symbol", symbol: pair, name: compact, venue: "crypto", exchange: "binance", market_type: "spot" });
    guessed.push({ kind: "symbol", symbol: `${pair}:FUT`, name: compact, venue: "crypto", exchange: "binance", market_type: "futures" });
  }
  const symbols = guessed.concat(searchIndex())
    .filter((row, i, all) => all.findIndex((item) => item.symbol === row.symbol && item.kind === row.kind) === i)
    .filter((row) => matchesQuery(row, query) || (row.venue === "crypto" && formatSymbolLabel(row.symbol).includes(compact)))
    .sort((a, b) => scoreHit(a, query) - scoreHit(b, query) || a.symbol.localeCompare(b.symbol))
    .slice(0, 12);
  const inds = catalogItems()
    .filter((ind) => matchesQuery({ symbol: ind.id, name: `${ind.name} ${t(ind.id)}` }, query))
    .sort((a, b) => scoreHit({ symbol: a.id, name: a.name }, query) - scoreHit({ symbol: b.id, name: b.name }, query))
    .slice(0, 6)
    .map((ind) => ({ kind: "indicator", id: ind.id, name: ind.id === "vrcs" ? t("vrcs") : ind.name, locked: ind.locked }));
  return symbols.concat(inds);
}

function toggleIndicator(id) {
  const item = catalogItems().find((ind) => ind.id === id);
  if ((item && item.id === "vrcs" && vrcsLocked()) || (id === "vrcs" && vrcsLocked())) {
    paywall("vrcs");
    return false;
  }
  if (state.active.has(id)) state.active.delete(id);
  else state.active.add(id);
  persist("shc_inds", [...state.active]);
  state.cells.forEach((cell) => {
    cache.delete(packUrl(cell.symbol));
    void loadCell(cell, { silent: true });
  });
  return true;
}

function pickSearchHit(hit) {
  if (!hit) return;
  if (hit.kind === "indicator") {
    toggleIndicator(hit.id);
    if (state.view !== "chart") go("chart");
    return;
  }
  if (hit.venue) {
    state.venue = hit.venue;
    document.querySelectorAll("[data-venue]").forEach((el) => el.classList.toggle("active", el.dataset.venue === state.venue));
    if (document.getElementById("symbols")) void loadScan();
  }
  if (state.view === "watchlist") {
    addWatch(hit.symbol);
    void renderWatchlistPage();
    return;
  }
  if (state.view === "analytics") {
    const input = document.getElementById("an-symbol");
    if (input) input.value = hit.symbol;
    if (hit.venue) state.venue = hit.venue;
    void loadAnalyticsProfile(hit.symbol);
    return;
  }
  if (state.view === "markets") {
    const input = document.getElementById("mk-search");
    if (input) input.value = hit.symbol;
    if (hit.venue) {
      setVenue(hit.venue, { rescan: false });
      document.querySelectorAll("[data-mk-venue]").forEach((el) => el.classList.toggle("active", el.dataset.mkVenue === hit.venue));
    }
    return;
  }
  if (state.view !== "chart") go("chart");
  setCellSymbol(state.activeCell, hit.symbol);
}

function bindLiveSearch(input, hits, opts) {
  if (!input || !hits) return;
  const onSymbolQuery = opts && opts.onSymbolQuery;
  const onPick = opts && opts.onPick;
  const onClear = opts && opts.onClear;
  input.setAttribute("autocomplete", "off");
  input.setAttribute("spellcheck", "false");
  input.setAttribute("role", "combobox");
  hits.classList.add("search-hits");
  let timer = 0;
  let seq = 0;
  let active = -1;
  let rows = [];

  const close = () => {
    hits.innerHTML = "";
    hits.classList.add("hidden");
    active = -1;
    rows = [];
  };

  const paint = (list, q) => {
    rows = list;
    if (!q) {
      close();
      return;
    }
    hits.classList.remove("hidden");
    if (!list.length) {
      hits.innerHTML = `<p class="muted pad">${t("noHits")}</p>`;
      return;
    }
    hits.innerHTML = list
      .map((row, i) => {
        if (row.kind === "indicator") {
          return `<button type="button" class="search-hit ${i === active ? "active" : ""}" data-i="${i}">
            <span class="search-main"><span class="asset-mark asset-ind">◈</span><span><b>${markMatch(row.name, q)}</b><small class="muted"> ${markMatch(row.id, q)}</small></span></span>
            <span class="search-kind">${t("kindIndicator")}${state.active.has(row.id) ? " · ✓" : ""}</span>
          </button>`;
        }
        return `<button type="button" class="search-hit ${i === active ? "active" : ""}" data-i="${i}">
          <span class="search-main">${assetLogo(row.symbol)}<span class="search-name"><span class="search-title"><b>${markMatch(formatSymbolLabel(row.symbol), q)}</b>${watchIcon(row.symbol)}</span><br><small class="muted">${markMatch(row.name, q)}</small></span></span>
          <span class="search-kind">${marketKindLabel(row)}</span>
        </button>`;
      })
      .join("");
    hits.querySelectorAll("[data-i]").forEach((btn) => {
      btn.onmousedown = (e) => e.preventDefault();
      btn.onclick = () => {
        const hit = rows[Number(btn.dataset.i)];
        if (onPick) {
          if (hit && hit.symbol && hit.kind !== "indicator") input.value = hit.symbol;
          else input.value = "";
          close();
          onPick(hit);
          return;
        }
        input.value = "";
        close();
        pickSearchHit(hit);
      };
    });
    bindSearchWatch(hits);
  };

  const run = (q) => {
    paint(liveSearchRows(q), q);
  };

  const remote = (q, token) => {
    void apiCached(`/api/market/search?q=${encodeURIComponent(q)}&venue=${state.venue || ""}`, 8000)
      .then((data) => {
        if (token !== seq || input.value.trim() !== q) return;
        state.searchRemote = [...(state.searchRemote || []), ...(data.results || [])].slice(-80);
        const next = liveSearchRows(q);
        paint(next, q);
        if (onSymbolQuery) onSymbolQuery(q, next);
      })
      .catch(() => {});
  };

  input.oninput = () => {
    const q = input.value.trim();
    const token = ++seq;
    active = 0;
    if (!q) {
      close();
      if (onClear) onClear();
      return;
    }
    run(q);
    if (onSymbolQuery) {
      clearTimeout(input._newsQuery);
      input._newsQuery = setTimeout(() => onSymbolQuery(q, liveSearchRows(q)), 280);
    }
    clearTimeout(timer);
    timer = setTimeout(() => remote(q, token), 60);
  };
  input.onfocus = () => {
    const q = input.value.trim();
    if (q) run(q);
  };
  input.onkeydown = (e) => {
    if (!rows.length) {
      if (e.key === "Escape") close();
      return;
    }
    if (e.key === "ArrowDown") {
      e.preventDefault();
      active = (active + 1) % rows.length;
      paint(rows, input.value.trim());
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      active = (active - 1 + rows.length) % rows.length;
      paint(rows, input.value.trim());
    } else if (e.key === "Enter") {
      e.preventDefault();
      const hit = rows[Math.max(0, active)] || rows[0];
      if (onPick) {
        if (hit && hit.symbol && hit.kind !== "indicator") input.value = hit.symbol;
        close();
        onPick(hit);
        return;
      }
      input.value = "";
      close();
      pickSearchHit(hit);
    } else if (e.key === "Escape") {
      e.preventDefault();
      close();
    }
  };
  if (state.searchCloser) document.removeEventListener("click", state.searchCloser);
  state.searchCloser = (e) => {
    if (!hits.contains(e.target) && e.target !== input) close();
  };
  document.addEventListener("click", state.searchCloser);
}

function bindSearch() {
  bindLiveSearch(document.getElementById("sym-search"), document.getElementById("search-hits"));
}

/* ------------------------------------------------------------ chrome / UI */

const PAGE_HREF = {
  chart: "/chart",
  terminal: "/chart",
  agents: "/agents",
  analytics: "/analytics",
  watchlist: "/watchlist",
  paper: "/paper-trading",
  news: "/markets",
  reports: "/reports",
  indicators: "/indicators",
  markets: "/markets",
  history: "/history",
  settings: "/settings",
  plans: "/settings",
  auth: "/auth",
  admin: "/admin",
  reset: "/reset",
};

const PAGE_ALIASES = {
  "": "chart",
  chart: "chart",
  terminal: "chart",
  agents: "agents",
  analytics: "analytics",
  watchlist: "watchlist",
  "paper-trading": "paper",
  paper: "paper",
  news: "markets",
  reports: "reports",
  indicators: "indicators",
  markets: "markets",
  history: "history",
  settings: "settings",
  plans: "settings",
  auth: "auth",
  admin: "admin",
  reset: "reset",
};

function normalizePage(page) {
  return PAGE_ALIASES[page] || "chart";
}

function pageHref(page) {
  return PAGE_HREF[normalizePage(page)] || "/chart";
}

function currentPage() {
  const path = (location.pathname.replace(/^\//, "").split("/")[0] || "").toLowerCase();
  if (PAGE_ALIASES[path]) return PAGE_ALIASES[path];
  const raw = (location.hash.replace(/^#\/?/, "") || "").split("?")[0].toLowerCase();
  return PAGE_ALIASES[raw] || "chart";
}

function migrateHashRoute() {
  const raw = (location.hash.replace(/^#\/?/, "") || "").split("?")[0].toLowerCase();
  if (raw && PAGE_ALIASES[raw]) {
    const page = PAGE_ALIASES[raw];
    const path = pageHref(page);
    if (location.pathname === "/" || !PAGE_ALIASES[location.pathname.replace(/^\//, "").split("/")[0] || ""]) {
      const qs = location.hash.includes("?") ? `?${location.hash.split("?")[1]}` : location.search;
      history.replaceState({ page }, "", path + (qs || ""));
    }
    return;
  }
  if (location.pathname === "/" || location.pathname === "/terminal") {
    history.replaceState({ page: "chart" }, "", "/chart" + location.search);
  }
}

function go(page) {
  const next = normalizePage(page);
  const path = pageHref(next);
  const qs = location.search && next === currentPage() ? location.search : "";
  if (location.pathname === path) {
    void route();
    return;
  }
  history.pushState({ page: next }, "", path + qs);
  void route();
}

async function route() {
  const page = currentPage();
  if (page === "chart" || page === "terminal") return renderChartPage();
  if (page === "agents") return renderAgentsPage();
  if (page === "analytics") return renderAnalyticsPage();
  if (page === "watchlist") return renderWatchlistPage();
  if (page === "paper") return renderPaperPage();
  if (page === "news" || page === "markets") return renderMarketsPage();
  if (page === "indicators") return renderIndicatorsPage();
  if (page === "history") return renderHistoryPage();
  if (page === "reports") return renderReportsPage();
  if (page === "settings" || page === "plans") return renderSettingsPage();
  if (page === "admin") return renderAdminPage();
  if (page === "auth") return renderAuth();
  if (page === "reset") return renderReset();
  return renderChartPage();
}

function topbar() {
  const u = state.user;
  const page = state.view;
  const nav = [
    ["chart", t("pageChart")],
    ["agents", t("pageAgents")],
    ["analytics", t("pageAnalytics")],
    ["watchlist", t("pageWatchlist")],
    ["paper", t("pagePaper")],
    ["markets", t("pageMarkets")],
    ["reports", t("pageReports")],
    ["settings", t("pageSettings")],
  ];
  return `<header class="topbar">
    <a class="brand" href="/chart" data-go="chart">
      <img class="brand-logo" src="/assets/shc-logo.svg" alt="SHC" />
    </a>
    <nav class="main-nav">
      ${nav
        .map(([id, label]) => {
          const locked = (id === "agents" && !can("agents")) || (id === "analytics" && !can("analytics"));
          return `<button class="ghost tiny nav-item ${page === id ? "active" : ""} ${locked ? "locked" : ""}" data-go="${id}">${ico(id)}<span>${label}</span>${locked ? " 🔒" : ""}</button>`;
        })
        .join("")}
    </nav>
    <div class="topbar-actions">
      <span id="feed-status" class="muted small"></span>
      <span class="plan-chip">${t(state.access.subscription_tier || "explorer")}</span>
      <button class="ghost tiny" id="assist-btn" title="${t("assistant")}">${t("assistant")}</button>
      <button class="ghost tiny" id="sound-btn" title="${t("sound")}">${state.sound ? "🔔" : "🔕"}</button>
      <button class="ghost tiny" id="stealth-btn" title="${t("stealth")}">${state.stealth ? "🌙" : "☀"}</button>
      <button class="ghost tiny" id="mode-btn" title="${t("modeHint")}">${state.uiMode === "pro" ? t("proMode") : t("simpleMode")}</button>
      <button class="ghost tiny" id="theme-btn" title="${t("theme")}" aria-pressed="${state.theme === "light" ? "true" : "false"}">${themeBtnLabel()}</button>
      <div class="lang-wrap">
        <button class="ghost tiny" id="lang" title="${t("language")}">🌐 ${localeMeta(state.locale).short}<span class="caret">▾</span></button>
        <div class="lang-menu hidden" id="lang-menu">
          ${LOCALES.map(
            (loc) => `<button type="button" class="lang-item ${state.locale === loc.id ? "active" : ""}" data-locale="${loc.id}">
              <span>${t(`lang_${loc.id}`)}</span><span class="lang-code">${loc.short}</span>
            </button>`,
          ).join("")}
        </div>
      </div>
      <button class="ghost tiny ico-btn ops-ico ${page === "admin" ? "active" : ""}" id="ops-nav" data-go="admin" title="${t("opsLogin")}" aria-label="${t("opsLogin")}">${ico("admin")}</button>
      ${u ? `<button class="ghost tiny" id="logout">${t("logout")}</button>` : `<button class="primary tiny" id="go-login">${t("login")}</button>`}
    </div>
  </header>`;
}

function bindChrome() {
  document.querySelectorAll("[data-go]").forEach((btn) => {
    btn.onclick = (e) => {
      e.preventDefault();
      go(btn.dataset.go);
    };
  });
  const langBtn = document.getElementById("lang");
  const langMenu = document.getElementById("lang-menu");
  if (langBtn && langMenu) {
    langBtn.onclick = (e) => {
      e.stopPropagation();
      const drawMenuEl = document.getElementById("draw-menu");
      if (drawMenuEl) drawMenuEl.classList.add("hidden");
      langMenu.classList.toggle("hidden");
    };
    langMenu.querySelectorAll("[data-locale]").forEach((item) => {
      item.onclick = (e) => {
        e.stopPropagation();
        state.locale = item.dataset.locale;
        applyDir();
        void route();
      };
    });
    if (state.langMenuCloser) document.removeEventListener("click", state.langMenuCloser);
    state.langMenuCloser = (e) => {
      if (!langMenu.contains(e.target) && !langBtn.contains(e.target)) langMenu.classList.add("hidden");
    };
    document.addEventListener("click", state.langMenuCloser);
  }
  const login = document.getElementById("go-login");
  if (login) login.onclick = () => go("auth");
  const logout = document.getElementById("logout");
  if (logout)
    logout.onclick = () => {
      setToken("");
      state.user = null;
      go("chart");
    };
  const assist = document.getElementById("assist-btn");
  if (assist) assist.onclick = toggleAssistant;
  const sound = document.getElementById("sound-btn");
  if (sound)
    sound.onclick = () => {
      state.sound = !state.sound;
      persist("shc_sound", state.sound ? "1" : "0");
      if (state.sound) {
        enableSound();
        beep("bullish");
        if (window.Notification && Notification.permission === "default") void Notification.requestPermission();
      }
      sound.textContent = state.sound ? "🔔" : "🔕";
    };
  const stealth = document.getElementById("stealth-btn");
  if (stealth)
    stealth.onclick = () => {
      state.stealth = !state.stealth;
      persist("shc_stealth", state.stealth ? "1" : "0");
      applyStealth();
      stealth.textContent = state.stealth ? "🌙" : "☀";
      state.cells.forEach((cell) => cell.chart && cell.chart.applyOptions(chartTheme()));
    };
  const modeBtn = document.getElementById("mode-btn");
  if (modeBtn) modeBtn.onclick = () => toggleUiMode();
  const themeBtn = document.getElementById("theme-btn");
  if (themeBtn) themeBtn.onclick = () => toggleTheme();
}

function applyMobile() {
  document.body.classList.remove("show-markets", "show-chart", "show-panels", "show-indicators");
  document.body.classList.add(`show-${state.mobile}`);
  document.querySelectorAll(".mobile-tabs button").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.pane === state.mobile);
  });
}

const CLASSIC_FREE = new Set([
  "volume", "sma20", "sma50", "sma200", "ema12", "ema26", "wma", "rsi", "macd", "stoch", "momentum", "bb",
]);
const FALLBACK_CATALOG = [
  { id: "vrcs", name: "SHC VRCS", group: "shc" },
  { id: "sma20", name: "SMA 20", group: "trend" },
  { id: "sma50", name: "SMA 50", group: "trend" },
  { id: "sma200", name: "SMA 200", group: "trend" },
  { id: "ema12", name: "EMA 12", group: "trend" },
  { id: "ema26", name: "EMA 26", group: "trend" },
  { id: "vwap", name: "VWAP", group: "trend" },
  { id: "supertrend", name: "Supertrend", group: "trend" },
  { id: "ichimoku", name: "Ichimoku", group: "trend" },
  { id: "donchian", name: "Donchian", group: "volatility" },
  { id: "keltner", name: "Keltner", group: "volatility" },
  { id: "bb", name: "Bollinger Bands", group: "volatility" },
  { id: "atr", name: "ATR 14", group: "volatility" },
  { id: "rsi", name: "RSI 14", group: "momentum" },
  { id: "macd", name: "MACD", group: "momentum" },
  { id: "stoch", name: "Stochastic", group: "momentum" },
  { id: "willr", name: "Williams %R", group: "momentum" },
  { id: "cci", name: "CCI 20", group: "momentum" },
  { id: "obv", name: "OBV", group: "volume" },
  { id: "volume", name: "Volume", group: "volume" },
  { id: "wma", name: "WMA 20", group: "trend" },
  { id: "hma", name: "Hull MA 21", group: "trend" },
  { id: "dema", name: "DEMA 21", group: "trend" },
  { id: "tema", name: "TEMA 21", group: "trend" },
  { id: "zlema", name: "ZLEMA 21", group: "trend" },
  { id: "vwma", name: "VWMA 20", group: "trend" },
  { id: "psar", name: "Parabolic SAR", group: "trend" },
  { id: "pivots", name: "Pivot Points", group: "trend" },
  { id: "chandelier", name: "Chandelier Exit", group: "volatility" },
  { id: "adx", name: "ADX / DMI", group: "direction" },
  { id: "aroon", name: "Aroon", group: "direction" },
  { id: "vortex", name: "Vortex", group: "direction" },
  { id: "roc", name: "Rate of Change", group: "momentum" },
  { id: "momentum", name: "Momentum", group: "momentum" },
  { id: "trix", name: "TRIX", group: "momentum" },
  { id: "ppo", name: "PPO", group: "momentum" },
  { id: "ao", name: "Awesome Oscillator", group: "momentum" },
  { id: "uo", name: "Ultimate Oscillator", group: "momentum" },
  { id: "coppock", name: "Coppock Curve", group: "momentum" },
  { id: "kst", name: "KST", group: "momentum" },
  { id: "fisher", name: "Fisher Transform", group: "momentum" },
  { id: "wavetrend", name: "WaveTrend", group: "momentum" },
  { id: "squeeze", name: "Squeeze Momentum", group: "volatility" },
  { id: "bbextras", name: "BB %B / Bandwidth", group: "volatility" },
  { id: "elder", name: "Elder Ray", group: "direction" },
  { id: "mfi", name: "Money Flow Index", group: "volume" },
  { id: "cmf", name: "Chaikin Money Flow", group: "volume" },
  { id: "adline", name: "Accumulation / Distribution", group: "volume" },
  { id: "chaikin", name: "Chaikin Oscillator", group: "volume" },
  { id: "fi", name: "Force Index", group: "volume" },
  { id: "eom", name: "Ease of Movement", group: "volume" },
].map((ind) => ({ ...ind, locked: ind.id === "vrcs" }));

function catalogItems() {
  return Array.isArray(state.catalog) && state.catalog.length ? state.catalog : FALLBACK_CATALOG;
}

function indicatorRows() {
  const groups = {};
  catalogItems().forEach((ind) => {
    groups[ind.group] = groups[ind.group] || [];
    groups[ind.group].push(ind);
  });
  const rows = Object.entries(groups)
    .map(
      ([group, list]) =>
        `<div class="group">${group.toUpperCase()}</div>` +
        list
          .map(
            (ind) => {
              const locked = ind.id === "vrcs" && vrcsLocked();
              return `<label class="check ${locked ? "locked" : ""}"><input type="checkbox" data-ind="${ind.id}" ${
                state.active.has(ind.id) ? "checked" : ""
              } ${locked ? "data-lock=1" : ""}/> ${ind.id === "vrcs" ? t("vrcs") : ind.name}${locked ? " 🔒" : ""}</label>`;
            },
          )
          .join(""),
    )
    .join("");
  return rows;
}

function indicatorMenu() {
  return `<div class="ind-wrap">
    <button class="ghost tiny ico-btn" id="ind-btn">${ico("indicators")}<span>${t("indicators")}</span><span class="caret">▾</span></button>
    <div class="ind-menu hidden" id="ind-menu">
      <input id="ind-search" placeholder="${t("searchInd")}" autocomplete="off" />
      <div id="ind-list">${indicatorRows()}</div>
      <label class="check ${can("alerts") ? "" : "locked"}"><input type="checkbox" id="alerts-chk" ${
        state.alerts && can("alerts") ? "checked" : ""
      } ${can("alerts") ? "" : "data-lock=1"}/> ${t("alerts")}${can("alerts") ? "" : " 🔒"}</label>
    </div>
  </div>`;
}

function placeIndMenu() {
  const btn = document.getElementById("ind-btn");
  const menu = document.getElementById("ind-menu");
  if (!btn || !menu || menu.classList.contains("hidden")) return;
  const box = btn.getBoundingClientRect();
  const width = Math.min(320, window.innerWidth - 16);
  const rtl = document.documentElement.dir === "rtl";
  let left = rtl ? box.right - width : box.left;
  left = Math.max(8, Math.min(left, window.innerWidth - width - 8));
  const maxH = Math.min(window.innerHeight * 0.7, 560);
  let top = box.bottom + 6;
  if (top + 240 > window.innerHeight - 8) top = Math.max(8, box.top - maxH - 6);
  menu.style.width = `${Math.round(width)}px`;
  menu.style.left = `${Math.round(left)}px`;
  menu.style.right = "auto";
  menu.style.top = `${Math.round(top)}px`;
}

function bindIndicatorInputs(root) {
  const scope = root || document;
  scope.querySelectorAll("input[data-ind]").forEach((input) => {
    input.onchange = () => {
      if (input.dataset.lock === "1") {
        input.checked = false;
        paywall("vrcs");
        return;
      }
      if (input.checked) state.active.add(input.dataset.ind);
      else state.active.delete(input.dataset.ind);
      persist("shc_inds", [...state.active]);
      const count = document.querySelector(".ind-page-count");
      if (count) count.textContent = `${state.active.size} / ${catalogItems().length}`;
      state.cells.forEach((cell) => {
        cache.delete(packUrl(cell.symbol));
        void loadCell(cell, { silent: true });
      });
    };
  });
  const chk = scope.querySelector("#alerts-chk");
  if (chk)
    chk.onchange = () => {
      if (chk.dataset.lock === "1") {
        chk.checked = false;
        paywall("alerts");
        return;
      }
      state.alerts = chk.checked;
      persist("shc_alerts", state.alerts ? "1" : "0");
    };
  const filter = scope.querySelector("#ind-search");
  const list = scope.querySelector("#ind-list") || document.getElementById("ind-list");
  if (filter && list)
    filter.oninput = () => {
      const q = filter.value.trim().toLowerCase();
      list.querySelectorAll("label.check").forEach((lab) => {
        lab.style.display = !q || lab.textContent.toLowerCase().includes(q) ? "" : "none";
      });
    };
}

function bindIndicatorMenu() {
  const btn = document.getElementById("ind-btn");
  const menu = document.getElementById("ind-menu");
  if (!btn || !menu) return;
  if (menu.parentElement !== document.body) document.body.appendChild(menu);
  if (!state.indMenuPlace) {
    state.indMenuPlace = () => placeIndMenu();
    window.addEventListener("resize", state.indMenuPlace);
    window.addEventListener("scroll", state.indMenuPlace, true);
  }
  btn.onclick = (e) => {
    e.stopPropagation();
    menu.classList.toggle("hidden");
    placeIndMenu();
  };
  if (state.indMenuCloser) document.removeEventListener("click", state.indMenuCloser);
  state.indMenuCloser = (e) => {
    if (!menu.contains(e.target) && e.target !== btn) menu.classList.add("hidden");
  };
  document.addEventListener("click", state.indMenuCloser);
  bindIndicatorInputs(menu);
}

async function ensureCatalog() {
  if (!Array.isArray(state.catalog) || !state.catalog.length) state.catalog = FALLBACK_CATALOG;
  try {
    const pack = await api("/api/indicators/catalog");
    if (Array.isArray(pack.indicators) && pack.indicators.length) state.catalog = pack.indicators;
  } catch {
    /* fallback catalog already in place */
  }
}

function indicatorDock() {
  return `<aside class="ind-dock">
    <div class="ind-dock-head">
      <h2>${t("indicators")}</h2>
      <p class="muted">${t("indDockHint")}</p>
    </div>
    <div class="search-box">
      <input id="ind-search" placeholder="${t("searchInd")}" autocomplete="off" />
    </div>
    <div id="ind-list" class="ind-dock-list">${indicatorRows()}</div>
    <div class="ind-dock-foot">
      <label class="check ${can("alerts") ? "" : "locked"}"><input type="checkbox" id="alerts-chk" ${
        state.alerts && can("alerts") ? "checked" : ""
      } ${can("alerts") ? "" : "data-lock=1"}/> ${t("alerts")}${can("alerts") ? "" : " 🔒"}</label>
    </div>
  </aside>`;
}

function bindChartWorkspace() {
  const tfBar = document.getElementById("tf-bar");
  if (!tfBar) return;
  tfBar.innerHTML = TIMEFRAMES.map(
    (tf) => `<button class="${tf === state.timeframe ? "primary" : "ghost"} tiny tf" data-tf="${tf}">${tf}</button>`,
  ).join("");
  document.querySelectorAll(".tf").forEach((btn) => {
    btn.onclick = () => {
      state.timeframe = btn.dataset.tf;
      persist("shc_tf", state.timeframe);
      document.querySelectorAll(".tf").forEach((el) => {
        const on = el.dataset.tf === state.timeframe;
        el.classList.toggle("primary", on);
        el.classList.toggle("ghost", !on);
      });
      renderGrid();
    };
  });
  document.querySelectorAll(".split").forEach((btn) => {
    btn.onclick = () => {
      const wanted = Number(btn.dataset.split);
      if (wanted > maxCharts()) {
        paywall(wanted === 4 ? "split4" : "split2");
        return;
      }
      state.split = wanted;
      persist("shc_split", String(state.split));
      document.querySelectorAll(".split").forEach((el) => {
        const on = Number(el.dataset.split) === state.split;
        el.classList.toggle("primary", on);
        el.classList.toggle("ghost", !on);
      });
      renderGrid();
    };
  });
  bindDrawMenu();
  bindZoomControls();
  const shareBtn = document.getElementById("share-btn");
  if (shareBtn) shareBtn.onclick = () => void shareChart();
  if (!state.resizeBound) {
    window.addEventListener("resize", layoutCells);
    state.resizeBound = true;
  }
  renderGrid();
}

function cellShell(index, symbol) {
  return `<div class="cell ${index === state.activeCell ? "active" : ""}" data-index="${index}" data-symbol="${symbol}">
    <div class="cell-head">
      <span class="cell-sym">${assetLogo(symbol, { eager: true, size: "sm" })}${formatSymbolLabel(symbol)}${marketChip(symbol)}</span>
      <span class="cell-meta"></span>
      <span class="cell-status"></span>
    </div>
    <div class="cell-chart">
      <div class="vrcs-dash hidden" data-dash="${index}"></div>
      <div class="price-badge hidden" data-price-badge="${index}"></div>
      <canvas class="draw-layer"></canvas>
    </div>
    <div class="cell-osc hidden"></div>
  </div>`;
}

function setCellSymbol(index, symbol) {
  state.symbols[index] = normalizeDeskSymbol(symbol);
  persist("shc_symbols", state.symbols);
  renderGrid();
  paintMarketTypeTabs();
}

const MARKET_VENUES = ["crypto", "tadawul", "us", "europe", "asia", "commodities"];

function venueOf(symbol) {
  if (!symbol) return "crypto";
  if (symbol.includes("/")) return "crypto";
  if (/=F$/i.test(symbol)) return "commodities";
  if (/\.SR$/i.test(symbol) || /^\d+$/.test(symbol)) return "tadawul";
  if (/\.(L|PA|DE|AS|MI|SW|MC)$/i.test(symbol)) return "europe";
  if (/\.(T|HK|KS|KQ|SS|SZ|AX|TW|NS|BO)$/i.test(symbol)) return "asia";
  return "us";
}

function parseMarketSymbol(symbol) {
  let raw = String(symbol || "")
    .trim()
    .toUpperCase()
    .replace(/\s+/g, "");
  let marketType = "spot";
  if (!raw) return { display: "", desk: "", exchange: "", marketType: "", crypto: false };
  if (raw.startsWith("BINANCEUSDM:")) {
    raw = raw.slice("BINANCEUSDM:".length);
    marketType = "futures";
  } else if (raw.startsWith("BINANCE:")) {
    raw = raw.slice("BINANCE:".length);
  }
  const fut = raw.match(/:(FUT|P|PERP|USDT)$/);
  if (fut && (raw.includes("/") || /USDT$/.test(raw.replace(/:(FUT|P|PERP|USDT)$/, "")))) {
    raw = raw.slice(0, -fut[0].length);
    marketType = "futures";
  }
  if (!raw.includes("/")) {
    const quotes = ["USDT", "USDC", "BUSD", "FDUSD", "USD"];
    const quote = quotes.find((item) => raw.endsWith(item) && raw.length > item.length);
    if (quote) raw = `${raw.slice(0, -quote.length)}/${quote}`;
  }
  const crypto = raw.includes("/");
  return {
    display: raw,
    desk: crypto && marketType === "futures" ? `${raw}:FUT` : raw,
    exchange: crypto ? "binance" : "",
    marketType: crypto ? marketType : "",
    crypto,
  };
}

function normalizeDeskSymbol(symbol) {
  const spec = parseMarketSymbol(symbol);
  return spec.crypto ? spec.desk : String(symbol || "").trim().toUpperCase();
}

function formatSymbolLabel(symbol) {
  const spec = parseMarketSymbol(symbol);
  return spec.display || symbol || "";
}

function isFuturesSymbol(symbol) {
  return parseMarketSymbol(symbol).marketType === "futures";
}

function marketChip(symbol) {
  if (venueOf(symbol) !== "crypto") return "";
  const spec = parseMarketSymbol(symbol);
  return `<span class="mkt-chip">${t("binance")} · ${spec.marketType === "futures" ? t("futuresMkt") : t("spotMkt")}</span>`;
}

function marketKindLabel(row) {
  const symbol = row && row.symbol;
  if (venueOf(symbol) !== "crypto") return t((row && row.venue) || venueOf(symbol)) || t("kindSymbol");
  return `${t("binance")} · ${isFuturesSymbol(symbol) || (row && row.market_type === "futures") ? t("futuresMkt") : t("spotMkt")}`;
}

const FIAT_STABLES = new Set([
  "DAI",
  "FRAX",
  "GHO",
  "MIM",
  "FEI",
  "DOLA",
  "EURC",
  "EURT",
  "EURI",
  "AEUR",
  "EURS",
  "XSGD",
  "IDRT",
  "BIDR",
]);

function isStableSymbol(symbol) {
  const raw = String(symbol || "")
    .toUpperCase()
    .split(":")[0];
  const base = raw.includes("/") ? raw.split("/")[0] : raw;
  if (!base) return false;
  return FIAT_STABLES.has(base) || base.includes("USD");
}

function filterHuntHits(hits) {
  return (hits || []).filter((hit) => hit && hit.symbol && !isStableSymbol(hit.symbol));
}

function assetTicker(symbol) {
  if (!symbol) return "";
  if (symbol.includes("/")) return symbol.split("/")[0].toUpperCase();
  return String(symbol).replace(/\.SR$/i, "").toUpperCase();
}

function assetInitials(symbol) {
  const key = assetTicker(symbol);
  if (!key) return "•";
  return /^\d+$/.test(key) ? key.slice(0, 2) : key.slice(0, 2);
}

function logoUrls(symbol) {
  const venue = venueOf(symbol);
  const key = assetTicker(symbol);
  const low = key.toLowerCase();
  if (!key) return [];
  const local = `/api/market/logo?symbol=${encodeURIComponent(symbol)}`;
  if (venue === "crypto") {
    return [
      local,
      `https://cdn.jsdelivr.net/gh/spothq/cryptocurrency-icons@master/svg/color/${encodeURIComponent(low)}.svg`,
      `https://assets.coincap.io/assets/icons/${encodeURIComponent(low)}@2x.png`,
    ];
  }
  const listed = venue === "tadawul" ? `${key}.SR` : key;
  return [
    local,
    `https://financialmodelingprep.com/image-stock/${encodeURIComponent(listed)}.png`,
    `https://assets.parqet.com/logos/symbol/${encodeURIComponent(listed)}?format=png`,
  ];
}

function failAssetLogo(img) {
  const alts = String(img.dataset.alts || "")
    .split("|")
    .filter(Boolean);
  if (alts.length) {
    img.dataset.alts = alts.slice(1).join("|");
    img.src = alts[0];
    return;
  }
  img.hidden = true;
  const glyph = img.nextElementSibling;
  if (glyph) glyph.hidden = false;
}

window.__shcLogoErr = failAssetLogo;

function assetLogo(symbol, opts) {
  const eager = opts && opts.eager;
  const size = (opts && opts.size) || "";
  const urls = logoUrls(symbol);
  const first = urls[0] || "";
  const rest = urls.slice(1).join("|");
  const lazy = eager ? "" : ' loading="lazy"';
  return `<span class="asset-mark ${size}" title="${escapeHtml(symbol)}">
    <img class="asset-logo" alt="" src="${escapeHtml(first)}" data-alts="${escapeHtml(rest)}"${lazy} decoding="async" referrerpolicy="no-referrer" onerror="window.__shcLogoErr&&window.__shcLogoErr(this)" />
    <span class="asset-glyph" hidden>${escapeHtml(assetInitials(symbol))}</span>
  </span>`;
}

function openOnChart(symbol) {
  if (!symbol) return;
  state.venue = venueOf(symbol);
  persist("shc_venue", state.venue);
  persist("shc_mk_venue", state.venue);
  state.mkVenue = state.venue;
  state.activeCell = 0;
  state.symbols[0] = symbol;
  persist("shc_symbols", state.symbols);
  go("chart");
}

function saveWatch() {
  persist("shc_watch", state.watchlist);
  void persistWatchRemote();
}

async function persistWatchRemote() {
  if (!state.user) return;
  try {
    const data = await api("/api/watchlist", {
      method: "PUT",
      body: JSON.stringify({ symbols: state.watchlist || [] }),
    });
    if (Array.isArray(data.symbols)) {
      state.watchlist = data.symbols;
      persist("shc_watch", state.watchlist);
    }
  } catch {
    /* keep the local copy until the next sync */
  }
}

async function syncWatchlist() {
  if (!state.user) {
    state.watchlist = readJSON("shc_watch", state.watchlist || ["BTC/USDT", "ETH/USDT"]);
    return state.watchlist;
  }
  try {
    const data = await api("/api/watchlist");
    const remote = data.symbols || [];
    const local = readJSON("shc_watch", []);
    if (!remote.length && local.length) {
      const merged = await api("/api/watchlist", { method: "PUT", body: JSON.stringify({ symbols: local }) });
      state.watchlist = merged.symbols || local;
    } else {
      state.watchlist = remote.length ? remote : local;
    }
    persist("shc_watch", state.watchlist);
  } catch {
    state.watchlist = readJSON("shc_watch", state.watchlist || []);
  }
  return state.watchlist;
}

function isWatched(symbol) {
  const key = String(symbol || "").toUpperCase();
  return (state.watchlist || []).some((item) => String(item).toUpperCase() === key);
}

function watchIcon(symbol) {
  const on = isWatched(symbol);
  return `<span class="search-watch ${on ? "on" : ""}" data-watch-add="${escapeHtml(symbol)}" title="${t("addWatch")}" role="button" aria-pressed="${on ? "true" : "false"}">${ico("star")}</span>`;
}

function bindSearchWatch(host) {
  if (!host) return;
  host.querySelectorAll("[data-watch-add]").forEach((btn) => {
    btn.onmousedown = (e) => e.preventDefault();
    btn.onclick = (e) => {
      e.preventDefault();
      e.stopPropagation();
      const symbol = btn.dataset.watchAdd;
      if (isWatched(symbol)) {
        const current = (state.watchlist || []).find((item) => String(item).toUpperCase() === String(symbol).toUpperCase());
        removeWatch(current || symbol);
      } else {
        addWatch(symbol);
      }
      btn.classList.toggle("on", isWatched(symbol));
      btn.setAttribute("aria-pressed", isWatched(symbol) ? "true" : "false");
      if (state.view === "markets") {
        paintSmartWatch();
        bindMarketActions(document.getElementById("mk-watch"));
        void refreshWatchQuotes();
      }
    };
  });
}

function addWatch(symbol) {
  if (!symbol) return;
  state.watchlist = [symbol, ...state.watchlist.filter((item) => item !== symbol)].slice(0, 40);
  saveWatch();
  paintWatchlist();
}

function removeWatch(symbol) {
  state.watchlist = state.watchlist.filter((item) => item !== symbol);
  saveWatch();
  paintWatchlist();
}

function renderGrid() {
  const grid = document.getElementById("grid");
  if (!grid) return;
  destroyCells();
  grid.className = `grid split-${state.split}`;
  const list = [];
  for (let i = 0; i < state.split; i += 1) list.push(state.symbols[i] || "BTC/USDT");
  if (state.symbols.length < list.length) {
    state.symbols = list.slice();
    persist("shc_symbols", state.symbols);
  }
  grid.innerHTML = list.map((sym, i) => cellShell(i, sym)).join("");
  if (state.activeCell >= state.split) state.activeCell = 0;
  state.cells = list.map((sym, i) => createCell(i, sym)).filter(Boolean);
  grid.querySelectorAll(".cell").forEach((el) => {
    el.onmousedown = () => {
      const idx = Number(el.dataset.index);
      if (idx === state.activeCell) return;
      state.activeCell = idx;
      grid.querySelectorAll(".cell").forEach((c) => c.classList.toggle("active", Number(c.dataset.index) === idx));
      void renderPanel();
    };
  });
  state.cells.forEach((cell) => void loadCell(cell));
  requestAnimationFrame(layoutCells);
  if (state.resizeObserver) state.resizeObserver.disconnect();
  if (window.ResizeObserver) {
    state.resizeObserver = new ResizeObserver(() => layoutCells());
    state.resizeObserver.observe(grid);
    grid.querySelectorAll(".cell").forEach((el) => state.resizeObserver.observe(el));
  }
  connectLiveFeed();
  void renderPanel();
}

async function renderTerminal() {
  return renderChartPage();
}

function simpleExecBar() {
  return `<div class="exec-bar" id="exec-bar">
    <button type="button" class="primary exec-long" id="exec-long">${t("execLong")}</button>
    <button type="button" class="ghost exec-short" id="exec-short">${t("execShort")}</button>
    <button type="button" class="ghost tiny" data-go="paper">${t("pagePaper")}</button>
  </div>`;
}

function bindSimpleExec() {
  const fire = (side) => {
    const cell = activeCell();
    if (!cell || !cell.lastBar) {
      toast(t("connecting"), "bearish");
      return;
    }
    const last = Number(cell.lastBar.close);
    const stop = side === "long" ? last * 0.99 : last * 1.01;
    const target = side === "long" ? last * 1.02 : last * 0.98;
    void openPaperFromRisk(cell, { entry: last, stop, target, side });
  };
  const longBtn = document.getElementById("exec-long");
  const shortBtn = document.getElementById("exec-short");
  if (longBtn) longBtn.onclick = () => fire("long");
  if (shortBtn) shortBtn.onclick = () => fire("short");
}

async function renderChartPage() {
  state.view = "chart";
  teardown();
  applyUiMode();
  await ensureCatalog();
  const simple = isSimple();
  if (simple && state.split > 1) state.split = 1;
  const deskClass = simple
    ? "chart-desk simple-desk"
    : `chart-desk pro-desk${state.panelOpen === false ? " panel-collapsed" : ""}`;
  document.getElementById("app").innerHTML = `
    <div class="app-shell chart-only">
      ${topbar()}
      <div class="${deskClass}">
        <section class="chart-wrap chart-full">
          <div class="chart-toolbar">
            <div class="chart-sym-search">
              <input id="sym-search" placeholder="${t("search")}" autocomplete="off" />
              <div id="search-hits"></div>
            </div>
            <span class="sep"></span>
            ${drawMenu()}
            <span class="sep"></span>
            ${indicatorMenu()}
            ${
              simple
                ? ""
                : `<span class="sep"></span>
            <span class="muted small">${t("split")}</span>
            ${[1, 2, 4]
              .map((n) => `<button class="${state.split === n ? "primary" : "ghost"} tiny split" data-split="${n}">${n}${n > maxCharts() ? " 🔒" : ""}</button>`)
              .join("")}
            <span class="sep"></span>
            <button class="ghost tiny ico-btn" id="share-btn">${ico("share")}<span>${t("shareChart")}</span></button>
            <button class="ghost tiny ico-btn" id="panel-toggle" title="${state.panelOpen === false ? t("showSide") : t("hideSide")}">${ico(state.panelOpen === false ? "panelShow" : "panelHide")}<span>${state.panelOpen === false ? t("showSide") : t("hideSide")}</span></button>`
            }
            ${zoomControls()}
          </div>
          <div class="desk-head">
            <div class="venue-tabs desk-venues" id="desk-venues">
              ${MARKET_VENUES.map(
                (v) =>
                  `<button type="button" data-desk-venue="${v}" class="${state.venue === v ? "active" : ""}">${t(v)}${
                    v !== "crypto" && !can("live_equities") && !can("delayed_equities") ? " 🔒" : ""
                  }</button>`,
              ).join("")}
            </div>
            <div class="venue-tabs mkt-type-tabs" id="mkt-type-tabs">
              <button type="button" data-mkt="spot">${t("spotMkt")}</button>
              <button type="button" data-mkt="futures">${t("futuresMkt")}</button>
            </div>
            <div class="desk-hunt" id="desk-hunt"></div>
          </div>
          <div class="tf-bar" id="tf-bar"></div>
          <div class="grid split-${state.split}" id="grid"></div>
          <div class="ticker" id="tick">${t("live")}: —</div>
          ${simple ? simpleExecBar() : ""}
        </section>
        ${
          simple
            ? ""
            : `<aside class="panel right" id="side-panel">
          ${panelTabs()}
          <div id="panel-body"></div>
        </aside>
        <button type="button" class="panel-reopen" id="panel-reopen">${t("showSide")}</button>`
        }
      </div>
    </div>
    ${simple ? "" : assistantDock()}
    <div id="toasts"></div>`;
  bindChrome();
  applyStealth();
  applyUiMode();
  bindSearch();
  bindChartWorkspace();
  bindDeskVenues();
  bindMarketTypeTabs();
  const panelToggle = document.getElementById("panel-toggle");
  if (panelToggle) panelToggle.onclick = () => toggleSidePanel();
  const panelClose = document.getElementById("panel-close");
  if (panelClose) panelClose.onclick = () => {
    if (isPanelOpen()) toggleSidePanel();
  };
  const panelReopen = document.getElementById("panel-reopen");
  if (panelReopen) panelReopen.onclick = () => {
    if (!isPanelOpen()) toggleSidePanel();
  };
  applyPanelOpen();
  bindIndicatorMenu();
  if (!simple) {
    document.querySelectorAll("[data-panel]").forEach((btn) => {
      btn.onclick = () => {
        state.panel = btn.dataset.panel;
        void renderPanel();
      };
    });
    void renderPanel();
    watchHunter();
  } else {
    bindSimpleExec();
    void runDeskHunter({ auto: true }).catch(() => {});
  }
  if (state.user) {
    void api("/api/agents/desk")
      .then((data) => {
        if (data.desk) state.desk = data.desk;
        if (data.book) {
          data.book._at = Date.now();
          state.paperBook = data.book;
        }
      })
      .catch(() => {});
  }
}

async function renderWatchlistPage() {
  state.view = "watchlist";
  teardown();
  await syncWatchlist();
  document.getElementById("app").innerHTML = pageShell(
    t("pageWatchlist"),
    t("watchlists"),
    `<div class="card">
      <div class="search-box" style="border:0;padding:0">
        <input id="sym-search" placeholder="${t("search")}" autocomplete="off" />
        <div id="search-hits"></div>
      </div>
      <div class="venue-tabs" style="margin-top:10px">
        ${MARKET_VENUES
          .map((v) => `<button data-venue="${v}" class="${state.venue === v ? "active" : ""}">${t(v)}</button>`)
          .join("")}
      </div>
    </div>
    <div class="card">
      <strong>${t("watchlist")}</strong>
      <div id="watch-page" class="watch-page"></div>
    </div>`,
  );
  bindChrome();
  applyStealth();
  document.querySelectorAll("[data-venue]").forEach((btn) => {
    btn.onclick = () => setVenue(btn.dataset.venue);
  });
  bindSearch();
  const paint = async () => {
    const host = document.getElementById("watch-page");
    if (!host) return;
    const list = state.watchlist || [];
    if (!list.length) {
      host.innerHTML = `<p class="muted">${t("crossWatch")}</p>`;
      return;
    }
    host.innerHTML = list
      .map(
        (sym) => `<div class="watch-row" data-sym-row="${sym}">
          <button class="linkish watch-sym" data-open="${sym}">${assetLogo(sym)}<span>${formatSymbolLabel(sym)}</span>${marketChip(sym)}</button>
          <span data-last class="muted">—</span>
          <span data-pct class="pct">—</span>
          <button class="ghost tiny" data-watch-del="${sym}">${t("removeWatch")}</button>
        </div>`,
      )
      .join("");
    host.querySelectorAll("[data-open]").forEach((btn) => {
      btn.onclick = () => {
        const hunt = state.mkHunter && state.mkHunter[btn.dataset.open];
        if (hunt) applyHuntToChart(hunt);
        else openOnChart(btn.dataset.open);
      };
    });
    startQuotePulse(list, "watchlist");
    host.querySelectorAll("[data-watch-del]").forEach((btn) => {
      btn.onclick = () => {
        removeWatch(btn.dataset.watchDel);
        void paint();
      };
    });
    try {
      const data = await apiCached(`/api/market/quotes?symbols=${encodeURIComponent(list.join(","))}`, 8000);
      (data.quotes || []).forEach((row) => {
        const line = host.querySelector(`[data-sym-row="${row.symbol}"]`);
        if (!line) return;
        const last = line.querySelector("[data-last]");
        const pct = line.querySelector("[data-pct]");
        if (last) last.textContent = fmtNum(row.last);
        if (pct) {
          pct.textContent = pctText(row.percentage);
          pct.className = `pct ${pctClass(row.percentage)}`;
        }
      });
    } catch {
      /* quotes are optional on this page */
    }
  };
  void paint();
}

async function renderPaperPage() {
  state.view = "paper";
  teardown();
  await ensurePaperBook();
  const symbol = state.symbols[0] || "BTC/USDT";
  document.getElementById("app").innerHTML = pageShell(
    t("pagePaper"),
    t("paperHint"),
    `<div class="card">
      <div class="rr-grid">
        <label>${t("markets")}<input id="paper-sym" value="${symbol}" /></label>
        <label>${t("virtualBank")}<strong id="rr-wallet" class="bank-fixed">$${fmtBank(PAPER_BANK)}</strong></label>
        <label>${t("tradeAmount")}<input id="rr-amount" type="number" min="10" max="${PAPER_BANK}" step="100" value="${tradeAmount()}" /></label>
      </div>
      <div class="amount-chips">${[500, 1000, 2500, 5000, 10000, 25000]
        .map((n) => `<button type="button" class="ghost tiny" data-amt="${n}">$${n.toLocaleString("en-US")}</button>`)
        .join("")}</div>
      <p class="muted small">${t("amountHint")}</p>
      <div class="exec-bar" style="margin-top:12px">
        <button type="button" class="primary exec-long" id="paper-long">${t("execLong")}</button>
        <button type="button" class="ghost exec-short" id="paper-short">${t("execShort")}</button>
      </div>
      <p class="muted small" id="paper-last">${t("live")}: —</p>
    </div>
    <div id="paper-host"></div>`,
  );
  bindChrome();
  applyStealth();
  const host = document.getElementById("paper-host");
  const fakeCell = { symbol, lastBar: null };
  const refreshLast = async () => {
    const sym = (document.getElementById("paper-sym") || {}).value || symbol;
    fakeCell.symbol = sym;
    try {
      const tick = await api(`/api/market/ticker?symbol=${encodeURIComponent(sym)}`);
      fakeCell.lastBar = { close: Number(tick.last) };
      const el = document.getElementById("paper-last");
      if (el) el.textContent = `${t("live")}: ${fmtNum(tick.last)}`;
    } catch {
      /* keep previous */
    }
    await renderPaperPanel(host, fakeCell);
  };
  const openSide = (side) => {
    const last = fakeCell.lastBar && fakeCell.lastBar.close;
    if (!last) {
      toast(t("connecting"), "bearish");
      return;
    }
    state.risk.wallet = PAPER_BANK;
    const next = Number((document.getElementById("rr-amount") || {}).value);
    if (Number.isFinite(next) && next > 0) {
      state.risk.amount = Math.max(10, Math.min(PAPER_BANK, next));
      state.risk.pct = (state.risk.amount / PAPER_BANK) * 100;
    }
    persist("shc_risk", state.risk);
    void openPaperFromRisk(fakeCell, {
      entry: last,
      stop: side === "long" ? last * 0.99 : last * 1.01,
      target: side === "long" ? last * 1.02 : last * 0.98,
      side,
    }).then(() => void refreshLast());
  };
  const amountEl = document.getElementById("rr-amount");
  if (amountEl) {
    amountEl.oninput = () => {
      const next = Number(amountEl.value);
      if (Number.isFinite(next) && next > 0) {
        state.risk.amount = Math.max(10, Math.min(PAPER_BANK, next));
        state.risk.pct = (state.risk.amount / PAPER_BANK) * 100;
        persist("shc_risk", state.risk);
      }
    };
  }
  document.querySelectorAll("#app [data-amt]").forEach((btn) => {
    btn.onclick = () => {
      state.risk.amount = Number(btn.dataset.amt);
      state.risk.pct = (state.risk.amount / PAPER_BANK) * 100;
      if (amountEl) amountEl.value = String(state.risk.amount);
      persist("shc_risk", state.risk);
    };
  });
  document.getElementById("paper-long").onclick = () => openSide("long");
  document.getElementById("paper-short").onclick = () => openSide("short");
  void refreshLast();
}

function newsItemHtml(item) {
  const when = item.published_at ? new Date(item.published_at).toLocaleString() : "";
  return `<article class="news-item">
    <a href="${item.url}" target="_blank" rel="noopener noreferrer">${item.title}</a>
    <div class="muted small">${item.source || ""} · ${when}</div>
  </article>`;
}

function newsSymbol() {
  return state.newsFilter && state.newsFilter !== "all" ? state.newsFilter : "";
}

function paintNewsFilters() {
  const all = document.querySelector("[data-news='all']");
  if (all) all.classList.toggle("active", state.newsFilter === "all");
}

function matchSearchSymbol(q, rows) {
  const needle = String(q || "").trim().toUpperCase();
  if (!needle) return null;
  const symbols = (rows || []).filter((row) => row && row.symbol && row.kind !== "indicator");
  if (!symbols.length) return null;
  return (
    symbols.find((row) => String(row.symbol).toUpperCase() === needle) ||
    symbols.find((row) => assetTicker(row.symbol) === needle) ||
    symbols.find((row) => String(row.name || "").toUpperCase() === needle) ||
    symbols[0]
  );
}

function applyDeskNews(symbol, venue, opts) {
  if (!symbol || state.view !== "markets") return;
  state.newsFilter = symbol;
  persist("shc_news_filter", symbol);
  if (venue) state.venue = venue;
  paintNewsFilters();
  const input = document.getElementById("news-symbol");
  if (input && !(opts && opts.keepQuery)) input.value = symbol;
  const live = document.getElementById("news-live");
  if (live) live.textContent = `${t("relatedNews")} · ${symbol}`;
  void loadNewsFeed();
}

function clearDeskNews() {
  if (state.view !== "markets") return;
  state.newsFilter = "all";
  persist("shc_news_filter", "all");
  paintNewsFilters();
  const live = document.getElementById("news-live");
  if (live) live.textContent = t("latestNews");
  void loadNewsFeed();
}

function bindNewsSymbolSearch() {
  const input = document.getElementById("news-symbol");
  const hits = document.getElementById("news-hits");
  if (!input || !hits) return;
  bindLiveSearch(input, hits, {
    onPick: (hit) => {
      if (!hit || !hit.symbol || hit.kind === "indicator") return;
      applyDeskNews(hit.symbol, hit.venue);
    },
    onSymbolQuery: (q, rows) => {
      const hit = matchSearchSymbol(q, rows);
      if (hit) applyDeskNews(hit.symbol, hit.venue, { keepQuery: true });
    },
    onClear: () => clearDeskNews(),
  });
}

async function loadNewsFeed() {
  const host = document.getElementById("news-list");
  if (!host) return;
  const symbol = newsSymbol();
  const venue = symbol ? venueOf(symbol) || state.venue || "crypto" : state.mkVenue || state.venue || "crypto";
  const qs = new URLSearchParams({
    venue,
    locale: state.locale,
    limit: "36",
  });
  if (symbol) qs.set("symbol", symbol);
  try {
    const data = await api(`/api/news?${qs}`);
    const items = data.items || [];
    host.innerHTML = items.length ? items.map(newsItemHtml).join("") : `<p class="muted">${t("newsEmpty")}</p>`;
    if (items[0] && items[0].title) {
      document.title = `${items[0].title.slice(0, 72)} · SHC`;
      const live = document.getElementById("news-live");
      if (live) live.textContent = `${t("latestNews")}: ${items[0].title}`;
    }
  } catch (err) {
    host.innerHTML = `<p class="down">${err.message}</p>`;
  }
}

function bindNewsFilters() {
  document.querySelectorAll("[data-news='all']").forEach((btn) => {
    btn.onclick = () => {
      const input = document.getElementById("news-symbol");
      if (input) input.value = "";
      clearDeskNews();
    };
  });
}

async function renderNewsPage() {
  return renderMarketsPage();
}

async function renderIndicatorsPage() {
  state.view = "indicators";
  teardown();
  await ensureCatalog();
  const on = [...state.active];
  document.getElementById("app").innerHTML = `
    <div class="app-shell">
      ${topbar()}
      <div class="ind-page">
        <div class="ind-page-head">
          <div>
            <h1>${t("indicators")}</h1>
            <p class="muted">${t("indDockHint")}</p>
          </div>
          <div class="ind-page-actions">
            <input id="ind-search" placeholder="${t("searchInd")}" autocomplete="off" />
            <button class="primary" data-go="chart">${t("pageChart")}</button>
          </div>
        </div>
        <p class="muted ind-page-count">${on.length} / ${catalogItems().length}</p>
        <div id="ind-list" class="ind-page-grid">${indicatorRows()}</div>
        <label class="check ${can("alerts") ? "" : "locked"}"><input type="checkbox" id="alerts-chk" ${
          state.alerts && can("alerts") ? "checked" : ""
        } ${can("alerts") ? "" : "data-lock=1"}/> ${t("alerts")}${can("alerts") ? "" : " 🔒"}</label>
      </div>
    </div>
    ${assistantDock()}
    <div id="toasts"></div>`;
  bindChrome();
  applyStealth();
  bindIndicatorInputs(document.querySelector(".ind-page"));
}

function paintWatchlist() {
  const box = document.getElementById("watchlist");
  if (!box || !can("watchlists")) return;
  box.innerHTML = (state.watchlist || [])
    .map((sym) => `<button class="symbol-row" data-watch="${sym}"><span class="sym-line">${assetLogo(sym)}<span>${sym}</span></span></button>`)
    .join("");
  box.querySelectorAll("[data-watch]").forEach((btn) => {
    btn.onclick = () => setCellSymbol(state.activeCell, btn.dataset.watch);
  });
}

function fmtNum(value, digits = 2) {
  const n = Number(value);
  if (!Number.isFinite(n)) return "—";
  if (Math.abs(n) >= 1e12) return `${(n / 1e12).toFixed(2)}T`;
  if (Math.abs(n) >= 1e9) return `${(n / 1e9).toFixed(2)}B`;
  if (Math.abs(n) >= 1e6) return `${(n / 1e6).toFixed(2)}M`;
  return n.toLocaleString(undefined, { maximumFractionDigits: digits });
}

function pctClass(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return "";
  return n >= 0 ? "up" : "down";
}

function pctText(value) {
  const n = Number(value);
  if (!Number.isFinite(n)) return "—";
  return `${n >= 0 ? "+" : ""}${n.toFixed(2)}%`;
}

function flashRow(el, pct) {
  if (!el) return;
  el.classList.remove("tick-up", "tick-down");
  void el.offsetWidth;
  el.classList.add(Number(pct) >= 0 ? "tick-up" : "tick-down");
  setTimeout(() => el.classList.remove("tick-up", "tick-down"), 900);
}

function applyQuotePatch(symbol, last, percentage) {
  document.querySelectorAll(`[data-sym-row="${symbol}"]`).forEach((row) => {
    const price = row.querySelector("[data-last]");
    const pct = row.querySelector("[data-pct]");
    if (price && last != null) price.textContent = fmtNum(last);
    if (pct && percentage != null) {
      pct.textContent = pctText(percentage);
      pct.className = `pct ${pctClass(percentage)}`;
    }
    flashRow(row, percentage);
  });
}

function marketTable(title, rows, kind) {
  const body = (rows || [])
    .map((row) => {
      const hunt = state.mkHunter[row.symbol];
      return `<tr class="mk-row" data-sym-row="${row.symbol}" data-sym="${row.symbol}" data-venue="${row.venue || state.mkVenue}">
        <td><button class="linkish watch-sym" data-open="${row.symbol}">${assetLogo(row.symbol)}<span>${formatSymbolLabel(row.symbol)}${hunt ? ` <span class="hunt-dot" title="${t("hunterNear")}">◎</span>` : ""}</span></button>
          <div class="muted small">${row.name || ""} ${marketChip(row.symbol)}</div></td>
        <td data-last>${fmtNum(row.last)}</td>
        <td data-pct class="pct ${pctClass(row.percentage)}">${pctText(row.percentage)}</td>
        <td class="muted">${fmtNum(row.quote_volume || row.volume || row.market_cap, 0)}</td>
        <td><button class="ghost tiny" data-watch-add="${row.symbol}">+</button></td>
      </tr>`;
    })
    .join("");
  return `<article class="card mk-card">
    <strong>${title}</strong>
    <table class="mini mk-table"><thead><tr>
      <th>${kind === "sectors" ? t("sectors") : t("markets")}</th>
      <th>${kind === "sectors" ? t("trades") : t("live")}</th>
      <th>%</th>
      <th>${kind === "sectors" ? "#" : t("vol")}</th>
      <th></th>
    </tr></thead><tbody>${body || `<tr><td colspan="5" class="muted">${t("scanning")}</td></tr>`}</tbody></table>
  </article>`;
}

function sectorTable(rows) {
  const body = (rows || [])
    .map(
      (row) => `<tr class="mk-row" data-open-sector="${row.leader || ""}">
        <td>${row.sector}<div class="muted small">${row.leader || ""} · ${row.leader_name || ""}</div></td>
        <td>${pctText(row.percentage)}</td>
        <td class="pct ${pctClass(row.percentage)}">${pctText(row.percentage)}</td>
        <td class="muted">${row.count}</td>
        <td></td>
      </tr>`,
    )
    .join("");
  return `<article class="card mk-card">
    <strong>${t("sectors")}</strong>
    <table class="mini mk-table"><thead><tr><th>${t("sectors")}</th><th>${t("live")}</th><th>%</th><th>#</th><th></th></tr></thead>
    <tbody>${body || `<tr><td colspan="5" class="muted">${t("scanning")}</td></tr>`}</tbody></table>
  </article>`;
}

function renderTape(data) {
  const host = document.getElementById("mk-ticker");
  if (!host) return;
  const items = [];
  (data.indices || []).forEach((idx) => {
    items.push(`<span class="ticker-item"><b>${state.locale === "ar" ? idx.name_ar : idx.name_en}</b>
      <span>${fmtNum(idx.last)}</span><span class="${pctClass(idx.percentage)}">${pctText(idx.percentage)}</span></span>`);
  });
  const g = data.crypto_global || {};
  if (g.btc_dominance != null) items.push(`<span class="ticker-item"><b>${t("btcDom")}</b> ${Number(g.btc_dominance).toFixed(2)}%</span>`);
  if (g.total_market_cap != null) items.push(`<span class="ticker-item"><b>${t("totalCap")}</b> ${fmtNum(g.total_market_cap)}</span>`);
  if (g.total_volume != null) items.push(`<span class="ticker-item"><b>${t("totalVol")}</b> ${fmtNum(g.total_volume)}</span>`);
  if (g.btc_last != null) items.push(`<span class="ticker-item"><b>BTC</b> ${fmtNum(g.btc_last)} <span class="${pctClass(g.btc_percentage)}">${pctText(g.btc_percentage)}</span></span>`);
  const track = items.join("") + items.join("");
  host.innerHTML = `<div class="ticker-track">${track || `<span class="ticker-item">${t("scanning")}</span>`}</div>`;
}

function paintSmartWatch() {
  const box = document.getElementById("mk-watch");
  if (!box) return;
  box.innerHTML = (state.watchlist || [])
    .map((sym) => {
      const hunt = state.mkHunter[sym];
      return `<div class="watch-row" data-sym-row="${sym}">
        <button class="linkish watch-sym" data-open="${sym}">${assetLogo(sym)}<span>${formatSymbolLabel(sym)}${hunt ? ` <span class="hunt-dot" title="${t("hunterNear")}">◎ ${Number(hunt.confidence || 0).toFixed(0)}%</span>` : ""}</span>${marketChip(sym)}</button>
        <span data-last class="muted">—</span>
        <span data-pct class="pct">—</span>
        <button class="ghost tiny" data-watch-del="${sym}">×</button>
      </div>`;
    })
    .join("") || `<p class="muted pad">${t("crossWatch")}</p>`;
}

function bindMarketActions(root) {
  (root || document).querySelectorAll("[data-open]").forEach((btn) => {
    btn.onclick = () => {
      const hunt = state.mkHunter && state.mkHunter[btn.dataset.open];
      if (hunt) applyHuntToChart(hunt);
      else openOnChart(btn.dataset.open);
    };
  });
  (root || document).querySelectorAll("[data-open-sector]").forEach((row) => {
    row.onclick = () => {
      if (row.dataset.openSector) openOnChart(row.dataset.openSector);
    };
  });
  (root || document).querySelectorAll("[data-watch-add]").forEach((btn) => {
    btn.onclick = (e) => {
      e.stopPropagation();
      addWatch(btn.dataset.watchAdd);
      paintSmartWatch();
      bindMarketActions(document.getElementById("mk-watch"));
      void refreshWatchQuotes();
    };
  });
  (root || document).querySelectorAll("[data-watch-del]").forEach((btn) => {
    btn.onclick = (e) => {
      e.stopPropagation();
      removeWatch(btn.dataset.watchDel);
      paintSmartWatch();
      bindMarketActions(document.getElementById("mk-watch"));
    };
  });
}

function openMarketsSocket(key, symbols, futures) {
  closeLiveSocket(key);
  if (!symbols.length) return;
  const streams = [...new Set(symbols.map((sym) => `${binanceStreamId(sym)}@miniTicker`))];
  const host = binanceStreamHost(futures);
  const socket = new WebSocket(`${host}?streams=${streams.join("/")}`);
  socket.shcClosed = false;
  state[key] = socket;
  socket.onmessage = (evt) => {
    if (state[key] !== socket || state.view !== "markets") return;
    let msg;
    try {
      msg = JSON.parse(evt.data);
    } catch {
      return;
    }
    const payload = msg.data || msg;
    const raw = (payload.s || "").toUpperCase();
    if (!raw) return;
    const base = raw.endsWith("USDT") ? `${raw.slice(0, -4)}/USDT` : raw;
    const symbol = futures ? `${base}:FUT` : base;
    const last = Number(payload.c);
    const open = Number(payload.o);
    const pct = open ? ((last - open) / open) * 100 : 0;
    applyQuotePatch(symbol, last, pct);
  };
  socket.onclose = () => {
    if (socket.shcClosed || state.view !== "markets") return;
    setTimeout(() => {
      if (state.view === "markets") openMarketsSocket(key, symbols, futures);
    }, 2500);
  };
}

function connectMarketsFeed(symbols) {
  const crypto = [...new Set((symbols || []).filter(isCrypto))].slice(0, 36);
  const spot = crypto.filter((sym) => !isFuturesSymbol(sym));
  const fut = crypto.filter((sym) => isFuturesSymbol(sym));
  openMarketsSocket("mkWs", spot, false);
  openMarketsSocket("mkFutWs", fut, true);
}

async function refreshWatchQuotes() {
  if (!state.watchlist.length) return;
  try {
    const data = await api(`/api/market/quotes?symbols=${encodeURIComponent(state.watchlist.join(","))}`);
    (data.quotes || []).forEach((row) => applyQuotePatch(row.symbol, row.last, row.percentage));
  } catch {
    /* keep last painted ticks */
  }
}

async function refreshHunterBadges() {
  try {
    const venue = state.mkVenue || state.venue || "crypto";
    const data = await apiCached(
      `/api/hunter/scan?venue=${encodeURIComponent(venue)}&timeframe=15m&top=40&min_confidence=70&volume_spike=1.5`,
      25000,
    );
    state.mkHunter = {};
    [...filterHuntHits(data.hits), ...filterHuntHits(data.elite)].forEach((hit) => {
      if (hit && hit.symbol) state.mkHunter[hit.symbol] = hit;
    });
    paintSmartWatch();
    bindMarketActions(document.getElementById("mk-watch"));
    document.querySelectorAll(".mk-row[data-sym]").forEach((row) => {
      const hunt = state.mkHunter[row.dataset.sym];
      const mark = row.querySelector(".hunt-dot");
      if (hunt && !mark) {
        const btn = row.querySelector("[data-open]");
        if (btn) btn.insertAdjacentHTML("beforeend", ` <span class="hunt-dot" title="${t("hunterNear")}">◎</span>`);
      }
    });
  } catch {
    state.mkHunter = {};
  }
}

async function loadMarketsVenue() {
  const grid = document.getElementById("mk-grid");
  if (!grid) return;
  try {
    const data = await api(`/api/market/scan?venue=${state.mkVenue}`);
    if (data.delayed) {
      document.getElementById("mk-delay")?.classList.remove("hidden");
    } else {
      document.getElementById("mk-delay")?.classList.add("hidden");
    }
    grid.innerHTML = [
      marketTable(t("gainers"), data.gainers, "gainers"),
      marketTable(t("losers"), data.losers, "losers"),
      marketTable(t("activeVol"), data.active || data.mcap, "active"),
      sectorTable(data.sectors),
    ].join("");
    bindMarketActions(grid);
    const live = [
      ...(data.gainers || []),
      ...(data.losers || []),
      ...(data.active || []),
      ...state.watchlist.map((symbol) => ({ symbol })),
    ].map((row) => row.symbol);
    connectMarketsFeed(live);
    startQuotePulse(live, "markets");
  } catch (err) {
    if (err.upgrade) {
      paywall(err.upgrade);
      return;
    }
    grid.innerHTML = `<div class="card"><p class="down">${err.message}</p></div>`;
  }
}

async function renderMarketsPage() {
  state.view = "markets";
  teardown();
  if (location.pathname === "/news") {
    history.replaceState({ page: "markets" }, "", "/markets" + location.search);
  }
  state.newsFilter = "all";
  persist("shc_news_filter", "all");
  document.getElementById("app").innerHTML = `<div class="app-shell markets-shell">
    ${topbar()}
    <div class="ticker-tape" id="mk-ticker"><div class="ticker-track"><span class="ticker-item">${t("scanning")}</span></div></div>
    <div class="markets-page">
      <section class="markets-main">
        <div class="page-head">
          <h1>${t("pageMarkets")}</h1>
          <p class="muted">${t("marketsNewsHint")}</p>
        </div>
        <p id="mk-delay" class="muted pad hidden">${t("delayedData")}</p>
        <div class="venue-tabs mk-venues">
          ${MARKET_VENUES
            .map(
              (v) => `<button data-mk-venue="${v}" class="${state.mkVenue === v ? "active" : ""}">${t(v)}${
                v !== "crypto" && !can("live_equities") ? " 🔒" : ""
              }</button>`,
            )
            .join("")}
        </div>
        <div class="search-box mk-search">
          <input id="mk-search" placeholder="${t("search")}" autocomplete="off" />
          <div id="mk-hits"></div>
        </div>
        <div class="mk-grid" id="mk-grid"></div>
        <section class="card mk-news">
          <div class="news-head">
            <strong>${t("latestNews")}</strong>
            <div class="news-tools">
              <button class="ghost tiny active" data-news="all">${t("allNews")}</button>
              <div class="chart-sym-search news-sym-search">
                <input id="news-symbol" value="" placeholder="${t("newsSearch")}" autocomplete="off" />
                <div id="news-hits"></div>
              </div>
            </div>
          </div>
          <p class="muted small" id="news-live">${t("scanning")}</p>
          <div id="news-list"><p class="muted">${t("scanning")}</p></div>
        </section>
      </section>
      <aside class="markets-watch card">
        <strong>${t("watchlist")}</strong>
        <p class="muted small">${t("crossWatch")}</p>
        <div id="mk-watch"></div>
      </aside>
    </div>
  </div>${assistantDock()}<div id="toasts"></div>`;
  bindChrome();
  paintSmartWatch();
  bindMarketActions(document.getElementById("mk-watch"));
  document.querySelectorAll("[data-mk-venue]").forEach((btn) => {
    btn.onclick = () => {
      if (btn.dataset.mkVenue !== "crypto" && !can("live_equities") && !can("delayed_equities")) {
        paywall("live_equities");
        return;
      }
      setVenue(btn.dataset.mkVenue, { rescan: false });
      void loadMarketsVenue();
      void refreshHunterBadges();
      void loadNewsFeed();
    };
  });
  bindNewsFilters();
  bindNewsSymbolSearch();
  bindLiveSearch(document.getElementById("mk-search"), document.getElementById("mk-hits"));
  try {
    renderTape(await apiCached("/api/market/indices", 20000));
  } catch {
    renderTape({ indices: [], crypto_global: {} });
  }
  await loadMarketsVenue();
  await refreshWatchQuotes();
  void refreshHunterBadges();
  void loadNewsFeed();
  state.newsTimer = setInterval(() => void loadNewsFeed(), 45000);
  state.mkPoll = setInterval(() => {
    if (state.view !== "markets") return;
    void refreshWatchQuotes();
    void api("/api/market/indices")
      .then(renderTape)
      .catch(() => {});
  }, 12000);
}

async function loadFundamentals(cell) {
  const box = document.getElementById("fund-box");
  if (!box || !cell) return;
  try {
    const data = await apiCached(`/api/market/fundamentals?symbol=${encodeURIComponent(cell.symbol)}`, 60000);
    const mood = data.sentiment;
    const moodLabel = mood ? `${t(mood.bias) || mood.bias} · ${mood.score}` : "—";
    if (data.last && !cell.lastBar) cell.lastBar = { close: Number(data.last) };
    const rr = document.getElementById("rr-box");
    const entry = document.getElementById("rr-entry");
    if (rr && entry && !Number(entry.value) && data.last) {
      rr.dataset.symbol = "";
      paintRR(cell);
    }
    box.innerHTML = `<strong>${t("fundamentals")}</strong>
      <div>${data.name || cell.symbol}</div>
      <div>${t("mcap")}: ${fmtNum(data.market_cap || data.quote_volume)}</div>
      ${data.venue !== "crypto" ? `<div>${t("pe")}: ${data.pe != null ? Number(data.pe).toFixed(2) : "—"}</div>` : ""}
      ${data.industry || data.sector ? `<div>${t("industry")}: ${data.industry || data.sector}</div>` : ""}
      ${mood ? `<div>${t("sentiment")}: <span class="${mood.score >= 62 ? "up" : mood.score <= 38 ? "down" : "muted"}">${moodLabel}</span></div>` : ""}`;
  } catch (err) {
    box.innerHTML = `<strong>${t("fundamentals")}</strong><p class="muted">${err.message}</p>`;
  }
}

async function shareChart() {
  const cell = activeCell();
  if (!cell || !cell.chart || typeof cell.chart.takeScreenshot !== "function") {
    toast(t("noResult"), "bearish");
    return;
  }
  const shot = cell.chart.takeScreenshot();
  const out = document.createElement("canvas");
  const pad = 36;
  out.width = shot.width;
  out.height = shot.height + pad;
  const ctx = out.getContext("2d");
  ctx.fillStyle = "#05070a";
  ctx.fillRect(0, 0, out.width, out.height);
  ctx.drawImage(shot, 0, 0);
  ctx.fillStyle = "#0b1016";
  ctx.fillRect(0, shot.height, out.width, pad);
  ctx.fillStyle = "#c8a45a";
  ctx.font = "600 14px IBM Plex Sans";
  const who = (state.user && (state.user.display_name || state.user.email)) || "SHC";
  ctx.fillText(`SHC  ·  ${cell.symbol}  ·  ${state.timeframe}  ·  ${who}`, 12, shot.height + 23);
  ctx.fillStyle = "#8a6b2c";
  ctx.font = "11px IBM Plex Sans";
  ctx.fillText("Sovereign Hedge Console", out.width - 210, shot.height + 23);
  await new Promise((resolve) => {
    out.toBlob((blob) => {
      if (!blob) {
        resolve();
        return;
      }
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `SHC_${cell.symbol.replace("/", "")}_${state.timeframe}.png`;
      link.click();
      setTimeout(() => URL.revokeObjectURL(url), 1500);
      resolve();
    }, "image/png");
  });
  toast(t("shared"), "bullish");
}

function opsAge(seconds) {
  if (seconds == null) return "—";
  const n = Number(seconds);
  if (n < 60) return `${Math.round(n)}s`;
  if (n < 3600) return `${Math.round(n / 60)}m`;
  return `${(n / 3600).toFixed(1)}h`;
}

function paintOpsRoom(data) {
  const host = document.getElementById("ops-box");
  if (!host || !data) return;
  const agents = data.agents || {};
  const exec = agents.execution || {};
  const audit = agents.auditor || {};
  const paper = data.paper || {};
  const filters = data.filters || {};
  const hooks = data.hooks || {};
  const feeds = data.feeds || {};
  const live = (on) => `<span class="ops-dot ${on ? "on" : "off"}"></span>${on ? t("opsLive") : t("opsIdle")}`;
  const feedRow = (id) => {
    const row = feeds[id] || {};
    return `<tr>
      <td>${t(id)}</td>
      <td class="${row.ok ? "up" : "down"}">${row.ok ? t("stable") : t("connecting")}</td>
      <td class="muted">${row.symbols ?? "—"}</td>
      <td class="muted">${row.latency_ms != null ? `${row.latency_ms}ms` : "—"}</td>
    </tr>`;
  };
  const auditRows = (data.audit || [])
    .map(
      (row) => `<tr>
        <td class="muted">${(row.at || "").replace("T", " ").slice(0, 16)}</td>
        <td>${escapeHtml(row.user || "")}</td>
        <td>${row.win_rate != null ? `${row.win_rate}%` : "—"}</td>
        <td>${row.historical_win_rate != null ? `${row.historical_win_rate}%` : "—"}</td>
        <td>${row.threshold_from ?? "—"} → <strong>${row.threshold_to ?? "—"}</strong></td>
        <td class="${row.applied ? "up" : "muted"}">${row.applied ? t("opsCorrected") : "—"}</td>
        <td class="muted">${(row.notes || []).join(" · ") || "—"}</td>
      </tr>`,
    )
    .join("");
  const hookRows = (hooks.recent || [])
    .map(
      (row) => `<tr>
        <td class="muted">${(row.at || "").replace("T", " ").slice(0, 16)}</td>
        <td>${escapeHtml(row.user || "")}</td>
        <td>${escapeHtml(row.channel || "")}</td>
        <td>${escapeHtml(row.symbol || "")}</td>
        <td class="${row.ok ? "up" : "down"}">${row.ok ? t("opsDelivered") : t("opsFailed")}</td>
        <td class="muted">${escapeHtml(row.detail || "")}</td>
      </tr>`,
    )
    .join("");
  host.innerHTML = `
    <section class="card admin-wide"><strong>${t("opsAgents")}</strong>
      <div class="ops-kpis">
        <article><span class="muted">${t("opsExec")}</span><div>${live(exec.live)}</div>
          <div class="muted">${t("lastAudit")}: ${opsAge(exec.age_seconds)}</div></article>
        <article><span class="muted">${t("opsAudit")}</span><div>${live(audit.live)}</div>
          <div class="muted">${t("opsThreshold")}: ${audit.threshold_avg ?? "—"}</div></article>
        <article><span class="muted">${t("opsFills")}</span><div class="big">${(exec.closed_fills || 0) + (exec.open_fills || 0)}</div>
          <div class="muted">${t("openTrades")}: ${exec.open_fills || 0}</div></article>
        <article><span class="muted">${t("opsWinRate")}</span>
          <div class="big ${Number(exec.win_rate) >= 50 ? "up" : Number(exec.win_rate) ? "down" : ""}">${exec.win_rate != null ? `${exec.win_rate}%` : "—"}</div></article>
      </div>
    </section>
    <section class="card admin-wide"><strong>${t("opsAuditLog")}</strong>
      ${
        auditRows
          ? `<table class="mini wide-table"><tr><th></th><th></th><th>${t("opsWinRate")}</th><th>${t("opsHist")}</th><th>${t("opsThreshold")}</th><th></th><th></th></tr>${auditRows}</table>`
          : `<p class="muted">${t("opsNoAudit")}</p>`
      }
    </section>
    <section class="card admin-wide"><strong>${t("opsBotDay")}</strong>
      <p class="muted small">${t("opsBotReset")}</p>
      <div class="ops-kpis">
        <article><span class="muted">${t("opsBotOpened")}</span><div class="big">${(data.bot_day && data.bot_day.live && data.bot_day.live.opened) || 0}</div>
          <div class="muted">${t("openTrades")}: ${(data.bot_day && data.bot_day.live && data.bot_day.live.open_now) || 0}</div></article>
        <article><span class="muted">${t("opsBotProfit")}</span>
          <div class="big up">$${fmtBank((data.bot_day && data.bot_day.live && data.bot_day.live.profit) || 0)}</div>
          <div class="muted">${(data.bot_day && data.bot_day.live && data.bot_day.live.wins) || 0}</div></article>
        <article><span class="muted">${t("opsBotLoss")}</span>
          <div class="big down">$${fmtBank((data.bot_day && data.bot_day.live && data.bot_day.live.loss) || 0)}</div>
          <div class="muted">${(data.bot_day && data.bot_day.live && data.bot_day.live.losses) || 0}</div></article>
        <article><span class="muted">${t("opsBotWallet")}</span>
          <div class="big ${Number((data.bot_day && data.bot_day.live && data.bot_day.live.wallet) || 100000) >= 100000 ? "up" : "down"}">$${fmtBank((data.bot_day && data.bot_day.live && data.bot_day.live.wallet) || 100000)}</div>
          <div class="muted">${t("opsBotNextReset")}: ${
            data.bot_day && data.bot_day.next_reset_at
              ? String(data.bot_day.next_reset_at).replace("T", " ").slice(0, 16)
              : "12:00"
          }</div></article>
      </div>
      ${
        data.bot_day && data.bot_day.history && data.bot_day.history.length
          ? `<table class="mini wide-table"><tr><th>${t("opsBotHistory")}</th><th>${t("opsBotOpened")}</th><th>${t("opsBotProfit")}</th><th>${t("opsBotLoss")}</th><th>${t("opsBotWallet")}</th></tr>${data.bot_day.history
              .map(
                (row) => `<tr>
                  <td>${escapeHtml(row.day || "")}</td>
                  <td>${row.opened || 0}</td>
                  <td class="up">$${fmtBank(row.profit)}</td>
                  <td class="down">$${fmtBank(row.loss)}</td>
                  <td>$${fmtBank(row.wallet)}</td>
                </tr>`,
              )
              .join("")}</table>`
          : `<p class="muted">${t("opsNoBotDay")}</p>`
      }
    </section>
    <section class="card admin-wide"><strong>${t("opsPaperFleet")}</strong>
      <div class="ops-kpis">
        <article><span class="muted">${t("opsBank")}</span><div class="big">$${fmtBank(paper.unit_bank || 100000)}</div></article>
        <article><span class="muted">${t("opsPnl")}</span>
          <div class="big ${Number(paper.bot_realized_pnl) >= 0 ? "up" : "down"}">${Number(paper.bot_realized_pnl || 0) >= 0 ? "+" : ""}${fmtBank(paper.bot_realized_pnl)}</div></article>
        <article><span class="muted">${t("paperEquity")}</span><div>$${fmtBank(paper.fleet_cash)}</div>
          <div class="muted">${paper.accounts || 0} · ${t("opsBank")} $${fmtBank(paper.fleet_starting_cash)}</div></article>
      </div>
    </section>
    <section class="card"><strong>${t("opsFeeds")}</strong>
      <table class="mini"><tr><th></th><th></th><th></th><th>ms</th></tr>
        ${feedRow("crypto")}${feedRow("tadawul")}${feedRow("us")}${feedRow("europe")}${feedRow("asia")}${feedRow("commodities")}
      </table>
    </section>
    <section class="card"><strong>${t("opsFilter")}</strong>
      <div>${t("opsTradeable")}: <strong>${filters.tradeable ?? 0}</strong></div>
      <div>${t("opsBlocked")}: <strong class="down">${filters.stables_blocked ?? 0}</strong> / ${filters.crypto_listed ?? 0}</div>
      <p class="muted">${(filters.blocked_sample || []).join(" · ") || "—"}</p>
    </section>
    <section class="card admin-wide"><strong>${t("opsHooks")}</strong>
      <div class="muted">${t("opsDelivered")}: ${hooks.delivered_ok || 0} · ${t("opsFailed")}: ${hooks.failed || 0} · Telegram ${hooks.telegram_configured ? t("stable") : t("connecting")}</div>
      ${
        hookRows
          ? `<table class="mini wide-table">${hookRows}</table>`
          : `<p class="muted">${t("opsNoHooks")}</p>`
      }
    </section>`;
}

async function loadOpsRoom() {
  const data = await api("/api/admin/ops");
  paintOpsRoom(data);
}

function bindOpsGate() {
  const form = document.getElementById("ops-form");
  if (!form) return;
  form.onsubmit = async (evt) => {
    evt.preventDefault();
    const err = document.getElementById("ops-err");
    const btn = document.getElementById("ops-go");
    btn.disabled = true;
    try {
      const data = await api("/api/admin/ops/unlock", {
        method: "POST",
        body: JSON.stringify({ password: document.getElementById("ops-pass").value }),
      });
      state.opsToken = data.token || "";
      sessionStorage.setItem("shc_ops", state.opsToken);
      void renderAdminPage();
    } catch {
      if (err) err.textContent = t("opsWrong");
    } finally {
      btn.disabled = false;
    }
  };
}

async function renderAdminPage() {
  state.view = "admin";
  teardown();
  if (!state.opsToken && !(state.user && state.user.is_admin)) {
    document.getElementById("app").innerHTML = `<div class="ops-gate">
      <form class="auth-card" id="ops-form">
        <div class="brand"><img class="brand-logo" src="/assets/shc-logo.svg" alt="SHC" /></div>
        <h1>${t("opsGate")}</h1>
        <label class="field">${t("password")}<input id="ops-pass" type="password" autocomplete="current-password" required /></label>
        <p class="down" id="ops-err"></p>
        <button class="primary wide" id="ops-go">${t("opsUnlock")}</button>
        <button type="button" class="ghost wide" id="ops-back">${t("opsBack")}</button>
      </form>
    </div>`;
    bindOpsGate();
    const back = document.getElementById("ops-back");
    if (back) back.onclick = () => go("chart");
    return;
  }
  document.getElementById("app").innerHTML = `<div class="ops-page">
    <header class="ops-bar">
      <strong>${t("opsRoom")}</strong>
      <div class="ops-bar-actions">
        <button class="ghost tiny" id="ops-refresh">${t("scanNow")}</button>
        <button class="ghost tiny" id="ops-back">${t("opsBack")}</button>
        <button class="ghost tiny" id="ops-exit">${t("opsLock")}</button>
      </div>
    </header>
    <div class="admin-grid ops-grid" id="ops-box"><p class="muted">${t("scanning")}</p></div>
  </div>`;
  const refresh = async () => {
    try {
      await loadOpsRoom();
    } catch (err) {
      if (String(err.message || "").toLowerCase().includes("locked")) {
        state.opsToken = "";
        sessionStorage.removeItem("shc_ops");
        void renderAdminPage();
        return;
      }
      const box = document.getElementById("ops-box");
      if (box) box.innerHTML = `<div class="card"><p class="down">${err.message}</p></div>`;
    }
  };
  document.getElementById("ops-refresh").onclick = () => void refresh();
  const leaveOps = async (lock) => {
    if (lock) {
      try {
        await api("/api/admin/ops/lock", { method: "POST" });
      } catch {
        /* still leave locally */
      }
      state.opsToken = "";
      sessionStorage.removeItem("shc_ops");
    }
    go("chart");
  };
  document.getElementById("ops-back").onclick = () => void leaveOps(false);
  document.getElementById("ops-exit").onclick = () => void leaveOps(true);
  await refresh();
  state.opsTimer = setInterval(() => void refresh(), 15000);
}

/* ------------------------------------------------------------ auth / plans */

function hashQuery() {
  const search = new URLSearchParams(location.search);
  if ([...search.keys()].length) return search;
  return new URLSearchParams(location.hash.split("?")[1] || "");
}

async function finishLogin(token) {
  setToken(token);
  state.user = await api("/api/auth/me").catch(() => null);
  await loadAccess();
  await syncWatchlist();
  applyUiMode();
  watchSwarm();
  go("chart");
}

function renderAuth() {
  teardown();
  state.view = "auth";
  document.getElementById("app").innerHTML = `
    <div class="auth-page">
      <form class="auth-card" id="auth-form">
        <div class="brand"><img class="brand-logo" src="/assets/shc-logo.svg" alt="SHC" /></div>
        <h1 id="auth-title">${t("login")}</h1>
        <p class="muted" id="auth-tag">${t("tagline")}</p>
        <label class="field hidden" id="name-field">${t("name")}<input id="name" /></label>
        <label class="field" id="email-field">${t("email")}<input id="email" type="email" required /></label>
        <label class="field" id="password-field">${t("password")}<input id="password" type="password" minlength="8" /></label>
        <label class="field hidden" id="totp-field">${t("twoFactorCode")}<input id="totp" inputmode="numeric" autocomplete="one-time-code" maxlength="8" /></label>
        <p class="down" id="auth-error"></p>
        <button class="primary wide" type="submit" id="auth-submit">${t("login")}</button>
        <button type="button" class="ghost wide" id="ops-login">${t("opsLogin")}</button>
        <p class="muted" id="welcome-hint"></p>
        <p>
          <button type="button" class="ghost tiny" id="toggle-auth">${t("register")}</button>
          <button type="button" class="ghost tiny" id="forgot-btn">${t("forgot")}</button>
          <button type="button" class="ghost tiny" id="back-terminal">${t("terminal")}</button>
        </p>
      </form>
    </div><div id="toasts"></div>`;
  let mode = "login";
  let ticket = "";
  const title = document.getElementById("auth-title");
  const submit = document.getElementById("auth-submit");
  const emailField = document.getElementById("email-field");
  const passwordField = document.getElementById("password-field");
  const totpField = document.getElementById("totp-field");
  const nameField = document.getElementById("name-field");
  const applyMode = () => {
    title.textContent = mode === "forgot" ? t("forgot") : mode === "2fa" ? t("twoFactor") : t(mode);
    submit.textContent = mode === "forgot" ? t("sendReset") : mode === "2fa" ? t("continue2fa") : t(mode);
    nameField.classList.toggle("hidden", mode !== "register");
    emailField.classList.toggle("hidden", mode === "2fa");
    passwordField.classList.toggle("hidden", mode === "forgot" || mode === "2fa");
    totpField.classList.toggle("hidden", mode !== "2fa");
    document.getElementById("password").required = mode === "login" || mode === "register";
    document.getElementById("email").required = mode !== "2fa";
  };
  document.getElementById("back-terminal").onclick = () => go("chart");
  const opsLogin = document.getElementById("ops-login");
  if (opsLogin) opsLogin.onclick = () => go("admin");
  document.getElementById("toggle-auth").onclick = () => {
    mode = mode === "login" ? "register" : "login";
    ticket = "";
    applyMode();
  };
  document.getElementById("forgot-btn").onclick = () => {
    mode = "forgot";
    applyMode();
  };
  document.getElementById("auth-form").onsubmit = async (e) => {
    e.preventDefault();
    const err = document.getElementById("auth-error");
    err.textContent = "";
    try {
      if (mode === "forgot") {
        await api("/api/auth/forgot", {
          method: "POST",
          body: JSON.stringify({ email: document.getElementById("email").value }),
        });
        document.getElementById("welcome-hint").textContent = t("resetSent");
        return;
      }
      if (mode === "2fa") {
        const data = await api("/api/auth/2fa/verify", {
          method: "POST",
          body: JSON.stringify({ ticket, code: document.getElementById("totp").value }),
        });
        await finishLogin(data.access_token);
        return;
      }
      const data = await api(mode === "login" ? "/api/auth/login" : "/api/auth/register", {
        method: "POST",
        body: JSON.stringify({
          email: document.getElementById("email").value,
          password: document.getElementById("password").value,
          display_name: document.getElementById("name").value,
          locale: state.locale,
        }),
      });
      if (data.requires_2fa) {
        ticket = data.ticket;
        mode = "2fa";
        applyMode();
        document.getElementById("totp").focus();
        return;
      }
      if (mode === "register") toast(t("welcomeSent"), "bullish");
      await finishLogin(data.access_token);
    } catch (ex) {
      err.textContent = ex.message;
    }
  };
}

function renderReset() {
  teardown();
  state.view = "reset";
  const token = hashQuery().get("token") || "";
  document.getElementById("app").innerHTML = `
    <div class="auth-page">
      <form class="auth-card" id="reset-form">
        <div class="brand"><img class="brand-logo" src="/assets/shc-logo.svg" alt="SHC" /></div>
        <h1>${t("resetTitle")}</h1>
        <label class="field">${t("newPassword")}<input id="npw" type="password" required minlength="8" /></label>
        <label class="field">${t("confirmPassword")}<input id="npw2" type="password" required minlength="8" /></label>
        <p class="down" id="auth-error"></p>
        <button class="primary wide" type="submit">${t("savePassword")}</button>
        <p><button type="button" class="ghost tiny" id="back-auth">${t("login")}</button></p>
      </form>
    </div><div id="toasts"></div>`;
  document.getElementById("back-auth").onclick = () => go("auth");
  document.getElementById("reset-form").onsubmit = async (e) => {
    e.preventDefault();
    const err = document.getElementById("auth-error");
    const a = document.getElementById("npw").value;
    const b = document.getElementById("npw2").value;
    if (a !== b) {
      err.textContent = t("resetMismatch");
      return;
    }
    try {
      await api("/api/auth/reset", { method: "POST", body: JSON.stringify({ token, password: a }) });
      toast(t("resetDone"), "bullish");
      go("auth");
    } catch (ex) {
      err.textContent = ex.message;
    }
  };
}

function plansArticles(data) {
  const current = state.access.subscription_tier || "explorer";
  const name = (p) => (state.locale === "ar" ? p.name_ar : p.name_en) || t(p.id);
  const tag = (p) => (state.locale === "ar" ? p.tagline_ar : p.tagline_en) || "";
  return (data.plans || [])
    .map(
      (p) => `<article class="plan-card ${current === p.id ? "current" : ""}">
            <h2>${name(p)}</h2>
            <p class="muted">${tag(p)}</p>
            <p class="big">${p.price ? `$${p.price}` : t("explorer")}</p>
            <ul>${(p.features || []).map((f) => `<li>${f}</li>`).join("")}</ul>
            ${(p.locked || []).length ? `<p class="muted">${t("locked")}</p><ul class="locked-list">${p.locked.map((f) => `<li>🔒 ${f}</li>`).join("")}</ul>` : ""}
            <button class="primary wide sub" data-plan="${p.id}" ${!state.user || current === p.id ? "disabled" : ""}>${
              current === p.id ? t("plan") : p.price ? t("checkout") : t("upgrade")
            }</button>
          </article>`,
    )
    .join("");
}

function bindPlansCheckout() {
  document.querySelectorAll(".sub").forEach((btn) => {
    btn.onclick = async () => {
      if (!state.user) {
        go("auth");
        return;
      }
      btn.disabled = true;
      try {
        const result = await api("/api/subscriptions/checkout", { method: "POST", body: JSON.stringify({ plan: btn.dataset.plan }) });
        if (result.checkout_url) {
          window.location.assign(result.checkout_url);
          return;
        }
        cache.delete("/api/auth/me");
        cache.delete("/api/subscriptions/entitlements");
        state.user = await api("/api/auth/me");
        await loadAccess();
        go("settings");
      } catch (err) {
        toast(err.message, "bearish");
        btn.disabled = false;
      }
    };
  });
}

async function consumePayReturn() {
  const paidQs = hashQuery();
  if (paidQs.get("paid") === "1") {
    cache.delete("/api/auth/me");
    cache.delete("/api/subscriptions/entitlements");
    state.user = await api("/api/auth/me").catch(() => state.user);
    await loadAccess();
    toast(t("paySuccess"), "bullish");
    history.replaceState({ page: "settings" }, "", "/settings");
  } else if (paidQs.get("canceled") === "1") {
    toast(t("payCancel"), "bearish");
    history.replaceState({ page: "settings" }, "", "/settings");
  }
}

async function paintPlansCard() {
  const host = document.getElementById("plans-card");
  if (!host) return;
  try {
    cache.delete("/api/subscriptions/plans");
    const data = await api("/api/subscriptions/plans");
    const payHint = (data.payments || {}).provider === "stripe" ? t("stripeHint") : t("testPayHint");
    host.innerHTML = `<strong>${t("plans")}</strong>
      <p class="muted">${t("compare")} · ${payHint}</p>
      <div class="plans settings-plans">${plansArticles(data)}</div>
      ${state.user ? "" : `<p class="muted">${t("needAuth")}</p>`}`;
    bindPlansCheckout();
  } catch (err) {
    host.innerHTML = `<strong>${t("plans")}</strong><p class="down">${err.message}</p>`;
  }
}

async function renderPlans() {
  return renderSettingsPage();
}

function pageShell(title, subtitle, body) {
  return `<div class="app-shell">${topbar()}
    <div class="page-scroll">
      <div class="page-head"><h1>${title}</h1><p class="muted">${subtitle}</p></div>
      ${body}
    </div>
  </div>${assistantDock()}<div id="toasts"></div>`;
}

async function renderHistoryPage() {
  state.view = "history";
  teardown();
  if (!can("backtest")) {
    document.getElementById("app").innerHTML = pageShell(t("pageHistory"), t("locked"), `<div class="card"><p>${t("paywallTitle")}</p><button class="primary" id="up">${t("upgrade")}</button></div>`);
    bindChrome();
    document.getElementById("up").onclick = () => go("plans");
    return;
  }
  const symbol = state.symbols[0] || "BTC/USDT";
  const tf = state.timeframe === "1s" ? "1m" : state.timeframe;
  document.getElementById("app").innerHTML = pageShell(
    t("pageHistory"),
    `${symbol} · ${tf}`,
    `<div class="card" id="hist-box"><p class="muted">${t("scanning")}</p></div>`,
  );
  bindChrome();
  try {
    const data = await apiCached(
      `/api/hunter/backtest?symbol=${encodeURIComponent(symbol)}&timeframe=${tf}&horizon=24&reward_multiple=2`,
      60000,
    );
    const buckets = Object.entries(data.buckets || {})
      .map(([range, v]) => `<tr><td>${range}%</td><td>${v.trades}</td><td>${v.win_rate}%</td></tr>`)
      .join("");
    document.getElementById("hist-box").innerHTML = `
      <div class="big ${data.win_rate >= 50 ? "up" : "down"}">${t("winRate")}: ${data.win_rate}%</div>
      <div>${t("trades")}: ${data.total_signals} · ${t("closed")}: ${data.closed} · ${t("avgPnl")}: ${data.avg_pnl_pct}%</div>
      <div>90%+: ${data.high_confidence_win_rate}%</div>
      <table class="mini"><tr><th>${t("confidence")}</th><th>${t("trades")}</th><th>${t("winRate")}</th></tr>${buckets}</table>
      <a class="ghost wide center" href="/api/hunter/export.csv?symbol=${encodeURIComponent(symbol)}&timeframe=${tf}" download>${t("export")}</a>
      <table class="mini wide-table">
        <tr><th>#</th><th>${t("confidence")}</th><th>PnL</th><th></th></tr>
        ${(data.trades || []).slice().reverse().slice(0, 60).map((tr) => `<tr>
          <td>${new Date(tr.time * 1000).toISOString().slice(5, 16).replace("T", " ")}</td>
          <td class="${tr.side === "bullish" ? "up" : "down"}">${tr.confidence}%</td>
          <td class="${tr.pnl_pct >= 0 ? "up" : "down"}">${tr.pnl_pct}%</td>
          <td>${tr.outcome === "win" ? "✔" : tr.outcome === "loss" ? "✘" : "…"}</td>
        </tr>`).join("")}
      </table>`;
  } catch (err) {
    document.getElementById("hist-box").innerHTML = `<p class="down">${err.message}</p>`;
  }
}

async function renderReportsPage() {
  state.view = "reports";
  teardown();
  if (!can("analytics")) {
    document.getElementById("app").innerHTML = pageShell(t("pageReports"), t("locked"), `<div class="card"><p>${t("paywallTitle")}</p><button class="primary" id="up">${t("upgrade")}</button></div>`);
    bindChrome();
    document.getElementById("up").onclick = () => go("plans");
    return;
  }
  const symbol = state.symbols[0] || "BTC/USDT";
  document.getElementById("app").innerHTML = pageShell(
    t("pageReports"),
    t("analytics"),
    `<div class="report-grid">
      <div class="card" id="corr-card"><strong>${t("correlation")}</strong><p class="muted">${t("scanning")}</p></div>
      <div class="card" id="heat-card"><strong>${t("heatmap")}</strong><p class="muted">${t("scanning")}</p></div>
      <div class="card" id="cal-card"><strong>${t("calibrate")}</strong><p class="muted">${t("scanning")}</p></div>
    </div>`,
  );
  bindChrome();
  try {
    const corr = await apiCached("/api/hunter/correlation?timeframe=1h&top=12", 120000);
    document.getElementById("corr-card").innerHTML = `<strong>${t("correlation")} (BTC)</strong>
      <table class="mini">${(corr.btc_correlation || []).map((r) => {
        const v = r.correlation;
        const cls = v >= 0.7 ? "up" : v <= 0.2 ? "down" : "muted";
        return `<tr><td>${r.symbol}</td><td class="${cls}">${v.toFixed(2)}</td>
          <td><div class="bar"><span style="width:${Math.max(0, Math.min(100, v * 100))}%"></span></div></td></tr>`;
      }).join("")}</table>`;
  } catch (err) {
    document.getElementById("corr-card").innerHTML = `<strong>${t("correlation")}</strong><p class="down">${err.message}</p>`;
  }
  try {
    const heat = await apiCached(`/api/hunter/heatmap?symbol=${encodeURIComponent(symbol)}&timeframe=1h`, 300000);
    const max = Math.max(1, ...heat.hours.map((h) => h.compression));
    document.getElementById("heat-card").innerHTML = `<strong>${t("heatmap")} · ${heat.symbol} (UTC)</strong>
      <div>${t("peakHours")}: ${(heat.peak_hours || []).map((h) => `${h}:00`).join(", ")}</div>
      <div class="heat">${heat.hours.map((h) => `<div class="heat-cell" style="opacity:${0.15 + (h.compression / max) * 0.85}">${h.hour}${h.springs ? "<i>•</i>" : ""}</div>`).join("")}</div>`;
  } catch (err) {
    document.getElementById("heat-card").innerHTML = `<strong>${t("heatmap")}</strong><p class="down">${err.message}</p>`;
  }
  try {
    const cal = await apiCached("/api/hunter/calibration", 15000);
    const profile = cal.profile;
    document.getElementById("cal-card").innerHTML = profile
      ? `<strong>${t("calibrate")}</strong>
         <div>${profile.verdict} · offset ${profile.confidence_offset} · 90%+ → ${profile.suggested_alert_threshold}%</div>
         <table class="mini">${(profile.points || []).map((p) => `<tr><td>${p.printed}%</td><td>${p.realised}%</td><td>${p.trades}</td></tr>`).join("")}</table>
         <button class="primary wide" id="run-cal">${t("applyCal")}</button>`
      : `<strong>${t("calibrate")}</strong><p class="muted">${t("scanning")}</p><button class="primary wide" id="run-cal">${t("calibrate")}</button>`;
    const run = document.getElementById("run-cal");
    if (run)
      run.onclick = async () => {
        run.disabled = true;
        try {
          const result = await api("/api/hunter/calibrate?top=6&timeframes=15m,1h&apply=true");
          toast(`${t("calibrate")}: ${result.verdict} · ${result.suggested_alert_threshold}%`, "bullish");
          void renderReportsPage();
        } catch (err) {
          toast(err.message, "bearish");
        } finally {
          run.disabled = false;
        }
      };
  } catch (err) {
    document.getElementById("cal-card").innerHTML = `<p class="down">${err.message}</p>`;
  }
}

async function paintSecurityCard() {
  const box = document.getElementById("security-card");
  if (!box || !state.user) return;
  const enabled = Boolean(state.user.totp_enabled);
  const once = state.backupCodesOnce || [];
  state.backupCodesOnce = null;
  box.innerHTML = `<strong>${t("twoFactor")}</strong>
    <p class="muted">${t("twoFactorHint")}</p>
    <div>${enabled ? t("twoFactorOn") : t("twoFactorOff")}</div>
    ${once.length ? `<div><strong>${t("backupCodes")}</strong><code class="otp-secret">${once.join("  ")}</code></div>` : ""}
    <div id="totp-setup"></div>
    ${
      enabled
        ? `<label class="field">${t("password")}<input id="totp-pass" type="password" /></label>
           <label class="field">${t("twoFactorCode")}<input id="totp-off" inputmode="numeric" maxlength="8" /></label>
           <button class="ghost wide" id="totp-disable">${t("disable2fa")}</button>`
        : `<button class="primary wide" id="totp-start">${t("enable2fa")}</button>`
    }`;
  const start = document.getElementById("totp-start");
  if (start)
    start.onclick = async () => {
      try {
        const data = await api("/api/auth/2fa/setup", { method: "POST" });
        const host = document.getElementById("totp-setup");
        host.innerHTML = `<code class="otp-secret">${data.secret}</code>
          <button class="ghost tiny" id="totp-copy">${t("copySecret")}</button>
          <p class="muted small">${data.otpauth_url}</p>
          <label class="field">${t("twoFactorCode")}<input id="totp-on" inputmode="numeric" maxlength="8" /></label>
          <button class="primary wide" id="totp-confirm">${t("confirm2fa")}</button>`;
        document.getElementById("totp-copy").onclick = async () => {
          try {
            await navigator.clipboard.writeText(data.secret);
            toast(t("copySecret"));
          } catch {
            toast(data.secret);
          }
        };
        document.getElementById("totp-confirm").onclick = async () => {
          try {
            const result = await api("/api/auth/2fa/enable", {
              method: "POST",
              body: JSON.stringify({ code: document.getElementById("totp-on").value }),
            });
            state.user.totp_enabled = true;
            state.backupCodesOnce = result.backup_codes || [];
            toast(t("twoFactorOn"));
            void paintSecurityCard();
          } catch (err) {
            toast(err.message, "bearish");
          }
        };
      } catch (err) {
        toast(err.message, "bearish");
      }
    };
  const disable = document.getElementById("totp-disable");
  if (disable)
    disable.onclick = async () => {
      try {
        await api("/api/auth/2fa/disable", {
          method: "POST",
          body: JSON.stringify({
            password: document.getElementById("totp-pass").value,
            code: document.getElementById("totp-off").value,
          }),
        });
        state.user.totp_enabled = false;
        toast(t("twoFactorOff"));
        void paintSecurityCard();
      } catch (err) {
        toast(err.message, "bearish");
      }
    };
}

async function renderSettingsPage() {
  state.view = "settings";
  teardown();
  document.getElementById("app").innerHTML = pageShell(
    t("pageSettings"),
    t("health"),
    `<div class="card" id="plans-card"><strong>${t("plans")}</strong><p class="muted">${t("scanning")}</p></div>
    <div class="report-grid">
      <div class="card" id="mode-card">
        <strong>${t("uiMode")}</strong>
        <p class="muted">${t("modeHint")}</p>
        <div class="exec-bar">
          <button class="ghost ${state.uiMode !== "pro" ? "primary" : ""}" id="mode-simple">${t("simpleMode")}</button>
          <button class="ghost ${state.uiMode === "pro" ? "primary" : ""}" id="mode-pro">${t("proMode")}</button>
        </div>
      </div>
      <div class="card" id="theme-card">
        <strong>${t("theme")}</strong>
        <div class="exec-bar">
          <button class="ghost ${state.theme !== "light" ? "primary" : ""}" id="theme-dark">${t("darkTheme")}</button>
          <button class="ghost ${state.theme === "light" ? "primary" : ""}" id="theme-light">${t("lightTheme")}</button>
        </div>
      </div>
      <div class="card" id="access-card"><strong>${t("membership")}</strong><p class="muted">${t("needAuth")}</p></div>
      <div class="card" id="security-card"><strong>${t("twoFactor")}</strong><p class="muted">${t("needAuth")}</p></div>
      <div class="card" id="health-card"><strong>${t("health")}</strong><p class="muted">${t("scanning")}</p></div>
      <div class="card" id="ops-entry">
        <strong>${t("opsLogin")}</strong>
        <p class="muted">${t("opsGate")}</p>
        <button class="primary wide" id="ops-open">${t("opsUnlock")}</button>
      </div>
      <div class="card" id="admin-card"></div>
    </div>`,
  );
  bindChrome();
  await consumePayReturn();
  void paintPlansCard();
  const opsOpen = document.getElementById("ops-open");
  if (opsOpen) opsOpen.onclick = () => go("admin");
  const modeSimple = document.getElementById("mode-simple");
  const modePro = document.getElementById("mode-pro");
  if (modeSimple)
    modeSimple.onclick = () => {
      state.uiMode = "simple";
      persist("shc_ui_mode", "simple");
      applyUiMode();
      void renderSettingsPage();
    };
  if (modePro)
    modePro.onclick = () => {
      if (!canProMode()) {
        paywall("elite_brain");
        return;
      }
      state.uiMode = "pro";
      persist("shc_ui_mode", "pro");
      applyUiMode();
      void renderSettingsPage();
    };
  const themeDark = document.getElementById("theme-dark");
  const themeLight = document.getElementById("theme-light");
  if (themeDark)
    themeDark.onclick = () => {
      if (state.theme !== "dark") toggleTheme();
      void renderSettingsPage();
    };
  if (themeLight)
    themeLight.onclick = () => {
      if (state.theme !== "light") toggleTheme();
      void renderSettingsPage();
    };
  if (state.user) {
    void paintSecurityCard();
    try {
      const access = await api("/api/auth/access");
      document.getElementById("access-card").innerHTML = `<strong>${t("membership")}</strong>
        <div>${state.user.email} · ${access.effective_plan} · ${access.active ? t("stable") : "—"}</div>
        <div class="muted">${t("entitlements")}: ${(access.entitlements || []).join(" · ")}</div>
        ${state.user.email_verified ? "" : `<button class="ghost wide" id="resend">${t("verifyEmail")}</button>`}
        ${can("webhooks") ? `<label class="field">${t("webhook")}<input id="wh-url" value="" placeholder="https://..." /></label>
          <button class="ghost wide" id="wh-save">${t("webhook")}</button>` : ""}
        ${can("telegram") ? `<label class="field">${t("telegram")}<input id="tg-id" placeholder="chat id" /></label>
          <button class="ghost wide" id="tg-save">${t("telegram")}</button>` : ""}
        ${can("webhooks") || can("telegram") ? `<button class="primary wide" id="alert-test">${t("testAlert")}</button>` : ""}`;
      const resend = document.getElementById("resend");
      if (resend)
        resend.onclick = async () => {
          await api("/api/auth/resend-verification", { method: "POST" });
          toast(t("welcomeSent"), "bullish");
        };
      const wh = document.getElementById("wh-save");
      if (wh)
        wh.onclick = async () => {
          await api("/api/integrations/webhook", { method: "POST", body: JSON.stringify({ url: document.getElementById("wh-url").value }) });
          toast(t("webhook"), "bullish");
        };
      const tg = document.getElementById("tg-save");
      if (tg)
        tg.onclick = async () => {
          await api("/api/integrations/telegram", { method: "POST", body: JSON.stringify({ chat_id: document.getElementById("tg-id").value }) });
          toast(t("telegram"), "bullish");
        };
      const testBtn = document.getElementById("alert-test");
      if (testBtn)
        testBtn.onclick = async () => {
          testBtn.disabled = true;
          try {
            const result = await api("/api/alerts/test", { method: "POST" });
            const channels = Object.keys(result.channels || {});
            toast(channels.length ? t("alertSent") : t("saveFirst"), channels.length ? "bullish" : "bearish");
          } catch (err) {
            toast(err.message, "bearish");
          } finally {
            testBtn.disabled = false;
          }
        };
      const linked = await api("/api/integrations/me").catch(() => null);
      if (linked) {
        const whIn = document.getElementById("wh-url");
        const tgIn = document.getElementById("tg-id");
        if (whIn) whIn.value = linked.webhook_url || "";
        if (tgIn) tgIn.value = linked.telegram_chat_id || "";
      }
    } catch (err) {
      document.getElementById("access-card").innerHTML = `<p class="down">${err.message}</p>`;
    }
  }
  try {
    const [diag, hist] = await Promise.all([
      api("/api/system/diagnostics"),
      api("/api/system/history"),
    ]);
    const leak = hist.leak_suspected;
    document.getElementById("health-card").innerHTML = `<strong>${t("health")}</strong>
      <div>RSS ${diag.memory_rss_mb ?? "—"} MB · peak ${diag.memory_peak_mb} MB</div>
      <div>cache ${diag.server_cache_entries} · uptime ${Math.round(diag.uptime_seconds / 60)}m</div>
      <div>Binance ${diag.binance?.ok ? `${diag.binance.latency_ms}ms` : (diag.binance?.error || "—")}</div>
      <div class="${leak ? "down" : "up"}">${leak ? t("leak") : t("stable")} · Δ ${hist.memory_growth_mb ?? 0} MB</div>
      <div class="muted">Tadawul ${diag.stock_providers?.venues?.tadawul?.symbols ?? "—"} · US ${diag.stock_providers?.venues?.us?.symbols ?? "—"}</div>
      <button class="ghost wide" id="clear-cache">${t("refresh")}</button>`;
    document.getElementById("clear-cache").onclick = async () => {
      await api("/api/system/cache/clear", { method: "POST" });
      cache.clear();
      toast(t("refresh"), "bullish");
    };
  } catch (err) {
    document.getElementById("health-card").innerHTML = `<p class="down">${err.message}</p>`;
  }
  if (state.user && state.user.is_admin) {
    try {
      const admin = await api("/api/subscriptions/admin/members");
      document.getElementById("admin-card").innerHTML = `<strong>${t("members")}</strong>
        <table class="mini">${(admin.members || []).map((m) => `<tr>
          <td>${m.email}</td><td>${m.plan}</td><td>${m.email_verified ? "✓" : "—"}</td>
          <td><select data-email="${m.email}" class="plan-pick">
            ${["explorer", "pro_hunter", "elite_brain"].map((p) => `<option ${p === m.plan ? "selected" : ""}>${p}</option>`).join("")}
          </select></td></tr>`).join("")}</table>
        <p class="muted">${t("welcomeSent")}: ${(admin.outbox || []).length}</p>`;
      document.querySelectorAll(".plan-pick").forEach((sel) => {
        sel.onchange = async () => {
          await api("/api/subscriptions/admin/set-plan", {
            method: "POST",
            body: JSON.stringify({ email: sel.dataset.email, plan: sel.value }),
          });
          toast(`${sel.dataset.email} → ${sel.value}`, "bullish");
        };
      });
    } catch (err) {
      document.getElementById("admin-card").innerHTML = `<p class="down">${err.message}</p>`;
    }
  }
}

function assistantDock() {
  return `<aside id="assist-dock" class="assist-dock hidden">
    <header><strong>${t("assistant")}</strong><button class="ghost tiny" id="assist-close">×</button></header>
    <div id="assist-log" class="assist-log"></div>
    <div id="assist-sugs" class="assist-sugs"></div>
    <form id="assist-form">
      <input id="assist-q" placeholder="${t("notePlaceholder")}" autocomplete="off" />
      <button class="primary tiny" type="submit">${t("ask")}</button>
    </form>
  </aside>`;
}

function toggleAssistant() {
  if (!can("assistant")) {
    paywall("assistant");
    return;
  }
  let dock = document.getElementById("assist-dock");
  if (!dock) {
    document.body.insertAdjacentHTML("beforeend", assistantDock());
    dock = document.getElementById("assist-dock");
  }
  dock.classList.toggle("hidden");
  if (!dock.classList.contains("hidden")) bindAssistant();
}

function bindAssistant() {
  const dock = document.getElementById("assist-dock");
  if (!dock || dock.dataset.bound === "1") return;
  dock.dataset.bound = "1";
  const close = document.getElementById("assist-close");
  if (close) close.onclick = () => dock.classList.add("hidden");
  const form = document.getElementById("assist-form");
  const log = document.getElementById("assist-log");
  const ask = async (question) => {
    if (!question) return;
    log.innerHTML += `<div class="bubble me">${question}</div>`;
    const cell = activeCell();
    try {
      const data = await api("/api/assistant/ask", {
        method: "POST",
        body: JSON.stringify({
          question,
          symbol: cell ? cell.symbol : state.symbols[0],
          timeframe: state.timeframe,
          locale: state.locale,
        }),
      });
      log.innerHTML += `<div class="bubble ai">${data.answer.replace(/\n/g, "<br>")}</div>`;
    } catch (err) {
      log.innerHTML += `<div class="bubble ai down">${err.message}</div>`;
    }
    log.scrollTop = log.scrollHeight;
  };
  form.onsubmit = (e) => {
    e.preventDefault();
    const input = document.getElementById("assist-q");
    const q = input.value.trim();
    input.value = "";
    void ask(q);
  };
  void apiCached(`/api/assistant/suggestions?locale=${state.locale}`, 300000).then((data) => {
    const box = document.getElementById("assist-sugs");
    if (!box) return;
    box.innerHTML = (data.suggestions || [])
      .map((s) => `<button class="ghost tiny sug">${s}</button>`)
      .join("");
    box.querySelectorAll(".sug").forEach((btn) => {
      btn.onclick = () => void ask(btn.textContent);
    });
  }).catch(() => {});
}

async function boot() {
  applyDir();
  applyStealth();
  applyTheme();
  migrateHashRoute();
  if (state.token) {
    try {
      state.user = await api("/api/auth/me");
    } catch {
      setToken("");
      state.user = null;
    }
  }
  await loadAccess();
  applyUiMode();
  await syncWatchlist();
  window.addEventListener("popstate", () => void route());
  window.addEventListener("hashchange", () => {
    migrateHashRoute();
    void route();
  });
  await route();
  watchSwarm();
}

boot();
