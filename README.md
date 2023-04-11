# Stargate-Bridger

 [My Profile](https://github.com/ryu666zaki/) | [My projects](https://github.com/ryu666zaki?tab=repositories) |
  🍩**Donate**: `0x27512edc51cAd8a5277090183858677915CC95c4`


![](image/stargate.jpg)

## <sup>Simple script to bridge USDC from Polygon to Fantom and back on Stargate.finance</sup>

### <sup>***❗You need to have Python 3.10+ installed❗***</sup>

  1. Fund your wallets in the **Polygon** network with USDC and some Matic for transaction fees, and **Fantom** network with some FTM for transaction fees.

  2. **Clone repository** to yours system.

> Open your development environment, such as VSCode or Pycharm. Select the option to clone repo by link and paste the link to this repo.

  3. Open terminal in the same folder as main.py and run this commands:

```
python3.10 -m venv .venv
source .venv/bin/activate
pip install web3
```

  4. Open the `main.py` and edit the values below the comments to suit your needs.
   > Change `AMOUNT_TO_SWAP`, `SLIPPAGE`, `PRIVATE_KEY`, `TIMES` variables
   
>❗It may be that a transaction from the Fantom network to the Polygon network will not get through in 100 seconds, so the subsequent transaction from    the Polygon network to the Fantom network will crash.
To avoid this, put `time.sleep(200)` on `line 244` instead of `time.sleep(100)`. This will give the transaction an `extra 100 seconds` to pass. 
In general, run transactions manually before using the script so that you know how long they will take when the script runs, and set delays based on     your observations.

  5. Now you're ready to start:
  ```
  python main.py
  ```

## 👨‍💻 All of my projects are available [here](https://github.com/ryu666zaki?tab=repositories)

#### 🍩Donate: `0x27512edc51cAd8a5277090183858677915CC95c4`
