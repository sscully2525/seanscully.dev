import yfinance as yf
import pandas as pd
import pandas_ta as ta
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json

class MarketAnalyzer:
    """AI-powered market analysis and signal generation"""
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0.1)
        
    def fetch_data(self, symbol: str, period: str = "3mo") -> pd.DataFrame:
        """Fetch market data from Yahoo Finance"""
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period)
        return df
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators"""
        # Trend indicators
        df['sma_20'] = ta.sma(df['Close'], length=20)
        df['sma_50'] = ta.sma(df['Close'], length=50)
        df['ema_12'] = ta.ema(df['Close'], length=12)
        
        # Momentum indicators
        df['rsi'] = ta.rsi(df['Close'], length=14)
        macd = ta.macd(df['Close'])
        df['macd'] = macd['MACD_12_26_9']
        df['macd_signal'] = macd['MACDs_12_26_9']
        
        # Volatility
        df['bbands_upper'] = ta.bbands(df['Close'])['BBU_5_2.0']
        df['bbands_lower'] = ta.bbands(df['Close'])['BBL_5_2.0']
        
        # Volume
        df['volume_sma'] = df['Volume'].rolling(20).mean()
        
        return df
    
    def detect_patterns(self, df: pd.DataFrame) -> List[str]:
        """Detect chart patterns"""
        patterns = []
        
        recent = df.tail(20)
        
        # Golden Cross / Death Cross
        if (recent['sma_20'].iloc[-1] > recent['sma_50'].iloc[-1] and 
            recent['sma_20'].iloc[-2] <= recent['sma_50'].iloc[-2]):
            patterns.append("Golden Cross (bullish)")
        elif (recent['sma_20'].iloc[-1] < recent['sma_50'].iloc[-1] and 
              recent['sma_20'].iloc[-2] >= recent['sma_50'].iloc[-2]):
            patterns.append("Death Cross (bearish)")
        
        # RSI conditions
        latest_rsi = df['rsi'].iloc[-1]
        if latest_rsi > 70:
            patterns.append(f"Overbought (RSI: {latest_rsi:.1f})")
        elif latest_rsi < 30:
            patterns.append(f"Oversold (RSI: {latest_rsi:.1f})")
        
        # MACD crossover
        if (df['macd'].iloc[-1] > df['macd_signal'].iloc[-1] and 
            df['macd'].iloc[-2] <= df['macd_signal'].iloc[-2]):
            patterns.append("MACD Bullish Crossover")
        elif (df['macd'].iloc[-1] < df['macd_signal'].iloc[-1] and 
              df['macd'].iloc[-2] >= df['macd_signal'].iloc[-2]):
            patterns.append("MACD Bearish Crossover")
        
        # Volume spike
        avg_volume = df['Volume'].tail(20).mean()
        if df['Volume'].iloc[-1] > avg_volume * 1.5:
            patterns.append("Volume Spike (>50% above average)")
        
        return patterns
    
    def analyze_with_llm(self, symbol: str, df: pd.DataFrame, patterns: List[str]) -> Dict:
        """Generate AI analysis"""
        
        # Prepare summary stats
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        price_change = ((latest['Close'] - prev['Close']) / prev['Close']) * 100
        
        summary = {
            "symbol": symbol,
            "current_price": round(latest['Close'], 2),
            "price_change_1d": round(price_change, 2),
            "rsi": round(latest['rsi'], 1) if not pd.isna(latest['rsi']) else None,
            "sma_20": round(latest['sma_20'], 2) if not pd.isna(latest['sma_20']) else None,
            "sma_50": round(latest['sma_50'], 2) if not pd.isna(latest['sma_50']) else None,
            "volume_vs_avg": round(latest['Volume'] / df['Volume'].tail(20).mean(), 2),
            "patterns_detected": patterns
        }
        
        # LLM analysis
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert technical analyst. Analyze the provided market data and generate a trading signal.
            
Respond with a JSON object:
{
    "signal": "BUY" | "SELL" | "HOLD",
    "confidence": 0-100,
    "reasoning": "detailed explanation",
    "key_levels": {"support": number, "resistance": number},
    "risk_factors": ["factor1", "factor2"]
}"""),
            ("human", "Data: {data}")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"data": json.dumps(summary, indent=2)})
        
        try:
            analysis = json.loads(response.content)
        except:
            analysis = {
                "signal": "HOLD",
                "confidence": 50,
                "reasoning": "Error parsing analysis",
                "key_levels": {},
                "risk_factors": []
            }
        
        return {**summary, **analysis}
    
    def analyze(self, symbol: str) -> Dict:
        """Complete analysis pipeline"""
        print(f"Analyzing {symbol}...")
        
        # Fetch data
        df = self.fetch_data(symbol)
        
        # Calculate indicators
        df = self.calculate_indicators(df)
        
        # Detect patterns
        patterns = self.detect_patterns(df)
        
        # LLM analysis
        result = self.analyze_with_llm(symbol, df, patterns)
        
        return result
    
    def screen_watchlist(self, symbols: List[str]) -> List[Dict]:
        """Analyze multiple symbols"""
        results = []
        for symbol in symbols:
            try:
                analysis = self.analyze(symbol)
                results.append(analysis)
            except Exception as e:
                print(f"Error analyzing {symbol}: {e}")
        
        # Sort by confidence
        results.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        return results

# Demo
if __name__ == "__main__":
    analyzer = MarketAnalyzer()
    
    # Single analysis
    print("="*60)
    print("MARKET ANALYZER DEMO")
    print("="*60)
    
    symbols = ["AAPL", "TSLA", "NVDA"]
    
    for symbol in symbols:
        print(f"\n{'='*40}")
        result = analyzer.analyze(symbol)
        
        print(f"\n{result['symbol']} @ ${result['current_price']}")
        print(f"Change: {result['price_change_1d']}%")
        print(f"RSI: {result['rsi']}")
        print(f"Patterns: {', '.join(result['patterns_detected']) if result['patterns_detected'] else 'None'}")
        print(f"\nAI Signal: {result['signal']} (Confidence: {result['confidence']}%)")
        print(f"Reasoning: {result['reasoning'][:200]}...")
