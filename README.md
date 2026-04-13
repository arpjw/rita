<div align="center">
  <img src="https://getrita.app/avatar.png" alt="Rita" width="120" height="120" style="border-radius: 50%"/>
  <h1>Rita</h1>
  <p><strong>The macro research layer for your Discord server.</strong></p>
  <p>
    <a href="https://getrita.app">Website</a> ·
    <a href="https://discord.com/oauth2/authorize?client_id=1493339120242786434&scope=bot+applications.commands&permissions=277025770560">Add to Discord</a> ·
    <a href="https://monolithsystematic.com">Monolith Systematic</a>
  </p>
  <br/>
</div>

Rita is an open-source Discord bot purpose-built for quantitative and macro traders. She brings a conversational research layer directly into your team's server — pulling live data from FRED and Kalshi, classifying the current macro regime via the [Lumina](https://github.com/arpjw/lumina) backend, and enabling document Q&A on central bank communications.

Built by [Monolith Systematic LLC](https://monolithsystematic.com).

---

## Add Rita to Your Server

**[→ Add Rita to Discord](https://discord.com/oauth2/authorize?client_id=1493339120242786434&scope=bot+applications.commands&permissions=277025770560)**

Or visit [getrita.app](https://getrita.app) for more information.

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

Priority areas for community contribution:
- COT (Commitments of Traders) positioning connector
- Bloomberg / Refinitiv adapter
- Norgate futures pricing connector
- ECB / BOJ / BOE data adapters

---

## Stack

- **Bot framework:** py-cord
- **Data:** FRED API, Kalshi Trading API, Norgate (optional)
- **Intelligence:** Anthropic Claude API (claude-sonnet-4-20250514)
- **Regime backend:** [Lumina](https://github.com/arpjw/lumina) (optional)
- **Infra:** Docker, Python 3.12

---

## License

MIT — see [LICENSE](./LICENSE).
