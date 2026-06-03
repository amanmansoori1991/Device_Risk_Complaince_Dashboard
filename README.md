# Device Risk & Compliance Dashboard

A Python-based dashboard for monitoring device compliance and risk in enterprise environments. Built with Streamlit for web-based visualisation and integrated with OpenAI for AI-powered remediation recommendations.

## Features
- AV compliance monitoring
- BitLocker encryption status
- Patch compliance tracking
- Reboot compliance tracking
- AI-generated remediation recommendations per device
- Colour-coded risk indicators (Low / Medium / High)

## Tech Stack
- Python
- Streamlit
- Pandas
- Plotly
- OpenAI API

## Data Source
Currently uses CSV data for demonstration. Designed to connect to Microsoft Intune via Microsoft Graph API for real enterprise device data.

## Setup
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Add your OpenAI API key to a `.env` file: `OPENAI_API_KEY=your_key`
4. Run: `streamlit run dashboard.py`

## Future Enhancements
- Microsoft Graph API integration
- Device filtering and export
- OS version compliance tracking
