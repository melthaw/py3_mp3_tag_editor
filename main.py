from app.bootstrap import bootstrap
from app.mp3_editor import mp3_editor


def main():
    bootstrap()
    mp3_editor.update_tag_all_under_mp3_home()


if __name__ == "__main__":
    main()
