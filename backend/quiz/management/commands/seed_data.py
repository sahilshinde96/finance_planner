"""
ARTH - Management command to seed database with all 72 KnowQuest questions.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from quiz.models import Quiz, Question
from schemes.models import GovernmentScheme
from streaks.models import Badge

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed ARTH database with all 72 questions, schemes, and badges'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🌱 Seeding ARTH database...'))
        self._create_quizzes()
        self._create_schemes()
        self._create_badges()
        self.stdout.write(self.style.SUCCESS('✅ ARTH database seeded successfully!'))

    def _create_quizzes(self):
        if Quiz.objects.exists():
            self.stdout.write('  Quizzes already exist, skipping...')
            return

        # ─── FARMER MODULE ─────────────────────────────────────────────────────
        farmer_l1 = Quiz.objects.create(
            title='Profitable Crops', description='Test your knowledge about high-profit crop selection',
            difficulty='easy', topic='farmer', user_type='farmer', level=1
        )
        farmer_l1_qs = [
            dict(text='Which crop typically gives the highest profit margin per acre in India?',
                 option_a='Rice', option_b='Sugarcane', option_c='Saffron', option_d='Wheat',
                 correct_option='C', difficulty_score=2,
                 hint='High-value spice crop',
                 explanation='Saffron fetches ₹2-3 lakh/kg and yields very high profit per acre, especially in Kashmir. It is the world\'s most expensive spice.'),
            dict(text='Tomatoes are best grown in which Indian season for maximum profit?',
                 option_a='Kharif (Monsoon)', option_b='Rabi (Winter)', option_c='Zaid (Summer)', option_d='Any season equally',
                 correct_option='B', difficulty_score=2,
                 hint='Cooler weather = better yield',
                 explanation='Tomatoes thrive in Rabi season (Oct-Feb). Winter temperatures reduce pest pressure and improve fruit quality, fetching better market prices.'),
            dict(text='Which oilseed crop is most profitable in semi-arid regions?',
                 option_a='Soybean', option_b='Groundnut', option_c='Mustard', option_d='Sesame',
                 correct_option='B', difficulty_score=2,
                 hint='Drought-tolerant oilseed',
                 explanation='Groundnut is highly profitable in semi-arid zones — it is drought-tolerant, grows well in sandy loam soil, and has steady market demand.'),
            dict(text="What is 'cash cropping'?",
                 option_a='Growing food only for family use', option_b='Growing crops primarily to sell for income',
                 option_c='Borrowing money for farming', option_d='Government farm subsidies',
                 correct_option='B', difficulty_score=1,
                 hint='Market-first farming',
                 explanation='Cash crops are grown specifically to sell in markets for monetary profit rather than personal consumption. Examples: cotton, tobacco, sugarcane.'),
            dict(text='Which vegetable crop has the fastest harvest cycle (~30 days)?',
                 option_a='Carrot', option_b='Cabbage', option_c='Radish', option_d='Brinjal',
                 correct_option='C', difficulty_score=1,
                 hint='Quick turnover = faster profit',
                 explanation='Radish matures in just 25-35 days, allowing 8-10 harvests per year. Its quick turnover makes it excellent for short-term cash generation.'),
            dict(text='Organic farming certification typically increases crop value by:',
                 option_a='5-10%', option_b='20-30%', option_c='50-200%', option_d='500%+',
                 correct_option='C', difficulty_score=3,
                 hint='Premium market opportunity',
                 explanation='Certified organic produce can command 50-200% higher prices in urban and export markets. Initial investment pays off within 2-3 seasons.'),
            dict(text="Which crop is known as 'white gold' due to its high profitability?",
                 option_a='Wheat', option_b='Cotton', option_c='Garlic', option_d='Potato',
                 correct_option='B', difficulty_score=2,
                 hint='Fiber crop with high market value',
                 explanation="Cotton is called 'white gold' — it is one of the most profitable crops globally, used in textiles and with a strong export market."),
            dict(text='What is the benefit of intercropping for farm profit?',
                 option_a='Reduces yield of both crops', option_b='Maximizes land use and income per acre',
                 option_c='Requires more water always', option_d='Only works in rainy seasons',
                 correct_option='B', difficulty_score=2,
                 hint='Two harvests, one field',
                 explanation='Intercropping grows two compatible crops simultaneously, maximizing land use efficiency. Example: maize + beans fixes nitrogen and doubles income per acre.'),
        ]
        for q in farmer_l1_qs:
            Question.objects.create(quiz=farmer_l1, **q)

        farmer_l2 = Quiz.objects.create(
            title='Soil & Region Science', description='Master soil types and regional crop suitability',
            difficulty='medium', topic='farmer', user_type='farmer', level=2
        )
        farmer_l2_qs = [
            dict(text='Which soil type is BEST suited for growing rice?',
                 option_a='Sandy loam', option_b='Laterite soil', option_c='Alluvial/clay soil', option_d='Black cotton soil',
                 correct_option='C', difficulty_score=4,
                 hint='Water-retaining soil wins',
                 explanation='Alluvial and clay soils retain water well, which is essential for paddy cultivation. River delta regions with these soils produce the best rice yields.'),
            dict(text='What does a soil pH of 8.5 indicate?',
                 option_a='Highly acidic', option_b='Slightly acidic', option_c='Neutral', option_d='Alkaline/basic',
                 correct_option='D', difficulty_score=4,
                 hint='pH scale: 7 is neutral, above = alkaline',
                 explanation='A pH of 8.5 is alkaline. Most crops prefer slightly acidic to neutral soil (6.0-7.5). Alkaline soil requires amendments like sulfur or organic matter.'),
            dict(text='Black cotton soil (Regur) is BEST for which crop?',
                 option_a='Tea', option_b='Cotton', option_c='Rice', option_d='Coconut',
                 correct_option='B', difficulty_score=3,
                 hint='The soil name gives a hint!',
                 explanation='Black cotton soil has excellent water retention and is rich in calcium, magnesium, and iron — perfect for cotton cultivation in Maharashtra, Gujarat, and MP.'),
            dict(text='Tea grows best in which type of region?',
                 option_a='Flat, dry plains', option_b='Hilly, acidic soil with high rainfall',
                 option_c='Coastal sandy soil', option_d='Desert with irrigation',
                 correct_option='B', difficulty_score=4,
                 hint='Think Darjeeling, Assam',
                 explanation='Tea requires well-drained, acidic soil (pH 4.5-6), high rainfall, cool temperatures, and misty hills. Assam and Darjeeling are ideal.'),
            dict(text='What is the main purpose of soil testing before planting?',
                 option_a='To check if land is fertile for any crop', option_b='To determine specific nutrient deficiencies and suitable crops',
                 option_c='To measure rainfall patterns', option_d='To check sunlight hours',
                 correct_option='B', difficulty_score=4,
                 hint='Targeted nutrition planning',
                 explanation='Soil testing reveals pH, NPK levels, and micronutrient status, allowing farmers to add precise amendments and select the most suitable crops.'),
            dict(text='Laterite soil found in coastal Karnataka is best for:',
                 option_a='Wheat and rice', option_b='Cashew and rubber', option_c='Sugarcane', option_d='Mustard',
                 correct_option='B', difficulty_score=5,
                 hint='Acidic tropical crops',
                 explanation='Laterite soil is acidic, low in nutrients, but suitable for cashew, rubber, and coconut — crops adapted to acidic, well-drained tropical conditions.'),
            dict(text='Which region in India is ideal for apple cultivation?',
                 option_a='Rajasthan', option_b='Punjab', option_c='Himachal Pradesh', option_d='Tamil Nadu',
                 correct_option='C', difficulty_score=3,
                 hint='Think cold mountains',
                 explanation='Himachal Pradesh, especially Shimla and Kullu valleys, provides the cool temperatures, high altitude, and well-distributed rainfall that apple trees need.'),
            dict(text='Over-application of chemical fertilizers typically causes:',
                 option_a='Permanently improved soil', option_b='Soil acidification and nutrient imbalance',
                 option_c='Better water retention', option_d='Faster seed germination',
                 correct_option='B', difficulty_score=5,
                 hint='More does not equal better in soil chemistry',
                 explanation='Excess chemical fertilizers acidify soil, disrupt microbial ecosystems, cause nutrient lock-up, and lead to long-term yield decline.'),
        ]
        for q in farmer_l2_qs:
            Question.objects.create(quiz=farmer_l2, **q)

        farmer_l3 = Quiz.objects.create(
            title='Farm Finance & Planning', description='Master financial strategies for farming success',
            difficulty='hard', topic='farmer', user_type='farmer', level=3
        )
        farmer_l3_qs = [
            dict(text='What is the PM-KISAN scheme in India?',
                 option_a='Free seeds program', option_b='Rs.6,000/year direct income support to farmers',
                 option_c='Free irrigation system', option_d='Crop loan waiver scheme',
                 correct_option='B', difficulty_score=6,
                 hint='Government direct benefit transfer',
                 explanation='PM-KISAN provides Rs.6,000 per year in three installments directly to eligible farmer families\' bank accounts as income support.'),
            dict(text='What is Crop Insurance (PMFBY) designed to protect?',
                 option_a='Only natural disaster losses', option_b='Losses due to pest attacks only',
                 option_c='Financial losses from crop failure due to various risks', option_d='Soil degradation only',
                 correct_option='C', difficulty_score=6,
                 hint='Comprehensive risk coverage',
                 explanation='Pradhan Mantri Fasal Bima Yojana (PMFBY) covers losses from natural calamities, pests, and diseases. Farmers pay minimal premium (2% Kharif, 1.5% Rabi).'),
            dict(text='What is a Kisan Credit Card (KCC) primarily used for?',
                 option_a='Buying farming land', option_b='Short-term crop production loans at subsidized rates',
                 option_c='Long-term infrastructure loans', option_d='Export subsidies',
                 correct_option='B', difficulty_score=5,
                 hint='Working capital for farmers',
                 explanation='KCC provides farmers revolving credit up to Rs.3 lakh at 4% interest for seeds, fertilizers, pesticides, and farm expenses.'),
            dict(text="If a farmer's input cost is Rs.50,000 and revenue is Rs.75,000, what is the profit margin?",
                 option_a='25%', option_b='33%', option_c='50%', option_d='150%',
                 correct_option='B', difficulty_score=7,
                 hint='Profit divided by Revenue x 100',
                 explanation='Profit = Rs.25,000. Margin = (25,000 / 75,000) x 100 = 33.3%. Understanding margins helps plan which crops to scale.'),
            dict(text="What is 'Minimum Support Price' (MSP)?",
                 option_a='Maximum price farmers can charge', option_b='Government guaranteed minimum price for crops',
                 option_c='Bank loan limit for farmers', option_d='Export price for crops',
                 correct_option='B', difficulty_score=6,
                 hint='Price floor protection',
                 explanation="MSP is the government's guaranteed minimum price for specific crops, ensuring farmers don't sell below cost of production."),
            dict(text='Which practice best helps a farmer reduce financial risk from a single crop failure?',
                 option_a='Mono-cropping the most popular crop', option_b='Crop diversification across multiple crops',
                 option_c='Applying more fertilizer', option_d='Selling crops before harvest',
                 correct_option='B', difficulty_score=6,
                 hint="Don't put all eggs in one basket",
                 explanation='Crop diversification means growing multiple crops so that if one fails due to weather or price crash, the others provide income — reducing overall farm financial risk.'),
            dict(text='Contract farming primarily benefits farmers by:',
                 option_a='Giving them freedom to sell anywhere', option_b='Guaranteeing pre-agreed prices and market access before harvest',
                 option_c='Providing free inputs only', option_d='Eliminating all farming risks',
                 correct_option='B', difficulty_score=7,
                 hint='Certainty before you plant',
                 explanation='In contract farming, companies guarantee a purchase price before the crop is planted. This eliminates market price uncertainty and often includes technical support.'),
            dict(text='The break-even point in farming means:',
                 option_a='Achieving maximum profit', option_b='Revenue equals total costs — zero profit or loss',
                 option_c='When the crop is fully grown', option_d='Government subsidy amount',
                 correct_option='B', difficulty_score=7,
                 hint='The survival minimum',
                 explanation='Break-even = when total revenue exactly covers total costs (seeds + labor + water + fertilizer). Knowing this helps farmers set minimum acceptable selling prices.'),
        ]
        for q in farmer_l3_qs:
            Question.objects.create(quiz=farmer_l3, **q)

        # ─── CORPORATE MODULE ───────────────────────────────────────────────────
        corp_l1 = Quiz.objects.create(
            title='Market Basics', description='Understand stock markets, indices, and trading fundamentals',
            difficulty='easy', topic='corporate', user_type='corporate', level=1
        )
        corp_l1_qs = [
            dict(text='What does SENSEX represent?',
                 option_a='30 large BSE-listed companies', option_b='All NSE-listed stocks',
                 option_c='Top 50 Indian banks', option_d='Government bond index',
                 correct_option='A', difficulty_score=2,
                 hint='Bombay Stock Exchange benchmark',
                 explanation='SENSEX (Sensitive Index) tracks 30 of the largest, most actively traded stocks on the Bombay Stock Exchange. It is India\'s oldest stock market index.'),
            dict(text='What is an IPO?',
                 option_a='A type of mutual fund', option_b='Initial Public Offering — a company\'s first stock sale to the public',
                 option_c='A government bond', option_d='An insurance product',
                 correct_option='B', difficulty_score=2,
                 hint='Company going public for first time',
                 explanation='An Initial Public Offering (IPO) is when a private company offers shares to the public for the first time to raise capital. Investors can apply during the subscription window.'),
            dict(text='Price-to-Earnings (P/E) ratio measures:',
                 option_a='Company\'s total debt', option_b='How much investors pay per rupee of earnings',
                 option_c='Annual dividend yield', option_d='Company\'s market share',
                 correct_option='B', difficulty_score=3,
                 hint='Valuation metric',
                 explanation='P/E = Stock Price / Earnings Per Share. A P/E of 20 means investors pay ₹20 for every ₹1 of earnings. High P/E = growth expectations; Low P/E = potential undervaluation.'),
            dict(text='What is an \'upper circuit\' in stock trading?',
                 option_a='When a stock gains more than expected', option_b='Maximum price limit a stock can rise in a single trading day',
                 option_c='When trading volume exceeds average', option_d='A stock\'s 52-week high',
                 correct_option='B', difficulty_score=3,
                 hint='Circuit breaker on upside',
                 explanation='SEBI sets circuit limits (typically 5%, 10%, 20%) to prevent extreme volatility. When a stock hits the upper circuit, no further buying is possible at higher prices.'),
            dict(text='NIFTY 50 tracks the performance of:',
                 option_a='50 largest government companies', option_b='Top 50 companies on NSE by market cap',
                 option_c='50 most profitable banks', option_d='50 infrastructure companies',
                 correct_option='B', difficulty_score=2,
                 hint='NSE\'s benchmark index',
                 explanation='NIFTY 50 is the flagship index of National Stock Exchange (NSE), comprising 50 diversified stocks from 13 sectors representing about 65% of NSE\'s total market cap.'),
            dict(text='Market capitalization of a company equals:',
                 option_a='Annual revenue', option_b='Total assets minus liabilities',
                 option_c='Share price × Total number of outstanding shares', option_d='Annual profit after tax',
                 correct_option='C', difficulty_score=3,
                 hint='Price × Shares',
                 explanation='Market Cap = Current Stock Price × Total Shares Outstanding. It represents the total market value of a company. Used to classify Large-cap, Mid-cap, Small-cap stocks.'),
            dict(text='An Index ETF (Exchange Traded Fund) aims to:',
                 option_a='Beat the market index consistently', option_b='Replicate the performance of a specific index like NIFTY 50',
                 option_c='Invest only in debt instruments', option_d='Invest in foreign markets only',
                 correct_option='B', difficulty_score=3,
                 hint='Passive investing vehicle',
                 explanation='Index ETFs passively track a specific index (like NIFTY 50) by holding the same stocks in the same proportion. They offer low-cost, diversified market exposure.'),
            dict(text='Short selling in stock markets means:',
                 option_a='Buying stocks for short duration', option_b='Selling borrowed shares hoping price will fall to buy back cheaper',
                 option_c='Selling only a few shares at a time', option_d='Placing stop-loss orders',
                 correct_option='B', difficulty_score=4,
                 hint='Profit from falling prices',
                 explanation='Short selling involves borrowing shares, selling them at current price, and buying them back later at a lower price. Profit = difference between sell price and buy-back price. High risk strategy.'),
        ]
        for q in corp_l1_qs:
            Question.objects.create(quiz=corp_l1, **q)

        corp_l2 = Quiz.objects.create(
            title='Investment Strategies', description='Advanced investment concepts and portfolio management',
            difficulty='medium', topic='corporate', user_type='corporate', level=2
        )
        corp_l2_qs = [
            dict(text='Dollar Cost Averaging (DCA) in investing means:',
                 option_a='Converting USD to INR regularly', option_b='Investing fixed amounts at regular intervals regardless of price',
                 option_c='Buying only at market lows', option_d='Timing the market perfectly',
                 correct_option='B', difficulty_score=5,
                 hint='Systematic investing approach',
                 explanation='DCA (same as SIP principle) means investing a fixed sum at regular intervals. You buy more units when prices are low and fewer when high, averaging out the purchase cost over time.'),
            dict(text='A stop-loss order is used to:',
                 option_a='Maximize profits', option_b='Automatically sell a security when it hits a preset lower price',
                 option_c='Buy stocks at a specific price', option_d='Lock in dividend income',
                 correct_option='B', difficulty_score=5,
                 hint='Downside protection tool',
                 explanation='A stop-loss order automatically triggers a sell order when the stock price falls to a specified level, limiting the investor\'s loss on a position.'),
            dict(text='Beta in stock analysis measures:',
                 option_a='Company\'s profitability', option_b='Stock\'s volatility relative to the broader market',
                 option_c='Dividend payout history', option_d='Company\'s debt level',
                 correct_option='B', difficulty_score=6,
                 hint='Sensitivity to market movements',
                 explanation='Beta measures how much a stock moves relative to the market. Beta > 1 = more volatile than market. Beta < 1 = less volatile. Beta = 1 = moves with market.'),
            dict(text='Portfolio rebalancing refers to:',
                 option_a='Adding more money to portfolio', option_b='Realigning portfolio weightings to maintain original desired risk-return profile',
                 option_c='Switching from stocks to bonds entirely', option_d='Selling all underperforming assets',
                 correct_option='B', difficulty_score=6,
                 hint='Maintaining target asset allocation',
                 explanation='As markets move, your portfolio drifts from target allocation. Rebalancing (selling over-performers, buying under-performers) restores your intended risk level.'),
            dict(text='Sharpe Ratio measures:',
                 option_a='Total portfolio returns', option_b='Risk-adjusted returns — excess return per unit of risk',
                 option_c='Portfolio liquidity', option_d='Dividend income',
                 correct_option='B', difficulty_score=7,
                 hint='Return per unit of risk',
                 explanation='Sharpe Ratio = (Portfolio Return - Risk-free Rate) / Standard Deviation. Higher Sharpe = better risk-adjusted performance. Used to compare funds with different risk levels.'),
            dict(text='A put option gives the buyer the right to:',
                 option_a='Buy shares at the strike price', option_b='Sell shares at the strike price before expiry',
                 option_c='Receive dividends guaranteed', option_d='Trade without paying brokerage',
                 correct_option='B', difficulty_score=6,
                 hint='Right to sell — useful for hedging',
                 explanation='A put option gives the holder the right (not obligation) to SELL the underlying asset at the strike price before expiry. Used to hedge against falling prices.'),
            dict(text='Debt-to-Equity (D/E) ratio of 0.5 means:',
                 option_a='Company has equal debt and equity', option_b='Company has 50 paise of debt for every ₹1 of equity',
                 option_c='Company is loss-making', option_d='Company has no equity',
                 correct_option='B', difficulty_score=6,
                 hint='Financial leverage indicator',
                 explanation='D/E = Total Debt / Total Equity. D/E of 0.5 means the company uses ₹0.50 of debt for every ₹1 of equity. Lower D/E generally means less financial risk.'),
            dict(text='RSI (Relative Strength Index) above 70 typically indicates:',
                 option_a='Stock is oversold — good time to buy', option_b='Stock is overbought — potential reversal downward',
                 option_c='Strong fundamentals', option_d='High dividend expected',
                 correct_option='B', difficulty_score=6,
                 hint='Momentum oscillator signal',
                 explanation='RSI ranges 0-100. Above 70 = overbought (possible sell signal). Below 30 = oversold (possible buy signal). It measures the speed and change of price movements.'),
        ]
        for q in corp_l2_qs:
            Question.objects.create(quiz=corp_l2, **q)

        corp_l3 = Quiz.objects.create(
            title='Advanced Corporate Finance', description='Expert-level corporate finance and valuation concepts',
            difficulty='hard', topic='corporate', user_type='corporate', level=3
        )
        corp_l3_qs = [
            dict(text='WACC (Weighted Average Cost of Capital) represents:',
                 option_a='Average stock market return', option_b='The average rate a company must pay to finance its assets, weighted by capital structure',
                 option_c='Government bond yield', option_d='Bank lending rate',
                 correct_option='B', difficulty_score=8,
                 hint='Hurdle rate for investments',
                 explanation='WACC = (Cost of Equity × Weight of Equity) + (Cost of Debt × Weight of Debt × (1-Tax)). Projects must earn returns above WACC to create shareholder value.'),
            dict(text='A hostile takeover occurs when:',
                 option_a='A company voluntarily merges with another', option_b='An acquirer bypasses target management to buy majority shares directly from shareholders',
                 option_c='Government nationalizes a company', option_d='Company declares bankruptcy',
                 correct_option='B', difficulty_score=8,
                 hint='Acquisition against management will',
                 explanation='In a hostile takeover, the acquiring company makes a direct tender offer to target shareholders or launches a proxy fight, bypassing or overriding the target management\'s resistance.'),
            dict(text='EV/EBITDA ratio is preferred over P/E for comparing companies because:',
                 option_a='It is simpler to calculate', option_b='It is capital structure neutral — unaffected by debt levels and tax differences',
                 option_c='It always gives lower valuation', option_d='It includes future growth projections',
                 correct_option='B', difficulty_score=9,
                 hint='Debt-neutral valuation metric',
                 explanation='EV/EBITDA (Enterprise Value to EBITDA) excludes the effects of capital structure, taxation, and non-cash charges, making it ideal for comparing companies across industries and countries.'),
            dict(text='An inverted yield curve (short-term rates > long-term rates) is a classic indicator of:',
                 option_a='Economic boom ahead', option_b='Likely recession in the near future',
                 option_c='Increasing inflation', option_d='Foreign investment inflow',
                 correct_option='B', difficulty_score=9,
                 hint='Historical recession predictor',
                 explanation='An inverted yield curve (where 2-year rates exceed 10-year rates) has historically preceded recessions by 6-18 months. It signals that investors expect future rate cuts due to economic slowdown.'),
            dict(text='In an LBO (Leveraged Buyout), the acquisition is primarily financed by:',
                 option_a='Target company\'s equity', option_b='Large amounts of debt (loans, bonds) using target company\'s assets as collateral',
                 option_c='Government grants', option_d='New equity issuance',
                 correct_option='B', difficulty_score=9,
                 hint='Debt-heavy acquisition structure',
                 explanation='An LBO uses significant debt (often 60-90% of deal value) to acquire a company. The acquired company\'s cash flows service the debt. Private equity firms commonly use LBOs.'),
            dict(text='Alpha in portfolio management refers to:',
                 option_a='The market return', option_b='Excess returns above benchmark attributable to fund manager\'s skill',
                 option_c='Portfolio volatility measure', option_d='Dividend yield percentage',
                 correct_option='B', difficulty_score=8,
                 hint='Manager\'s value-add above market',
                 explanation='Alpha measures how much a fund manager adds (or destroys) beyond the expected return based on market risk (beta). Positive alpha = outperformance due to skill.'),
            dict(text='Contango in commodity futures markets means:',
                 option_a='Spot price is higher than futures price', option_b='Futures price is higher than current spot price',
                 option_c='Market is falling', option_d='Supply exceeds demand',
                 correct_option='B', difficulty_score=9,
                 hint='Normal futures market state',
                 explanation='Contango is the normal condition where futures prices are higher than current spot prices, reflecting storage costs, insurance, and financing costs until delivery.'),
            dict(text='Return on Equity (ROE) is calculated as:',
                 option_a='Net Income / Total Assets', option_b='Net Income / Shareholder\'s Equity',
                 option_c='Revenue / Total Equity', option_d='EBIT / Market Cap',
                 correct_option='B', difficulty_score=7,
                 hint='Profitability for shareholders',
                 explanation='ROE = Net Income / Shareholders\' Equity × 100. It measures how efficiently management uses equity capital to generate profit. High ROE (>15%) typically indicates strong performance.'),
        ]
        for q in corp_l3_qs:
            Question.objects.create(quiz=corp_l3, **q)

        # ─── GENERAL PUBLIC MODULE ──────────────────────────────────────────────
        gen_l1 = Quiz.objects.create(
            title='Money Basics', description='Essential financial literacy for everyday life',
            difficulty='easy', topic='general', user_type='general', level=1
        )
        gen_l1_qs = [
            dict(text='The 50-30-20 budgeting rule says:',
                 option_a='Invest 50%, save 30%, spend 20%', option_b='50% needs, 30% wants, 20% savings/investments',
                 option_c='50% tax, 30% rent, 20% food', option_d='60% salary, 30% bonus, 20% pension',
                 correct_option='B', difficulty_score=1,
                 hint='Popular personal budgeting framework',
                 explanation='The 50-30-20 rule: 50% for necessities (rent, food, utilities), 30% for lifestyle wants (dining, entertainment), 20% for savings and investments.'),
            dict(text='Compound interest is powerful because:',
                 option_a='Interest is calculated only on principal', option_b='You earn interest on both principal AND previously earned interest',
                 option_c='The interest rate stays fixed', option_d='Banks offer special compound rates',
                 correct_option='B', difficulty_score=2,
                 hint='Interest on interest — snowball effect',
                 explanation='Compound interest calculates interest on the growing total (principal + accumulated interest). ₹1 lakh at 10% annually becomes ₹2.59 lakh in 10 years — not ₹2 lakh!'),
            dict(text='Which is the SAFEST investment option below?',
                 option_a='Stock market directly', option_b='Cryptocurrency', option_c='Fixed Deposit in nationalized bank', option_d='Real estate with loans',
                 correct_option='C', difficulty_score=1,
                 hint='Government guarantee up to ₹5 lakh',
                 explanation='Fixed Deposits in nationalized banks are DICGC-insured up to ₹5 lakh. They offer guaranteed returns with no market risk.'),
            dict(text='An emergency fund should ideally cover:',
                 option_a='1 week of expenses', option_b='3-6 months of monthly expenses',
                 option_c='1 year of expenses always', option_d='Only medical bills',
                 correct_option='B', difficulty_score=2,
                 hint='Financial safety buffer',
                 explanation='3-6 months of expenses in a liquid account covers job loss, medical emergency, or unexpected repairs. Keep it in a savings account or liquid fund — not invested in stocks.'),
            dict(text='A CIBIL score of 750+ means:',
                 option_a='Very high debt burden', option_b='Excellent credit health — likely to get best loan rates',
                 option_c='You cannot apply for loans', option_d='You have no credit history',
                 correct_option='B', difficulty_score=2,
                 hint='Higher score = better creditworthiness',
                 explanation='CIBIL score ranges 300-900. 750+ is considered excellent, meaning you\'re a reliable borrower. Banks offer lower interest rates and faster approvals to high-CIBIL borrowers.'),
            dict(text='For a home loan, financial experts typically recommend EMI should not exceed:',
                 option_a='70% of monthly income', option_b='40-50% of monthly income',
                 option_c='10% of monthly income', option_d='100% of monthly income',
                 correct_option='B', difficulty_score=3,
                 hint='Debt-to-income ratio limit',
                 explanation='Keeping total EMI (all loans combined) below 40-50% of monthly income maintains financial stability. Higher EMI-to-income ratios reduce quality of life and emergency savings.'),
            dict(text='GST stands for:',
                 option_a='General Sales Tax', option_b='Goods and Services Tax',
                 option_c='Government Service Tax', option_d='Global Spending Tax',
                 correct_option='B', difficulty_score=1,
                 hint='India\'s unified indirect tax',
                 explanation='Goods and Services Tax (GST) replaced multiple indirect taxes in India from 2017. It has 4 main slabs: 5%, 12%, 18%, 28%. Essential goods are at 0% or 5%.'),
            dict(text='If inflation is 6% and your salary rises by 4%, your real income has:',
                 option_a='Increased by 10%', option_b='Decreased — purchasing power fell',
                 option_c='Remained the same', option_d='Increased by 4%',
                 correct_option='B', difficulty_score=3,
                 hint='Real income = nominal - inflation',
                 explanation='When inflation exceeds your salary increase, your purchasing power declines. At 6% inflation and 4% raise, your real income actually fell by ~2%. Your money buys LESS than before.'),
        ]
        for q in gen_l1_qs:
            Question.objects.create(quiz=gen_l1, **q)

        gen_l2 = Quiz.objects.create(
            title='Save & Invest', description='Smart saving and investment strategies for wealth building',
            difficulty='medium', topic='general', user_type='general', level=2
        )
        gen_l2_qs = [
            dict(text='What is a Mutual Fund?',
                 option_a='A government savings scheme', option_b='Pooled money from investors, managed by professionals, invested in markets',
                 option_c='A type of bank loan', option_d='Private company stock',
                 correct_option='B', difficulty_score=4,
                 hint='Collective investing made easy',
                 explanation='A mutual fund pools money from thousands of investors. Professional fund managers invest this in stocks, bonds etc. You get units proportional to your investment.'),
            dict(text='Starting a SIP of Rs.3,000/month at age 25 vs 35 (assuming 12% returns), by 60 you would have:',
                 option_a='Nearly the same amount', option_b='About 25% more if starting at 25',
                 option_c='About 3-4 times more if starting at 25', option_d='Twice the amount starting at 25',
                 correct_option='C', difficulty_score=5,
                 hint='Time in market is everything',
                 explanation='Starting at 25 gives 35 years of compounding vs 25 years at 35. The difference is roughly 3-4x more wealth — compounding rewards those who start early.'),
            dict(text="What does 'term life insurance' provide?",
                 option_a='Investment returns plus life cover', option_b='Pure life cover for a specific term — family gets sum assured if you die',
                 option_c='Medical expense coverage', option_d='Property insurance',
                 correct_option='B', difficulty_score=4,
                 hint='Pure protection, no investment',
                 explanation='Term insurance is pure life cover (no maturity benefit). If you die during the term, nominees receive the sum assured. Very affordable — Rs.1 Cr cover for Rs.8,000-12,000/year.'),
            dict(text='PPF (Public Provident Fund) lock-in period is:',
                 option_a='3 years', option_b='7 years', option_c='15 years', option_d='25 years',
                 correct_option='C', difficulty_score=4,
                 hint='Long-term tax-free savings',
                 explanation='PPF has 15-year lock-in with partial withdrawals allowed from Year 7. It offers tax-free returns (~7.1%), EEE tax status — exempt at investment, interest, and maturity.'),
            dict(text='ELSS Mutual Fund gives tax deduction under:',
                 option_a='Section 80C', option_b='Section 80D', option_c='Section 24', option_d='Section 10(14)',
                 correct_option='A', difficulty_score=5,
                 hint='Up to Rs.1.5 lakh deduction',
                 explanation='ELSS (Equity Linked Savings Scheme) qualifies for Rs.1.5 lakh deduction under Section 80C. It has the shortest lock-in (3 years) among tax-saving options.'),
            dict(text="Health insurance 'deductible' means:",
                 option_a='Amount insurer pays immediately', option_b='Amount YOU pay out-of-pocket before insurance coverage kicks in',
                 option_c='Annual premium amount', option_d='Hospital network discount',
                 correct_option='B', difficulty_score=5,
                 hint='Your first financial exposure in a claim',
                 explanation='A deductible is what you pay first before your insurer pays the rest. Higher deductible = lower premium but more out-of-pocket during claims.'),
            dict(text="What is 'rupee cost averaging' in SIP investing?",
                 option_a='Always buying at lowest price', option_b='Automatically getting more units when prices fall, fewer when high',
                 option_c='Fixing purchase price forever', option_d='Monthly currency exchange benefit',
                 correct_option='B', difficulty_score=5,
                 hint='Market timing done automatically',
                 explanation='With SIP, a fixed amount buys more units when NAV is low (market down) and fewer when high. Over time, this averages out the purchase cost — removing market timing stress.'),
            dict(text='Which investment has the HIGHEST liquidity?',
                 option_a='Real estate', option_b='PPF',
                 option_c='Savings account / Liquid mutual fund', option_d='5-year Fixed Deposit',
                 correct_option='C', difficulty_score=4,
                 hint='Access your money instantly',
                 explanation='Savings accounts and liquid mutual funds offer same-day or next-day withdrawal. Real estate takes months; PPF has 15-year lock-in; FDs have penalties for early withdrawal.'),
        ]
        for q in gen_l2_qs:
            Question.objects.create(quiz=gen_l2, **q)

        gen_l3 = Quiz.objects.create(
            title='Plan Ahead', description='Advanced financial planning for long-term wealth',
            difficulty='hard', topic='general', user_type='general', level=3
        )
        gen_l3_qs = [
            dict(text="What is the 'Rule of 72' in finance?",
                 option_a='Tax calculation shortcut', option_b='Years to double money = 72 divided by interest rate',
                 option_c='Retirement age formula', option_d='Loan EMI calculation',
                 correct_option='B', difficulty_score=6,
                 hint='Quick doubling time calculator',
                 explanation='Divide 72 by your annual return rate to estimate years to double money. At 8% returns: 72/8 = 9 years. At 12%: 72/12 = 6 years. Simple mental math!'),
            dict(text='For a home loan of Rs.50 lakh, which factor most affects your EMI?',
                 option_a='Bank branch location', option_b='Your employer type',
                 option_c='Interest rate and loan tenure', option_d="Bank's total assets",
                 correct_option='C', difficulty_score=6,
                 hint='Two variables, massive impact',
                 explanation='Interest rate and tenure determine EMI. Rs.50L at 8.5% for 20 years = Rs.43,391/month. At 9% = Rs.44,986/month. A 0.5% difference = Rs.3.7L extra over 20 years!'),
            dict(text='NPS (National Pension System) is best described as:',
                 option_a='Tax-free savings account', option_b='Market-linked pension scheme with partial tax-free withdrawal at 60',
                 option_c='Bank fixed deposit for seniors', option_d='Life insurance for retirees',
                 correct_option='B', difficulty_score=7,
                 hint='Government-run retirement investment',
                 explanation='NPS invests in equity + bonds. At 60, you can withdraw 60% tax-free and must use 40% to buy annuity for pension income. Extra Rs.50,000 deduction under Section 80CCD(1B).'),
            dict(text="What is 'reverse mortgage' designed for?",
                 option_a='Young couples buying first home', option_b='Senior citizens converting home equity into regular monthly income',
                 option_c='Rental property financing', option_d='Commercial property investment',
                 correct_option='B', difficulty_score=7,
                 hint='Home as retirement income source',
                 explanation='Senior citizens (60+) can mortgage their home to a bank and receive monthly payments. They continue living there. The bank recovers the loan when the property is eventually sold.'),
            dict(text='Long-term capital gains (LTCG) tax on equity mutual funds in India applies after holding:',
                 option_a='3 months', option_b='6 months', option_c='1 year', option_d='3 years',
                 correct_option='C', difficulty_score=7,
                 hint='Equity holding period for tax benefits',
                 explanation='Equity investments held >1 year qualify for LTCG at 10% on gains above Rs.1 lakh. Short-term (<1 year) gains are taxed at 15% STCG rate.'),
            dict(text="A financial goal is 'SMART' when it is:",
                 option_a='Simple, Manageable, Appropriate, Realistic, Time-based',
                 option_b='Specific, Measurable, Achievable, Relevant, Time-bound',
                 option_c='Safe, Moderate, Approved, Reliable, Tested',
                 option_d='Standard, Market, Allocated, Reviewed, Tracked',
                 correct_option='B', difficulty_score=6,
                 hint='Goal-setting framework',
                 explanation='SMART goals: Specific (what exactly), Measurable (how much), Achievable (realistic), Relevant (aligned with priorities), Time-bound (deadline). This makes goals actionable.'),
            dict(text='The primary benefit of diversifying across asset classes (equity + debt + gold) is:',
                 option_a='Guaranteed maximum returns', option_b='Eliminating all market risk',
                 option_c='Reducing overall portfolio volatility through low correlation', option_d='Avoiding all taxes',
                 correct_option='C', difficulty_score=8,
                 hint='Assets that zig when others zag',
                 explanation='Different assets respond differently to market conditions. When equities fall, gold often rises. Diversification reduces volatility without necessarily reducing long-term returns.'),
            dict(text='If you want Rs.1 Cr retirement corpus in 20 years at 12% return, approximate monthly SIP needed is:',
                 option_a='Rs.5,000', option_b='Rs.10,000', option_c='Rs.15,000', option_d='Rs.25,000',
                 correct_option='B', difficulty_score=8,
                 hint='Power of compounding at work',
                 explanation='At 12% annual return, Rs.10,000/month SIP for 20 years grows to ~Rs.1 Cr. But starting earlier dramatically reduces this amount needed!'),
        ]
        for q in gen_l3_qs:
            Question.objects.create(quiz=gen_l3, **q)

        total_q = Question.objects.count()
        total_quiz = Quiz.objects.count()
        self.stdout.write(f'  ✅ Created {total_quiz} quizzes with {total_q} questions (all 72 from KnowQuest)')

    def _create_schemes(self):
        if GovernmentScheme.objects.exists():
            self.stdout.write('  Schemes already exist, skipping...')
            return
        schemes_data = [
            {'name': 'Pradhan Mantri Jan Dhan Yojana', 'description': 'Financial inclusion program providing zero-balance bank accounts', 'category': 'savings', 'benefits': 'Zero-balance bank account, RuPay debit card, ₹2 lakh accident insurance, ₹30,000 life insurance', 'eligibility_criteria': 'Any Indian citizen above 10 years of age', 'min_age': 10, 'state': 'All India', 'applicable_categories': 'General,SC,ST,OBC'},
            {'name': 'Sukanya Samriddhi Yojana', 'description': 'Savings scheme for girl children with tax benefits and high interest', 'category': 'savings', 'benefits': 'High interest rate (8.2%), Tax-free returns, EEE status under 80C, ₹1.5L max annual deposit', 'eligibility_criteria': 'Parents/guardians of girl child below 10 years', 'max_age': 10, 'state': 'All India', 'applicable_categories': 'General,SC,ST,OBC'},
            {'name': 'Atal Pension Yojana', 'description': 'Pension scheme for unorganized sector workers aged 18-40', 'category': 'pension', 'benefits': 'Guaranteed pension of ₹1,000 to ₹5,000 per month after 60, government co-contribution', 'eligibility_criteria': 'Indian citizens aged 18-40 with savings bank accounts', 'min_age': 18, 'max_age': 40, 'state': 'All India', 'applicable_categories': 'General,SC,ST,OBC'},
            {'name': 'PM Mudra Yojana', 'description': 'Micro-finance loans for small businesses — Shishu, Kishore, Tarun categories', 'category': 'business', 'benefits': 'Collateral-free loans: Shishu up to ₹50K, Kishore ₹50K-5L, Tarun ₹5L-10L', 'eligibility_criteria': 'Any Indian citizen with a non-farm business plan', 'min_age': 18, 'state': 'All India', 'applicable_categories': 'General,SC,ST,OBC'},
            {'name': 'PM Kisan Samman Nidhi', 'description': 'Direct income support of ₹6,000/year for small and marginal farmers', 'category': 'subsidy', 'benefits': '₹6,000 per year in three equal installments directly to bank account', 'eligibility_criteria': 'Small and marginal farmer families with cultivable land', 'min_age': 18, 'state': 'All India', 'applicable_categories': 'General,SC,ST,OBC'},
            {'name': 'PM Fasal Bima Yojana (PMFBY)', 'description': 'Comprehensive crop insurance scheme for farmers against natural calamities', 'category': 'insurance', 'benefits': 'Coverage against crop loss, pest attacks, natural disasters. Farmers pay 2% Kharif, 1.5% Rabi premium', 'eligibility_criteria': 'All farmers growing notified crops in notified areas', 'min_age': 18, 'state': 'All India', 'applicable_categories': 'General,SC,ST,OBC'},
            {'name': 'National Scholarship Portal Scheme', 'description': 'Merit-cum-means scholarships for economically weaker students', 'category': 'education', 'benefits': 'Full tuition fee coverage, monthly stipend, book allowance', 'eligibility_criteria': 'Students from families with annual income below ₹8 lakh', 'min_age': 16, 'max_age': 30, 'max_income': 800000, 'state': 'All India', 'applicable_categories': 'SC,ST,OBC'},
            {'name': 'NPS (National Pension System)', 'description': 'Market-linked voluntary retirement savings scheme open to all Indian citizens', 'category': 'pension', 'benefits': 'Tax benefits under 80C + 80CCD(1B) (extra ₹50K), flexible asset allocation, low fund management charges', 'eligibility_criteria': 'Indian citizens aged 18-70', 'min_age': 18, 'max_age': 70, 'state': 'All India', 'applicable_categories': 'General,SC,ST,OBC'},
        ]
        for s_data in schemes_data:
            GovernmentScheme.objects.create(**s_data)
        self.stdout.write(f'  ✅ Created {GovernmentScheme.objects.count()} government schemes')

    def _create_badges(self):
        if Badge.objects.exists():
            self.stdout.write('  Badges already exist, skipping...')
            return
        badges_data = [
            {'name': 'First Steps', 'description': 'Complete your first quiz', 'icon': '🎯', 'requirement': 'Complete 1 quiz', 'points_value': 25, 'badge_type': 'quiz'},
            {'name': 'Consistent Learner', 'description': 'Complete 5 quizzes', 'icon': '📚', 'requirement': 'Complete 5 quizzes', 'points_value': 75, 'badge_type': 'quiz'},
            {'name': 'Quiz Master', 'description': 'Complete 10 quizzes', 'icon': '🏆', 'requirement': 'Complete 10 quizzes', 'points_value': 150, 'badge_type': 'quiz'},
            {'name': 'Perfect Score', 'description': 'Score 100% on any quiz', 'icon': '💯', 'requirement': '100% on a quiz', 'points_value': 100, 'badge_type': 'achievement'},
            {'name': '3-Star Farmer', 'description': 'Get 3 stars on any Farmer quiz', 'icon': '🌾', 'requirement': '3 stars on Farmer quiz', 'points_value': 80, 'badge_type': 'achievement'},
            {'name': '3-Star Corporate', 'description': 'Get 3 stars on any Corporate quiz', 'icon': '🏢', 'requirement': '3 stars on Corporate quiz', 'points_value': 80, 'badge_type': 'achievement'},
            {'name': '3-Star General', 'description': 'Get 3 stars on any General Public quiz', 'icon': '👥', 'requirement': '3 stars on General quiz', 'points_value': 80, 'badge_type': 'achievement'},
            {'name': 'Week Warrior', 'description': 'Maintain a 7-day streak', 'icon': '🔥', 'requirement': '7-day streak', 'points_value': 100, 'badge_type': 'streak'},
            {'name': 'Month Champion', 'description': 'Maintain a 30-day streak', 'icon': '⭐', 'requirement': '30-day streak', 'points_value': 300, 'badge_type': 'streak'},
            {'name': 'Finance Explorer', 'description': 'Use all calculator tools in Finance Planner', 'icon': '🧭', 'requirement': 'Use all 4 calculators', 'points_value': 60, 'badge_type': 'feature'},
            {'name': 'Plan Master', 'description': 'Complete the ML Finance Plan questionnaire', 'icon': '🎯', 'requirement': 'Get personalized finance plan', 'points_value': 75, 'badge_type': 'feature'},
            {'name': 'Scheme Hunter', 'description': 'Check eligibility for government schemes', 'icon': '🏛️', 'requirement': 'Check scheme eligibility', 'points_value': 40, 'badge_type': 'feature'},
            {'name': 'Chat Pro', 'description': 'Have 20 conversations with the chatbot', 'icon': '💬', 'requirement': '20 chatbot conversations', 'points_value': 60, 'badge_type': 'feature'},
            {'name': 'Heartless Hero', 'description': 'Complete a quiz without losing any hearts', 'icon': '💪', 'requirement': 'Perfect hearts on any quiz', 'points_value': 120, 'badge_type': 'achievement'},
            {'name': 'XP Legend', 'description': 'Earn 1000 total XP', 'icon': '⚡', 'requirement': '1000 total XP', 'points_value': 200, 'badge_type': 'achievement'},
        ]
        for b_data in badges_data:
            Badge.objects.create(**b_data)
        self.stdout.write(f'  ✅ Created {Badge.objects.count()} achievement badges')
