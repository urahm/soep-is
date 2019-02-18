from ddi.onrails.repos import merge_instruments


def main():
    merge_instruments.main(export_json=True, export_yaml=False)


if __name__ == "__main__":
    main()
