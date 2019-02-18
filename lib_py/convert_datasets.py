from ddi.onrails.repos import convert_r2ddi


def main():
    print("[INFO] Read datasets...")
    data = convert_r2ddi.Parser("soep-is", version="v2015.1")
    print("[INFO] Write JSON file...")
    data.write_json()
    print("[INFO] Write YAML file...")
    data.write_yaml()


if __name__ == "__main__":
    main()
