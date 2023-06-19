from .app import App


def main():
    app = App()
    app.setup()
    app.parse_args()
    app.run()


if __name__ == "__main__":
    main()
