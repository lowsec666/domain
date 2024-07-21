import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Gantilah dengan API key dari penyedia domain
API_KEY = 'at_8TFfWwrE3HUiZJa5UgaHSkCbbpKKu'  
WHOIS_API_URL = 'https://www.whoisxmlapi.com/whoisserver/WhoisService'

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def help(ctx):
    help_text = (
        "**Available Commands:**\n"
        "!checkdomain <domain> - Check if a domain is available.\n"
        "!searchdomains <keyword> - Search for domains with different TLDs based on a keyword.\n"
        "!whois <domain> - Get WHOIS information for a domain.\n"
        "!alertdomain <domain> - Alert if a domain becomes available.\n"
        "!popular - Check availability for a list of popular domains.\n"
        "\nFor further assistance, please contact [Your Support Contact Information]."
    )
    await ctx.send(help_text)

@bot.command()
async def checkdomain(ctx, domain):
    headers = {'Content-Type': 'application/json'}
    params = {'apiKey': API_KEY, 'domainName': domain, 'outputFormat': 'JSON'}
    response = requests.get(WHOIS_API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'WhoisRecord' in data and 'domainAvailability' in data['WhoisRecord']:
            availability = data['WhoisRecord']['domainAvailability']
            if availability == 'AVAILABLE':
                await ctx.send(f'The domain `{domain}` is available!')
            else:
                await ctx.send(f'The domain `{domain}` is not available.')
        else:
            await ctx.send('Error retrieving domain information.')
    else:
        await ctx.send('Failed to connect to the domain API.')

@bot.command()
async def searchdomains(ctx, keyword):
    tlds = ['.com', '.net', '.org', '.io', '.co']  # Daftar TLD yang ingin Anda periksa
    results = []

    for tld in tlds:
        domain = keyword + tld
        headers = {'Content-Type': 'application/json'}
        params = {'apiKey': API_KEY, 'domainName': domain, 'outputFormat': 'JSON'}
        response = requests.get(WHOIS_API_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'WhoisRecord' in data and 'domainAvailability' in data['WhoisRecord']:
                availability = data['WhoisRecord']['domainAvailability']
                if availability == 'AVAILABLE':
                    results.append(f'{domain} is available!')
                else:
                    results.append(f'{domain} is not available.')
        else:
            results.append(f'Failed to check {domain}.')
    
    await ctx.send('\n'.join(results))

@bot.command()
async def whois(ctx, domain):
    headers = {'Content-Type': 'application/json'}
    params = {'apiKey': API_KEY, 'domainName': domain, 'outputFormat': 'JSON'}
    response = requests.get(WHOIS_API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if 'WhoisRecord' in data:
            whois_info = data['WhoisRecord']
            details = [
                f"Domain: {domain}",
                f"Registrar: {whois_info.get('registrarName', 'N/A')}",
                f"Creation Date: {whois_info.get('createdDate', 'N/A')}",
                f"Expiration Date: {whois_info.get('expiresDate', 'N/A')}",
                f"Updated Date: {whois_info.get('updatedDate', 'N/A')}"
            ]
            await ctx.send('\n'.join(details))
        else:
            await ctx.send('No WHOIS information found.')
    else:
        await ctx.send('Failed to retrieve WHOIS information.')

@bot.command()
async def alertdomain(ctx, domain):
    async with ctx.typing():
        headers = {'Content-Type': 'application/json'}
        params = {'apiKey': API_KEY, 'domainName': domain, 'outputFormat': 'JSON'}
        response = requests.get(WHOIS_API_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'WhoisRecord' in data and 'domainAvailability' in data['WhoisRecord']:
                availability = data['WhoisRecord']['domainAvailability']
                if availability == 'AVAILABLE':
                    await ctx.send(f'Alert: The domain `{domain}` is now available!')
                else:
                    await ctx.send(f'The domain `{domain}` is still not available.')
            else:
                await ctx.send('Error retrieving domain information.')
        else:
            await ctx.send('Failed to connect to the domain API.')

@bot.command()
async def popular(ctx):
    popular_domains = ['example.com', 'testsite.net', 'mywebsite.org']
    results = []

    for domain in popular_domains:
        headers = {'Content-Type': 'application/json'}
        params = {'apiKey': API_KEY, 'domainName': domain, 'outputFormat': 'JSON'}
        response = requests.get(WHOIS_API_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'WhoisRecord' in data and 'domainAvailability' in data['WhoisRecord']:
                availability = data['WhoisRecord']['domainAvailability']
                if availability == 'AVAILABLE':
                    results.append(f'{domain} is available!')
                else:
                    results.append(f'{domain} is not available.')
        else:
            results.append(f'Failed to check {domain}.')
    
    await ctx.send('\n'.join(results))

bot.run('YOUR_BOT_TOKEN')
