Requirements:
- Python version must be 3.6 or higher (we use f-strings)
- Code must be run from root of 'Lightning Network Analysis' directory
- If the code fails, you likely don't have some of the dependencies installed. Run the code commands below to install all dependencies

```
python -m pip install -r requirements.txt
```

Notes:
- the `pickles` directory store all of the saved pickles that the program uses
- the program uses custom `save` and `load` functions defined in `helper.py` to read and write to these JSON's
- Use the following instructions to run function with default settings

Running Function:
- run `python main`
- you will be prompted first with 3 setup questions. Just hit return for all three of them.
- then enter the public keys for the nodes you want to route between
- enter the amount in satoshi you want to route
- choose your graph edge weight metric to be hop distance, or transaction fees
- choose your routing algorithm

