import pandas as pd


def main():

    df = pd.read_csv("INPUT/shark_attacks.csv", dtype={
        "SKU_SELLER":str,
        "PRECO_POR":float,
        "PRECO_DE":float
    })

    return


if __name__ == "_main__":
    try:
        main()
    except Exception as e:
        print(e)