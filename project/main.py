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
        f.write('{"birg": "Binance", "val": "BTC", "time": "hour"}')

def read_json():
    with open('dt.json', 'r') as f:
        dt = json.load(f)
        birg = dt["birg"]
        val = dt["val"]
        time = dt["time"]
        return birg, val, time

def write_json(birg: str, val: str, time: str):
    with open('dt.json', 'w') as d:
        json.dump({"birg": birg, "val": val, "time": time}, d)

birg, val, time = read_json()

with st.sidebar:
    st.subheader("Select cryptocurrency")
    c1, c2, c3 = st.columns(3)
    with c1:
        img = Image.open("project/bitcoin.png")
        st.image(img)
        click_BTC = st.button("BTC/USD")
        if click_BTC:
            write_json(birg, "BTC", time)
            st.experimental_rerun()

        img = Image.open("project/coin.png")
        st.image(img)
        click_SOL = st.button("SOL/USD")
        if click_SOL:
            write_json(birg, "SOL", time)
            st.experimental_rerun()

    with c2:
        img = Image.open("project/ethereum(1).png")
        st.image(img)
        click_ETH = st.button("ETH/USD")
        if click_ETH:
            write_json(birg, "ETH", time)
            st.experimental_rerun()

        img = Image.open("project/bnb.png")
        st.image(img)
        click_BNB = st.button("BNB/USD")
        if click_BNB:
            write_json(birg, "BNB", time)
            st.experimental_rerun()

    with c3:
        img = Image.open("project/litecoin.png")
        st.image(img)
        click_LTC = st.button("LTC/USD")
        if click_LTC:
            write_json(birg, "LTC", time)
            st.experimental_rerun()

        img = Image.open("project/currency.png")
        st.image(img)
        click_XRP = st.button("ADA/USD")
        if click_XRP:
            write_json(birg, "ADA", time)
            st.experimental_rerun()

    st.divider()
    st.subheader("Select a time interval")
    but1, but2, but3 = st.columns(3)
    with but1:
        bro1 = st.button("Minute", key="345jkh6")
        if bro1:
            write_json(birg, val, "minute")
            st.experimental_rerun()
    with but2:
        bro2 = st.button("Hour", key="l3452ad")
        if bro2:
            write_json(birg, val, "hour")
            st.experimental_rerun()
    with but3:
        bro3 = st.button("Day", key="sd211s")
        if bro3:
            write_json(birg, val, "day")
            st.experimental_rerun()

    with col2:
        img = Image.open("project/binance.png")
        st.image(img)
        click = st.button("Binance")
        if click:
            write_json("Binance", val, time)
            st.experimental_rerun()

with col4:
    img2 = Image.open("project/bybit.png")
    st.image(img2)
    click2 = st.button("Bybit")
    if click2:
        write_json("bybit", val, time)
        st.experimental_rerun()

with col3:
    img1 = Image.open("project/Kucoin.png")
    st.image(img1)
    click1 = st.button("Kucoin")
    if click1:
        write_json("Kucoin", val, time)
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
                        f'https://min-api.cryptocompare.com/data/v2/histo{time}?fsym={val}&tsym=USDT&e={birg}&limit=1&api_key={ak1}')
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
