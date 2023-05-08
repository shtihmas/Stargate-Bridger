# Stargate-Bridger



![](image/stargate.jpg)

## <sup>Simple script to bridge USDC from Polygon to Fantom and back on Stargate.finance</sup>

### <sup>***❗You need to have Python 3.10+ installed❗***</sup>


  1. Fund your wallet in the **Polygon** network with USDC and some Matic for transaction fees, and **Fantom** network with some FTM for transaction fees.

  2. **Clone repository** to yours system.

> Open your development environment, such as VSCode or Pycharm. Select the option to clone repo by link and paste the link to this repo.

  3. Open terminal in the same folder as main.py and run this commands:

```
python3.10 -m venv .venv
source .venv/bin/activate
pip install web3
```

  4. Open the `main.py` and edit the values below the comments to suit your needs.
   > Change `AMOUNT_MIN`, `AMOUNT_MAX`, `TIMES` variables. 
   > Put your private keys in private_keys.txt

  5. Now you're ready to start:
  ```
  python main.py
  ```
