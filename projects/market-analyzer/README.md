# AI Market Analyzer

Real-time market analysis using LLMs for sentiment analysis, trend detection, and trading signal generation.

## Features

- **Sentiment Analysis**: News and social media sentiment scoring
- **Technical Analysis**: Pattern recognition and indicator calculation
- **Trend Detection**: LLM-powered trend identification
- **Signal Generation**: Buy/sell recommendations with confidence scores
- **Risk Assessment**: Portfolio risk analysis

## Data Sources

- Yahoo Finance (price data)
- NewsAPI (market news)
- Reddit/Twitter (social sentiment)

## Architecture

```
Market Data → Preprocessing → [Sentiment | Technical | Trend] → Synthesis → Signals
```

## Tech Stack

- LangChain for LLM orchestration
- yfinance for market data
- pandas-ta for technical indicators
- OpenAI for analysis and reasoning
