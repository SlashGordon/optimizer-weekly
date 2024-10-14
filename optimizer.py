# generate_trading_signal_table.py

# Define trading signal details for MSFT and AAPL
signals = [
    {
        "Asset": "MSFT",
        "Signal Type": "Long",
        "Signal Strength": "Strong",
        "Entry Price": 310.00,
        "Entry Date & Time": "2024-10-14 10:30 UTC",
        "Target Price 1": 320.00,
        "Target Price 2": 330.00,
        "Stop Loss Price": 305.00,
        "Risk Level": "Medium",
    },
    {
        "Asset": "AAPL",
        "Signal Type": "Short",
        "Signal Strength": "Moderate",
        "Entry Price": 175.00,
        "Entry Date & Time": "2024-10-14 10:30 UTC",
        "Target Price 1": 170.00,
        "Target Price 2": 165.00,
        "Stop Loss Price": 180.00,
        "Risk Level": "High",
    },
]

# Generate markdown table
markdown_message = """
# 📈 Algorithmic Trading Signals

| Asset | Signal Type | Signal Strength | Entry Price | Entry Date & Time   | Target Price 1 | Target Price 2 | Stop Loss Price | Risk Level |
|-------|-------------|-----------------|-------------|---------------------|----------------|----------------|-----------------|------------|
"""

# Add rows to the table
for signal in signals:
    markdown_message += (
        f"| {signal['Asset']} | {signal['Signal Type']} | {signal['Signal Strength']} | "
        f"${signal['Entry Price']:.2f} | {signal['Entry Date & Time']} | "
        f"${signal['Target Price 1']:.2f} | ${signal['Target Price 2']:.2f} | "
        f"${signal['Stop Loss Price']:.2f} | {signal['Risk Level']} |\n"
    )

# Write to markdown file
with open("trading_signals.md", "w") as f:
    f.write(markdown_message)

print("Markdown trading signals table generated in 'trading_signals.md'")
