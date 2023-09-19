import streamlit as st
from PIL import Image
import asyncio
import json
import websockets
import requests
import os.path

col1, col2, col3, col4 = st.columns([1.5, 2, 2, 2], gap="small")
if os.path.exists("dt.json") == False:
    with open('dt.json', 'w') as f:
        f.write('{"birg": "Binance", "val": "BTC"}')

def read_json():
    with open('dt.json', 'r') as f:
        dt = json.load(f)
        birg = dt["birg"]
        val = dt["val"]
        return birg, val

def write_json(birg: str, val: str):
    with open('dt.json', 'w') as fuck:
        json.dump({"birg": birg, "val": val}, fuck)

birg, val = read_json()

with st.sidebar:
    c1, c2, c3 = st.columns(3)
    with c1:
        img = Image.open("bitcoin.png")
        st.image(img)
        click_BTC = st.button("BTC/USD")
        if click_BTC:
            write_json(birg, "BTC")
            st.experimental_rerun()
        st.divider()
        img = Image.open("coin.png")
        st.image(img)
        click_SOL = st.button("SOL/USD")
        if click_SOL:
            write_json(birg, "SOL")
            st.experimental_rerun()

    with c2:
        img = Image.open("ethereum(1).png")
        st.image(img)
        click_ETH = st.button("ETH/USD")
        if click_ETH:
            write_json(birg, "ETH")
            st.experimental_rerun()
        st.divider()

        img = Image.open("bnb.png")
        st.image(img)
        click_BNB = st.button("BNB/USD")
        if click_BNB:
            write_json(birg, "BNB")
            st.experimental_rerun()

    with c3:
        img = Image.open("litecoin.png")
        st.image(img)
        click_LTC = st.button("LTC/USD")
        if click_LTC:
            write_json(birg, "LTC")
            st.experimental_rerun()
        st.divider()

        img = Image.open("currency.png")
        st.image(img)
        click_XRP = st.button("ADA/USD")
        if click_XRP:
            write_json(birg, "ADA")
            st.experimental_rerun()

    with col2:
        img = Image.open("binance.png")
        st.image(img)
        click = st.button("Binance")
        if click:
            write_json("Binance", val)
            st.experimental_rerun()

with col4:
    img2 = Image.open("bybit.png")
    st.image(img2)
    click2 = st.button("Bybit")
    if click2:
        write_json("bybit", val)
        st.experimental_rerun()

with col3:
    img1 = Image.open("Kucoin.png")
    st.image(img1)
    click1 = st.button("Kucoin")
    if click1:
        write_json("Kucoin", val)
        st.experimental_rerun()

with col1:
    st.subheader("UCrypter")
    st.divider()

ioloop = asyncio.new_event_loop()
asyncio.set_event_loop(ioloop)

async def cryptocompare():
    # this is where you paste your api key
    ak1 = "c0e8f4bde364fe97bb78b1b8a4cf7ed21b0f427b28c5ecd43092ce9b989c45e4"
    ak2 = "c61d8a00a52c9edac7451788f3f1de8ce087df61f10403e2841434bcf415db70"
    url = "wss://streamer.cryptocompare.com/v2?api_key=" + ak1
    async with websockets.connect(url) as websocket:
        await websocket.send(json.dumps({
            "action": "SubAdd",
            "subs": [f"2~{birg}~{val}~USDT"],
        }))
        print(val)
        print(birg)
        with st.empty():
            while True:
                try:
                    data = await websocket.recv()
                except websockets.ConnectionClosed:
                    break

                try:
                    data = json.loads(data)
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        if data["TYPE"] == "2" and 'PRICE' in data:
                            st.metric("Current Price", data["PRICE"])
                    r = requests.get(
                        f'https://min-api.cryptocompare.com/data/v2/histominute?fsym={val}&tsym=USDT&e={birg}&limit=1&api_key={ak1}')
                    rd = json.loads(r.text)
                    with c2:
                        co1, co2 = st.columns(2)
                        with co1:
                            st.metric("High", rd["Data"]['Data'][1]['high'])
                            st.metric("Open", rd["Data"]['Data'][1]['open'])
                        with co2:
                            st.metric("Low", rd["Data"]['Data'][1]['low'])
                            st.metric("Close", rd["Data"]['Data'][1]['close'])

                except ValueError:
                    print(data)

ioloop.run_until_complete(cryptocompare())
ioloop.close()
