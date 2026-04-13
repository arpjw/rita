# Rita

**The macro research assistant that lives in your server.**

Rita is an open-source Discord bot for quantitative and macro traders. She brings a conversational research layer directly into your team's Discord — pulling live data from FRED and Kalshi, classifying the current macro regime via the [Lumina](https://github.com/arpjw/lumina) backend, and enabling document Q&A on central bank communications.

Built by [Monolith Systematic LLC](https://monolithsystematic.com).

---

## Commands

| Command | Description |
|---|---|
| `/brief` | Morning macro snapshot — rates, FX, credit spreads, top Kalshi events, Fed posture |
| `/regime` | Current macro regime classification with confidence score and signal breakdown |
| `/analyze` | Document Q&A — paste or attach a Fed speech, ECB minutes, or IMF report |
| `/watch` | Subscribe to threshold alerts on macro variables, delivered via DM |
| `/watchlist` | View your active alerts |
| `/watchcancel` | Cancel an alert by ID |

---

## Self-Hosting

**Requirements:** Python 3.12+, Docker (optional)

### 1. Clone the repo
```bash
git clone https://github.com/arpjw/rita.git && cd rita
```

### 2. Configure environment variables
```bash
cp .env.example .env
```
Fill in your `DISCORD_TOKEN`, `FRED_API_KEY`, `KALSHI_API_KEY`, and `ANTHROPIC_API_KEY`.
`LUMINA_API_URL` is optional — if omitted, `/regime` returns a graceful fallback.

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the bot
```bash
python -m bot.main
```

### 5. Or run via Docker
```bash
make dev
```

---

## Data Sources

| Source | Used for | Key required |
|---|---|---|
| [FRED](https://fred.stlouisfed.org) | Rates, FX, credit, macro indicators | `FRED_API_KEY` |
| [Kalshi](https://kalshi.com) | Prediction market probabilities on macro events | `KALSHI_API_KEY` |
| [Lumina](https://github.com/arpjw/lumina) | Regime classification (optional) | `LUMINA_API_URL` |
| [Anthropic](https://anthropic.com) | Fed posture synthesis, document Q&A, alert context | `ANTHROPIC_API_KEY` |

---

## Contributing

Rita's data layer is built around a clean connector interface. Adding a new data source is straightforward — see [CONTRIBUTING.md](./CONTRIBUTING.md).

---

## License

MIT — see [LICENSE](./LICENSE).
