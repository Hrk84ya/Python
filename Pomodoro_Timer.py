import time
import sys
import os


# Default durations in minutes
DEFAULT_WORK = 25
DEFAULT_SHORT_BREAK = 5
DEFAULT_LONG_BREAK = 15
SESSIONS_BEFORE_LONG_BREAK = 4


def clear_line():
    """Clear the current terminal line."""
    sys.stdout.write("\r" + " " * 60 + "\r")
    sys.stdout.flush()


def format_time(seconds):
    """Format seconds as MM:SS."""
    m, s = divmod(seconds, 60)
    return f"{m:02d}:{s:02d}"


def countdown(label, total_seconds):
    """Run a countdown timer with live display. Returns False if user quits."""
    print(f"\n  [{label}] Starting — {format_time(total_seconds)}")
    print("  Press Ctrl+C to pause/skip\n")

    remaining = total_seconds
    try:
        while remaining > 0:
            sys.stdout.write(f"\r  ⏱  {format_time(remaining)} remaining ")
            sys.stdout.flush()
            time.sleep(1)
            remaining -= 1

        clear_line()
        print(f"  ✓ {label} complete!")
        # Terminal bell
        print("\a", end="")
        return True

    except KeyboardInterrupt:
        clear_line()
        print(f"\n  Paused at {format_time(remaining)}.")
        while True:
            choice = input("  (r)esume / (s)kip / (q)uit? ").strip().lower()
            if choice == "r":
                return countdown(label, remaining)
            elif choice == "s":
                print(f"  Skipped {label}.")
                return True
            elif choice == "q":
                return False
            else:
                print("  Enter r, s, or q.")


def get_duration(prompt, default):
    """Prompt user for a duration in minutes, with a default."""
    val = input(f"  {prompt} (default {default} min): ").strip()
    if not val:
        return default * 60
    try:
        return int(val) * 60
    except ValueError:
        print(f"  Invalid input, using {default} min.")
        return default * 60


def main():
    print()
    print("#################################")
    print("|     Pomodoro Timer            |")
    print("#################################")
    print()

    work_sec = get_duration("Work duration", DEFAULT_WORK)
    short_break_sec = get_duration("Short break duration", DEFAULT_SHORT_BREAK)
    long_break_sec = get_duration("Long break duration", DEFAULT_LONG_BREAK)

    session = 0
    total_sessions = 0

    print(f"\n  Config: {work_sec // 60}m work / {short_break_sec // 60}m short break / {long_break_sec // 60}m long break")
    print(f"  Long break every {SESSIONS_BEFORE_LONG_BREAK} sessions\n")

    while True:
        session += 1
        total_sessions += 1
        print(f"\n  === Session {total_sessions} ===")

        if not countdown(f"Work Session {total_sessions}", work_sec):
            break

        if session % SESSIONS_BEFORE_LONG_BREAK == 0:
            print("\n  Time for a long break!")
            if not countdown("Long Break", long_break_sec):
                break
            session = 0
        else:
            if not countdown("Short Break", short_break_sec):
                break

        cont = input("\n  Start next session? (yes/no): ").strip().lower()
        if cont != "yes":
            break

    print(f"\n  Great work! You completed {total_sessions} session(s). 🍅")
    print("  Goodbye!\n")


if __name__ == "__main__":
    main()
