"""
Created by Phuong Nguyen
"""

from .app import App


def main():
    """Main script function"""
    app = App()
    app.setup()
    app.parse_args()
    app.run()


if __name__ == "__main__":
    main()
